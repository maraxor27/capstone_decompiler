import re

from .. import BaseInstruction, load

@load
class Jump(BaseInstruction):
	name = "JSR"
	regex = re.compile("^JSR$", re.I)

	def __init__(self, line):
		super().__init__(line)
		return 