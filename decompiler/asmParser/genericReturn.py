from .instruction import Instruction

class GenericReturn(Instruction):
	
	def __init__(self, line):
		super().__init__(line)
		return