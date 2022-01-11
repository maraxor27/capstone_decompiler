import re

from .instruction import UnknownInstruction

class InstructionRepository():
	pre_processor_instructions = [
		re.compile(r"^\s*ENDIF(\s|$)", re.I), 
		re.compile(r"^\s*IFNDEF(\s|$)", re.I), 
		re.compile(r"^\s*END(\s|$)", re.I), 
		re.compile(r"^\s*SWITCH(\s|$)", re.I), 
		re.compile(r"^\s*ORG(\s|$)", re.I),
		re.compile(r"^\s*LIST(\s|$)", re.I),
		re.compile(r"^\s*NOLIST(\s|$)", re.I),
	]
	opcode_regex = re.compile(r"^([A-Z]+)", re.I)
	def __init__(self):
		self.instructions = []
		self.default = UnknownInstruction
		self.label = None
		return

	def addInstruction(self, instruction):
		if instruction not in self.instructions:
			self.instructions.append(instruction)
		return

	def matchInstruction(self, line):

		comment = line.find(';')
		if comment != -1:
			line = line[:comment]

		first_space = line.find(' ')
		if first_space != -1:
			inst = line[:first_space]
		else:
			inst = line

		# For now ignore those instruction
		for pre_proc_inst in self.pre_processor_instructions:
			if pre_proc_inst.match(line):
				#print("Ignoring: " + line)
				return []

		instruction_obj = self.default(line)

		# instruction 
		for instruction in self.instructions:
			if instruction.getRegex().match(inst):
				return [instruction(line)]

		# label followed by instruction
		for chars in [' ', ':', ': ']:
			colon = line.find(chars)
			len_chars = len(chars)
			if colon != -1:
				second_space = line.find(' ', colon + len_chars)
				if second_space != -1:
					inst = line[colon+len_chars:second_space]
				else:
					inst = line[colon+len_chars:]
				for instruction in self.instructions:
					if instruction.getRegex().match(inst):
						return [self.label(line[:colon]), instruction(line[colon+len_chars:])]

		# label on its own
		if match := self.label.getRegex().match(line):
			return [self.label(match.group(1))]

		#print("Failed analysing:", line)
		return [instruction_obj]

	def setLabel(self, label):
		self.label = label

	def parse_instuction__regex(self, debug=False):
		if debug:
			print("--- parse_instuction__regex --- debug ---")
		for instruction in self.instructions:
			if not instruction._regex_parsed and instruction._regex is not None and instruction.num_arg > 0:
				instruction._regex_main_group_indexes = []
				instruction._regex_parser(instruction._regex.pattern)
				instruction._regex_parsed = True
				if debug:
					print(instruction.name, "_regex parse:", instruction._regex_main_group_indexes)

	def __str__(self):
		ret = "Currently loaded instructions:\n| "
		for instruction in self.instructions:
			ret = ret  + instruction.getName() + " | "
		return ret