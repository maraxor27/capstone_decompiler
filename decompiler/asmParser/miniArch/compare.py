from .miniArchInstruction import MiniArchInstruction

class Compare(MiniArchInstruction):
	def __init__(self, arg1, arg2, dependency=[]):
		self.arg1 = arg1
		self.arg2 = arg2
		self.dep = dependency

	def get_dependency(self):
		return self.dep

	def updates_ccr(self):
		return True

	def __str__(self):
		return f"{self.arg1} - {self.arg2};"