import re
from collections import defaultdict
from my_phrasing import avm_to_phrase, avm_to_outlines
from verb_data import verbs_without_do_support, defective_verbs, verbs_without_infinitive

# from my_phrasing import select
def select(verb, select, avm, raise_grammar_errors=True):
	forms = verb_forms[verb]
	suffix = ''
	if select == 'infinitive':
		select = ''
	if not select in forms:
		# Only be/have/get have irregular forms; most others are stripped here
		select = select.rstrip('123Pp')
	if verb == 'used to':
		select = ''
	if not select in forms:
		if verb in ['just', 'really']:
			select = ''
		# likely an illegal inflection of a modal ('to may', 'we maying')
		# raise_grammar_error(f'No inflection "{select}" of (defective) verb "{verb}"', avm, raise_grammar_errors)
		raise_grammar_error(avm, f'No inflection "{select}" of (defective) verb "{verb}"')
		suffix = '' # '†' # f'[*{select}]'
		select = ''
	return forms[select] + suffix

from noun_data import noun_data, STARTERS, SIMPLE_STARTERS, SIMPLE_PRONOUNS
from verb_data import verb_forms, verb_ender_data, MODALS

errors = False
def raise_grammar_error(avm, message, d=None):
	if errors:
		raise KeyError(message)
	else:
		if d:
			# replace following line with debug() equivalent:
			debug(avm, '', '', '', d, f'\033[31m× Bailing: \033[0m{message}')
			# print('\t'*d + '\033[31m× Bailing: \033[0m', end='')
		# print(message)
		# avm['grammar'] = message
		pass

negative_contractions = {'can': 'ca', 'will': 'wo', 'shall': 'sha'}
contractions = {'am': "'m", 'are': "'re", 'is': "'s", 'has': "'s",
	'had': "'d", 'have': "'ve", 'will': "'ll", 'would': "'d",
	'not': "n't"}
interrogative_contractions = {'did': "'d", "does": "'s"}

def reverse_dicts_with_repeats(ds):
	r = defaultdict(list)
	for d in ds:
		for k, v in d.items():
			if k not in r[v]: # unique (i.e. ordered set)
				r[v].append(k)
	return dict(r)
def reverse_keymap_via_data(map, data, keyf):
	r = defaultdict(list)
	for k, v in map.items():
		subject_data = data[v]
		_select = subject_data['person'] + 'p'[:subject_data['number'] == 'plural']
		r[keyf(data[v])].append(dict(subject_data, _select=_select))
	return dict(r)

reverse_SIMPLE_STARTERS = {v: k for k, v in SIMPLE_STARTERS.items()}
reverse_SIMPLE_PRONOUNS = reverse_keymap_via_data(SIMPLE_PRONOUNS, noun_data, lambda d: d['subject'])
reverse_STARTERS        = reverse_keymap_via_data(STARTERS,        noun_data, lambda d: d['subject'])
reverse_MODALS          = {v: k for k, v in MODALS.items()}
reverse_verb_forms = {form: (verb, inflection) for verb, forms in verb_forms.items() for inflection, form in forms.items()}
reverse_contractions = reverse_dicts_with_repeats(
	[contractions, negative_contractions, interrogative_contractions])
all_contractions = [*contractions, *negative_contractions, *interrogative_contractions]
# del reverse_STARTERS[''][1] # remove later

def reverse_lookup(text, debug=False):
	for avm in phrase_to_avms(text, debug=debug):
		yield from avm_to_outlines(avm)

def phrase_to_avms(text, debug=False):
	avm = {'extra_word': None, 'tense': None, 'debug': debug}
	# split words at space, except do not split the word "used to"
	words = re.split(r'(?<!used(?= to)) ', text)
	# words = text.split(' ')

	for parse in parse_contractions(avm, words, 0, 0):
		# print(' \033[32mPARSE:', parse, '\033[0m')
		phrase = avm_to_phrase(parse)
		# print(' \033[34mPHRASE:', phrase, '\033[0m', end='')
		# print("❌✅"[phrase == text], end=' ')
		# print('/'.join(avm_to_outline(parse)))
		if phrase == text:
			yield parse

def insert(words, i, parts):
	return words[:i] + parts + words [i+1:]

