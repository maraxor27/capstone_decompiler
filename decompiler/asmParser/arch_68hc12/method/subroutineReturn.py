import re

from .. import GenericReturn, load

@load
class SubroutineReturn(GenericReturn):
	name = "RTS"
	regex = re.compile("^RTS$", re.I)

	def __init__(self, line):
		super().__init__(line)
		return

	def __str__(self):
		return "SubroutineReturn: [opcode: RTS]"