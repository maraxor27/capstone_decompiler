from .miniArchInstruction import MiniArchInstruction

class MiniReturn(MiniArchInstruction):
	def __init__(self, dependency=[]):
		self.dep = dependency

	def get_dependency(self):
		return self.dep

	def __str__(self):
		return f"return;"