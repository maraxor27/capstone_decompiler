from .miniArchInstruction import MiniArchInstruction

class Add(MiniArchInstruction):
	def __init__(self, dst, arg1, arg2, dependency=[]):
		self.dst = dst
		self.arg1 = arg1
		self.arg2 = arg2
		self.dep = dependency

	def get_dependency(self):
		return self.dep

	def updates_ccr(self):
		return True

	def __str__(self):
		return f"{self.dst} = {self.arg1} + {self.arg2};"