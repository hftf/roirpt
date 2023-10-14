import re
import sys

# Part Ia: Verb form data (regular verbs are implicitly generated in Part Ib)

negative_contractions = {'can': 'ca', 'will': 'wo', 'shall': 'sha'}
contractions = {'am': "'m", 'are': "'re", 'is': "'s", 'has': "'s",
	'will': "'ll", 'would': "'d", 'had': "'d", 'have': "'ve",
	'not': "n't"} # n't is only for reversing purposes
interrogative_contractions = {'did': "'d", "does": "'s"}

irregular_verb_data = {
	# Irregular verbs with 5+ forms (unpredictable -s forms, predictable -ing form)
	'be':         {'en': 'been', 'ed': 'were', 'ed13': 'was', 's': 'are', 's1': 'am', 's3': 'is'},
	'have':       {'en': 'had',  'ed': 'had',                 's': 'has'                        },
	# Irregular verbs with 5 forms (2 different irregular past forms; predictable -s, -ing forms)
	'become':     {'en': 'become',    'ed': 'became'},
	'come':       {'en': 'come',      'ed': 'came'  },
	'do':         {'en': 'done',      'ed': 'did'   },
	'forget':     {'en': 'forgotten', 'ed': 'forgot'},
	'get':        {'en': 'got',       'ed': 'got'   , 'enP': 'gotten'}, # he had gotten vs. he had got to (must)
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
	'used to':    False, # note: requires do-support
	# Adverbs / words with 1 form
	'just':       False,
	'really':     False,
	'':           False,
}

# dummy subject 'there' is only allowed for intransitive verbs (no direct object required for meaning)
verbs_forbidding_existential_there = [
	'',
	# modals
	'can', 'shall', 'will', 'may', 'must', 'need', 'used to',
	# presentational verbs (like 'exist', 'occur', 'appear', 'follow')
	'be',
	'have', # only as 'have to' main verb
	'do',   # only as auxiliary (do-support or emphatic-do)
	# intransitive verbs
	'happen', 'seem',
	# intransitive in some contexts, but also useful for locative inversion
	# can be (stressed) deictic-there, pronoun-there rather than existential-there
	'become', 'come', 'live',
	'go',   # also as 'going to' future auxiliary
	# non-verbs (adverbs)
	'just', 'really',
]
# verbs not used in passive voice
verbs_forbidding_passive = [
	'can', 'shall', 'will', 'may', 'must',
	'be',
	'happen', 'seem',
	'mind',
	'remain', 'live',
]

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

# Part 2a: Key mappings

