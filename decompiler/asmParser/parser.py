import re

from . import pre_proc, arch
from .preProcessorValueRepository import PreProcessorValue

regex_offset = re.compile(r"^OFFSET\s+0$")
regex_data_store = re.compile(r"^\s*([A-Z][A-Z0-9_]*)[\s:]+(DS.[BWL])\s+([1-9][0-9]*)", re.I)
regex_label_data_store = re.compile(r"^\s*([A-Z][A-Z0-9_]*)[\s:]*$")

class StackPreProcessorOffset(PreProcessorValue):
	def __init__(self, string, offset, store_type, quantity):
		super().__init__(string, offset)
		self.store_type = store_type.upper()
		self.quantity = quantity

	def get_offset(self):
		return self.value

	def get_size(self):
		unit_size = 0
		if self.store_type == 'B':
			unit_size = 1
		if self.store_type == 'W':
			unit_size = 2
		if self.store_type == 'L':
			unit_size = 4
		return unit_size * int(self.quantity)

	def __str__(self):
		return f"StackPreProcessorOffset: [string: {self.string}, type: DS.{self.store_type}, quantity: {self.quantity}, value: {self.value}]"

	def compose(self):
		return f"stack allocation: {self.string} of {self.get_size()} Byte at offset {self.value}."

class PreProcessorInstruction:
	def __init__(self, string):
		self.string = string

	def get_string(self):
		return self.string

	def __str__(self):
		return f"PreProcessorInstruction: [string: '{self.string}']"

def stack_parser(lines, index=0, repo=pre_proc):
	is_stack = False
	offset = None
	while index < len(lines):
		line = lines[index]
		if type(line) == type(""):
			if not is_stack:
				if (match := regex_offset.match(line)) is not None:
					lines[index] = PreProcessorInstruction(line)
					is_stack = True
					offset = 0
			else: # if in stack
				if (match := regex_data_store.match(line)) is not None:
					stackPreProcessorOffset = StackPreProcessorOffset(match.group(1), offset, match.group(2)[-1], match.group(3))
					repo.add_new_value(stackPreProcessorOffset)
					lines[index] = stackPreProcessorOffset

					if match.group(2)[-1] == 'B' or match.group(2)[-1] == 'b':
						offset += 1 * int(match.group(3))
					if match.group(2)[-1] == 'W' or match.group(2)[-1] == 'w':
						offset += 2 * int(match.group(3))
					if match.group(2)[-1] == 'L' or match.group(2)[-1] == 'l':
						offset += 4 * int(match.group(3))

				elif (match := regex_label_data_store.match(line)) is not None:
					# TODO: check next line until label + instruction found 
					# The current code works for the moment being, but may need to be improve for edge cases not found yet
					if match2 := regex_data_store.match(lines[index + 1]):
						stackPreProcessorOffset = StackPreProcessorOffset(match.group(1), offset, match2.group(2)[-1], match2.group(3))
						repo.add_new_value(stackPreProcessorOffset)
						lines[index] = stackPreProcessorOffset
					elif match2 := regex_label_data_store.match(lines[index + 1]) is not None:
						raise Exception("Two label in a row. Not supported!")
					else:
						is_stack = False
				else:
					is_stack = False
		
		index += 1

	return

regex_global_data = re.compile(r"^\s*([A-Z][A-Z0-9_]*)[\s:]+(D[CS].[BWL])\s+(([\S\$\,\'\"]+\s*)+)", re.I)

class GlobalVar(PreProcessorValue):
	def __init__(self, string, store_type, data, const=False):
		super().__init__(string, 0)
		self.store_type = store_type.upper()
		self.data = data
		self.const = const
		

	def get_value(self):
		return f"&{self.string}"

	def __str__(self):
		return f"GlobalVar: [string: {self.string}, type: DC.{self.store_type}, point_to: '{self.data}', constant: {self.const}]"

	def compose(self):
		if self.const:
			if self.store_type == "B":
				return f"const char[] {self.string} = {self.data};"
			elif self.store_type == "W":
				return f"const short int[] {self.string} = {self.data}; // 2 Bytes per index"
			elif self.store_type == "L":
				return f"const int[] {self.string} = {self.data}; // 4 Bytes per index"
		else:
			if self.store_type == "B":
				return f"char[{self.data}] {self.string};"
			elif self.store_type == "W":
				return f"short int[{self.data}] {self.string}; // 2 Bytes per index"
			elif self.store_type == "L":
				return f"int[{self.data}] {self.string}; // 4 Bytes per index"
			


def global_var_parser(lines, index=0, repo=pre_proc):
	while index < len(lines):
		line = lines[index]

		if type(line) == type(""):
			if (match := regex_global_data.match(line)) is not None:
				global_data = GlobalVar(match.group(1), match.group(2)[-1], match.group(3), match.group(2)[1].upper() == "C")
				repo.add_new_value(global_data)
				lines[index] = global_data

		index += 1
	return

def pre_processor_value_parser(lines, index=0, repo=pre_proc):
	while index < len(lines):
		line = lines[index]

		if type(line) == type("") and repo.match_and_add(line):
				lines[index] = repo.get_last_value_added()

		index += 1

	return

def instruction_parser(lines, index=0, architecture=arch, repo=pre_proc):
	while index < len(lines):
		line = lines[index]

		if type(line) == type(""):
			instructions = architecture.matchInstruction(line, repo)
			n_instruction = len(instructions)
			if n_instruction == 0:
				pass
			elif n_instruction == 1:
				lines[index] = instructions[0]
			elif n_instruction > 1:
				lines[index] = instructions[0]
				for i in range(1, n_instruction):
					lines.insert(index + i, instructions[i])

		index += 1
	return 

def normalize_line(line):
	comment = line.find(';')
	if comment != -1:
		line = line[:comment]
	return line.strip()

def normalization_pass(lines, index=0):
	while index < len(lines):
		line = normalize_line(lines[index])
		if len(line) > 0:
			lines[index] = line
		else:
			lines.pop(index)
		index += 1