from .miniArchInstruction import MiniArchInstruction

class Div(MiniArchInstruction):
	def __init__(self, dst, arg1, arg2, dependency=[]):
		self.quotient = dst
		self.arg1 = arg1
		self.arg2 = arg2
		self.dep = dependency

	def get_dependency(self):
		return self.dep

	def __str__(self):
		return f"{self.quotient} = {self.arg1} / {self.arg2};"

class Mod(MiniArchInstruction):
	def __init__(self, dst, arg1, arg2, dependency=[]):
		self.remainder = dst
		self.arg1 = arg1
		self.arg2 = arg2
		self.dep = dependency

	def get_dependency(self):
		return self.dep

	def __str__(self):
		return f"{self.remainder} = {self.arg1} % {self.arg2};"