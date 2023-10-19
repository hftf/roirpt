import json
import re
import glob

import my_phrasing as phrasing
import noun_data, verb_data
from my_phrasing_reverse_lookup import reverse_lookup

PARTS_MATCHER = re.compile(
	r'(\#?\^?\+?)(S?T?K?P?W?H?R?)(A?O?)-?(\*?)(E?U?)(F?R?P?B?L?G?T?S?D?Z?)'
)
ALPHABET = '/#^1+ST2KP3WH4RA5O0-*euf6rp7bl8gt9sdz'
def sortkey(key):
	return [ALPHABET.index(c) for c in re.sub('[-*].*$', lambda m: m[0].lower(), key)]
def sort(l):
	return sorted(l, key=sortkey)

# These are strokes that are okay to remove, typically because they are mis-stroke entries
# spellchecker: disable
AUDITED_STROKES = {
	"SWR": True,          # 'somewhere' -- Use 'SW-R' instead
	"SWR-S": True,        # 'somewheres' -- use 'SW-RS' instead
	"KPWRAEUT": True,     # 'grate'   -- '`TKPWRAEUT`
	"KPWROUR": True,      # 'your'    -- 'KWROUR'
	"KWHR": True,         # 'why'     -- 'KWR'
	"KWHRAOERL": True,    # 'clearly' -- 'KHRAOERL'
	"KWHRE": True,        # 'yes'     -- 'KWRE'
	"TWHA": True,         # 'that'    -- 'THA'
	"KWHRAOER": True,     # 'year'    -- 'KWRAOER'
	"SKWHRAR": True,      # 'scholar' -- 'SKHRAR'
	"TWRAGS": True,       # 'tradition' -- 'TRAGS'
	"KPWHAOUPBT": True,   # 'community' -- 'KPHAOUPBT'
	"KPWHEUPBGS": True,   # 'combination' -- 'KPWEUPBGS'
	"SWR-PBT": True,      # 'haven't' -- 'SR-PBT'
	"TWRAOEUD": True,     # 'divide' -- 'TKWAOEUD'
	"SKWHRAEUB": True,    # 'Jane' -- 'SKWRAEUB'
	"KWHREBGT": True,     # 'collect' -- 'KHREBGT'
	"KPWRAOELD": True,    # 'yield' -- 'KWRAOELD'
	"STKPWHRAEU": True,   # 'display' -- 'STKPHRAUE'
	"TWRAFR": True,       # 'transfer' -- 'TRAFR'
	"TWHEPL": True,       # 'them' -- 'THEPL'
	"SKWHREPL": True,     # 'generally' -- 'SKWHREPBL'
	"KPWHRAEUPB": True,   # 'complain' -- "KPHRAEUPB"
	"KPWHRAEUPBG": True,  # 'complaining' -- "KPHRAEUPBG"
	"STPHRAEUPB": True,   # 'explain' -- "SPHRAUEPB"
	"STPHRAOUGS": True,   # 'institution' -- "STPHAOUGS"
	"STPHRAOER": True,    # 'sphere' -- "STPAOER"
	"STPAEUS": True,      # 'space' -- "SPAEUS"
	"STPAEURL": True,     # 'fairly' -- "TPAEURL"
	"STHAEUR": True,      # 'their' -- "THAEUR"
	"STKPWHRURBGS": True, # 'jurisdiction' -- "SKWRURBGS"

	# Things that seem better alternates already exist
	"STKPWHR-FPLT": True,  # "{!}" -- expect TP-BG, or other form to be used.
	"SWHEPB": True,        # "when is" -- "WH-S" seems easier
	"SKPET": True,         # "and the" -- probably a typo entry for "SKP-T"

	# Things that are superseded by this phrasing system.
	"KPWROEU": True,    # "I don't"
	"KWHROEPB": True,   # "I don't know"
	"SWRAOE": True,     # "we have"
	"SWROEPBT": True,   # "won't have"
	"STHAEUD": True,    # "said that"
	"SWHAE": True,      # "what she"
	"SWHE": True,       # "when she"
	"STHAE": True,      # "that she"
	"SWRE": True,       # "where she"
	"SWHOE": True,      # "who she"
	"SKPEUBS": True,    # "and I said"
	"SKPEUBG": True,    # "and I can"
	"SKPEBG": True,     # "and he can"
	"SKPUBG": True,     # "and you can"
	"SKPUF": True,      # "and you have"
	"SKPEURBD": True,   # "and I should"
	"SKPEUFS": True,    # "and I was"

	# Things that are identitcal
	"SKPE": True,       # "and he"
	"SKPEU": True,      # "and I"
	"SKPU": True,       # "and you"

	# Things that are okay to lose:
	"TWHAPBG": True,    # "thwang"
	"TWHABG": True,     # "thwack"
}
# spellchecker: enable


def increment_collision_counter(d, key, collision_count):
	d[key] = d.get(key, 0) + collision_count


starter_collisions = {}
ender_collisions = {}
simple_starter_collisions = {}
obsolete_translations = {}

count = 0

def get_dicts_in_order():
	# plover.cfg lives above the directory this script is in
	plover_cfg_path = __file__.replace('collision_check.py', '../plover.cfg')
	with open(plover_cfg_path) as config:
		flag = False
		for line in config:
			if line.startswith('[System: Stenotype Extended]'):
				flag = True
			if line.startswith('dictionaries = ') and flag:
				return [d['path'] for d in json.loads(line.split('=')[1].strip()) if d['enabled'] and d['path'].endswith('.json') and d['path'] != 'tapey_tape.json']

