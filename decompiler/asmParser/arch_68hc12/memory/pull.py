import re

from . import load
from .. import BaseInstruction

@load
class Pull(BaseInstruction):
	name = "PUL<A,B,C,D,X,Y>"
	regex = re.compile("^PUL[ABCDXY]$", re.I)

	def __init__(self, line):
		super().__init__(line)
		self.opcode = line
		return

	def get_args(self):
		return None

	def get_args_object(self):
		return None

	def __str__(self):
		return f"Pull instruction: [opcode: {self.opcode}]"