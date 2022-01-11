class Condition:
	def __init__(self, prefix, content, not_cond=False):
		self.paths = paths
		self.if_content = []
		self.else_content = []
		self.not_cond = not_cond

	def add_to_if(self, elem):
		self.if_content.append(elem)

	def add_to_else(self, elem):
		self.else_content.append(elem)

	# TODO: redo once the class is fully done
	def __str__(self):
		ret = prefix.to_string(label=False, link=False)
		ret += "if ( " + ("!" if self.not_cond else "") + " <condition> ) {"
		for c in self.if_content:
			ret += str(c) + '\n'
		if len(self.else_content) > 0:
			ret += "} else {"
			for c in self.if_content:
				ret += str(c)
		ret += "}"	
		return ret