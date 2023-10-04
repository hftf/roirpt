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

from noun_data import noun_data,  STARTERS, SIMPLE_STARTERS, SIMPLE_PRONOUNS
from verb_data import verb_forms, irregular_verb_data, ENDERS
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

MODALS = {'': None, 'A': 'can', 'AO': 'will', 'O': 'shall'}
NEGATIVE_CONTRACTIONS = {'can': 'ca', 'will': 'wo', 'shall': 'sha'}
CONTRACTIONS = {'am': "'m", 'are': "'re", 'is': "'s", 'has': "'s",
	'will': "'ll", 'would': "'d", 'had': "'d", 'have': "'ve"}

def stroke_to_obj(stroke):
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

	data = {}
	if valid_simple:
		data['cosubordinator'] = SIMPLE_STARTERS[simple_starter]
		if simple_pronoun in SIMPLE_PRONOUNS:
			if question:
				raise KeyError('Subject–aux question inversion does not apply to simple starters')
			# should invalidate subordinator + '' pronoun + present
			data.update(noun_data[SIMPLE_PRONOUNS[simple_pronoun]])
	# NORMAL STARTER
	elif valid_normal:
		data.update(noun_data[STARTERS[starter]])
		data['have']     = 'E' in aspect
		data['be']       = 'U' in aspect
		data['modal']    = MODALS[modal]
		data['question'] = question == '^'
		data['negation'] = negation == '*'
	data['contract'] = contract == '+'

	data.update(ENDERS[ender])
	return data

VERBS_WITHOUT_DO_SUPPORT = [None, 'be'] + [v for v, d in irregular_verb_data.items() if type(d) in [str, bool] and v]

def obj_to_phrase(obj):
	if not obj:
		return

	subject, person, number, tense, modal, have, be, verb, question, negation, contract, cosubordinator, extra_word = (obj.get(k, False) for k in
	'subject, person, number, tense, modal, have, be, verb, question, negation, contract, cosubordinator, extra_word'.split(', '))

	phrase = []
	finite = not (subject == '' and question)
	selects = [tense + person + 'p'[:number == 'plural'] if finite else '']
	if not finite:
		subject = 'to'
		question = negation
	if modal:
		phrase.append(modal),  selects.append('')
	elif (question or negation) and not (have or be) and finite and verb not in VERBS_WITHOUT_DO_SUPPORT:
		phrase.append('do'),   selects.append('') # do-support
	if have:
		phrase.append('have'), selects.append('en')
	if be:
		phrase.append('be'),   selects.append('ing')
	if verb:
		phrase.append(verb)

	for i, verb in enumerate(phrase):
		select = selects[i]
		forms = verb_forms[verb]
		if not select in forms:
			select = select.rstrip('123p')
		if not select in forms:
			# likely an illegal inflection of a modal ('to may', 'we maying')
			select = ''
			# raise KeyError(f'No inflection "{select}" of (defective) verb "{verb}"')
		phrase[i] = forms[select]

	if negation:
		if contract and finite and phrase[0] != 'am':
			if phrase[0] in NEGATIVE_CONTRACTIONS:
				phrase[0] = NEGATIVE_CONTRACTIONS[phrase[0]]
			phrase[0] += "n't"
		elif phrase and phrase[0] == 'can' and not question:
			phrase[0] += 'not'
		else:
			phrase.insert(finite, 'not')

	# inversion
	if subject:
		if contract and not question and phrase[0] in CONTRACTIONS:
			subject += CONTRACTIONS[phrase.pop(0)]
		phrase.insert(question, subject)

	if cosubordinator:
		phrase.insert(0, cosubordinator)

	if extra_word:
		phrase.append(extra_word)

	return ' '.join(phrase)

def lookup(stroke):
	if len(stroke) > 1:
		# naive conflict workaround
		if stroke[1] == '+':
			pass
		# can do other things here, like add post-hoc adverbs, contractions, passive voice, etc.
		else:
			raise KeyError(f'Two-stroke outline "{"/".join(stroke)}" not valid')
	phrase = obj_to_phrase(stroke_to_obj(stroke[0]))
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
