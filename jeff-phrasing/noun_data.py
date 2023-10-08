# Grammatical data
noun_data = {
	'I':      {'subject': 'I',     'person': '1', 'number': 'singular' },
	'he':     {'subject': 'he',    'person': '3', 'number': 'singular' },
	'she':    {'subject': 'she',   'person': '3', 'number': 'singular' },
	'it':     {'subject': 'it',    'person': '3', 'number': 'singular' },

	'we':     {'subject': 'we',    'person': '1', 'number': 'plural'   },
	'you':    {'subject': 'you',   'person': '2', 'number': 'plural'   },
	'they':   {'subject': 'they',  'person': '3', 'number': 'plural'   },

	'this':   {'subject': 'this',  'person': '3', 'number': 'singular' },
	'that':   {'subject': 'that',  'person': '3', 'number': 'singular' },
	'there':  {'subject': 'there', 'person': '3', 'number': 'singular' },
	'there2': {'subject': 'there', 'person': '3', 'number': 'plural'   },
	'':       {'subject': '',      'person': '3', 'number': 'singular' },
	'2':      {'subject': '',      'person': '3', 'number': 'plural'   },
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
