import json
import re
import glob

import importlib
jeff_phrasing = importlib.import_module("jeff-phrasing")

PARTS_MATCHER = re.compile(
    r'(S?T?K?P?W?H?R?)(A?O?)-?(\*?)(E?U?)(F?)(R?P?B?L?G?T?S?D?Z?)'
)

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

    # Things that are superceded by this phrasing system.
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


def increment_collision_counter(dict, key, collision_count):
    dict[key] = dict.get(key, 0) + collision_count


starter_collisions = {}
ender_collisions = {}
simple_starter_collisions = {}

count = 0

dict_filenames = sorted(glob.glob("*.json"))
for dict_filename in dict_filenames:
    with open(dict_filename) as dict_json:
        dict_data = json.load(dict_json)
        print("\033[47mLoaded dict %s with %d entries\033[0m" % (dict_filename, len(dict_data)))

        defined_strokes = {}
        simple_defined_strokes = {}

        for strokes in dict_data:
            if strokes in AUDITED_STROKES:
                continue

            if strokes in jeff_phrasing.NON_PHRASE_STROKES:
                continue

            if '/' in strokes:
                continue

            match = PARTS_MATCHER.match(strokes)
            if not match:
                continue

            # Tally full form
            starter, v1, star, v2, f, ending = match.groups()
            key = starter + "-" + ending
            dict = defined_strokes.get(key)
            if not dict:
                dict = {}
                defined_strokes[key] = dict

            dict[strokes] = dict_data[strokes]

            # Tally simple form.
            if (star + v2) not in jeff_phrasing.SIMPLE_PRONOUNS:
                continue

            key = starter + v1 + '-' + ending
            dict = simple_defined_strokes.get(key)
            if not dict:
                dict = {}
                simple_defined_strokes[key] = dict

            dict[strokes] = dict_data[strokes]

        # Full form
        for starter in jeff_phrasing.STARTERS:
            enders = jeff_phrasing.STARTERS[starter][2]
            if enders == None:
                enders = jeff_phrasing.ENDERS
            for ender in enders:
                key = starter + "-" + ender
                if key in defined_strokes:
                    collision_count = len(defined_strokes[key])
                    e = jeff_phrasing.ENDERS[ender][1]
                    print('Match on %s (%s +%s)' %
                        (key,
                        jeff_phrasing.STARTERS[starter][0],
                        e[None] if isinstance(e, dict) and None in e else e))
                    
                    print(defined_strokes[key])
                    print('')
                    increment_collision_counter(
                        starter_collisions, starter, collision_count)
                    increment_collision_counter(
                        ender_collisions, ender, collision_count)
                    count = count + collision_count

        # Simple form
        for starter in jeff_phrasing.SIMPLE_STARTERS:
            for ender in jeff_phrasing.ENDERS:
                key = starter + "-" + ender
                if key in simple_defined_strokes:
                    collision_count = len(simple_defined_strokes[key])
                    e = jeff_phrasing.ENDERS[ender][1]
                    print('Alt match on %s (%s +%s)' %
                        (key,
                        jeff_phrasing.SIMPLE_STARTERS[starter][0],
                        e[None] if isinstance(e, dict) and None in e else e))

                    print(simple_defined_strokes[key])
                    print('')
                    increment_collision_counter(
                        simple_starter_collisions, starter, collision_count)
                    increment_collision_counter(
                        ender_collisions, ender, collision_count)
                    count = count + collision_count

if len(starter_collisions):
    print('Collisions caused by starters')
    for k in starter_collisions:
        print(' %s: %d' % (k, starter_collisions[k]))

if len(simple_starter_collisions):
    print('Collisions caused by simple-starters')
    for k in simple_starter_collisions:
        print(' %s: %d' % (k, simple_starter_collisions[k]))

if len(ender_collisions):
    print('Collisions caused by enders')
    for k in ender_collisions:
        print(' %s: %d' % (k, ender_collisions[k]))

if count:
    print('Total collisions: %d\n' % count)
