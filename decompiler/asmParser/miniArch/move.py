from .miniArchInstruction import MiniArchInstruction

class Move(MiniArchInstruction):
	def __init__(self, dst, src, dependency=[]):
		self.dst = dst
		self.src = src
		self.dep = dependency

	def get_dependency(self):
		return self.dep

	def __str__(self):
		return f"{self.dst} = {self.src};"