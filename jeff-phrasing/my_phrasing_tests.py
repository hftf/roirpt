import my_phrasing

# print(obj_to_phrase(test_obj_1))
'were you'

tests = {
	'^KPWRAO*EBT': 'will you not have been a',
	'KPWR*B':      'you are not',
	'^KPWR*B':     'are you not',
	'^KPWRERP':    'have you done',
	'^KPWRAOBLGD': 'would you like',
	'KPWRAOUBLGD': 'you would be liking',
	'SWR*BD':      'I was not',
	'^SWR*BD':     'was I not',
	'SWR*D':       'I did not',
	'^SWR*D':      'did I not',
	'KPWR*BD':     'you were not',
	'^KPWR*BD':    'were you not',
	'KPWR*D':      'you did not',
	'^KPWR*D':     'did you not',
	'KWHR*BD':     'he was not',
	'^KWHR*BD':    'was he not',
	'KWHR*D':      'he did not',
	'^KWHR*D':     'did he not',
	'SWR*B':       'I am not',
	'^SWR*B':      'am I not',
	'SWR*':        'I do not',
	'^SWR*':       'do I not',
	'KPWR*B':      'you are not',
	'^KPWR*B':     'are you not',
	'KPWR*':       'you do not',
	'^KPWR*':      'do you not',
	'KWHR*B':      'he is not',
	'^KWHR*B':     'is he not',
	'KWHR*':       'he does not',
	'^KWHR*':      'does he not',
	'SWRAO*RP':    'I will not do',
	'SWHAUPBLG':   'what you find',
	'SWROERPD':    'I should have done',
	'SWRO*ERPD':   'I should not have done',
}

for test, expected in tests.items():
	print('')
	result = my_phrasing.obj_to_phrase(my_phrasing.stroke_to_obj(test))
	print(f'Test:     {test}\n Expect: {expected}')
	print(f' Result: {result}')
	assert expected == result
