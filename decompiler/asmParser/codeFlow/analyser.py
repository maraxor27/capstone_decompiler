from .singleExitLoop import SingleExitLoop
from .loopAnalyser import *
from .conditionAnalyser import *

from ..codeGraph import Node



def analyse_code_path(nodes, debug=False):
	debug=True
	path_list = crawl_code(nodes[0])
	if debug or True:
		print("All path of the function")
		for path in path_list:
			print(path)
	code_block = []
	context = []
	for node_index in range(len(nodes)):
		node = nodes[node_index]
		if debug:
			print("--- Analysing:", node.__repr__(), "---")
		if len(context) > 0:
			while len(context) > 0 and not context[-1].contains(node):
				context.pop()
			
		in_loop = False
		loop_context_index = None

		if len(context) > 0:
			if debug:
				print("Current context:", type(context[-1]))
			for index in range(len(context) - 1, -1, -1):
				print(index)
				if issubclass(type(context[index]), SingleExitLoop):
					print("Found loop context")
					in_loop = True
					loop_context_index = index
					break

		if len(node.get_links()) == 0:
			if debug:
				print("Found end of function") 
			code_block.append(node)
			continue

		if is_loop(node, path_list, debug=debug):
			if debug:
				print("Loop found")
			content = loop_nodes(node, path_list, debug=debug)
			exits = loop_exits(node, content, debug=debug)
			if len(exits) == 1:
				paths = loop_paths(node, path_list, exits[0], debug=debug)
				loop = SingleExitLoop(paths, content, exits)
				if len(context) == 0:
					code_block.append(loop)
				else:
					context[-1].append(loop)
				context.append(loop)
				in_loop = True
				loop_context_index = len(context) - 1
			else:
				raise Exception(f"Number of loop exit not supported. {len(exits)} exits found!")
		
		if len(node.get_links()) == 1: 
			if debug:
				print("Linear node")
			if len(context) == 0:
				code_block.append(node)
			else:
				context[-1].append(node)
			continue

		if is_condition(node, debug=debug):
			# if this is the last node of a loop
			if in_loop:
				lasts = context[loop_context_index].get_last_nodes()
				if debug:
					print("Current loop entry point:", context[loop_context_index].get_entry_node().__repr__())
					print("Current node links:", node.get_links())
				if context[loop_context_index].get_entry_node() in node.get_links():
					if debug:
						print("while condition found")
					context[loop_context_index].add_loop_cond_node(node)
				elif len(lasts) == 0 and node == lasts[0]:
					raise Exception("if break not implemented")
				elif node in lasts:
					print(lasts)
					raise Exception("multi loop exit not implemented")
				elif node.get_links[1] in lasts:
					context[loop_context_index].append(Condition(node, [], not_cond=True))
				else:
					if debug:
						print("TEST2")
					context[loop_context_index].append(node)
			else:
				if debug:
					print("TEST3")
				raise Exception("Stand alone condition not implemented")
		else:
			print("This shouldn't happen.")
		


	if debug or True:
		for block in code_block:
			if issubclass(type(block), Node):
				print(block.to_string(label=True, link=False))
			else:
				try:
					print(block)
				except:
					print(type(block))

def crawl_code(c_node, path=[]):
	paths = []
	path = path + [c_node]
	for next_node in c_node.get_links():
		new_path = path + [next_node]
		if next_node in path:
			paths.append(new_path)
		elif next_node.contains_return():
			paths.append(new_path)
		else:
			paths += crawl_code(next_node, path)
	return paths