from .genericValueType import GenericValueType

class Register(GenericValueType):
	def __init__(self, name, size, var=True):
		self.name = name
		self.size = size
		self.var = var

	def can_be_var(self):
		return var

	def get_name(self):
		return "reg_" + str(self.name)

	def __eq__(self, other):
		return self.name.upper() == other.name.upper() and self.size == other.size

