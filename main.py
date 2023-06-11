from time import sleep
import sys

instructions = ['<', '>', '+', '-', '[', ']', ',', '.']
mem = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
pointer = 0
address = 0
ordInp = 0

outLog = open('out.log', 'w', encoding='utf-8')
codeFile = open('input.bf', 'r').readlines()
code = ''

for i in range(len(codeFile)):
	if '#' in codeFile[i]: code = '{}{}'.format(code, codeFile[i][:codeFile[i].find('#')])
	else: code = '{}{}'.format(code, codeFile[i])
code = code.replace('\n', '').replace('\t', '').replace(' ', '')

loops = []

tempCode = code

while tempCode.find('[') != -1:
	i += 1

	openIndex = tempCode.rfind('[')
	closeIndex = tempCode.find(']', openIndex + 1)
	loops.append(openIndex)
	loops.append(closeIndex)

	tempCode = '{} {}'.format(tempCode[:openIndex], tempCode[openIndex + 1:])
	tempCode = '{} {}'.format(tempCode[:closeIndex], tempCode[closeIndex + 1:])

while address < len(code):
	if code[address] == '<':
		pointer -= 1
		if pointer == -1: pointer = len(mem) - 1
	elif code[address] == '>':
		pointer += 1
		if pointer == len(mem): pointer = 0
	elif code[address] == '+':
		mem[pointer] += 1
		if mem[pointer] == 256: mem[pointer] = 0
	elif code[address] == '-':
		mem[pointer] -= 1
		if mem[pointer] == -1: mem[pointer] = 255
	elif code[address] == '[':
		if mem[pointer] == 0: address = loops[loops.index(address) + 1]
	elif code[address] == ']':
		if mem[pointer] != 0: address = loops[loops.index(address) - 1]
	elif code[address] == ',':
		ordInp = 256
		while ordInp > 255:
			try: ordInp = ord(input("\nInput: "))
			except TypeError: ordInp = 256
		mem[pointer] = ordInp
	elif code[address] == '.':
		print(chr(mem[pointer]), end='')
		outLog.write(str(chr(mem[pointer])))
	else:
		print('{}{}'.format("\nERROR: Invalid instruction at char ", address))
		exit()

	address += 1

if '--mem' in sys.argv: print('\n{}'.format(mem))
