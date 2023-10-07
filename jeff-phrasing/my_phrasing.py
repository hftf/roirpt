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

def raise_grammar_error(message, data, raise_grammar_errors=True):
	if raise_grammar_errors:
		raise KeyError(message)
	else:
		data['grammar'] = message

def stroke_to_obj(stroke, data={}, raise_grammar_errors=True):
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
	if 'passive' in data and data['passive'] and ENDERS[ender]['verb'] in verbs_forbidding_passive:
		raise_grammar_error(f'Passive voice does not apply to ender "{ENDERS[ender]}"', data, raise_grammar_errors)

	if valid_simple:
		data['cosubordinator'] = SIMPLE_STARTERS[simple_starter]
		if simple_pronoun in SIMPLE_PRONOUNS:
			if question:
				if SIMPLE_STARTERS[simple_starter] in simple_starters_forbidding_inversion:
					raise_grammar_error(f'Subject–aux question inversion does not apply to simple starter "{SIMPLE_STARTERS[simple_starter]}"', data, raise_grammar_errors)
				data['question'] = question == '^'
			if SIMPLE_STARTERS[simple_starter] in simple_starters_requiring_subject and \
				not SIMPLE_PRONOUNS[simple_pronoun] and \
				ENDERS[ender]['verb'] and \
				ENDERS[ender]['tense'] != 'past':
				raise_grammar_error(f'Subject required after simple starter (subordinator) "{SIMPLE_STARTERS[simple_starter]}" unless in past', data, raise_grammar_errors)

			data.update(noun_data[SIMPLE_PRONOUNS[simple_pronoun]])
	# NORMAL STARTER
	elif valid_normal:
		if noun_data[STARTERS[starter]]['subject'] == 'there' and \
			ENDERS[ender]['verb'] not in verbs_forbidding_existential_there and \
			('E' not in aspect or ENDERS[ender]['tense'] != 'past'):
			raise_grammar_error(f'Existential "{STARTERS[starter]}" cannot go with verb "{ENDERS[ender]["verb"]}" unless in past', data, raise_grammar_errors)

		data.update(noun_data[STARTERS[starter]])
		data['have']     = 'E' in aspect
		data['be']       = 'U' in aspect
		data['modal']    = MODALS[modal]
		data['question'] = question == '^'
		data['negation'] = negation == '*'
	data['contract'] = contract == '+'

	data.update(ENDERS[ender])
	return data

def obj_to_phrase(obj, raise_grammar_errors=True):
	if not obj:
		return

	subject, person, number, tense, modal, have, be, verb, question, negation, contract, cosubordinator, extra_word, passive = (obj.get(k, False) for k in
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
		if not select in forms:
			# likely an illegal inflection of a modal ('to may', 'we maying')
			raise_grammar_error(f'No inflection "{select}" of (defective) verb "{verb}"', obj, raise_grammar_errors)
			suffix = f'[*{select}]'
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

	if 'grammar' in obj:
		result = f'*{result}'

	return result

def lookup(stroke, raise_grammar_errors=True):
	data = {}
	if len(stroke) > 1:
		# naive conflict workaround
		if stroke[1] == '+':
			raise_grammar_errors = False # only for debugging
			pass
		elif stroke[1] == '+-P':
			data['passive'] = True
		# can do other things here, like add post-hoc adverbs, contractions, passive voice, etc.
		else:
			raise KeyError(f'Two-stroke outline "{"/".join(stroke)}" not valid')
	phrase = obj_to_phrase(stroke_to_obj(stroke[0], data, raise_grammar_errors), raise_grammar_errors)
	if phrase:
		return phrase
	else:
		raise KeyError

test_obj_1 = {
	# coordinator or subordinator (also conjunction, preposition, complementizer)
	'cosubordinator': None,
	
	# NOUN (SUBJECT) FEATURES
	# singular, plural
	'number': 'singular',
	# 1, 2, 3
	'person': '1',

	# VERB FEATURES
	# V  main verb
	'verb': 'love',
	# T  present, past
	'tense': 'past',
	# H  True = have (perfect), False = imperfect
	'have': True,
	# B  True = be (progressive/continuous), False = simple
	'be': True,
	# M  None, will, can, shall, may, must, need to
	'modal':    'can',
	# ±  polarity: False = positive (affirmative), True = negative
	'negation': True,
	# ‽  False = declarative (statement, indicative), True = interrogative (question, subject–auxiliary inversion)
	'question': True,

	# X  to, it, a, the, that, on, like
	'extra_word': 'to',

	# ’  True, False
	'contract': False,

	# A  None, just, really, even, still, always, never
	'adverb': None,

	# P  voice: False = active, True passive
	'passive': False,
	# subjunctive (irrealis), imperative
}
