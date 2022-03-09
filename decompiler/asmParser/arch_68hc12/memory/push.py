import re

from . import load
from .. import BaseInstruction

@load
class Push(BaseInstruction):
	name = "PSH<A,B,C,D,X,Y>"
	regex = re.compile("^PSH[ABCDXY]$", re.I)
	_regex = re.compile(f"^(PSH[ABCDXY])$")
	num_arg = 0

	def __init__(self, line, repo):
		super().__init__(line)
		self.opcode = line
		return

	def get_args(self):
		return None

	def get_args_object(self):
		return None

	def __str__(self):
		return f"// Instruction saves register {self.opcode[-1]} on the stack. Push instruction: [opcode: {self.opcode}]"