def debug(avm, words, f, i, d, message):
	if not avm['debug']:
		return
	print('├     '*d + f, str(message), end='')
	if any(x in message for x in ["Finish", "Branch", "Found"]):
		print(f'  \033[37mwords queue: {words}\033[0m')
		print(f'│ \033[37m{avm}\033[0m')
	else:
		print()

def parse_contractions(avm, words, i, d):
	f = 'CONTR'
	contraction_has_no_effect = True

	while i < len(words):
		word = words[i]

		# Resolve contracted element (e.g. "ca" → "can", "sha" → "shall")
		if word in reverse_contractions:
			if len(reverse_contractions[word]) > 1:
				debug(avm, words, f, i, d, f'> Branch for ambiguous contracted element: {word} → {reverse_contractions[word]}')
				for uncontracted in reverse_contractions[word]:
					if 'do' == reverse_verb_forms[uncontracted][0]:
						avm = dict(avm, _cosubordinator_required=True, _question_required=True)
					yield from parse_contractions(avm, insert(words, i, [uncontracted]), i + 1, d+1)
					debug(avm, words, f, i, d, f'< Resuming: {word} → {reverse_contractions[word]}')
				break
			else:
				# debug(avm, words, f, i, d, f'= Found contracted element: {word} → {reverse_contractions[word][0]}')
				words[i] = reverse_contractions[word][0]
				i += 1
		# Split "cannot" → "can not"
		elif 'cannot' == word:
				# debug(avm, words, f, i, d, f'= Found cannot: {word} → can not')
				# Resolve "not" anyway and skip an iteration
				words = insert(words, i, ['can', 'not'])
				avm['_question_required'] = False
				i += 1
		# Split contractions (e.g. "aren't" → "are n't")
		elif "'" in word:
			if "aren't" == word:
				debug(avm, words, f, i, d, f'> Branch for ambiguous aren\'t: {word} → am not')
				# Resolve "not" anyway and skip an iteration
				yield from parse_contractions(dict(avm, contract=True, _question_required=True), insert(words, i, ['am', 'not']), i + 2, d+1)
				debug(avm, words, f, i, d, f'< Resuming: {word} → am not')

			parts = re.split(r"(?=\Bn't\b)|(?='[^t])", word)
			if any(part in reverse_contractions for part in parts):
				# debug(avm, words, f, i, d, f'= Found contraction to split: {word} → {parts}')
				words = insert(words, i, parts)
				avm['contract'] = True
			else:
				raise_grammar_error(avm, f'Invalid contraction: {word}', d)
				break
		# Found a word that could have been a contraction, but wasn't
		elif word in all_contractions:
			contraction_has_no_effect = False
			debug(avm, words, f, i, d, f'= Contraction has an effect, since "{word}" could have been a contraction')
			i += 1
		else:
			# word is not a contraction, so continue
			# debug(avm, words, f, i, d, f'= Skip non-contraction: {word}')
			i += 1
	else:
		if contraction_has_no_effect and 'contract' not in avm:
			debug(avm, words, f, i, d, '> Branch since contraction has no effect')
			yield from parse_cosubordinator(dict(avm, contract=True), words, d)
		debug(avm, words, f, i, d, 'v Finished parsing contractions')
		yield from parse_cosubordinator(avm, words, d)
	
def parse_cosubordinator(avm, words, d):
	f = 'COSUB'
	word = words[0]

	if word in reverse_SIMPLE_STARTERS:
		debug(avm, words, f, '', d, f'> Branch for cosubordinator: {word} → {reverse_SIMPLE_STARTERS[word]}')
		yield from parse_subject(dict(avm, cosubordinator=word), words[1:], d+1)
		# debug(avm, words, f, '', d, f'< Resuming: {word} → {reverse_SIMPLE_STARTERS[word]}')

		# Some words (currently, only 'that') are both cosubordinators and full subjects
		if word in reverse_STARTERS:
			debug(avm, words, f, '', d, f'> Branch for starter: {word} → {reverse_STARTERS[word]}')
			yield from parse_subject(avm, words, d+1)
			# debug(avm, words, f, '', d, f'< Resuming: {word} → {reverse_STARTERS[word]}')
	else:
		if '_cosubordinator_required' in avm:
			raise_grammar_error(avm, f'Cosubordinator required due to contraction with "do"', d)
			return
		debug(avm, words, f, '', d, f'v Finished parsing cosubordinator')
		yield from parse_subject(avm, words, d)
		# debug(avm, words, f, '', d, f'< Resuming')


