class TempValue:
	id_counter = 0
	def __init__(self, value):
		self.value = value
		self.identifier = self.id_counter
		self.name = "var_" + str(self.identifier)
		self.id_counter += 1

	def get_value(self):
		return self.value

	def get_name(self):
		return self.name

	def __eq__(self, other):
		return self.identifier == other.identifier

	@classmethod
	def reset_id_counter(cls):
		cls.id_counter = 0