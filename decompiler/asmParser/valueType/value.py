from .genericValueType import GenericValueType

class Value(GenericValueType):
	def __init__(self, value):
		self.value = value

	def __eq__(self, other):
		return self.value == other.value