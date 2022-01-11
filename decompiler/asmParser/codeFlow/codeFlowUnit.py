class CodeFlowUnit:
	def __init__(self, content):
		self.content = content

	def contains(self, node):
		return node in self.content
