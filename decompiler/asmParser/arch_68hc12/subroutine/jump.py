import re

from .. import BaseInstruction, load, MiniFunc

@load
class Jump(BaseInstruction):
	name = "JSR"
	regex = re.compile("^JSR$", re.I)
	_regex = re.compile(f"^(JSR)\\s+([a-z0-9_]+)\\s*$", re.I)
	num_arg = 1

	def __init__(self, line, repo):
		super().__init__(line)
		(self.opcode, self.func_name) = self.parse_line(line, repo)
		return 

	def _parse_line(self, line):
		match = self._regex.match(line)
		if match is  None:
			raise Exception("No match found in '"+line+"'")
		opcode = match.group(self._regex_main_group_indexes[0])
		func_name = match.group(self._regex_main_group_indexes[1])
		return (opcode, func_name)

	def to_mini_arch(self):
		return [MiniFunc(self.func_name)]

	def __str__(self):
		return f"jump to subroutine: [opcode: {self.opcode}, func_name: {self.func_name}, line: '{self.line}']"