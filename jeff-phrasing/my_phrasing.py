# Following ten lines of jank needed because Plover doesn't know how to import local modules
try:
	import plover
	plover_dir = plover.oslayer.config.CONFIG_DIR
except:
	import appdirs
	plover_dir = appdirs.user_data_dir('plover', 'plover')
import os, sys
jeff_dir = os.path.join(plover_dir, 'jeff-phrasing/')
sys.path.append(jeff_dir)

from noun_data import noun_data,  STARTERS, SIMPLE_STARTERS, SIMPLE_PRONOUNS, \
	simple_starters_requiring_subject, simple_starters_forbidding_inversion
from verb_data import verb_forms, verb_ender_data, MODALS, ENDERS, \
	contractions, negative_contractions, interrogative_contractions, defective_verbs, \
	verbs_without_do_support, verbs_forbidding_existential_there, verbs_forbidding_passive
from jeff_phrasing import NON_PHRASE_STROKES
import re
from collections import defaultdict

LONGEST_KEY = 2

STROKE_PARTS = re.compile(r'''^\#?
	(?P<question> \^?)
	(?P<contract> \+?)
	(?P<starter>  S?T?K?P?W?H?R?)
	(?P<modal>    A?O?)-?
	(?P<negation> \*?)
	(?P<aspect>   E?U?)
	(?P<ender>    F?R?P?B?L?G?T?S?D?Z?)$''', # note: D is tense
	re.X)

# raise_grammar_errors should always be true, except in testing mode
def raise_grammar_error(message, avm, raise_grammar_errors=True):
	if raise_grammar_errors:
		raise KeyError(message)
	else:
		avm['grammar'] = message

def outline_to_avm(outline, raise_grammar_errors=True):
	if not outline:
		raise KeyError('Outline argument empty')

	if type(outline) == str:
		outline = tuple(outline.split('/'))

	avm = {}
	# parse second stroke and add features to avm
	if len(outline) > 1:
		# naive conflict workaround
		if outline[1] == '+':
			raise_grammar_errors = False # only for debugging
			pass
		elif outline[1] == '+-P':
			avm['passive'] = True
		# can do other things here, like add post-hoc adverbs, contractions, passive voice, etc.
		else:
			raise KeyError(f'Two-stroke outline "{"/".join(outline)}" not valid')

	return stroke_to_avm(outline[0], avm, raise_grammar_errors)

def stroke_to_avm(stroke, avm={}, raise_grammar_errors=True):
	stroke_parts = STROKE_PARTS.match(stroke)
	if not stroke_parts:
		raise KeyError(f'Stroke "{stroke}" does not match STROKE_PARTS regex')

	# TODO: shouldn't use bare .groups()
	#                  [simple_starter] [simple_pronoun]
	question, contract, starter, modal, negation, aspect, ender = stroke_parts.groups()

	# SIMPLE STARTER
	simple_starter = starter + modal
	simple_pronoun = negation + aspect

	valid_normal = starter in STARTERS
	valid_simple = simple_starter in SIMPLE_STARTERS and simple_pronoun in SIMPLE_PRONOUNS
	if not (valid_normal or valid_simple):
		raise KeyError(f'Starter "{starter}" not found')
	valid_ender  = ender in ENDERS
	if not valid_ender:
		raise KeyError(f'Ender "{ender}" not found')
	if 'passive' in avm and avm['passive'] and ENDERS[ender]['verb'] in verbs_forbidding_passive:
		raise_grammar_error(f'Passive voice does not apply to ender "{ENDERS[ender]}"', avm, raise_grammar_errors)

	if valid_simple:
		avm['cosubordinator'] = SIMPLE_STARTERS[simple_starter]
		if simple_pronoun in SIMPLE_PRONOUNS:
			if question:
				if SIMPLE_STARTERS[simple_starter] in simple_starters_forbidding_inversion:
					raise_grammar_error(f'Subject–aux question inversion does not apply to simple starter "{SIMPLE_STARTERS[simple_starter]}"', avm, raise_grammar_errors)
					question = ''
				avm['question'] = question == '^'
			if SIMPLE_STARTERS[simple_starter] in simple_starters_requiring_subject and \
				not SIMPLE_PRONOUNS[simple_pronoun] and \
				ENDERS[ender]['verb'] and \
				ENDERS[ender]['tense'] != 'past':
				raise_grammar_error(f'Subject required after simple starter (subordinator) "{SIMPLE_STARTERS[simple_starter]}" unless in past', avm, raise_grammar_errors)

			avm.update(noun_data[SIMPLE_PRONOUNS[simple_pronoun]])
	# NORMAL STARTER
	elif valid_normal:
		if noun_data[STARTERS[starter]]['subject'] == 'there' and \
			ENDERS[ender]['verb'] not in verbs_forbidding_existential_there and \
			('E' not in aspect or ENDERS[ender]['tense'] != 'past'):
			raise_grammar_error(f'Existential "{STARTERS[starter]}" cannot go with verb "{ENDERS[ender]["verb"]}" unless in past', avm, raise_grammar_errors)

		avm.update(noun_data[STARTERS[starter]])
		avm['have']     = 'E' in aspect
		avm['be']       = 'U' in aspect
		avm['modal']    = MODALS[modal]
		avm['question'] = question == '^'
		avm['negation'] = negation == '*'
	avm['contract'] = contract == '+'

	avm.update(ENDERS[ender])
	return avm

