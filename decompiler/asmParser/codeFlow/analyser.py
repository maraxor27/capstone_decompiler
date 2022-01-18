from .singleExitLoop import SingleExitLoop
from .loopAnalyser import *
from .condition import Condition, If, Else
from .conditionAnalyser import *

from ..codeGraph import Node


def analyse_code_path(nodes, debug=False):
	debug=True
	#analyse_code_path_v1(nodes, debug=debug)
	code_blocks = analyse_code_path_v2(nodes, start=nodes[0], debug=debug)

	print("--- Function code ---")
	print(f"void {nodes[0].label}() {{")
	for block in code_blocks:
		if issubclass(type(block), Node):
			print(block.to_string(label=False, link=False))
		else:
			try:
				print(block)
			except:
				print(type(block))
	print("}")

def analyse_code_path_v1(nodes, debug=False):
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
					print("Loop exit nodes:", lasts)
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
				elif node.get_links()[1] in lasts:
					raise Exception("Stand alone condition not implemented")
				else:
					raise Exception("Stand alone condition not implemented")
			else:
				if debug:
					print("TEST3")
				raise Exception("Stand alone condition not implemented")
		else:
			print("This shouldn't happen.")
		


	if debug or True:
		print("--- Function code ---")
		for block in code_block:
			if issubclass(type(block), Node):
				print(block.to_string(label=True, link=False))
			else:
				try:
					print(block)
				except:
					print(type(block))