# Theory design guidelines:
# 1. verbs with T in present ender should pair with another verb that doesn't have an extra word
# 2. verbs with Z in present ender should not have extra word (only due to finger gymnastics)
# but maybe use S for extra word?
verb_ender_data = {
	'':           ('',       None  ),
	# Auxiliary verbs
	'can':        (None,     None  ), # was 'BGS'
	'shall':      (None,     None  ), # was 'RBL'
	'will':       (None,     None  ), # was 'RBGS'
	'may':        ('PL',     'be'  ),
	'must':       ('PBLGS',  'be'  ), # no past tense: taken by 'just'
	# adverbs
	'just':       ('PBLGSZ', None  ), # list after 'must' to override
	'really':     ('RLG',    None  ),

	# common
	'be':         ('B',      'a'   ),
	'have':       ('F',      'to'  ), # was T
	'do':         ('RP',     'it'  ),
	'go':         ('G',      'to'  ),
	'get':        ('GS',     'to'  ), # he had gotten (obtain); he had got to (obligation)
	'say':        ('BS',     'that'),
	'use':        ('Z',      None  ), # consider as having extra word 'to' rather than None
	'used to':    ('TZ',     None  ), # special case, but really acts as use + to (=T)
	# desire
	'want':       ('P',      'to'  ),
	'wish':       ('RBS',    'to'  ),
	'need':       ('PBL',    'to'  ), # was RPG

	# mind, cognition
	'know':       ('PB',     'that'),
	'think':      ('PBG',    'that'),
	'remember':   ('RPL',    'that'),
	'understand': ('RPB',    'the' ),
	'believe':    ('BL',     'that'),
	'imagine':    ('PLG',    'that'),
	'forget':     ('FRG',    'to'  ), # was RG
	'mean':       ('FR',     'to'  ), # was PBL
	'learn':      ('RPBL',   'to'  ), # was RPBS
	'seem':       ('PLS',    'to'  ), # TODO remap FPL?
	'expect':     ('FPGT',   'that'), # was PGS. could be FPBG
	'realize':    ('RLZ',    'that'), # was RLS
	'mind':       ('FRPB',   None  ), # was PBLS

	'hope':       ('FP',     'to'  ), # was RPS
	'like':       ('LG',     'to'  ), # was BLG
	'love':       ('LGZ',    'to'  ), # was LG
	'care':       ('RG',     None  ), # was RZ

	'become':     ('BGS',    'a'   ), # was RPBG
	'change':     ('FPG',    None  ), # was PBGZ
	'consider':   ('RBGS',   None  ), # was RBGZ
	'find':       ('FPB',    'that'), # was PBLG
	'happen':     ('PZ',     'to'  ), # TRYING 'to'
	'try':        ('RT',     'to'  ),
	'make':       ('PBLG',   'a'   ), # was RPBL
	'work':       ('RBG',    'on'  ),

	'put':        ('PS',     'it'  ),
	'set':        ('FS',     None  ), # was BLS
	'let':        ('LS',     None  ),
	'give':       ('GZ',     None  ),
	'take':       ('RBT',    None  ),
	'keep':       ('PBGS',   None  ),

	# action, communication
	'come':       ('BG',     'to'  ),
	'live':       ('LZ',     None  ),
	'move':       ('PLZ',    None  ),
	'leave':      ('FLZ',    None  ), # was LGZ
	'remain':     ('RPLS',   None  ),
	'call':       ('BLG',    None  ), # was RBLG
	'recall':     ('RL',     None  ),
	'read':       ('RS',     None  ),
	'run':        ('R',      None  ),
	'show':       ('RB',     None  ), # was RBZ
	'ask':        ('FBG',    None  ), # was RB
	'tell':       ('LT',     None  ), # was RLT
	# sensory, perception
	'feel':       ('FL',     'like'), # was LT
	'hear':       ('PG',     'that'), # TODO remap FRP?
	'see':        ('S',      None  ),
	'look':       ('L',      None  ),

	'help':       ('FPL',    None  ), # was PLGS
	'recognize':  ('RGZ',    'that'),
	'notice':     ('PBS',    'that'),
	'talk':       ('T',      'to'  ), # was BLGT
	# play
}

# Part Ib: Generate all verb forms
# (after Part 2a because it depends on verb_ender_data.keys() for the list of verbs)
verb_forms = {}
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
		if 'enP' in exceptions:
			forms.update({'enP': exceptions['enP']})
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

defective_verbs = [v for v, d in irregular_verb_data.items() if type(d) in [str, bool] and v]
verbs_without_do_support = [None, 'be'] + defective_verbs[:5]

# Part 2b: Generate all ender variants

# adds key to stroke
# if result has 3 of 4 pinky keys, then returns both it and version with all 4 (TSDZ)
# TODO: doesn't handle unergonomic diagonals with 2 pinky keys (TZ, SD)
# TODO: replace with plover_stroke?
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

ENDERS = {}
for verb, (verb_ender, extra_word) in verb_ender_data.items():
	if verb_ender is None:
		continue
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

	for (tense, enders, extra_word_) in queue:
		for ender in enders if type(enders) is list else [enders]:
			# sys.stderr.write(f'{verb:10} {ender:10} {tense}\n')
			if ender in ENDERS:
				sys.stderr.write(f'{verb}, {ender} already in ENDERS as {ENDERS[ender]}\n')
			ENDERS[ender] = {'tense': tense, 'verb': verb, 'extra_word': extra_word_}

# Part 2c: Key mapping for modals

MODALS = {'': None, 'A': 'can', 'AO': 'will', 'O': 'shall'}
