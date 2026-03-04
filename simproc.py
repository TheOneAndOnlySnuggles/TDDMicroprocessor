"""
	Implements an interpreter for simple microprocessor.
"""

def is_mem_ref(param):
	return param[0] == '[' and param[-1] == ']'

def mem_ref(param):
	return int(param[1:-1])

JUMP_LIST = ['JZ', 'JMP', 'JNZ']


class Simproc:

	def __init__(self):
		self.memory = [0] * 10	# Memory
		self.r0 = 0							# Register
		self.ip = 0							#	Instruction pointer
		self.code = []					#	Program

	def load(self, code):
		"""Load a program."""
		code = code.strip()
		code = [line.strip() for line in code.split('\n')]
		code = [line for line in code if not line.startswith(';')]
		self.code = code

	def preprocess(self):
		"""Strip labels and replace them with line code"""
		code = self.code
		label_dict = {}
		
		# Save each label to a dict with its corresponding line number 
		for line_num, line_content in enumerate(code):
			# Check if line (excpected: word) ends with ':' - is label
			if line_content[-1] == ':':
				label_dict[line_content[:-1]] = line_num - len(label_dict)

		# Strip labels
		for _, labelLine in label_dict.items():
			code.pop(labelLine)

		# Swap label names with line number
		for line_num in range(len(code)):
			inst_list = code[line_num].split(' ')
			if (inst_list[0] in JUMP_LIST and not inst_list[1].isdigit()):
				print('%s -> %d' % (inst_list[1] ,label_dict[inst_list[1]]))
				code[line_num] = code[line_num].replace(inst_list[1], str(label_dict[inst_list[1]]))
				# code[line_num] = ' '.join(code[line_num])

		# return '\n'.join(code)
		self.code = code
				 

	def fetch(self):
		"""Fetches the next instructions"""
		line = self.code[self.ip]
		self.ip += 1
		return line

	def decode(self, line):
		"""Decodes instructions"""
		sep = line.find(' ')
		inst = line[0:sep]
		args = line[sep:]
		args = [arg.strip() for arg in args.split(',')]
		return inst, args

	def run(self):
		"""Runs the program"""
		while self.ip < len(self.code):
			line = self.fetch()
			inst, args = self.decode(line)
			self.execute(inst, *args)

	def execute(self, inst, *args):
		"""Executes an intruction"""
		if inst == 'NOP':
			pass
		
		elif inst == 'MOV':
			dst, src = args
			if is_mem_ref(src):
				src = self.memory[mem_ref(src)]
			if dst == 'r0':
				self.r0 = int(src)
			else:
				self.memory[int(dst)] = int(src)

		elif inst == 'INC':
			dst = args[0]
			if dst == 'r0':
				self.r0 += 1
			else:
				self.memory[int(dst)] += 1

		elif inst == 'DEC':
			dst = args[0]
			if dst == 'r0':
				self.r0 -= 1
			else:
				self.memory[int(dst)] -= 1

		elif inst in JMP_LIST:
			val = args[0]
			if inst == 'JNZ' and self.r0 != 0:
				self.ip = int(val)
			elif inst == 'JZ' and == 0:
				self.ip = int(val)
			elif inst == 'JMP':
				self.ip = int (val)

	def debug(self):
		"""Shows the contents of memory."""
		print(self.memory)
		print('r0 = %s, ip = %s' % (self.r0, self.ip))

if __name__ == '__main__':
	mp = Simproc()
	# mp.execute('MOV', '0', '67')
	mp.load("""
						MOV 0, 4
						MOV 1, 0
						MOV 2, 1
						SUM_LOOP:
						MOV r0, [0]
						ADD_LOOP:
						INC 1
						DEC r0
						JNZ ADD_LOOP
						DEC 0
						MOV r0, [0]
						JNZ SUM_LOOP
						MOV r0, [1]
					""")
	mp.preprocess()
	print(mp.code)
	mp.run()
	mp.debug()
