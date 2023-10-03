import re
from collections import OrderedDict
import pprint
import sys

# Part I: Verb forms

irregular_verb_data = {
	# Irregular verbs with 5+ forms (unpredictable -s forms, predictable -ing form)
	'be':         {'en': 'been', 'ed': 'were', 'ed13': 'was', 's': 'are', 's1': 'am', 's3': 'is'},
	'have':       {'en': 'had',  'ed': 'had',                 's': 'has'                        },
	# Irregular verbs with 5 forms (2 different irregular past forms; predictable -s, -ing forms)
	'become':     {'en': 'become',    'ed': 'became'},
	'come':       {'en': 'come',      'ed': 'came'  },
	'do':         {'en': 'done',      'ed': 'did'   },
	'forget':     {'en': 'forgotten', 'ed': 'forgot'},
	'get':        {'en': 'got',       'ed': 'got'   }, # he had gotten vs. he had got to (must)
	'give':       {'en': 'given',     'ed': 'gave'  },
	'go':         {'en': 'gone',      'ed': 'went'  },
	'know':       {'en': 'known',     'ed': 'knew'  },
	'run':        {'en': 'run',       'ed': 'ran'   },
	'see':        {'en': 'seen',      'ed': 'saw'   },
	'show':       {'en': 'shown',     'ed': 'showed'},
	'take':       {'en': 'taken',     'ed': 'took'  },
	# Irregular verbs with 4 forms (same irregular past and past participle form)
	'feel':       {'en': 'felt'       },
	'find':       {'en': 'found'      },
	'hear':       {'en': 'heard'      },
	'keep':       {'en': 'kept'       },
	'leave':      {'en': 'left'       },
	'let':        {'en': 'let'        },
	'make':       {'en': 'made'       },
	'mean':       {'en': 'meant'      },
	'put':        {'en': 'put'        },
	'read':       {'en': 'read'       },
	'say':        {'en': 'said'       },
	'set':        {'en': 'set'        },
	'tell':       {'en': 'told'       },
	'think':      {'en': 'thought'    },
	'understand': {'en': 'understood' },
	# Auxiliary verbs with 2 forms
	'can':        'could',
	'will':       'would',
	'shall':      'should',
	'may':        'might',
	# Auxiliary verbs with 1 form
	'must':       False, # have to?
	'used to':    False,
	# Adverbs / words with 1 form
	'just':       False,
	'really':     False,
	'':           False,
}

# For regular verb, exceptions is None or {}
def inflect(verb, suffix, exceptions=None):
	# Irregular verb with 1 form
	if exceptions is False:
		return verb
	# Irregular verb with 2 forms
	if type(exceptions) == str:
		return exceptions if suffix == 'ed' else verb
	# Irregular verb with 4 forms
	if exceptions and 'en' in exceptions and 'ed' not in exceptions:
		exceptions['ed'] = exceptions['en']
	# Irregular verb: use exception if exists
	if exceptions and suffix in exceptions:
		return exceptions[suffix]

	# Build remaining forms
	if not suffix:
		return verb
	if suffix == 'en':
		suffix = 'ed'
	# Double final consonant. Exceptions: consider, remember, happen
	if suffix[0] in 'ei' and re.search(r'[^aeiou](?!e[nr])[aeiou][bcdfgklmnrptvz]$', verb):
		verb += verb[-1]
	# take -ing -> taking 
	if suffix[0] in 'ei' and re.search(r'(?<!^)[^e]e$',  verb):
		verb = verb[:-1]
	# try  -s   -> tries
	if suffix[0] in 'es' and re.search(r'[^aeiou]y$',    verb):
		verb = verb[:-1] + 'i' + 'e'[:suffix[0] in 's']
	# wish -s   -> wishes
	if suffix[0] in 's'  and re.search(r'[osx]$|[cs]h$', verb):
		verb += 'e'

	return verb + suffix

# Part 2: Ender data

