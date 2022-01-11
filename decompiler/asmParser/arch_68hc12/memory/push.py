import re

from . import load
from .. import BaseInstruction

@load
class Push(BaseInstruction):
	name = "PSH<A,B,C,D,X,Y>"
	regex = re.compile("^PSH[ABCDXY]$", re.I)
	_regex = re.compile(f"^(PSH[ABCDXY])$")
	num_arg = 0

	def __init__(self, line):
		super().__init__(line)
		self.opcode = line
		return

	def get_args(self):
		return None

	def get_args_object(self):
		return None

	def _parse_line(self, line):
		match = self._regex.match(line)
		if match is  None:
			raise Exception("No match found in '"+line+"'")
		opcode = match.group(self._regex_main_group_indexes[0])
		arg1 = match.group(self._regex_main_group_indexes[1])
		arg2 = match.group(self._regex_main_group_indexes[2])
		return (opcode, arg1, arg2)

	def __str__(self):
		return f"Push instruction: [opcode: {self.opcode}]"