import re

from . import BaseInstruction, load
from .. import GenericArgument, pre_proc


@load
class ArgInherent(GenericArgument): #Inhenrent addressing
	regex = re.compile(f"^{BaseInstruction.arg_inherent}$", re.I)

	def __init__(self, string):
		super().__init__(string)

	def parse(self, string):
		if len(string) == 0:
			raise Exception("Can't create a ArgInherent with empty string")

	def get_value(self):
		return f"reg_{self.string}"

	def __str__(self):
		return f"ArgInherent: [string: {self.string}]"


arg_type_int = "[0-9]+"

arg_type_hexa = "\\$[0-9A-Fa-f]+"
regex_arg_type_hexa = re.compile(arg_type_hexa, re.I)
arg_type_octal = "\\@[0-8]+"
regex_arg_type_octal = re.compile(arg_type_octal, re.I)
arg_type_binary = "\\%[01]+"
regex_arg_type_binary = re.compile(arg_type_binary, re.I)
arg_type_pointer = f"\\&[A-Z][A-Z0-9_]*(|\\+{arg_type_int}|-{arg_type_int})"
regex_arg_type_pointer = re.compile(arg_type_pointer, re.I)
arg_pre_proc_value = f"\\*[A-Z][A-Z0-9_]*(|\\+{arg_type_int}|-{arg_type_int})"
regex_arg_pre_proc_value = re.compile(arg_pre_proc_value, re.I)
arg_type_ascii = "\\'.+\\'"
regex_arg_type_ascii = re.compile(arg_type_ascii, re.I)

arg_mask8 = "(\\$[0-9A-Fa-f]{1,2}|\\@[0-8]{1,3}|\\%[01]{1,8})"
arg_inherent = "(A|B|D|X|Y|SP|PC)"
arg_immediate = f"(#(-|){arg_type_int}|#{arg_type_hexa}|#{arg_type_octal}|#{arg_type_binary}|#{arg_type_ascii}|#{arg_type_pointer}|#{arg_pre_proc_value})"
arg_indexed = f"((A|B|D|(-|){arg_type_int}|{arg_type_hexa}|{arg_type_octal}|{arg_type_binary}|(-|){arg_pre_proc_value})\\s*,\\s*(\\+|-|)(X|Y|SP|PC)(\\+|-|))"
arg_direct = f"({arg_type_int}|{arg_type_hexa}|{arg_type_octal}|{arg_type_binary}|{arg_type_pointer}|{arg_pre_proc_value})"
arg_indexed_indirect = f"(\\[\\s*((-|){arg_type_int}|{arg_type_hexa}|{arg_type_octal}|{arg_type_binary}|(-|){arg_pre_proc_value})\\s*,\\s*(D|X|Y|SP|PC)\\s*\\])"

@load
class ArgImmediate(GenericArgument): #Immediate Addressing
	regex = re.compile(f"^{arg_immediate}$", re.I)

	def __init__(self, string):
		super().__init__(string)
		(self.prefix, self.value, self.suffix) = self.parse(str(string))

	def parse(self, string):
		if len(string) == 0:
			raise Exception("Can't create a ArgImmediate with empty string")

		if m := regex_arg_type_hexa.match(string[1:]): # hexadecimal
			return ('0x', int(m.group(0)[1:], 16), '')
		elif m := regex_arg_type_octal.match(string[1:]): # octal
			return ('0x', int(m.group(0)[1:], 8), '') # All octal value will be shown in hexadecimal
		elif m := regex_arg_type_binary.match(string[1:]): # binary
			return ('0b', int(m.group(0)[1:], 2), '')
		elif m := regex_arg_type_pointer.match(string[1:]):
			return ('', pre_proc.get_matching_object(string[1:]), '')
		elif m := regex_arg_pre_proc_value.match(string[1:]):
			return ('', pre_proc.get_matching_object(string[1:]), '')
		elif m := regex_arg_type_ascii.match(string[1:]): # char array
			value = 0
			for char in range(1,len(m.group(0)[1:-1])):
				value = value * 256 + ord(char)
			return ('\'', value, '\'')
		else:
			return ('', int(string[1:], 10), '')

	def get_value(self):
		value = self.value
		if self.prefix == "0x":
			value = str(hex(value))[2:]
		elif self.prefix == "0b":
			value = str(bin(value))[2:]
		return f"{self.prefix}{value}{self.suffix}"

	def __str__(self):
		return f"ArgImmediate: [value: {self.value}, string: {self.string}]"


@load
class ArgDirect(GenericArgument): #Direct, extended and relative Addressing
	regex = re.compile(f"^{arg_direct}$", re.I)

	def __init__(self, string):
		super().__init__(string)
		(self.prefix, self.value, self.suffix) = self.parse(str(string))

	def parse(self, string):
		try:
			if len(string) == 0:
				raise Exception("Can't create a ArgDirect with empty string")

			if m := regex_arg_type_hexa.match(string): # hexadecimal
				return ('0x', int(m.group(0)[1:], 16), '')
			elif m := regex_arg_type_octal.match(string): # octal
				return ('0x', int(m.group(0)[1:], 8), '') # All octal value will be shown in hexadecimal
			elif m := regex_arg_type_binary.match(string): # binary
				return ('0b', int(m.group(0)[1:], 2), '')
			elif m := regex_arg_type_pointer.match(string):
				return ('global var', '', '')
			elif m := regex_arg_pre_proc_value.match(string):
				return ('global const var', '', '')
			elif m := regex_arg_type_ascii.match(string): # char array
				value = 0
				for char in range(1,len(m.group(0)[1:-1])):
					value = value * 256 + ord(char)
				return ('\'', value, '\'')
			else:
				return ('', int(string, 10), '')
		except Exception as e:
			print(f"Error while parsing \"{string}\" as ArgDirect")
			raise e

	def get_value(self):
		value = self.value
		if self.prefix == "0x":
			value = str(hex(value))[2:]
		elif self.prefix == "0b":
			value = str(bin(value))[2:]
		return f"*{self.prefix}{value}{self.suffix}"

	def __str__(self):
		return f"ArgDirect: [c_format: {self.prefix}{self.value}{self.suffix}, string: {self.string}]"


@load
class ArgIndexed(GenericArgument): #indexed Addressing
	regex = re.compile(f"^{arg_indexed}$", re.I)
	arg_regex = re.compile(r"^\s*([^,]+)\s*,\s*([^,]+)\s*", re.I)
	def __init__(self, string):
		super().__init__(string)
		# (self.value, self.prefix) = self.parse(str(string))

	def parse(self, string):
		if len(string) == 0:
			raise Exception("Can't create a ArgIndexed with empty string")

		match = self.arg_regex.match(string)
		arg1 = match.group(1)
		arg2 = match.group(2)
		print("arg1:", arg1)
		print("arg2:", arg2)

	def get_value(self):
		return f"some ArgIndexed"

	def __str__(self):
		return f"ArgIndexed: [string: {self.string}]"


@load
class ArgIndexedIndirect(GenericArgument): #indexed-indirect Addressing
	regex = re.compile(f"^{arg_indexed}$", re.I)

	def __init__(self, string):
		super().__init__(string)
		# (self.value, self.prefix) = self.parse(str(string))

	def parse(self, string):
		if len(string) == 0:
			raise Exception("Can't create a ArgIndexedIndirect with empty string")

	def get_value(self):
		return f"some ArgIndexedIndirect"

	def __str__(self):
		return f"ArgIndexedIndirect: [string: {self.string}]"