def select(verb, select, avm, raise_grammar_errors=True):
	forms = verb_forms[verb]
	suffix = ''
	if not select in forms:
		# Only be/have/get have irregular forms; most others are stripped here
		select = select.rstrip('123Pp')
	if verb == 'used to':
		select = ''
	if not select in forms:
		# likely an illegal inflection of a modal ('to may', 'we maying')
		raise_grammar_error(f'No inflection "{select}" of (defective) verb "{verb}"', avm, raise_grammar_errors)
		suffix = '' # '†' # f'[*{select}]'
		select = ''
	return forms[select] + suffix

def avm_to_phrase(avm, raise_grammar_errors=True):
	if not avm:
		return

	subject, person, number, tense, modal, have, be, verb, question, negation, contract, cosubordinator, extra_word, passive = (avm.get(k, False) for k in
	'subject, person, number, tense, modal, have, be, verb, question, negation, contract, cosubordinator, extra_word, passive'.split(', '))

	finite = not (subject == '' and question and not modal)
	subject_select = tense + person + 'p'[:number == 'plural']

	# Queue of verbs (modal, auxiliary, main verb), e.g. ['have', 'be', 'go']
	phrase = []
	# Queue of verb forms selected by verbs above, e.g. ['past3p', 'en', 'ing']
	selects = [subject_select if finite else '']

	if not finite:
		subject = 'to'
		question = negation
	if modal:
		phrase.append(modal),  selects.append('')
	elif (question or negation) and not (have or be or passive) and finite and verb not in verbs_without_do_support:
		phrase.append('do'),   selects.append('') # do-support
	if have:
		phrase.append('have'), selects.append('en')
	if be:
		phrase.append('be'),   selects.append('ing')
	if passive:
		phrase.append('be'),   selects.append('enP')
	if verb:
		phrase.append(verb)
	else:
		selects.pop()
	# At this point, selects should have same length as phrase.
	assert len(phrase) == len(selects)

	# Loop through verbs in phrase and apply the verb form selected by the previous verb/subject
	for i, verb in enumerate(phrase):
		phrase[i] = select(verb, selects[i], avm, raise_grammar_errors)

	if negation:
		if contract and finite and phrase[0] != 'am':
			if phrase[0] in negative_contractions:
				phrase[0] = negative_contractions[phrase[0]]
			phrase[0] += "n't"
		elif contract and question and phrase[0] == 'am':
			phrase[0] = "aren't"
		elif phrase and phrase[0] == 'can' and (not question or subject == ''):
			phrase[0] += 'not'
		else:
			phrase.insert(finite, 'not')

	# inversion
	if subject:
		if contract and finite and modal and tense and len(phrase) >= 2 and phrase[1] in contractions:
			if not "'" in phrase[0]: # to allow two contractions (shouldn't've), change here
				phrase[0] += contractions[phrase.pop(1)]
		elif contract and finite and not question and phrase and phrase[0] in contractions:
			subject += contractions[phrase.pop(0)]
		elif contract and phrase and "'" not in phrase[0]:
			# contract was enabled, but there was nothing found to contract
			pass
			# raise_grammar_error('There was nothing to contract', avm, raise_grammar_errors)
		phrase.insert(question, subject)

	if cosubordinator:
		if contract and (cosubordinator[0] in 'wht' and cosubordinator != 'whether') and phrase and phrase[0] in (contractions | interrogative_contractions):
			cosubordinator += (contractions | interrogative_contractions)[phrase.pop(0)]
		phrase.insert(0, cosubordinator)

	if extra_word:
		phrase.append(extra_word)

	result = ' '.join(phrase)

	if 'grammar' in avm:
		result = f'*{result}'

	return result

