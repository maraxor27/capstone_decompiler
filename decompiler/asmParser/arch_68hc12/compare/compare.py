import re

from .. import BaseInstruction, load, ArgFactory, MiniCmp
from ..arguments import *


@load
class Compare(BaseInstruction):
	name = "C<MPA,MPB,PD,PS,PX,PY>"
	regex = re.compile("^C(MPA|MPB|PD|PS|PX|PY)$", re.I)
	_regex = re.compile(f"^(C(MPA|MPB|PD|PS|PX|PY))\\s+(\
{arg_immediate}|{arg_indexed}|{arg_direct}|{arg_indexed_indirect})\\s*$", re.I)
	num_arg = 1
	def __init__(self, line):
		line = line.strip()
		super().__init__(line)
		(self.opcode, self.arg1) = self.parse_line(line)
		return

	def _parse_line(self, line):
		match = self._regex.match(line)
		if match is  None:
			raise Exception("No match found in '"+line+"'")
		opcode = match.group(self._regex_main_group_indexes[0])
		arg1 = match.group(self._regex_main_group_indexes[1])
		return (opcode, ArgFactory.make_argument(arg1))

	def to_mini_arch(self):
		reg = str(self.opcode[-1]).lower()
		if reg == "s":
			reg = "sp"
		return [MiniCmp("reg_"+reg, self.arg1.get_value())]

	def __str__(self):
		return f"Compare: [opcode: {self.opcode}, arg1: {self.arg1}]"