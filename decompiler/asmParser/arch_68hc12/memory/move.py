import re

from . import load
from .. import BaseInstruction, ArgFactory, MiniMove
from ..arguments import *


@load
class Move(BaseInstruction):
	name = "MOV<B,W>"
	regex = re.compile("MOV(B|W)", re.I)
	_regex = re.compile(f"^(MOV(B|W))\\s+({arg_immediate}|{arg_direct}|{arg_indexed})\\s*,\\s*({arg_direct}|{arg_indexed}|{arg_indexed_indirect})\\s*$", re.I)
	num_arg = 2
	def __init__(self, line):
		super().__init__(line)
		(self.opcode, self.arg1, self.arg2) = self.parse_line(line)
		return

	def _parse_line(self, line):
		match = self._regex.match(line)
		if match is  None:
			raise Exception("No match found in '"+line+"'")
		opcode = match.group(self._regex_main_group_indexes[0])
		arg1 = match.group(self._regex_main_group_indexes[1])
		arg2 = match.group(self._regex_main_group_indexes[2])
		return (opcode, ArgFactory.make_argument(arg1), ArgFactory.make_argument(arg2))

	def to_mini_arch(self):
		return [MiniMove(self.arg2.get_value(), self.arg1.get_value())]

	def __str__(self):
		return f"Move instruction: [opcode: {self.opcode}, arg1: {self.arg1}, arg2: {self.arg2}]"