def lookup(outline, raise_grammar_errors=True):
	phrase = avm_to_phrase(outline_to_avm(outline, raise_grammar_errors), raise_grammar_errors)
	if phrase:
		return phrase
	else:
		raise KeyError

def reverse_dict_with_repeats(ds):
	r = {}
	for d in ds:
		for k, v in d.items():
			if v in r:
				if type(r[v]) == tuple:
					r[v] += (k,)
				else:
					r[v] = (r[v], k)
			else:
				r[v] = k
	return r
def reverse_keymap_via_data(map, keyf):
	r = defaultdict(list)
	for k, v in map.items():
		r[keyf(v)].append(k)
	return dict(r)

reverse_STARTERS        = {tuple(noun_data[v].values()): k for k, v in STARTERS.items()}
reverse_SIMPLE_STARTERS = {v: k for k, v in SIMPLE_STARTERS.items()}
reverse_SIMPLE_PRONOUNS = {tuple(noun_data[v].values()): k for k, v in SIMPLE_PRONOUNS.items()}
reverse_MODALS          = {v: k for k, v in MODALS.items()}
reverse_ENDERS          = reverse_keymap_via_data(ENDERS, lambda d: (d['tense'], d['verb'], d['extra_word']))
reverse_contractions    = reverse_dict_with_repeats([contractions, negative_contractions, interrogative_contractions])
reverse_verb_forms = {form: (inflection, verb) for verb, forms in verb_forms.items() for inflection, form in forms.items()}

POSSIBLE_REVERSE_MATCH = re.compile(r"[a-zI ']+")


def avm_to_outlines(avm):
	lookups = {
		'question':       '^',
		'contract':       '+',
		'cosubordinator': reverse_SIMPLE_STARTERS,
		'subject':        reverse_STARTERS,
		'modal':          reverse_MODALS,
		'negation':       '*',
		'have':           'E',
		'be':             'U',
	}

	if 'cosubordinator' in avm and avm['cosubordinator']:
		lookups['subject'] = reverse_SIMPLE_PRONOUNS
		del lookups['modal'], lookups['have'], lookups['be'], lookups['negation']

	outline = ''
	for feature in lookups:
		if feature in avm and avm[feature] not in [None, False]:
			if feature == 'subject':
				k = (avm['subject'], avm['person'], avm['number'])
			else:
				k = avm[feature]
			if type(lookups[feature]) == str:
				outline += lookups[feature]
			else:
				outline += lookups[feature][k]

	if outline[-1] not in 'A5O0*EU':
		outline += '-'

	k = (avm['tense'], avm['verb'], avm['extra_word'])
	if k not in reverse_ENDERS:
		print(f"Not in reverse_ENDERS: {(avm['tense'], avm['verb'], avm['extra_word'])}")
		return
	else:
		# Branch because one form can have multiple enders (e.g. 'saw' = -SD and -SZ)
		for ender in reverse_ENDERS[k]:
			yield from avm_to_outline_aux(avm, outline + ender)

def avm_to_outline_aux(avm, outline):
	if outline[-1] == '-':
		outline = outline[:-1]

	if 'passive' in avm and avm['passive']:
		outline += '/+-P'

	yield tuple(outline.split('/'))