def parse_subject(avm, words, d):
	f = 'SUBJ '
	if 'cosubordinator' in avm:
		reverse_subjects = reverse_SIMPLE_PRONOUNS
	else:
		reverse_subjects = reverse_STARTERS

	for subject, subject_datas in reverse_subjects.items():
		if subject in words[:2 + ('not' in words[:1 + ('contract' in avm)])]:
			# words[words.index(subject)] = '_'
			words = insert(words, words.index(subject), ['_'])
			for subject_data in subject_datas:
				debug(avm, words, f, '', d, f'> Branch for subject: {subject}')
				yield from parse_negation({**avm, **subject_data}, words, d+1)
				# debug(avm, words, f, '', d, f'< Resuming: {subject}')
			return # break due to for-else
	# No subject was found
	else:
		for subject_data in reverse_subjects['']:
			debug(avm, words, f, '', d, f'> Branch for empty subject with number {subject_data["number"]}')
			yield from parse_negation({**avm, **subject_data}, words, d+1)
			# debug(avm, words, f, '', d, f'< Resuming: {subject}')

def parse_negation(avm, words, d):
	# Negation
	if 'not' in words:
		# TODO refactor to abstract out list of features not allowed by cosubordinator
		if 'cosubordinator' in avm:
			raise_grammar_error(avm, f'Invalid negation with cosubordinator', d)
			return
		avm['negation'] = True
		not_index = words.index('not')
		if 'to' in words[:not_index]:
			raise_grammar_error(avm, f'Invalid negation: infinitive "to" before "not"', d)
			return
		if ['_'] == words[:not_index]:
			raise_grammar_error(avm, f'Invalid negation: phrase has no verb between subject and "not"', d)
			return
		# words.pop(not_index) but do not mutate
		words = insert(words, not_index, [])
		if not_index > 1:
			debug(avm, words, 'NEG  ', '', d, f'! Do-support required: negation found {not_index} words in')
			avm['_do_support'] = True

	# Question
	# need smarter: subject can't actually be far in
	if '_' in words[1:]:
		# words.pop(words.index('_')) but do not mutate
		subject_index = words.index('_')
		words = insert(words, subject_index, [])
		avm['question'] = True
		debug(avm, words, 'QUEST', '', d, f'! Do-support required: subject found {subject_index} words in')
		avm['_do_support'] = True
	if 'to' in words[:1]: # why not [:0]?
		avm['question'] = True
		avm['_infinitive'] = True
		avm['_select'] = 'infinitive'
		# words.pop(words.index('to')) but do not mutate
		words = insert(words, words.index('to'), [])
	if words and '_' == words[0]:
		# words.pop(0)
		words = words[1:]

	if '_question_required' in avm:
		if avm['_question_required'] is True and 'question' not in avm:
			raise_grammar_error(avm, f'Question required due to contraction "aren\'t" expanded as "am not"', d)
			return
		elif avm['_question_required'] is False and 'question' in avm and avm['question']:
			raise_grammar_error(avm, f'Question required due to contraction "cannot" expanded as "can not"', d)
			return

	debug(avm, words, 'NEG/Q', '', d, 'v Finished parsing negation/question')
	yield from parse_verbs(avm, words, 0, d)

