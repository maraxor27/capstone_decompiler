from .. import GenericReturn

class Node():
	def __init__(self, buffer):
		self.buffer = buffer
		self.links = []
		self.reverse_links = []
		self.id = None

	def get_name(self):
		return self.buffer.get_label_name()

	def set_id(self, name):
		self.id = name

	def get_id(self):
		return self.id

	def add_link(self, link):
		self.links.append(link)

	def add_reverse_link(self, link):
		self.reverse_links.append(link)

	def get_links(self):
		return self.links

	def get_reverse_link(self):
		return self.reverse_links

	def link_string_links(self, nodes):
		for i in range(len(self.links)):
			if type(self.links[i]) == type(""):
				for node in nodes: 
					if node.get_name() == self.links[i]:
						self.links[i] = node
						break
				if type(self.links[i]) == type(""):
					raise Exception("Couldn't find label:", self.links[i], "in the nodes")
		return 

	def __str__(self):
		return self.to_string()

	def to_string(self, label=True, link=True):
		ret = ""

		if label:
			ret = f'Label: {self.get_name()}, id: {self.get_id()}\n'
			
		ret += f"--- {len(self.buffer.instructions)} instructions in this block ---\n"
		for inst in self.buffer.instructions:
			ret += f'\t{str(inst)}\n' 

		if link:
			ret += "Links: ["
			for l in self.get_links():
				ret += str(l.get_id()) + ","
			ret += "]\n"
		return ret

	def contains_return(self):
		return issubclass(type(self.buffer.get_end()), GenericReturn)

	def __repr__(self):
		return f'Node: [{self.get_name()}, id: {self.get_id()}]'

	# All the node name are supposed to be different. 
	# If not, there is a bug somewhere else or the provided code as an error
	def __eq__(self, other):
		if other is None:
			return False
		return self.get_name() == other.get_name()