dict_filenames = reversed(get_dicts_in_order())
for dict_filename in dict_filenames:
	with open(dict_filename) as dict_json:
		dict_data = json.load(dict_json)
		print("\033[47mLoaded dict %s with %d entries\033[0m" % (dict_filename, len(dict_data)))

		defined_strokes = {}
		simple_defined_strokes = {}

		for strokes in dict_data:
			# 1. Go through all dictionaries and find obsolete entries superseded by the phrasing system:
			translation = dict_data[strokes]
			if ' ' in translation:
				outlines = ['/'.join(outline) for outline in list(reverse_lookup(translation))]
				if outlines:
					obsolete_translations[strokes] = (dict_filename, translation, outlines)

			# 2. Go through all dictionaries and find conflicts with the phrasing system:
			if strokes in AUDITED_STROKES:
				continue

			if strokes in phrasing.NON_PHRASE_STROKES:
				continue

			if '/' in strokes:
				continue

			match = PARTS_MATCHER.match(strokes)
			if not match:
				continue

			# Tally full form
			symbols, starter, v1, star, v2, ending = match.groups()
			key = starter + "…" + ending
			d = defined_strokes.get(key)
			if not d:
				d = {}
				defined_strokes[key] = d

			d[strokes] = dict_data[strokes]

			# Tally simple form.
			if (star + v2) not in phrasing.SIMPLE_PRONOUNS:
				continue

			key = symbols + starter + v1 + '…' + ending
			d = simple_defined_strokes.get(key)
			if not d:
				d = {}
				simple_defined_strokes[key] = d

			d[strokes] = dict_data[strokes]

		def r(d):
			if d[0] == '*':
				return f'\033[91m{d:35}\033[30m'
			return d
		# Full form
		for starter in phrasing.STARTERS:
			# enders = phrasing.STARTERS[starter][2]
			# if enders == None:
			# 	enders = phrasing.ENDERS
			enders = phrasing.ENDERS
			for ender in enders:
				key = starter + "…" + ender
				# if noun_data.noun_data[phrasing.STARTERS[starter]]['subject'] == 'there':
				# 	if phrasing.ENDERS[ender]['verb'] not in verb_data.existential_there_data:
				# 		continue

				if key in defined_strokes:
					collision_count = len(defined_strokes[key])
					verb = phrasing.ENDERS[ender]['verb']
					print(f"\033[1m{key:18} {phrasing.STARTERS[starter]:10} {phrasing.ENDERS[ender]['verb']:10}\033[0m")
					
					for conflict, translation in defined_strokes[key].items():
						# if v2 and verb in verb_data.DEFECTIVE_VERBS:
						# 	print(f'Skipping {conflict} (illegal inflection of {verb})')
						# 	continue
						phrase = r(phrasing.lookup((conflict,), raise_grammar_errors=False))
						print(f"{conflict:18} {phrase:35}", end=' ')
						print(f"{translation:25}", end=' ')
						if ' ' in translation:
							outlines = ['/'.join(outline) for outline in list(reverse_lookup(translation))]
							if outlines:
								print(f'use phrasing instead: {outlines}', end='')
						print()
					print('')
					increment_collision_counter(
						starter_collisions, starter, collision_count)
					increment_collision_counter(
						ender_collisions, '-' + ender, collision_count)
					count = count + collision_count

		# Simple form
		for starter in phrasing.SIMPLE_STARTERS:
			for ender in phrasing.ENDERS:
				key = starter + "…" + ender
				if key in simple_defined_strokes:
					collision_count = len(simple_defined_strokes[key])
					verb = phrasing.ENDERS[ender]['verb']
					key_ = f'\033[32m{starter}\033[30m…{ender}'
					print(f"\033[1m{key_:28} {phrasing.SIMPLE_STARTERS[starter]:10} {phrasing.ENDERS[ender]['verb']:10}\033[0m")

					for conflict, translation in simple_defined_strokes[key].items():
						phrase = r(phrasing.lookup((conflict,), raise_grammar_errors=False))
						print(f"{conflict:18} {phrase:35}", end=' ')
						print(f"{translation:25}", end=' ')
						if ' ' in translation:
							outlines = ['/'.join(outline) for outline in list(reverse_lookup(translation))]
							if outlines:
								print(f'use phrasing instead: {outlines}', end='')
						print()

					print('')
					increment_collision_counter(
						simple_starter_collisions, starter, collision_count)
					increment_collision_counter(
						ender_collisions, '-' + ender, collision_count)
					count = count + collision_count

if len(starter_collisions):
	print('Collisions caused by starters')
	for k in sort(starter_collisions):
		print(f'{k:10} {starter_collisions[k]}')

if len(simple_starter_collisions):
	print('Collisions caused by simple-starters')
	for k in sort(simple_starter_collisions):
		print(f'{k:10} {simple_starter_collisions[k]}')

if len(ender_collisions):
	print('Collisions caused by enders')
	for k in sort(ender_collisions):
		print(f'{k:10} {ender_collisions[k]}')

if count:
	print('Total collisions: %d\n' % count)

for strokes, (dict_filename, translation, outlines) in obsolete_translations.items():
	print(f'{strokes:20} {dict_filename:40} {translation:20} {str(outlines)}')
