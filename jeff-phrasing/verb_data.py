import re
from collections import OrderedDict
from jeff_phrasing import TO_BE
import pprint

def inflect(verb, suffix, exceptions=None):
	if type(exceptions) == str:
		exceptions = {'en': exceptions, 'ed': exceptions}
	if exceptions and suffix in exceptions:
		return ' ' + exceptions[suffix]

	if suffix == 'en':
		suffix = 'ed'
	# double final consonant
	# except: consider, remember, happen
	if suffix and suffix[0] in 'aeiou' and re.search('([bcdfghjklmnprstvwxyz]|qu)(?!e[rn])[aeiou][bcdfgklmnprtvz]$', verb):
		verb += verb[-1]
	if suffix and suffix[0] in 'aeiou' and re.search('(?<!^)[^e]e$', verb):
		verb = verb[:-1]
	if suffix and suffix[0] in 'aeous' and re.search('[^aeiou]y$', verb):
		verb = verb[:-1] + 'i' + 'e'[:suffix[0] in 's']
	if suffix and suffix[0] in 's'     and re.search('([osx]|sh|ch)$', verb):
		verb += 'e'

	return ' ' + verb + suffix

# design constraints:
# verbs with T in present ender paired with another verb that doesn't have an extra word
# verbs with Z in present ender cannot have extra word (only due to finger gymnastics)
verbs = {
	# Auxiliary verbs
	# These do not combine naturally with middle/structures.
	'':           ('',       None  , ''          ),
	'Can':        ('BGS',    None  , 'could'     ),
	'May':        ('PL',     'be'  , 'might'     ),
	'Must':       ('PBLGS',  'be'  , 'must'      ), # no past tense: taken by just
	'Shall':      ('RBL',    None  , 'should'    ),
	'Will':       ('RBGS',   None  , 'would'     ),
	# Adverbs
	'Just':       ('PBLGSZ', None  , 'just'      ),
	'Really':     ('RLG',    None  , 'really'    ),

	'ask':        ('RB',     None  , None        ),
	'be':         ('B',      'a'   , {'en': 'been', 'ed': 'was/were', 's': 'is/are'}),
	'become':     ('RPBG',   'a'   , {'en': 'become', 'ed': 'became'}),
	'believe':    ('BL',     'that', None        ),
	'call':       ('RBLG',   None  , None        ),
	'care':       ('RZ',     None  , None        ),
	'change':     ('PBGZ',   None  , None        ),
	'come':       ('BG',     'to'  , {'en': 'come', 'ed': 'came'}),
	'consider':   ('RBGZ',   None  , None        ),
	'do':         ('RP',     'it'  , {'en': 'done', 'ed': 'did'}),
	'expect':     ('PGS',    'that', None        ),
	'feel':       ('LT',     'like', 'felt'      ),
	'find':       ('PBLG',   'that', 'found'     ),
	'forget':     ('RG',     'to'  , {'en': 'forgotten', 'ed': 'forgot'}),
	'get':        ('GS',     'to'  , {'en': 'gotten', 'ed': 'got'}), # he had gotten; he had got to
	'give':       ('GZ',     None  , {'en': 'given', 'ed': 'gave'}),
	'go':         ('G',      'to'  , {'en': 'gone', 'ed': 'went'}),
	'have':       ('T',      'to'  , {'en': 'had', 'ed': 'had', 's': 'has'}),
	'happen':     ('PZ',     None  , None        ),
	'hear':       ('PG',     'that', 'heard'     ),
	'hope':       ('RPS',    'to'  , None        ),
	'imagine':    ('PLG',    'that', None        ),
	'keep':       ('PBGS',   None  , 'kept'      ),
	'know':       ('PB',     'that', {'en': 'known', 'ed': 'knew'}),
	'learn':      ('RPBS',   'to'  , None        ),
	'leave':      ('LGZ',    None  , 'left'      ),
	'let':        ('LS',     None  , 'let'       ),
	'like':       ('BLG',    'to'  , None        ),
	'live':       ('LZ',     None  , None        ),
	'look':       ('L',      None  , None        ),
	'love':       ('LG',     'to'  , None        ),
	'make':       ('RPBL',   'a'   , 'made'      ),
	'mean':       ('PBL',    'to'  , 'meant'     ),
	'mind':       ('PBLS',   None  , None        ),
	'move':       ('PLZ',    None  , None        ),
	'need':       ('RPG',    'to'  , None        ),
	'put':        ('PS',     'it'  , 'put'       ),
	'read':       ('RS',     None  , 'read'      ),
	'recall':     ('RL',     None  , None        ),
	'realize':    ('RLS',    'that', None        ),
	'remember':   ('RPL',    'that', None        ),
	'remain':     ('RPLS',   None  , None        ),
	'run':        ('R',      None  , {'en': 'run',  'ed': 'ran'}),
	'say':        ('BS',     'that', 'said'      ),
	'see':        ('S',      None  , {'en': 'seen', 'ed': 'saw'}),
	'set':        ('BLS',    None  , 'set'       ),
	'seem':       ('PLS',    'to'  , None        ),
	'show':       ('RBZ',    None  , {'en': 'shown', 'ed': 'showed'}),
	'take':       ('RBT',    None  , {'en': 'taken', 'ed': 'took'}),
	'tell':       ('RLT',    None  , 'told'      ),
	'think':      ('PBG',    'that', 'thought'   ),
	'try':        ('RT',     'to'  , None        ),
	'understand': ('RPB',    'the' , 'understood'),
	# 'use':        ('Z',      'to'  , None        ),
	'use':        ('Z',      None  , None        ),
	'Used to':    ('TZ',     None  , 'used to'   ),
	'want':       ('P',      'to'  , None        ),
	'wish':       ('RBS',    'to'  , None        ),
	'work':       ('RBG',    'on'  , None        ),
	# 'talk':     ('BLGT',   None  , None        ), # conflicts with like to

	# help
}

