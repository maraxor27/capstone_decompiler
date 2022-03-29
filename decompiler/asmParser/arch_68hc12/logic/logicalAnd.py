import re

from .. import BaseInstruction, load, MiniAnd, MiniCmp, ArgFactory
from ..arguments import *

@load
class AndMem(BaseInstruction):
	name = "AND<A,B>"
	regex = re.compile("^AND(A|B)$", re.I)
	_regex = re.compile(f"^(AND(A|B))\\s+(\
{arg_immediate}|{arg_indexed}|{arg_direct}|{arg_indexed_indirect})\\s*", re.I)
	num_arg = 1

	def __init__(self, line, repo):
		super().__init__(line)
		(self.opcode, self.arg1) = self.parse_line(line, repo)
		return

	def _parse_line(self, line, repo):
		match = self._regex.match(line)
		if match is  None:
			raise Exception("No match found in '"+line+"'")
		opcode = match.group(self._regex_main_group_indexes[0])
		arg1 = match.group(self._regex_main_group_indexes[1])
		return (opcode, ArgFactory.make_argument(arg1, repo))

	def to_mini_arch(self):	
		reg = str(self.opcode[-1]).lower()
		return [MiniAnd("reg_"+reg, "reg_"+reg, self.arg1.get_value())]

	def __str__(self):
		return f"AndMem: [opcode: {self.opcode}, arg1: {self.arg1.get_value()}, line: '{self.line}']"