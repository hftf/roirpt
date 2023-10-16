import re
from collections import defaultdict

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

reverse_contractions = reverse_dicts_with_repeats(
	[contractions, negative_contractions, interrogative_contractions])
print(reverse_contractions)

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
		yield (avm, words)
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

text = "I'd like to go, but I can't cannot shouldn't've"
reverse_lookup(text)
