import noun_data, verb_data, jeff_phrasing
import re

STROKE_PARTS = re.compile(r'''\#?
	(?P<question>    \^?)
	(?P<contraction> \+?)
	(?P<starter>     S?T?K?P?W?H?R?)
	(?P<modal>       A?O?)-?
	(?P<negation>    \*?)
	(?P<aspect>      E?U?)
	(?P<ender>       F?R?P?B?L?G?T?S?D?Z?)''',
	re.X)

MODALS = {
	'A':  'can',
	'AO': 'will',
	'O':  'shall',
}
NEGATIVE_CONTRACTIONS = {'will': 'wo', 'can': 'ca', 'shall': 'sha'}
CONTRACTIONS = {'am': "'m", 'are': "'re", 'is': "'s", 'has': "'s",
	'will': "'ll", 'would': "'d", 'had': "'d", 'have': "'ve"}

jeff_phrasing.SIMPLE_PRONOUNS[''] = ('', None, None)

def stroke_to_obj(stroke):
	stroke = STROKE_PARTS.match(stroke)
	question, contraction, starter, modal, negation, aspect, ender = stroke.groups()

	data = {}
	# SIMPLE STARTER
	simple_starter = starter + modal
	if simple_starter in jeff_phrasing.SIMPLE_STARTERS:
		cosubordinator = jeff_phrasing.SIMPLE_STARTERS[simple_starter][0].strip()
		data.update({'cosubordinator': cosubordinator})
		
		simple_pronoun = negation + aspect
		if simple_pronoun in jeff_phrasing.SIMPLE_PRONOUNS:
			subject = jeff_phrasing.SIMPLE_PRONOUNS[simple_pronoun][0]
			data.update(noun_data.noun_data[subject])

		data['aspect_have'] = False
		data['aspect_be']   = False
		data['modal']       = None
		data['question']    = None
		data['negation']    = None
		data['contraction'] = None

	# NORMAL STARTER
	elif starter in noun_data.STARTERS:
		subject = noun_data.STARTERS[starter]
		data.update(noun_data.noun_data[subject])

		data['cosubordinator'] = None
		data['aspect_have'] = 'E' in aspect
		data['aspect_be']   = 'U' in aspect
		data['modal']       = MODALS[modal] if modal else None
		data['question']    = question == '^'
		data['negation']    = negation == '*'
		data['contraction'] = contraction == '+'
		# data['tense']       = 'D' in ender

	else:
		raise KeyError(f'Starter {starter} not found')

	if ender in verb_data.verb_enders:
		vd = verb_data.verb_enders[ender]
		data['tense']      = vd[0]
		data['verb']       = vd[2]
		data['extra_word'] = vd[3]
	else:
		raise KeyError(f'Ender {ender} not found')

	return data


def pick_lookup(vs, ks, d):
	subset = dict((k, vs[k]) for k in ks)
	for k, v in d.items():
		if v == subset:
			return k

def obj_to_phrase(obj):
	phrase = []
	finite = not (obj['subject'] == '' and obj['question'])
	selects = ['finite'] if finite else ['infinitive']
	if not finite:
		obj['subject'] = 'to'
		obj['question'] = obj['negation']
	if obj['modal']:
		phrase.append(obj['modal'])
		selects.append('infinitive')
	elif obj['question'] or obj['negation']:
		if not obj['aspect_have'] and not obj['aspect_be'] and finite:
			if obj['verb'] != 'be' or not obj['verb']: # do-support
				phrase.append('do')
				selects.append('infinitive')
	if obj['aspect_have']:
		phrase.append('have')
		selects.append('en')
	if obj['aspect_be']:
		phrase.append('be')
		selects.append('ing')
	if obj['verb']:
		phrase.append(obj['verb'])

	for i, verb in enumerate(phrase):
		select = selects[i]
		if select == 'finite':
			select = obj['person'] + 'p' + obj['number'][0]
			tense = 0 + (obj['tense'] == 'past')
		else:
			tense = 0
		forms = verb_data.verb_forms[verb][tense]
		if select not in forms:
			select = None
		phrase[i] = forms[select]

	if obj['negation']:
		if obj['contraction'] and finite and phrase[0] != 'am':
			if phrase[0] in NEGATIVE_CONTRACTIONS:
				phrase[0] = NEGATIVE_CONTRACTIONS[phrase[0]]
			phrase[0] += "n't"
		elif phrase[0] == 'can':
			phrase[0] += 'not'
		else:
			phrase.insert(1 if finite else 0, 'not')

	# inversion
	if obj['subject']:
		phrase.insert(1 if obj['question'] else 0, obj['subject'])

		if obj['contraction'] and not obj['question']:
			if phrase[1] in CONTRACTIONS:
				phrase[0] = phrase[0] + CONTRACTIONS[phrase.pop(1)]

	if obj['cosubordinator']:
		phrase.insert(0, obj['cosubordinator'])

	if obj['extra_word']:
		phrase.append(obj['extra_word'])

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
	'aspect_have': True,
	# B  True = be (progressive/continuous), False = simple
	'aspect_be': True,
	# M  None, will, can, shall, may, must, need to
	'modal':    'can',
	# ±  polarity: False = positive (affirmative), True = negative
	'negation': True,
	# ‽  False = declarative (statement, indicative), True = interrogative (question, subject–auxiliary inversion)
	'question': True,

	# X  to, it, a, the, that, on, like
	'extra_word': 'to',

	# ’  True, False
	'contracted': False,

	# A  None, just, really, even, still, always, never
	'adverb': None,

	# P  voice: False = active, True passive
	'passive': False,
	# subjunctive (irrealis), imperative
}