# Theory design guidelines:
# 1. verbs with T in present ender should pair with another verb that doesn't have an extra word
# 2. verbs with Z in present ender should not have extra word (only due to finger gymnastics)
verb_ender_data = {
	# Auxiliary verbs
	'':           ('',       None  ),
	'can':        ('BGS',    None  ),
	'may':        ('PL',     'be'  ),
	'must':       ('PBLGS',  'be'  ), # no past tense: taken by 'just'
	'shall':      ('RBL',    None  ),
	'will':       ('RBGS',   None  ),
	# adverbs
	'just':       ('PBLGSZ', None  ), # list after 'must' to override
	'really':     ('RLG',    None  ),

	'ask':        ('RB',     None  ),
	'be':         ('B',      'a'   ),
	'become':     ('RPBG',   'a'   ),
	'believe':    ('BL',     'that'),
	'call':       ('RBLG',   None  ),
	'care':       ('RZ',     None  ),
	'change':     ('PBGZ',   None  ),
	'come':       ('BG',     'to'  ),
	'consider':   ('RBGZ',   None  ),
	'do':         ('RP',     'it'  ),
	'expect':     ('PGS',    'that'),
	'feel':       ('LT',     'like'),
	'find':       ('PBLG',   'that'),
	'forget':     ('RG',     'to'  ),
	'get':        ('GS',     'to'  ), # he had gotten; he had got to
	'give':       ('GZ',     None  ),
	'go':         ('G',      'to'  ),
	'have':       ('T',      'to'  ),
	'happen':     ('PZ',     None  ),
	'hear':       ('PG',     'that'),
	'hope':       ('RPS',    'to'  ),
	'imagine':    ('PLG',    'that'),
	'keep':       ('PBGS',   None  ),
	'know':       ('PB',     'that'),
	'learn':      ('RPBS',   'to'  ),
	'leave':      ('LGZ',    None  ),
	'let':        ('LS',     None  ),
	'like':       ('BLG',    'to'  ),
	'live':       ('LZ',     None  ),
	'look':       ('L',      None  ),
	'love':       ('LG',     'to'  ),
	'make':       ('RPBL',   'a'   ),
	'mean':       ('PBL',    'to'  ),
	'mind':       ('PBLS',   None  ),
	'move':       ('PLZ',    None  ),
	'need':       ('RPG',    'to'  ),
	'put':        ('PS',     'it'  ),
	'read':       ('RS',     None  ),
	'recall':     ('RL',     None  ),
	'realize':    ('RLS',    'that'),
	'remember':   ('RPL',    'that'),
	'remain':     ('RPLS',   None  ),
	'run':        ('R',      None  ),
	'say':        ('BS',     'that'),
	'see':        ('S',      None  ),
	'set':        ('BLS',    None  ),
	'seem':       ('PLS',    'to'  ),
	'show':       ('RBZ',    None  ),
	'take':       ('RBT',    None  ),
	'tell':       ('RLT',    None  ),
	'think':      ('PBG',    'that'),
	'try':        ('RT',     'to'  ),
	'understand': ('RPB',    'the' ),
#	'use':        ('Z',      'to'  ),
	'use':        ('Z',      None  ),
	'used to':    ('TZ',     None  ),
	'want':       ('P',      'to'  ),
	'wish':       ('RBS',    'to'  ),
	'work':       ('RBG',    'on'  ),
	# 'talk':     ('BLGT',   None  , None        ), # conflicts with like to

	# help
}

# generate verb forms
verb_forms = {} #OrderedDict()
for verb in verb_ender_data.keys():
	if verb in irregular_verb_data:
		exceptions = irregular_verb_data[verb] 
	else:
		exceptions = {}
	if type(exceptions) in [str, bool]:
		forms = {
			'': verb,
			'ed': inflect(verb, 'ed', exceptions),
		}

	else:
		forms = {
			'3':   inflect(verb, 's'  , exceptions),
			'ing': inflect(verb, 'ing', exceptions),
			'en':  inflect(verb, 'en' , exceptions),
			'ed':  inflect(verb, 'ed' , exceptions),
			'':    verb,
		}
		if 's1' in exceptions:
			forms.update({
				'1p':  exceptions['s'],
				'2p':  exceptions['s'],
				'3p':  exceptions['s'],
				'1':   exceptions['s1'],
				'3':   exceptions['s3'],
				'ed1': exceptions['ed13'],
				'ed3': exceptions['ed13'],
			})

	verb_forms[verb] = forms

# adds key to stroke
# if result has 3 of 4 pinky keys, then returns both it and version with all 4 (TSDZ)
# TODO: doesn't handle unergonomic diagonals with 2 pinky keys (TZ, SD)
def press(stroke, key):
	if key in stroke:
		sys.stderr.write(f'{key} already in {stroke}\n')
		return [stroke]
	# candidate = stroke + key
	candidate = re.sub(re.sub(rf'.*{key}.', '', 'T?S?D?Z?$'), rf'{key}\g<0>', stroke, 1)
	if sum(k in candidate for k in 'TSDZ') == 3 \
		and not candidate == 'TDZ': # exception to avoid 'used to' 'had to' conflict
		return [candidate, re.sub(r'T?S?D?Z?$', rf'TSDZ', candidate, 1)]
	return [candidate]
# flattens sublists, then gets unique items
def fu(lists):
	return list(set([i for l in lists for i in l]))

verb_enders = {}# OrderedDict() #{}
for verb, (verb_ender, extra_word) in verb_ender_data.items():
	present_ender = verb_ender
	past_enders   = fu([
		press(present_ender, 'Z' if 'S' in present_ender and 'Z' not in present_ender else 'D'),
		press(present_ender, 'D'),
	])
	if extra_word:
		present_ender_extra_word =   press(present_ender, 'S' if 'T' in present_ender else 'T')
		past_enders_extra_word = fu([press(past_ender,    'S' if 'T' in past_ender else 'T') for past_ender in past_enders])

	queue = [
			('',   present_ender,            None),
			('ed', past_enders,              None),
	]
	if extra_word:
		queue += [
			('',   present_ender_extra_word, extra_word),
			('ed', past_enders_extra_word,   extra_word),
		]

	for (tense, enders, extra_word) in queue:
		for ender in enders if type(enders) is list else [enders]:
			# sys.stderr.write(f'{verb:10} {ender:10} {tense}\n')
			if ender in verb_enders:
				sys.stderr.write(f'{verb}, {ender} already in verb_enders as {verb_enders[ender]}\n')
			verb_enders[ender] = {'tense': tense, 'verb': verb, 'extra_word': extra_word}

# now verb_enders can be imported in jeff_phrasing.py as drop-in replacement for ENDERS
# pprint.pprint(verb_enders, width=180)
