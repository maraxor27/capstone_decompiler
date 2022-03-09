import re

from .. import GenericReturn, load, MiniRet

@load
class SubroutineReturn(GenericReturn):
	name = "RTS"
	regex = re.compile("^RTS$", re.I)

	def __init__(self, line, repo):
		super().__init__(line)
		return

	def __str__(self):
		return "SubroutineReturn: [opcode: RTS]"

	def to_mini_arch(self):
		return [MiniRet()]