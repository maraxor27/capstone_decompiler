from ..genericBranch import GenericBranch
from ..genericReturn import GenericReturn
from .miniArchInstruction import MiniArchInstruction


class MiniCodeBlock:
	def __init__(self, node):
		self.id = node.id
		self.label = node.get_name()
		self.mini_code = self.convert_code_to_mini_arch(node.buffer.instructions)
		self.links = self.convert_links(node.get_links())
		self.reverse_links = self.convert_links(node.get_reverse_link())
		self.branch_cmp = self.get_branch_compare()

	def convert_code_to_mini_arch(self, instructions):
		mini_code = []
		for instruction in instructions:
			if not issubclass(type(instruction), GenericBranch):
				try:
					mini_code += instruction.to_mini_arch()
				except Exception as e:
					mini_code.append(instruction)
			else:
				mini_code.append(instruction)

		return mini_code

	def convert_links(self, links):
		links_id = []
		for link in links:
			links_id.append(link.get_id())
		return links_id

	def get_id(self):
		return self.id

	def get_links(self):
		return self.links

	def get_reverse_links(self):
		return self.reverse_links

	def get_branch(self):
		for line in self.mini_code:
			if issubclass(type(line), GenericBranch):
				return line
		return None

	def get_branch_compare(self):
		compare = None
		for i in range(len(self.mini_code)-1, -1, -1):
			if issubclass(type(self.mini_code[i]), MiniArchInstruction) and self.mini_code[i].updates_ccr():
				compare = self.mini_code[i]
				break
		return compare

	def contains_return(self):
		return issubclass(type(self.mini_code[-1]), GenericReturn)

	def code_to_string(self, label=True, branch=True, link=False, exclude=[]):
		ret = ""
		if label:
			ret = f'Label: {self.label}, id: {self.id}\n'
			
		for mini_instruction in self.mini_code:
			if not issubclass(type(mini_instruction), GenericBranch):
				if mini_instruction not in exclude:
					ret += f'\t{str(mini_instruction)}\n' 
			elif branch:
				ret += f'\t{str(mini_instruction)}\n' 

		if link:
			ret += "Links: ["
			for l in self.get_links():
				ret += str(l.get_id()) + ","
			ret += "]\n"
		return ret

	def __str__(self):
		return self.code_to_string(label=False, branch=False, link=False)

	def __repr__(self):
		return f"MiniCodeBlock:{{id: {self.id}}}"

	def __eq__(self, other):
		if other is None:
			return False
		return self.id == other.id