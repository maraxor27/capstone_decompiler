import re

class Label():
	regex = re.compile("^([a-zA-Z][a-zA-Z0-9\\_]+)(:|)\\s*$", re.I)
	def __init__(self, name):
		self.name = name
		if name[-1] == ':':
			self.name = self.name[:-1]
		return 

	def getLabel(self):
		return self.name

	def __str__(self):
		return f"Label: [name: '{self.name}']"

	@classmethod
	def getRegex(cls):
		return cls.regex