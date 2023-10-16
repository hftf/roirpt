import re
from collections import defaultdict

negative_contractions = {'can': 'ca', 'will': 'wo', 'shall': 'sha'}
contractions = {'am': "'m", 'are': "'re", 'is': "'s", 'has': "'s",
	'had': "'d", 'have': "'ve", 'will': "'ll", 'would': "'d",
	'not': "n't"}
interrogative_contractions = {'did': "'d", "does": "'s"}

def reverse_dicts_with_repeats(ds):
	r = defaultdict(set)
	for d in ds:
		for k, v in d.items():
			r[v].add(k)
	return dict(r)

reverse_contractions = reverse_dicts_with_repeats(
	[contractions, negative_contractions, interrogative_contractions])
print(reverse_contractions)

def reverse_lookup(text):
	avm = {}
	words = text.split(' ')

	for parse in parse_contractions(avm, words, 0):
		print(parse)

def parse_contractions(avm, words, i):
	if i >= len(words):
		yield (avm, words)

	else:
		word = words[i]
		parts = re.split(r"(?=\Bn't\b)|(?='[^t])", word)

		if word in reverse_contractions:
			for uncontracted in reverse_contractions[word]:
				yield from parse_contractions(avm, words[:i] + [uncontracted] + words[i+1:], i + 1)
			# return
		elif 'cannot' == word:
			yield from parse_contractions(avm, words[:i] + ['can', 'not'] + words[i+1:], i + 2)
		elif "'" in word and any(part in reverse_contractions for part in parts):
			yield from parse_contractions(dict(avm, contract=True), words[:i] + parts + words [i+1:], i)
		else:
			yield from parse_contractions(avm, words, i + 1)

text = "I'd like to go, but I can't cannot shouldn't've za'q."
reverse_lookup(text)
