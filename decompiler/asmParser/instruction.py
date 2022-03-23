import re

from . import pre_proc

class BadInstructionClass(Exception):
	def __init__(self, msg):
		super().__init__(msg)
		return

class MetaInstruction(type):
	def __new__(cls, name, bases, dct):
		# Ensure name is defined for instruction
		if name != "Instruction" and name != "UnknownInstruction" and name[:7] != "Generic":
			if dct.get('name') is None:
				raise BadInstructionClass(f"Class variable 'name' must be defined in class {name}")
		
			# If no regex is defined, create one with the name
			if dct.get('regex') is None:
				# print(name, "is missing regex")
				dct['regex'] = re.compile(f"^{dct.get('name')}$", re.I)

		return super().__new__(cls, name, bases, dct) 


class Instruction(metaclass=MetaInstruction):
	name = None
	_regex = None
	num_arg = 0
	_regex_parsed = False
	_regex_main_group_indexes = None

	# The arg_XXXXX definition are depricated. The argument definition and 
	# regex have been moved to /decompiler/asmParser/arch_68hc12/arguments.

	arg_type_int = "[0-9]+"
	arg_type_hexa = "\\$[0-9A-Fa-f]+"
	arg_type_octal = "\\@[0-8]+"
	arg_type_binary = "\\%[01]+"
	arg_type_ascii = "\\'.+\\'"

	# Added to deal with global variable only in immediate and direct for now.
	arg_type_pointer = f"\\&[A-Z][A-Z0-9_]*(|\\+{arg_type_int}|-{arg_type_int})"
	arg_pre_proc_value = f"\\*[A-Z][A-Z0-9_]*(|\\+{arg_type_int}|-{arg_type_int})"

	arg_mask8 = "(\\$[0-9A-Fa-f]{1,2}|\\@[0-8]{1,3}|\\%[01]{1,8})"
	arg_inherent = "(A|B|D|X|Y|SP|PC)"
	arg_immediate = f"(#{arg_type_int}|#{arg_type_hexa}|#{arg_type_octal}|#{arg_type_binary}|#{arg_type_ascii}|#{arg_type_pointer}|#{arg_pre_proc_value})"
	arg_direct = f"({arg_type_int}|{arg_type_hexa}|{arg_type_octal}|{arg_type_binary}|{arg_type_pointer}|{arg_pre_proc_value})"
	arg_indexed = f"((A|B|D|(-|){arg_type_int}|{arg_type_hexa}|{arg_type_octal}|{arg_type_binary}|(-|){arg_pre_proc_value})\\s*,\\s*(\\+|-|)(X|Y|SP|PC)(\\+|-|))"
	arg_indexed_indirect = f"(\\[\\s*((-|){arg_type_int}|{arg_type_hexa}|{arg_type_octal}|{arg_type_binary}|(-|){arg_pre_proc_value})\\s*,\\s*(D|X|Y|SP|PC)\\s*\\])"
	

	def __init__(self, line):
		# Deep copy of the line
		self.line = '%s' % line

	@classmethod
	def _regex_parser(cls, pattern):
		counter = 1
		depth = 0
		for char in pattern:
			if (char == "("):
				if depth == 0:
					cls._regex_main_group_indexes.append(counter)
				counter += 1
				depth += 1
			elif (char == ")"):
				depth -= 1

	def parse_line(self, line, repo=pre_proc):
		try:
			return self._parse_line(line, repo)
		except:
			new_line = repo.try_replace_pre_proc_inline(line)
			if new_line == line:
				print(repo)
				print("old line:", line)
				print("new line:", new_line)
				raise Exception("Couldn't find pre-processor value in line:", line) 
			try:
				return self._parse_line(new_line, repo)
			except Exception as e:
				print("Pattern:", self._regex.pattern)
				print("old line:", line)
				print("new line:", new_line)
				raise Exception("Holly shit!!!")


	def _parse_line(self, line):
		raise Exception(f"_parse_line() needs to be implemented in the child class {type(self)}")

	def to_mini_arch(self):
		raise Exception(f"to_mini_arch must be implemented for non branching instruction")

	def getLine(self):
		return self.line

	def __str__(self):
		return f"Instruction: [text: \"{self.line}\"]"

	@classmethod
	def getName(cls):
		return cls.name

	# override if name can change
	@classmethod
	def getRegex(cls):
		return cls.regex

	def compose(self, align=0):
		return '\t'*align + self.__str__()


class UnknownInstruction(Instruction):
	def __init__(self, line):
		super().__init__(line)
		return

	def __str__(self):
		return "Unknown instruction: '" + self.line + "'"