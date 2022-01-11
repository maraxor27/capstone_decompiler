from .genericValueType import GenericValueType

class RelativeMemoryPointer(GenericValueType):
	def __init__(self, register, offset):
		self.register = register
		self.offset = offset

	def __eq__(self, other):
		return self.register == other.register and self.offset == other.offset