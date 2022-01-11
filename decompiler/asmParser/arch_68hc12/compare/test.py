import re

from .. import BaseInstruction, load

@load
class TestAB(BaseInstruction):
	name = "TST<A,B>"
	regex = re.compile("^TST[A,B]$", re.I)
	
	def __init__(self, line):
		super().__init__(line)
		return 

@load
class Test(BaseInstruction):
	name = "TST"