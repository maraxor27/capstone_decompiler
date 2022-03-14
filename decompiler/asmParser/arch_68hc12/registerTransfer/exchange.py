import re

from .. import BaseInstruction, load

@load
class Exchange(BaseInstruction):
	name = "XGD<X,Y>"
	regex = re.compile("^XGD(X|Y)$", re.I)

	def __init__(self, line, repo):
		super().__init__(line)