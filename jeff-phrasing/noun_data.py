noun_data = {
	'I':      {'subject': 'I',     'number': 'singular', 'person': '1'},
	'he':     {'subject': 'he',    'number': 'singular', 'person': '3'},
	'she':    {'subject': 'she',   'number': 'singular', 'person': '3'},
	'it':     {'subject': 'it',    'number': 'singular', 'person': '3'},

	'we':     {'subject': 'we',    'number': 'plural',   'person': '1'},
	'you':    {'subject': 'you',   'number': 'plural',   'person': '2'},
	'they':   {'subject': 'they',  'number': 'plural',   'person': '3'},

	'this':   {'subject': 'this',  'number': 'singular', 'person': '3'},
	'that':   {'subject': 'that',  'number': 'singular', 'person': '3'},
	'there':  {'subject': 'there', 'number': 'singular', 'person': '3'},
	'there2': {'subject': 'there', 'number': 'plural',   'person': '3'},
	'':       {'subject': '',      'number': 'singular', 'person': '3'},
	'2':      {'subject': '',      'number': 'plural',   'person': '3'},
}

STARTERS = {
	'SWR':     'I',
	'KWHR':    'he',
	'SKWHR':   'she',
	'KPWH':    'it',

	'TWR':     'we',
	'KPWR':    'you',
	'TWH':     'they',

	'STKH':    'this',
	'STWH':    'that',
	'STHR':    'there',
	'STPHR':   'there2',
	'STKPWHR': '',
	'STWR':    '2',
}

# TODO rename 'simple'
SIMPLE_STARTERS = {
	# subordinators / complementizers / relativizers
	'STHA':  'that',
	'STPA':  'if',
	'SWH':   'when',
	'SWHA':  'what',
	'SWHR':  'where',
	'SWHO':  'who',
	'STKWH': 'why',
	# STWHR  whether ?

	# coordinators
	'SPWH':  'but',
	'SKP':   'and',
	# SKPR   or ?
}
require_subject_unless_past = [
	'if', 'when',
	'where', 'why',
]

SIMPLE_PRONOUNS = {
	'E':   'he',
	'*E':  'she',
	'U':   'you',
	'*U':  'they',
	'EU':  'I',
	'*EU': 'we',
	'*':   'it',
	'':    '',
}
