import re

class PreProcessorValue:
	def __init__(self, string, value):
		self.string = string
		self.value = value
		self.regex = re.compile(fr"([^A-Z0-9_\&\*])({string})(,|\s|$|\+[0-9]+)", re.I)

	def get_value(self):
		return f"*{self.string}"

	def get_string(self):
		return self.string

	def __eq__(self, other):
		return self.string == other.string

	def __str__(self):
		return f"PreProcessorValue: [string: '{self.string}', value: {self.value}]"

	def compose(self):
		c_value = self.value
		if c_value[0] == "%":
			c_value = '0b'+c_value[1:]
		elif c_value[0] == "@":
			c_value = hex(int(c_value[1:], 8)) + f" // This value was converted from octal to hexadecimal. Original value: {self.value}"
		elif c_value[0] == '$':
			c_value = hex(int(c_value[1:], 16))
		return f"#define {self.string} {c_value}"

# TODO: add check to through exception when trying to define name used by the compiler
class PreProcessorValueRepository:
	regex = re.compile(r"^\s*([A-Z][A-Z0-9_]*)[\s:]+EQU\s+(\S+)", re.I)
	def __init__(self):
		self.values = []
		self.last_value_added = None
		return

	def match_and_add(self, line):
		match = self.regex.match(line)
		if match is not None:
			self.add_new_value(PreProcessorValue(match.group(1), match.group(2)))
			return True
		return False

	def add_new_value(self, new_value):
		if new_value in self.values:
			raise Exception(f"'{new_value.get_string()}' already defined!")

		# if a value that is a string contained in the new_value put it at the end 
		# in order to ensure that the longuer string will be check for matching first.
		for i in range(len(self.values)):
			if self.values[i].string in new_value.string:
				self.last_value_added = new_value
				buffer = self.values[i]
				self.values[i] = new_value
				self.values.append(buffer)
				return
		self.values.append(new_value)
		self.last_value_added = new_value
		return

	def get_last_value_added(self):
		return self.last_value_added

	def try_replace_pre_proc_inline(self, line):
		for pre_value in self.values:
			m = re.search(pre_value.regex, line)
			if m is not None:
				pos = m.start()
				pre_char = line[m.start()]
				if pre_char != "&" or pre_char != "*":
					line = line[:pos + 1] + pre_value.get_value() + line[pos + 1 + len(pre_value.string):]
		return line

	def get_matching_object(self, string):
		normalized_string = string.upper()
		for pre_value in self.values:
			if normalized_string == pre_value.get_value().upper():
				return pre_value
		return None

	def getAll(self):
		return self.values

	def __str__(self):
		ret = "Pre-processor value defined: ["
		for pre_value in self.values:
			ret = ret + str(pre_value) + "\n "
		return ret + "]"