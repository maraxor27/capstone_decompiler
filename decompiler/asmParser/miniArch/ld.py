from .miniArchInstruction import MiniArchInstruction

class Load(MiniArchInstruction):
	def __init__(self, dst, arg1, dependency=[]):
		self.dst = dst
		self.arg1 = arg1
		self.dep = dependency

	def get_dependency(self):
		return self.dep

	def __str__(self):
		return f"{self.dst} = {self.arg1};"