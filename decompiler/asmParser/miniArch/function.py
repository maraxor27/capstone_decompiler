from .miniArchInstruction import MiniArchInstruction

class Function(MiniArchInstruction):
	def __init__(self, name, dependency=[]):
		self.name = name
		self.dep = dependency

	def get_dependency(self):
		return self.dep

	def __str__(self):
		return f"{self.name}(); // Argument and return value are not detected"