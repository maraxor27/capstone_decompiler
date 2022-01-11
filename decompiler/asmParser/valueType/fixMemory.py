from .genericValueType import GenericValueType

class FixMemory(GenericValueType):
	def __init__(self, address):
		self.address = address

	def __eq__(self, other):
		return self.address == other.address