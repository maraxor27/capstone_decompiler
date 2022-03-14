import re

from . import load
from .. import BaseInstruction, ArgFactory
from ..arguments import *
from ... import pre_proc

@load
class BitSet(BaseInstruction):
	name = "BSET"
	_regex = re.compile(f"^(BSET)\\s+({arg_direct}|{arg_indexed})\\s*,\\s*({arg_mask8})\\s*$", re.I)
	num_arg = 2
	def __init__(self, line, repo):
		super().__init__(line)
		(self.opcode, self.arg1, self.arg2) = self.parse_line(line, repo)
		return

	def get_args(self):
		return (self.arg1.string, self.arg2.string)

	def get_args_object(self):
		return (self.arg1, self.arg2)

	def _parse_line(self, line):
		match = self._regex.match(line)
		if match is  None:
			raise Exception("No match found in '"+line+"'")
		opcode = match.group(self._regex_main_group_indexes[0])
		arg1 = match.group(self._regex_main_group_indexes[1])
		arg2 = match.group(self._regex_main_group_indexes[2])
		return (opcode, arg1, arg2)

	def __str__(self):
		return f"BitSet instruction: [opcode: {self.opcode}, arg1: {self.arg1}, arg2: {self.arg2}]"