def parse_verbs(avm, words, i, d):
	f = 'VERB '
	# debug(avm, words, f, i, d, '• entered parse_verbs()')

	if i >= len(words):
		debug(avm, words, f, i, d, '  No words left')
		if avm['_select'] is not None and 'verb' not in avm:
			debug(avm, words, f, i, d, '= No verb; trying with empty verb')
			yield from parse_extra_word(dict(avm, verb='', tense='',   _select=None), words, i, d)
			yield from parse_extra_word(dict(avm, verb='', tense='ed', _select=None), words, i, d)
			# raise_grammar_error(avm, f'Invalid select: 1')
			return
		# if '_do_support' in avm and avm['_do_support']:
		# 	raise_grammar_error(avm, f'Expected verb after do support', d)
		# 	return
		if 'verb' in avm:
			debug(avm, words, f, i, d, 'v Finished parsing verbs')
			yield from parse_extra_word(avm, words, i, d)
		return

	if avm['_select'] is None:
		debug(avm, words, f, i, d, '= Attempting extra word')
		yield from parse_extra_word(avm, words, i, d)
		raise_grammar_error(avm, f'Invalid select: ', d)
		return

	inflected_verb = words[i]
	if inflected_verb not in reverse_verb_forms:
		debug(avm, words, f, i, d, '= Not a verb, attempting extra word?')
		yield from parse_extra_word(avm, words, i, d)
		raise_grammar_error(avm, f'Invalid verb: {inflected_verb}', d)
		return
	verb, inflection = reverse_verb_forms[inflected_verb]

	if '_infinitive' in avm:
		debug(avm, words, f, i, d, f'! Non-finite base form required by "to"')
		avm['tense'] = ''
	elif 'tense' not in avm or avm['tense'] is None:
		debug(avm, words, f, i, d, f'! Agreement required: {avm["_select"]}')
		tense_found = False
		for tense in ['', 'ed']:
			# next to lines aren't strictly necessary but save space in debug
			selected_verb = select(verb, tense + avm['_select'], avm)
			if selected_verb == inflected_verb:
				debug(avm, words, f, i, d, f'> Branch for tense "{tense}" because found agreement {avm["_select"]}: {inflected_verb} == {verb}[{tense}{avm["_select"]}]')
				yield from parse_verbs(dict(avm, tense=tense, _select=tense + avm['_select']), words, i, d+1)
				# Some verbs (e.g. "", "used to") have the same form in both tenses, so flag to return instead of returning here
				tense_found = True
		if tense_found:
			return
		else:
			raise_grammar_error(avm, f'Invalid inflection: {inflected_verb}', d)
			return
	
	if verb in defective_verbs and avm['_select'] in ['en', 'enP', 'ing']:
		raise_grammar_error(avm, f'Invalid selection of defective verb: {verb}[{avm["_select"]}]', d)
		return
	if verb in verbs_without_do_support and '_do_support' in avm and '_do_support_do' in avm:
		raise_grammar_error(avm, f'Invalid do-support-consuming verb after "do": {inflected_verb}', d)
		return


	try:
		selected_verb = select(verb, avm['_select'], avm)
	except KeyError as e:
		raise_grammar_error(avm, e, d)
		return
	if selected_verb != inflected_verb:
		debug(avm, words, f, i, d, f'> Branch at inflection mismatch ({selected_verb} ≠ {inflected_verb}), attempting extra word')
		yield from parse_extra_word(avm, words, i, d+1)
		raise_grammar_error(avm, f'Inflection mismatch: need to select {verb}[{avm["_select"]}], ' +
			f'but "{inflected_verb}" is {verb}[{inflection}]', d)
		return

	debug(avm, words, f, i, d, f'  Agreement {avm["_select"]} matched by: {inflected_verb} == {verb}[{avm["_select"]}]')

	# verbs_remaining = any(w in reverse_verb_forms for w in words[i+1:])
	if verb in reverse_MODALS:
		if 'cosubordinator' not in avm and 'modal' not in avm:
			debug(avm, words[i+1:], f, i, d, f'> Branch for modal: {inflected_verb}')
			yield from parse_verbs(dict(avm, modal=verb, _do_support=False, _select='infinitive'), words[i+1:], i, d+1)
	elif verb == 'do':
		# need to check not verbs_without_do_support
		if '_do_support' in avm and avm['_do_support']: # should we del from avm?
			debug(avm, words[i+1:], f, i, d, f'> Branch for do-support: {inflected_verb}')
			yield from parse_verbs(dict(avm, _do_support=False, _do_support_do=True, _select='infinitive'), words[i+1:], i, d+1)
	elif verb == 'have':
		# if avm['_do_support'] and
		if 'cosubordinator' not in avm and 'have' not in avm:
			debug(avm, words[i+1:], f, i, d, f'> Branch for aspect: {inflected_verb}')
			yield from parse_verbs(dict(avm, _do_support=False, have=True, _select='en'), words[i+1:], i, d+1)
	elif verb == 'be':
		if 'cosubordinator' not in avm and 'be' not in avm:
			debug(avm, words[i+1:], f, i, d, f'> Branch for aspect: {inflected_verb}')
			yield from parse_verbs(dict(avm, _do_support=False, be=True, _select='ing'), words[i+1:], i, d+1)
		# not strictly necessary, but {passive: True, verb: ''} isn't useful
		if words[i+1:] and words[i+1] in reverse_verb_forms and reverse_verb_forms[words[i+1]][1].startswith('e'):
			debug(avm, words[i+1:], f, i, d, f'> Branch for passive: {inflected_verb}')
			yield from parse_verbs(dict(avm, _do_support=False, passive=True, _select='enP'), words[i+1:], i, d+1)

	debug(avm, words[i+1:], f, i, d, f'= Attempting to use as main verb: {inflected_verb}')
	# There shouldn't already be a verb
	if 'verb' in avm:
		raise_grammar_error(avm, f'Already found the verb, but found {inflected_verb}', d)
		return

	if verb_ender_data[verb][0] is None:
		raise_grammar_error(avm, f'No ender mapped to "{verb}"', d)
		return
	# If there is do-support, then it must be consumed by a valid do-support verb
	if '_do_support' in avm and avm['_do_support']:
		if verb not in verbs_without_do_support:
			raise_grammar_error(avm, f'Invalid do-support-consuming verb: {inflected_verb}', d)
			return
		else:
			debug(avm, words[i+1:], f, i, d, f'= Consuming do-support with: {inflected_verb}')
			yield from parse_verbs(dict(avm, verb=verb, _do_support=False, _select=None), words[i+1:], i, d)
	else:
		debug(avm, words[i+1:], f, i, d, f'= Found main verb: {verb}')
		yield from parse_extra_word(dict(avm, verb=verb, _select=None), words[i+1:], i, d)

