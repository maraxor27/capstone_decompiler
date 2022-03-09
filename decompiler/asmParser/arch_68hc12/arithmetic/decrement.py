import re

from .. import BaseInstruction, load, MiniSub, MiniCmp

@load
class Decrement(BaseInstruction):
	name = "DE<C<A,B, >,S,X,Y>"
	regex = re.compile("^DE(C[A,B]{0,1}|S|X|Y])$", re.I)

	def __init__(self, line, repo):
		super().__init__(line)
		self.opcode = line
		return

	def to_mini_arch(self):
		reg = str(self.opcode[-1]).lower()
		if reg == "s":
			reg = "sp"
		return [MiniSub("reg_"+reg, "reg_"+reg, "1"), MiniCmp("reg_"+reg, 0)]