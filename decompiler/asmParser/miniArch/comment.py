from .miniArchInstruction import MiniArchInstruction

class Comment(MiniArchInstruction):
	def __init__(self, info, dependency=[]):
		self.info = info
		self.dep = dependency

	def get_dependency(self):
		return self.dep

	def __str__(self):
		return "// "+self.info