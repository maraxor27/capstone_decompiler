import re

from .. import BaseInstruction, load

@load
class Pull(BaseInstruction):
	name = "PUL<A,B,C,D,X,Y>"
	regex = re.compile("^PUL[ABCDXY]$", re.I)

	def __init__(self, line):
		super().__init__(line)
		return