import re

from . import GenericReturn, load, MiniRet


@load
class SoftwareInterrupt(GenericReturn):
	name = "SWI"
	regex = re.compile("^SWI$", re.I)

	def __init__(self, line, arch):
		super().__init__(line)
		return

	def __str__(self):
		return "SubroutineReturn: [opcode: SWI]"

	def to_mini_arch(self):
		return [MiniRet()]