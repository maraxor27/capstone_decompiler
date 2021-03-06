import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from .node import Node
from .buffer import Buffer

from .. import Label
from .. import Instruction
from .. import GenericReturn
from .. import GenericBranch
from ..parser import StackPreProcessorOffset

class CodeGraph():
	def __init__(self):
		self.stack = []
		self.nodes = []
		self.instruction_buffer = []
		self.functionName = "Unknown"
		return

	def input(self, instructions):
		self.instruction_buffer += instructions

	def parse_instruction_buffer(self):
		self.parser_first_pass()
		self.parser_final_linking()
		for node in self.nodes:
			if len(links := node.get_links()) == 2 and links[0] == links[1]:
				raise Exception("Branch in node is it's usefull at all!!!")
		self.set_ids()

	def parser_first_pass(self, debug=False):
		links = []
		start = False
		buffer = None
		node = None
		while len(self.instruction_buffer) > 0:
			instruction = self.instruction_buffer.pop(0)
			
			try:
				# Any instruction before the first label is not considered to be part of the function
				if not start:
					if issubclass(type(instruction), StackPreProcessorOffset):
						self.stack.append(instruction)
					elif issubclass(type(instruction), Label):
						start = True

						buffer = Buffer(instruction)
						node = Node(buffer) 
						self.nodes.append(node) 

						self.functionName = instruction.getLabel()
						if debug:
							print("Function found:", self.functionName)
				else:
					# For each label or branching instruction within the function a new buffer and 
					# a new node are created to do code separation
					if issubclass(type((label := instruction)), Label):
						if label.getLabel() in links:
							raise Exception(f"Duplicate label detected! Label: {label.getLabel()}")
						links.append(label.getLabel())

						new_buffer = Buffer(label)
						new_node = Node(new_buffer)
						node.add_link(new_node)
						self.nodes.append(new_node) 

						buffer = new_buffer
						node = new_node
					elif issubclass(type((branch := instruction)), GenericBranch):
						buffer.append(branch)
						if branch.n_path == 1:
							if issubclass(type(self.instruction_buffer[0]), Label):
								new_buffer = Buffer(self.instruction_buffer.pop(0))
							else:
								new_buffer = Buffer()
							new_node = Node(new_buffer)
							node.add_link(branch.operand)
							self.nodes.append(new_node) 

							buffer = new_buffer
							node = new_node

						elif branch.n_path == 2:
							if issubclass(type(self.instruction_buffer[0]), Label):
								new_buffer = Buffer(self.instruction_buffer.pop(0))
							else:
								new_buffer = Buffer()
							new_node = Node(new_buffer)
							node.add_link(new_node)
							node.add_link(branch.operand)
							self.nodes.append(new_node) 

							buffer = new_buffer
							node = new_node
					elif issubclass(type(instruction), Instruction):
						buffer.append(instruction)
						if issubclass(type(instruction), GenericReturn):
							if len(self.nodes) > 1 and "UNKNOWN_LABEL_" in buffer.label and "end_of_function" not in links:
								buffer.label = "end_of_function"
							break
			except Exception as e:
				print("Error with instruction:", instruction)
				print("10 next instructions:")
				for i in range(1, 10):
					print(str(self.instruction_buffer[i]))
				raise e
		return

	def parser_final_linking(self):
		for node in self.nodes:
			node.link_string_links(self.nodes)
			for link in node.get_links():
				link.add_reverse_link(node)
		return
	
	def set_ids(self, debug=False):
		index = 0
		for node in self.nodes:
			node.set_id(index)
			index += 1

	def remove_extra_instructions(self):
		instructions = self.instruction_buffer
		self.instruction_buffer = []
		return instructions

	def print_instruction_buffer(self):
		print("Instruction Buffer:")
		for inst in self.instruction_buffer:
			print('\t' + str(inst))

	def print_asm_function(self):
		if len(self.stack) > 0: 
			print("Stack Layout")
			for var in self.stack:
				print("\t"+str(var))
		for node in self.nodes:
			print(node)

	def show(self, id=False, debug=False):
		fromNodeName = []
		ToNodeName = []

		for node in self.nodes:
			for next_node in node.get_links():
				if id:
					fromNodeName.append(node.get_id())
					ToNodeName.append(next_node.get_id())
				else:
					fromNodeName.append(node.get_name())
					ToNodeName.append(next_node.get_name())

		df = pd.DataFrame({ 'from':fromNodeName, 'to':ToNodeName})

		G=nx.from_pandas_edgelist(df, 'from', 'to', create_using=nx.DiGraph())
		for node in self.nodes:
			if len(node.get_links()) == 0:
				if id:
					G.add_node(node.get_id())
				else:
					G.add_node(node.get_name())
		 
		nx.draw(G, with_labels=True, node_size=1500, alpha=0.5, arrows=True)
		plt.title("Directed")
		plt.get_current_fig_manager().set_window_title(self.functionName)
		plt.show()