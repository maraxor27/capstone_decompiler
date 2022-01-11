import re

from . import load
from .. import BaseInstruction

@load
class RegClear(BaseInstruction):
	name = "CLR<A,B>"
	regex = re.compile("^CLR[A,B]$", re.I)

	def __init__(self, line):
		super().__init__(line)
		self.opcode = line
		return