from ..codeGraph import Node
from ..miniArch import MiniCodeBlock

class Condition:
	def __init__(self, paths, prefix, merge, loop=None, not_cond=False):
		self.paths = paths
		self.prefix = prefix
		self.merge = merge
		self.loop = loop 
		self.if_content = []
		self.else_content = []
		self.not_cond = not_cond

	def add_to_if(self, elem):
		print(f"==========> added {type(elem)} to if content")
		self.if_content.append(elem)

	def add_to_else(self, elem):
		print(f"==========> added {type(elem)} to else content")
		self.else_content.append(elem)

	def contains(self, node):
		for content in [self.if_content, self.else_content]:
			for thing in content:
				if issubclass(type(thing), Node) or issubclass(type(thing), MiniCodeBlock):
					if thing.id == node.id:
						return True
				else: # can be either a Loop or a Condition
					if thing.contains(node):
						return True

	# TODO: redo once the class is fully done
	def __str__(self):
		ret = ""
		branch_cmp = self.prefix.get_branch_compare()
		if issubclass(type(self.prefix), Node):
			ret += self.prefix.to_string(label=True, link=False) + '\n'
		elif issubclass(type(self.prefix), MiniCodeBlock):
			ret += self.prefix.code_to_string(label=False, branch=False, link=False, exclude=[branch_cmp]) + '\n'
		else:
			ret += str(self.prefix) + '\n'

		cond = self.prefix.get_branch().get_condition(str(branch_cmp)[:-1])
		ret += "if (" + (" !" if self.not_cond else "") + f" {cond} ) {{\n"
		for c in self.if_content:
			ret += str(c)# + '\n'
		if len(self.else_content) > 0:
			ret += "} else {\n"
			for c in self.else_content:
				ret += str(c)
		ret += "}\n"	
		return ret

	def __repr__(self):
		return f"Condition: [prefix: {self.prefix.__repr__()}]"

class If(Condition):
	def __init__(self, condition):
		self.cond = condition

	def append(self, obj):
		self.cond.add_to_if(obj)

	def __repr__(self):
		return f"Condition-if: [prefix: {self.cond.prefix.__repr__()}, not_cond: {self.cond.not_cond}]"

class Else(Condition):
	def __init__(self, condition):
		self.cond = condition

	def append(self, obj):
		self.cond.add_to_else(obj)

	def __repr__(self):
		return f"Condition-else: [prefix: {self.cond.prefix.__repr__()}]"