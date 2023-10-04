import re

try:
	from plover.system import NUMBERS, NUMBER_KEY
except:
	from plover.system.english_stenotype import NUMBERS, NUMBER_KEY
	NUMBERS = {'^-': '1-'} | dict(list(NUMBERS.items())[1:])
NUMBERS_REPLACEMENT_TABLE = str.maketrans(
	''.join(NUMBERS.values()).replace('-',''),
	''.join(NUMBERS.keys  ()).replace('-',''),
	)

def denumber(stroke):
	stroke = re.sub(r'(^[1^]?\+?S?[2T]?K?[3P]?W?[4H]?R?[5A]?[0O]?)(?=.)(E?U?[6F]?R?[7P]?B?[8L]?G?[9T]?S?D?Z?$)',
		r'\1-\2', stroke)
	translated = stroke.translate(NUMBERS_REPLACEMENT_TABLE)
	return NUMBER_KEY[:translated != stroke] + translated

	if any(number.strip('-') in stroke for number in NUMBERS.values()):
		for letter, number in NUMBERS.items():
			stroke = stroke.replace(number.strip('-'), letter.strip('-'))
		return NUMBER_KEY + stroke
	return stroke

tests = {
	'450*EUB89SZ': '#HAO*EUBLTSZ',
	'HAO*EUBLTSZ': 'HAO*EUBLTSZ',
	'37':          '#P-P',
	'3-7B':        '#P-PB',
	'3':           '#P',
	'7':           '#-P',
}

for test, expected in tests.items():
	error = ''
	try:
		result = denumber(test)
	except Exception as e:
		result = None
		error = f' ({e})'
	emoji = "❌✅"[expected == result]
	print(f'Test: {test:24} Expect: {str(expected):40} Result: {str(result) + error:40} {emoji}')
	# assert expected == result
