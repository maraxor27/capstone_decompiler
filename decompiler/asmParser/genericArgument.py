class GenericArgument:
	def __init__(self, string):
		self.string = string
		self.value = None
		self.value_type = None

	def is_value_read_variable(self):
		return True

	def get_value_read_dependencies(self):
		return []

	def get_value(self):
		return self.value

	def get_value_type(self):
		return self.value_type

	def parse_arg(self, string):
		raise Exception("This needs to be implemented!!!")