from ..codeGraph import Node
from ..miniArch import MiniCodeBlock

class SingleExitLoop:
	def __init__(self, paths, content, exit):
		self.content = content
		print("created loop with following paths")
		for path in paths:
			print(path)
		self.paths = paths
		self.exit = exit
		self.order = []
		self.loop_back_node = []

	def append(self, obj):
		try:
			print(f"adding {obj.id} to loop {self.content}")
		except Exception as e:
			print(f"adding obj to loop {self.content}")
		self.order.append(obj)

	def get_entry_node(self):
		return self.paths[0][0]

	def get_last_nodes(self, debug=False):
		lasts = []
		if debug:
			print("get_last_nodes debug")
		for link in self.get_entry_node().get_reverse_links():
			if debug:
				print(link.__repr__(), "can go to", self.get_entry_node().__repr__())
			if self.contains(link) and link not in lasts:
				lasts.append(link)
		if debug:
			print("lasts node from loop:", lasts)
		return lasts

	def add_loop_cond_node(self, node):
		self.append(node)
		self.loop_back_node.append(node)

	def contains(self, node):
		print("self.content:", self.content)
		print("node:", node)
		return node in self.content

	# TODO: redo once the class is fully done
	def __str__(self):
		ret = "do {\n"
		if len(self.loop_back_node) == 0:
			for c in self.order:
				if issubclass(type(c), Node):
					ret += c.to_string(label=True, link=False) + '\n'
				elif issubclass(type(c), MiniCodeBlock):
					ret += c.code_to_string(label=True, link=False) + '\n'
				else:
					ret += str(c) + '\n'
			ret = ret + "} while (True);"
		elif len(self.loop_back_node) == 1:
			loop_condition = "<condition>"
			for c in self.order:
				if issubclass(type(c), Node):
					ret += c.to_string(label=True, link=False) + '\n'
				elif issubclass(type(c), MiniCodeBlock):
					if c in self.loop_back_node:
						branch_cmp = c.get_branch_compare()
						ret += c.code_to_string(label=False, branch=False, link=False, exclude=[branch_cmp]) + '\n'
						loop_condition = c.get_branch().get_condition(str(branch_cmp)[:-1])
					else:
						ret += c.code_to_string(label=False, link=False) + '\n'
				else:
					ret += str(c) + '\n'
			ret = ret + f"}} while ( {loop_condition} );"
		elif len(self.loop_back_node) > 1:
			for c in self.order:
				if issubclass(type(c), Node):
					ret += c.to_string(label=True, link=False) + '\n'
					if c in self.loop_back_node:
						loop_condition = c.get_branch().get_condition("test_var")
						ret += f"if ( {loop_condition} ) continue; \n"
				else:
					ret += str(c) + '\n'
			ret = ret + "} while (True);"
		return ret


		