from .miniCodeBlock import MiniCodeBlock

class MiniFunction:
	def __init__(self, code_graph):
		self.code_graph = code_graph
		self.code_blocks = self.generate_mini_code_blocks(code_graph.nodes)
		self.link_blocks()

	def generate_mini_code_blocks(self, nodes):
		mini_code_block = []
		for node in nodes:
			mini_code_block.append(MiniCodeBlock(node))
		return mini_code_block

	def link_blocks(self, debug=False):
		for block in self.code_blocks:
			for link_index in range(len(block.links)):
				for link_block in self.code_blocks:
					if link_block.id == block.links[link_index]:
						block.links[link_index] = link_block
						break
			for link_index in range(len(block.reverse_links)):
				for link_block in self.code_blocks:
					if link_block.id == block.reverse_links[link_index]:
						block.reverse_links[link_index] = link_block
						break
			if debug:
				print("block", block, "links:", block.links, "reverse_links:", block.reverse_links)					
		return

	def __str__(self):
		for block in self.code_blocks:
			print(str(block))