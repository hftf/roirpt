import re
from collections import defaultdict

from noun_data import noun_data, STARTERS, SIMPLE_STARTERS, SIMPLE_PRONOUNS

negative_contractions = {'can': 'ca', 'will': 'wo', 'shall': 'sha'}
contractions = {'am': "'m", 'are': "'re", 'is': "'s", 'has': "'s",
	'had': "'d", 'have': "'ve", 'will': "'ll", 'would': "'d",
	'not': "n't"}
interrogative_contractions = {'did': "'d", "does": "'s"}

def reverse_dicts_with_repeats(ds):
	r = defaultdict(list)
	for d in ds:
		for k, v in d.items():
			if k not in r[v]:
				r[v].append(k)
	return dict(r)

reverse_STARTERS        = {tuple(noun_data[v].values()): k for k, v in STARTERS.items()}
reverse_SIMPLE_STARTERS = {v: k for k, v in SIMPLE_STARTERS.items()}
reverse_SIMPLE_PRONOUNS = {tuple(noun_data[v].values()): k for k, v in SIMPLE_PRONOUNS.items()}
reverse_contractions = reverse_dicts_with_repeats(
	[contractions, negative_contractions, interrogative_contractions])
print(reverse_SIMPLE_STARTERS, reverse_STARTERS)

errors = False
def reverse_lookup(text):
	avm = {}
	words = text.split(' ')

	for parse in parse_contractions(avm, words, 0):
		print(parse)

def insert(words, i, parts):
	return words[:i] + parts + words [i+1:]

def parse_contractions(avm, words, i):
	if i >= len(words):
		yield from parse_cosubordinator(avm, words)
		return

	word = words[i]
	parts = re.split(r"(?=\Bn't\b)|(?='[^t])", word)

	if word in reverse_contractions:
		for uncontracted in reverse_contractions[word]:
			yield from parse_contractions(avm, insert(words, i, [uncontracted]), i + 1)
	elif 'cannot' == word:
			yield from parse_contractions(avm, insert(words, i, ['can', 'not']), i + 2)
	elif "'" in word:
		if any(part in reverse_contractions for part in parts):
			yield from parse_contractions(dict(avm, contract=True), insert(words, i, parts), i)
		else:
			if errors:
				raise KeyError(f'Invalid contraction: {word}')
	else:
		yield from parse_contractions(avm, words, i + 1)

def parse_cosubordinator(avm, words):
	word = words[0]

	if word in reverse_SIMPLE_STARTERS:
		yield from parse_subject(dict(avm, cosubordinator=word), words[1:])

		# Some words (currently, only 'that') are both cosubordinators and full subjects
		if word == 'that':
			yield from parse_subject(avm, words)
	else:
		yield from parse_subject(avm, words)


def parse_subject(avm, words):
	if 'cosubordinator' in avm:
		reverse_subjects = reverse_SIMPLE_PRONOUNS
	else:
		reverse_subjects = reverse_STARTERS

	for (subject, person, number) in reverse_subjects:
		if subject in words:
			words[words.index(subject)] = '_'
			avm.update(noun_data[subject])
			yield from parse_negation(avm, words)
			return
	else:
		for subject in ['', '2'][:1 + ('cosubordinator' not in avm)]:
			avm.update(noun_data[subject])
			yield from parse_negation(avm, words)

def parse_negation(avm, words):
	# Negation
	if 'not' in words:
		avm['negation'] = True
		not_index = words.index('not')
		words.pop(not_index)
		if not_index > 1:
			avm['_do_support'] = True

	# Question
	if '_' in words[1:]:
		words.pop(words.index('_'))
		avm['question'] = True
		avm['_do_support'] = True
	if 'to' in words[:1]: # why not [:0]?
		avm['question'] = True
		words.pop(words.index('to'))
	if words and '_' == words[0]:
		words.pop(0)

	yield from parse_verbs(avm, words, 0)

def parse_verbs(avm, words, i):
	yield (avm, words)



text = "I'd like to go, but I can't cannot shouldn't've"
texts = [
	"that is",
	"that",
	"did I not go",
	"did",
	"not to go",
	"to not go",
	"hello",
	"why to go",
]
for text in texts:
	print(f'\n{text}')
	reverse_lookup(text)
