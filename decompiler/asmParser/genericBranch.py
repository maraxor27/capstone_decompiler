import re

from .instruction import Instruction

class GenericBranch(Instruction):
	n_path = 0
	groupRegex = re.compile(r'^L{0,1}(B\w+)\s+(\w+)$', re.I)

	def __init__(self, line):
		super().__init__(line.strip())
		m = self.groupRegex.match(self.line)
		if m is None:
			raise Exception(f"No branch instruction match found for: '{self.line}'")
		self.operation = m.group(1)
		self.operand = m.group(2)
		return

	def __str__(self):
		return f"Generic branch: [text: \"{self.line}\"]"

	def get_condition(self):
		raise Exception("get condition not implemented in sub class of GenericBranch")
