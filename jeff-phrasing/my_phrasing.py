import noun_data, verb_data
import re

STROKE_PARTS = re.compile(r'''\#?
	(?P<question> \^?)
	(?P<contract> \+?)
	(?P<starter>  S?T?K?P?W?H?R?)
	(?P<modal>    A?O?)-?
	(?P<negation> \*?)
	(?P<aspect>   E?U?)
	(?P<ender>    F?R?P?B?L?G?T?S?D?Z?)''', # note: D is tense
	re.X)

MODALS = {'': None, 'A': 'can', 'AO': 'will', 'O': 'shall'}
NEGATIVE_CONTRACTIONS = {'can': 'ca', 'will': 'wo', 'shall': 'sha'}
CONTRACTIONS = {'am': "'m", 'are': "'re", 'is': "'s", 'has': "'s",
	'will': "'ll", 'would': "'d", 'had': "'d", 'have': "'ve"}

def stroke_to_obj(stroke):
	stroke = STROKE_PARTS.match(stroke)
	question, contract, starter, modal, negation, aspect, ender = stroke.groups()

	data = {}
	# SIMPLE STARTER
	simple_starter = starter + modal
	simple_pronoun = negation + aspect
	if simple_starter in noun_data.SIMPLE_STARTERS:
		data['cosubordinator'] = noun_data.SIMPLE_STARTERS[simple_starter]
		if simple_pronoun in noun_data.SIMPLE_PRONOUNS:
			data.update(noun_data.noun_data[noun_data.SIMPLE_PRONOUNS[simple_pronoun]])
	# NORMAL STARTER
	elif starter in noun_data.STARTERS:
		data.update(noun_data.noun_data[noun_data.STARTERS[starter]])
		data['have']     = 'E' in aspect
		data['be']       = 'U' in aspect
		data['modal']    = MODALS[modal]
		data['question'] = question == '^'
		data['negation'] = negation == '*'
		data['contract'] = contract == '+'
	else:
		raise KeyError(f'Starter {starter} not found')

	if ender in verb_data.verb_enders:
		data.update(verb_data.verb_enders[ender])
	else:
		raise KeyError(f'Ender {ender} not found')

	return data


def obj_to_phrase(obj):
	subject, person, number, tense, modal, have, be, verb, question, negation, contract, cosubordinator, extra_word = (obj.get(k, False) for k in
	'subject, person, number, tense, modal, have, be, verb, question, negation, contract, cosubordinator, extra_word'.split(', '))

	phrase = []
	finite = not (subject == '' and question)
	selects = ['finite' if finite else 'infinitive']
	if not finite:
		subject = 'to'
		question = negation
	if modal:
		phrase.append(modal),  selects.append('infinitive')
	elif (question or negation) and not (have or be) and finite and (verb not in ['be', None]):
		phrase.append('do'),   selects.append('infinitive') # do-support
	if have:
		phrase.append('have'), selects.append('en')
	if be:
		phrase.append('be'),   selects.append('ing')
	if verb:
		phrase.append(verb)

	for i, verb in enumerate(phrase):
		select = selects[i]
		if select == 'finite':
			select = person + 'p' + number[0]
			tense = tense == 'past'
		else:
			tense = 0
		forms = verb_data.verb_forms[verb][tense]
		if select not in forms:
			select = None
		phrase[i] = forms[select]

	if negation:
		if contract and finite and phrase[0] != 'am':
			if phrase[0] in NEGATIVE_CONTRACTIONS:
				phrase[0] = NEGATIVE_CONTRACTIONS[phrase[0]]
			phrase[0] += "n't"
		elif phrase[0] == 'can':
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
