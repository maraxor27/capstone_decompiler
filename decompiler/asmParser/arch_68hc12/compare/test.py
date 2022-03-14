import re

from .. import BaseInstruction, load, MiniCmp

@load
class TestAB(BaseInstruction):
	name = "TST<A,B>"
	regex = re.compile("^TST[A,B]$", re.I)
	
	def __init__(self, line, repo):
		super().__init__(line)
		return 

	def to_mini_arch(self):
		reg = str(self.opcode[-1]).lower()
		if reg == "s":
			reg = "sp"
		return [MiniCmp("reg_"+reg, "0")]

@load
class Test(BaseInstruction):
	name = "TST"