def reverse_lookup(text):
	if not text or not POSSIBLE_REVERSE_MATCH.fullmatch(text):
		return []

	avm = {'subject': None, 'person': None, 'number': None, 'have': False, 'be': False, \
		'modal': None, 'question': False, 'negation': False, 'contract': False, \
		'tense': None, 'verb': None, 'extra_word': None}
	words = text.split(' ')

	# Quit early if beyond maximum phrase length
	if len(words) > 8:
		return []

	# Should probably memoize a lookup table for 1-word-long phrases

	# 1. Undo contractions
	try:
		for i, word in enumerate(words):
			if "'" in word or word == 'cannot':
				parts = re.split(r"(?=\Bn't\b)|(?<=\bcan)(?=not\b)|(?='[^t])", word)
				if parts[1] in reverse_contractions:
					parts[1] = reverse_contractions[parts[1]]
				if parts[0] in reverse_contractions:
					parts[0] = reverse_contractions[parts[0]]

				words = words[:i] + parts + words[i+1:]
				avm['contract'] = word != 'cannot'
				break
	except IndexError:
		# raise KeyError(f'Failed at contractions: {text}')
		return []

	# 2. Cosubordinator
	if words[0] in reverse_SIMPLE_STARTERS:
		avm['cosubordinator'] = words.pop(0)
		reverse_subjects = reverse_SIMPLE_PRONOUNS
	else:
		reverse_subjects = reverse_STARTERS

	# 3. Subject
	for (subject, person, number) in reverse_subjects:
		if subject in words:
			words[words.index(subject)] = '_'
			break
	else:
		subject = '2'[:'cosubordinator' not in avm] # or first verb is 3ps
	avm.update(noun_data[subject])

	do_support = False
	# 4. Negation
	if 'not' in words:
		avm['negation'] = True
		not_index = words.index('not')
		# print(words, not_index)
		words.pop(not_index)
		do_support = not_index > 1

	# 5. Question
	if '_' in words[1:]:
		avm['question'] = True
		words.pop(words.index('_'))
		do_support = True
	if 'to' in words[:1]:
		avm['question'] = True
		words.pop(words.index('to'))
	if words and '_' == words[0]:
		words.pop(0)

	# Only verbs and extra_word left
	# print(words)

	subject, person, number = [noun_data[avm['subject']][k] for k in ['subject', 'person', 'number']]
	subject_select = person + 'p'[:number == 'plural']
	selects = [subject_select]
	avm['tense'] = ''
	verb_ = ''
	for i, inflected_verb in enumerate(words):
		if type(inflected_verb) == tuple and len(inflected_verb) > 1:
			inflected_verb = inflected_verb[0]
		if i >= len(selects):
			break
		if inflected_verb not in reverse_verb_forms:
			break

		inflection, verb = reverse_verb_forms[inflected_verb]
		# if finite, figure out the actual tense
		if len(selects) == 1:
			for tense in ['', 'ed']:
				selected_verb = select(verb, tense + selects[i], avm)
				if selected_verb == inflected_verb:
					avm['tense'] = tense
					break

		verbs_remaining = any(w in reverse_verb_forms for w in words[i+1:])
		if verb in reverse_MODALS and 'cosubordinator' not in avm:
			avm['modal'] = verb
			if verbs_remaining or do_support:
				if do_support:
					verb = ''
					do_support = False
				selects.append('')
		elif verb == 'do':
			if (verbs_remaining or do_support) and 'cosubordinator' not in avm:
				selects.append('') # do-support
				if do_support:
					verb = ''
					do_support = False
		elif verb == 'have':
			if (verbs_remaining or do_support) and 'cosubordinator' not in avm:
				avm['have'] = True
				if do_support:
					verb = ''
					do_support = False
			selects.append('en')
		elif verb == 'be':
			if (verbs_remaining or do_support) and 'cosubordinator' not in avm:
				if verbs_remaining and words[i+1] in reverse_verb_forms and reverse_verb_forms[words[i+1]][0].startswith('e'):
					avm['passive'] = True
				else:
					avm['be'] = True
				if do_support:
					verb = ''
					do_support = False
			elif not words[i+1:] and 'cosubordinator' not in avm: # DO NOT KEEP THIS WAY
				# yield
				avm['be'] = True
				verb = ''
			selects.append('ing')
		verb_ = verb
		# if verb == 'be':    selects.append('enP') passive?
		# print([inflected_verb, inflection, verb, '|', tense, selects[i], selected_verb])



	avm.update({'verb': verb_, 'extra_word': None})

	# 6. Extra word
	if words and (words[-1] in ['a', 'be', 'it', 'on', 'that', 'the', 'to'] or words[-1] == 'like' and len(words) >= 2 and words[-2] in reverse_verb_forms and reverse_verb_forms[words[-2]][1] == 'feel'):
		# print(verb_ender_data[verb], words[-1])
		if verb_ and verb_ender_data[verb_][1] == words[-1]:
			avm['extra_word'] = words.pop()

	# 7.
	# if words and words[-1] in reverse_verb_forms:
		# last_tense, avm['verb'] = reverse_verb_forms[words.pop()]


	result = []
	# return result
	# for:
	# print(words)
	# print(avm)
	outline = avm_to_outline(avm)
	looked_up = ''
	if outline:
		looked_up = lookup(outline, raise_grammar_errors=False)
	if not outline or not text or looked_up.strip('*') != text:
		print('##', [outline, text, looked_up])
		return []
	return [outline]