def analyse_code_path_v2(nodes, start=None, end=None, paths=None, contexts=[], debug=False):
	node = None
	code_blocks = []

	if start is None:
		node = nodes[0]
	else:
		node = start

	if paths is None:
		paths = crawl_code(node)

	if debug:
		print("========> context <========")
		print("nodes:", nodes)
		print("start:", start.__repr__())
		if end is not None:
			print("end:", end.__repr__())
		else:
			print("end: None")
		print("paths:")
		for path in paths:
			print(path)
		print("contexts", contexts)
				
	while True:
		if debug:
			print(f"---------- node:{node.id} ----------")
		if len(contexts) == 0:
			node_links = node.get_links()
			n_links = len(node_links)

			if node not in nodes:
				break	

			elif n_links == 0:
				code_blocks.append(node)
				break

			elif is_loop(node, paths):
				l_content = loop_nodes(node, paths, debug=debug)
				l_exits = loop_exits(node, l_content, debug=debug)

				if len(l_exits) == 1:
					l_paths = loop_paths(node, paths, l_exits[0], debug=debug)
					loop = SingleExitLoop(l_paths, l_content, l_exits)

					contexts.append(loop)
					code_blocks.append(loop)
					if debug:
						print("------ Entering loop ------")
					analyse_code_path_v2(l_content, start=node, end=l_exits[0], paths=l_paths, contexts=contexts, debug=debug)
					
					contexts.pop(-1)
					node = l_exits[0]
				else:
					raise Exception("Multi exit loop not supported yet")

			elif n_links == 1:
				code_blocks.append(node)
				node = node_links[0]

			elif is_condition(node, paths): # equivalent to n_links == 2
				if_paths, else_paths, c_exit = condition_paths(node, paths, contexts=contexts, debug=debug)
				if debug:
					print("----- analyse_code_path_v2 -----")
					print("if_paths:", if_paths)
					print("else_paths:", else_paths)
					print("c_exit:", c_exit)
					
				if len(if_paths) > 0 and len(else_paths) > 0:
					condition = Condition(if_paths + else_paths, node, c_exit)
					code_blocks.append(condition)

					cond_if = If(condition)
					cond_if_content = condition_nodes(if_paths)
					contexts.append(cond_if)
					if debug:
						print("------ Entering if ------")
					analyse_code_path_v2(cond_if_content, start=if_paths[0][0], end=c_exit, paths=if_paths, contexts=contexts, debug=debug)
					contexts.pop(-1)

					cond_else = Else(condition)
					cond_else_content = condition_nodes(else_paths)
					contexts.append(cond_else)
					if debug:
						print("------ Entering else ------")
					analyse_code_path_v2(cond_else_content, start=else_paths[0][0], end=c_exit, paths=else_paths, contexts=contexts, debug=debug)
					contexts.pop(-1)

				elif len(if_paths) > 0 and len(else_paths) == 0:
					condition = Condition(if_paths + else_paths, node, c_exit)
					code_blocks.append(condition)

					cond_if = If(condition)
					cond_if_content = condition_nodes(if_paths)
					contexts.append(cond_if)
					if debug:
						print("------ Entering if ------")
					analyse_code_path_v2(cond_if_content, start=if_paths[0][0], end=c_exit, paths=if_paths, contexts=contexts, debug=debug)
					contexts.pop(-1)
				elif len(if_paths) == 0 and len(else_paths) > 0:
					condition = Condition(if_paths + else_paths, node, c_exit, not_cond=True)
					code_blocks.append(condition)

					cond_if = If(condition)
					cond_if_content = condition_nodes(else_paths)
					contexts.append(cond_if)
					if debug:
						print("------ Entering if not ------")
					analyse_code_path_v2(cond_if_content, start=if_paths[0][0], end=c_exit, paths=else_paths, contexts=contexts, debug=debug)
					contexts.pop(-1)
				else:
					raise Exception("if_path and else_path are empty. No condition? WTF!!!")
					
				node = c_exit

			else:
				code_blocks.append(node)
				node = node_links[0]

		else:
			node_links = node.get_links()
			n_links = len(node_links)
			if issubclass(type(contexts[-1]), SingleExitLoop) or issubclass(type(contexts[-1]), Condition):
				
				context_loop = None
				for context_index in range(len(contexts)-1, -1, -1):
					#print("context_index:", context_index, ":", contexts[context_index].__repr__())
					if issubclass(type(contexts[context_index]), SingleExitLoop):
						context_loop = contexts[context_index]
						break

				if debug:
					print("context_loop:", type(context_loop) if context_loop is not None else context_loop)
					if context_loop is not None:
						print("context_loop last nodes:", context_loop.get_last_nodes())

				if node not in nodes or node == end:
					break

				elif n_links == 0:
					raise Exception("End of function node found inside a loop!!!")

				elif is_loop(node, paths) and \
						(issubclass(type(contexts[-1]), Condition) or \
						 issubclass(type(contexts[-1]), SingleExitLoop) and contexts[-1].get_entry_node() != node):
					l_content = loop_nodes(node, paths, debug=debug)
					l_exits = loop_exits(node, l_content, debug=debug)

					if len(l_exits) == 1:
						l_paths = loop_paths(node, paths, l_exits[0], debug=debug)
						loop = SingleExitLoop(l_paths, l_content, l_exits)

						contexts[-1].append(loop)
						contexts.append(loop)
						
						if debug:
							print("------ Entering loop ------")
						analyse_code_path_v2(l_content, start=node, end=l_exits[0], paths=l_paths, contexts=contexts, debug=debug)
						
						contexts.pop(-1)
						node = l_exits[0]
					else:
						raise Exception("Multi exit loop not supported yet")

				elif n_links == 1:
					contexts[-1].append(node)
					node = node_links[0]

				elif is_condition(node, paths) and context_loop is not None and node not in context_loop.get_last_nodes(): # is_condition(node, paths) is equivalent to n_links == 2
					if_paths, else_paths, c_exit = condition_paths(node, paths, contexts=contexts, debug=debug)
					if debug:
						print("----- analyse_code_path_v2 -----")
						print("if_paths:", if_paths)
						print("else_paths:", else_paths)
						print("c_exit:", c_exit)

					if (len(if_paths) > 1 or len(if_paths) == 1 and if_paths[0][0] != c_exit) and len(else_paths) > 0:
						condition = Condition(if_paths + else_paths, node, c_exit)
						contexts[-1].append(condition)

						cond_if = If(condition)
						cond_if_content = condition_nodes(if_paths)
						contexts.append(cond_if)
						if debug:
							print("------ Entering if ------")
						analyse_code_path_v2(cond_if_content, start=if_paths[0][0], end=c_exit, paths=if_paths, contexts=contexts, debug=debug)
						contexts.pop(-1)

						cond_else = Else(condition)
						cond_else_content = condition_nodes(else_paths)
						contexts.append(cond_else)
						if debug:
							print("------ Entering else ------")
						analyse_code_path_v2(cond_else_content, start=else_paths[0][0], end=c_exit, paths=else_paths, contexts=contexts, debug=debug)
						contexts.pop(-1)

					elif (len(if_paths) > 1 or len(if_paths) == 1 and if_paths[0][0] != c_exit) and len(else_paths) == 0:
						condition = Condition(if_paths + else_paths, node, c_exit)
						contexts[-1].append(condition)

						cond_if = If(condition)
						cond_if_content = condition_nodes(if_paths)
						contexts.append(cond_if)
						if debug:
							print("------ Entering if ------")
						analyse_code_path_v2(cond_if_content, start=if_paths[0][0], end=c_exit, paths=if_paths, contexts=contexts, debug=debug)
						contexts.pop(-1)
					elif len(else_paths) > 0:
						condition = Condition(if_paths + else_paths, node, c_exit, not_cond=True)
						contexts[-1].append(condition)

						cond_if = If(condition)
						cond_if_content = condition_nodes(else_paths)
						contexts.append(cond_if)
						if debug:
							print("------ Entering if not ------")
						analyse_code_path_v2(cond_if_content, start=else_paths[0][0], end=c_exit, paths=else_paths, contexts=contexts, debug=debug)
						contexts.pop(-1)
					else:
						raise Exception("if_path and else_path are empty. No condition? WTF!!!")
						
					node = c_exit
				elif issubclass(type(contexts[-1]), SingleExitLoop) and node in context_loop.get_last_nodes():
					context_loop.add_loop_cond_node(node)
					node = node_links[0]
				else:
					contexts[-1].append(node)
					node = node_links[0]
			else:
				raise Exception("Unsupported obj type:", contexts[-1])
	if debug:
		print("========> exit context <========")
	return code_blocks

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