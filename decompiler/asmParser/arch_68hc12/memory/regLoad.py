import re

from .. import BaseInstruction, load, ArgFactory, MiniMove, MiniComment
from ..arguments import *


@load
class RegLoad(BaseInstruction):
	name = "L<D<A<A,B>,D,X,Y>,EA<S,X,Y>>"
	regex = re.compile("^L(DAA|DAB|DD|DX|DY|EAS|EAX|EAY)$", re.I)
	_regex = re.compile(f"^(L(DAA|DAB|DD|DX|DY|EAS|EAX|EAY))\\s+(\
{arg_immediate}|{arg_indexed}|{arg_direct}|{arg_indexed_indirect})\\s*", re.I)
	num_arg = 1
	
	def __init__(self, line, repo):
		line = line.strip()
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
		if reg == "s":
			reg = "sp"
		if self.opcode.lower() == "leas":
			# return [MiniComment("stack operation!!!")]
			return [self]
		if self.opcode.lower() in ["leax", "leay"]:
			return [MiniMove("reg_"+reg, f"&({self.arg1.get_value()})")]
		return [MiniMove("reg_"+reg, self.arg1.get_value())]

	def __str__(self):
		return f"RegLoad: [opcode: {self.opcode}, arg1: {self.arg1.get_value()}, line: '{self.line}']"