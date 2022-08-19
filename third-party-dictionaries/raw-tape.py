from plover.system import *
from plover_stroke import BaseStroke

LONGEST_KEY = 1

class Stroke(BaseStroke):
	pass

Stroke.setup(KEYS, IMPLICIT_HYPHEN_KEYS, NUMBER_KEY, NUMBERS)

def lookup(steno):
	if len(steno) != 1:
		raise KeyError

	stroke = steno[0]
	if stroke == "*":
		return "=undo"
	elif stroke == "RA*U" or stroke == "RA*UP":
		return "{^}{plover:end_solo_dict}"

	keys = [" "] * len(KEYS)
	stroke = Stroke(stroke)
	for key in stroke.keys():
		keys[KEY_ORDER[key]] = key.replace("-", "")
	keys = "".join(keys)

	return f"{{^{keys}^}}\n{{^}}"
