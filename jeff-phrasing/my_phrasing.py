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
from verb_data import verb_forms, MODALS, ENDERS, contractions, negative_contractions, defective_verbs, \
	verbs_without_do_support, verbs_forbidding_existential_there, verbs_forbidding_passive
from jeff_phrasing import NON_PHRASE_STROKES
import re

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

def raise_grammar_error(message, avm, raise_grammar_errors=True):
	if raise_grammar_errors:
		raise KeyError(message)
	else:
		avm['grammar'] = message

def outline_to_avm(outline, raise_grammar_errors=True):
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
		select = selects[i]
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
			suffix = '†' # f'[*{select}]'
			select = ''
		phrase[i] = forms[select] + suffix

	if negation:
		if contract and finite and phrase[0] != 'am':
			if phrase[0] in negative_contractions:
				phrase[0] = negative_contractions[phrase[0]]
			phrase[0] += "n't"
		elif phrase and phrase[0] == 'can' and not question:
			phrase[0] += 'not'
		else:
			phrase.insert(finite, 'not')

	# inversion
	if subject:
		if contract and not question and phrase and phrase[0] in contractions:
			subject += contractions[phrase.pop(0)]
		phrase.insert(question, subject)

	if cosubordinator:
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


reverse_STARTERS        = {v: k for k, v in STARTERS.items()}
reverse_SIMPLE_STARTERS = {v: k for k, v in SIMPLE_STARTERS.items()}
reverse_SIMPLE_PRONOUNS = {v: k for k, v in SIMPLE_PRONOUNS.items()}
reverse_MODALS          = {v: k for k, v in MODALS.items()}
reverse_ENDERS          = {tuple(v.values()): k for k, v in ENDERS.items()}
reverse_contractions = {}
for k, v in (contractions | negative_contractions).items():
	reverse_contractions[v] = [reverse_contractions[v], k] if v in reverse_contractions else k

POSSIBLE_REVERSE_MATCH = re.compile(r"[a-zI ']+")


def avm_to_outline(avm):
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

	outline = ''
	for feature in lookups:
		if feature in avm and avm[feature]:
			if type(lookups[feature]) == str:
				outline += lookups[feature]
			else:
				outline += lookups[feature][avm[feature]]

	outline += reverse_ENDERS[(avm['tense'], avm['verb'], avm['extra_word'])]

	if 'passive' in avm and avm['passive']:
		outline += '/+-P'

	return outline

def reverse_lookup(text):
	if not text or not POSSIBLE_REVERSE_MATCH.fullmatch(text):
		return []

	# 1. Undo contractions
	words = re.split(r" |(?=\Bn't\b)|(?<=\bcan)(?=not\b)|(?='[^t])", text)
	words = [reverse_contractions[w] if w in reverse_contractions else w for w in words]

	# Quit early if beyond maximum phrase length
	if len(words) > 8:
		return []

	result = []
	# return result
	return words
