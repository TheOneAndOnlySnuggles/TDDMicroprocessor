import unittest

from simproc import Simproc


class SMPTests(unittest.TestCase):

	def setUp(self):
		self.mp = Simproc()

	def test_nop(self):
		self.mp.execute('NOP')
		self.assertEqual(sum(self.mp.memory), 0)

	def test_mov_mem_val(self):
		self.mp.execute('MOV', '0', '10')
		self.assertEqual(self.mp.memory[0], 10)

	def test_mov_mem_mem_ref(self):
		self.mp.execute('MOV', '0', '10')
		self.mp.execute('MOV', '1', '[0]')
		self.assertEqual(self.mp.memory[1], 10)

	def test_mov_reg_val(self):
		self.mp.execute('MOV', 'r0', '10')
		self.assertEqual(self.mp.r0, 10)
			
	def test_inc_mem_val(self):
		self.mp.execute('MOV', '6', '66')
		self.mp.execute('INC', '6')
		self.assertEqual(self.mp.memory[6], 67)
	
	def test_inc_reg_val(self):
		self.mp.execute('MOV', 'r0', '66')
		self.mp.execute('INC', 'r0')
		self.assertEqual(self.mp.r0, 67)

	def test_dec_mem_val(self):
		self.mp.execute('MOV', 'r0', '68')
		self.mp.execute('DEC', 'r0')
		self.assertEqual(self.mp.r0, 67)

	def test_dec_reg_val(self):
		self.mp.execute('MOV', 'r0', '68')
		self.mp.execute('DEC', 'r0')
		self.assertEqual(self.mp.r0, 67)

	def test_jnz(self):
		self.mp.execute('MOV', 'r0', '67')
		self.mp.execute('JNZ', '5')
		self.assertEqual(self.mp.ip, 5) 
