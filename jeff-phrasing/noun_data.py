# Grammatical data
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
# Simple starters that require a following subject
# (unless in past/passive, e.g. if found, but *if finds)
simple_starters_requiring_subject = [
	'if', 'when',
	'where', 'why',
]
# Simple starters that cannot be followed by subject–auxiliary question inversion
# e.g. what do you find vs. *that do you find
simple_starters_forbidding_inversion = [
	'that', 'if',
]

# Key mappings
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
	'SWHR':  'where',
	'SWHA':  'what',
	'SWHO':  'who',
	'SWHAO': 'why', # was STKWH
	# how
	# STWHR  whether ?

	# coordinators
	'SPWH':  'but',
	'SKP':   'and',
	# SKPR   or ?
}

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