def parse_extra_word(avm, words, i, d):
	f = 'EXTRA'
	if i >= len(words):
		debug(avm, words, f, i, d, '  No extra word found')
		debug(avm, words, '🏆   ', i, d, '  Finished parsing extra word')
		yield avm
		return

	if 'verb' in avm and avm['verb'] and \
		not ('extra_word' in avm and avm['extra_word']) and \
		words and words[i] in ['a', 'be', 'it', 'on', 'that', 'the', 'to', 'like']:
		if verb_ender_data[avm['verb']][1] == words[i]:
			debug(avm, words, f, i, d, f'= Found extra word: {words[i]}')
			yield from parse_extra_word(dict(avm, extra_word=words[i]), words[i+1:], i, d)
		# elif avm['verb'] == 'use' and words[i] == 'to' and avm['tense'] == 'ed':
			# debug(avm, words, f, i, d, f'> Branch for "use to"')
			# yield from parse_extra_word(dict(avm, verb='used to'), words[i+1:], i, d+1)
		else:
			raise_grammar_error(avm, f'Invalid extra word: {words[i]}; allowed extra word for {avm["verb"]} is "{verb_ender_data[avm["verb"]][1]}"', d)
			return
	else:
		raise_grammar_error(avm, f'Invalid extra word: {words[i]}; none allowed', d)
		return


tests = {
# "I'd like to go, but I can't cannot shouldn't've za't": [],
}
if __name__ == "__main__":
	for text, expected_outlines in tests.items():
		print(f'\n{text}')
		outlines = reverse_lookup(text, debug=True)
		outlines = ['/'.join(outline) for outline in outlines]

		# if all outlines are in expected_outlines and no others:
		passed = set(outlines) == set(expected_outlines)
		partially_passed = any(outline in expected_outlines for outline in outlines) or \
			any(expected_outline in outlines for expected_outline in expected_outlines)
		if passed:
			print(f'✅ {outlines} == {expected_outlines}')
		elif partially_passed:
			print(f'🉑 {outlines} <> {expected_outlines}')
		else:
			print(f'❌ {outlines} != {expected_outlines}')
