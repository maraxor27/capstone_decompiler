from .miniArchInstruction import MiniArchInstruction

class MiniBreak(MiniArchInstruction):
	def __init__(self, dependency=[]):
		self.dep = dependency

	def get_dependency(self):
		return self.dep

	def __str__(self):
		return f"break;"

	def compose(self, align=1):
		return '\t'*align + self.__str__() + "\n"