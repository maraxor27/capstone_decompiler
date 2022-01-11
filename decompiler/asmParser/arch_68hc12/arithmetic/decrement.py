import re

from .. import BaseInstruction, load

@load
class Decrement(BaseInstruction):
	name = "DE<C<A,B, >,S,X,Y>"
	regex = re.compile("^DE(C[A,B]{0,1}|S|X|Y])$", re.I)

	def __init__(self, line):
		super().__init__(line)
		return