import re

from .. import BaseInstruction, load, MiniAdd, MiniCmp, ArgFactory
from ..arguments import *

@load
class IncrementReg(BaseInstruction):
	name = "IN<C<A,B>,S,X,Y>"
	regex = re.compile("^IN(C[A,B]|S|X|Y)$", re.I)

	def __init__(self, line, repo):
		super().__init__(line)
		self.opcode = line
		return

	def to_mini_arch(self):
		reg = str(self.opcode[-1]).lower()
		if reg == "s":
			reg = "sp"
		return [MiniAdd("reg_"+reg, "reg_"+reg, "1"), MiniCmp("reg_"+reg, 0)]

	def __str__(self):
		return f"IncrementReg: [opcode: {self.opcode}, line: '{self.line}']"

@load
class IncrementMem(BaseInstruction):
	name = "INC"
	regex = re.compile("^INC$", re.I)
	_regex = re.compile(f"^(INC)\\s+(\
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
		return [MiniAdd(self.arg1.get_value(), self.arg1.get_value(), "1"), MiniCmp(self.arg1.get_value(), 0)]

	def __str__(self):
		return f"IncrementMem: [opcode: {self.opcode}, arg1: {self.arg1.get_value()}, line: '{self.line}']"