# generate verb forms
verb_forms = {} # OrderedDict()
for verb, (present_ender, extra_word, exceptions) in verbs.items():
	# auxiliaries
	if not verb or verb[0] != verb[0].lower():
		present_forms = verb.lower()
		if verb:
			present_forms = ' ' + present_forms
		if extra_word:
			m = present_forms + ' ' + extra_word
	else:
		present_forms = {
				None:                 inflect(verb, ""   , exceptions),
				"3ps":                inflect(verb, "s"  , exceptions),
				"present-participle": inflect(verb, "ing", exceptions),
				"past-participle":    inflect(verb, "en" , exceptions),
			}
		if extra_word:
			m = {k: v + ' ' + extra_word for k, v in present_forms.items()}
	if present_ender in verb_forms:
		print( present_ender)
	verb_forms[present_ender] = ("present", 
		(present_forms))
	if extra_word:
		if 'T' in present_ender:
			x = re.sub("D?Z?$", r"S\g<0>", present_ender, 1)
		else:
			x = re.sub("S?D?Z?$", r"T\g<0>", present_ender, 1)
		if x in verb_forms:
			print( x)
		verb_forms[x] = ("present",
			m)


	# R -> RD; Z -> DZ
	past_enders = [re.sub("Z?$", r"D\g<0>", present_ender, 1)]
	# SD -> DS, SZ
	# SZ -> SDZ, TSDZ
	if "S" in present_ender:
		if "Z" in present_ender:
			# past_enders.append(re.sub("(?<!T)SZ$", r"TSDZ", present_ender, 1))
			past_enders[0] = re.sub("(?<!T)SZ$", r"TSDZ", present_ender, 1)
		else:
			past_enders[0] = present_ender + "Z"
	for past_ender in past_enders:
		if not verb or verb[0] != verb[0].lower():
			past_forms = exceptions
			if exceptions:
				past_forms = ' ' + past_forms
			if extra_word:
				m = past_forms + ' ' + extra_word
		else:
			past_forms = {
				None:                 inflect(verb, "ed" , exceptions),
				"root":               inflect(verb, ""   , exceptions),
				# "3ps":                inflect(verb, "s"  , exceptions),
				"present-participle": inflect(verb, "ing", exceptions),
				"past-participle":    inflect(verb, "en" , exceptions),
			}
			if extra_word:
				m = {k: v + ' ' + extra_word for k, v in past_forms.items()}

		if past_ender in verb_forms:
			print( past_ender)
		verb_forms[past_ender] = ("past", 
			(past_forms))
		if extra_word:
			if 'T' in past_ender or 'S' in past_ender:
				x = re.sub("T?D?S?Z?$", r"TSDZ", past_ender, 1)
			else:
				x = re.sub("S?D?Z?$", r"T\g<0>", past_ender, 1)

			if x in verb_forms:
				print( x)
			verb_forms[x] = ("past",
				m)

pprint.pprint(verb_forms, width=180)
