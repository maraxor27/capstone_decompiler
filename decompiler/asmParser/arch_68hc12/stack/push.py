import re

from .. import BaseInstruction, load

@load
class Push(BaseInstruction):
	name = "PSH<A,B,C,D,X,Y>"
	regex = re.compile("^PSH[ABCDXY]$", re.I)

	def __init__(self, line):
		super().__init__(line)
		return