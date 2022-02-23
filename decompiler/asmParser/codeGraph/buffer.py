from .. import Label

class Buffer():
	generic_label_name_counter = 0
	def __init__(self, label=None):
		if issubclass(type(label), Label):
			self.label = label.getLabel()
		elif type(label) == type(""):
			self.label = label
		elif label is None:
			self.label = "UNKNOWN_LABEL_" + str(Buffer.generic_label_name_counter)
			Buffer.generic_label_name_counter += 1
		else:
			raise Exception("Wrong arg type for Buffer! Support Label, str and None")
			
		self.instructions = []

	def append(self, instruction):
		self.instructions.append(instruction)
		return

	def get_end(self):
		return self.instructions[-1]

	def get_label_name(self):
		return self.label