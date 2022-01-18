from .singleExitLoop import SingleExitLoop

def is_condition(node, debug=False):
	return len(node.get_links()) == 2

def condition_nodes(paths, debug=False):
	contains = []
	
	for path in paths:
		for node in path:
			if node not in contains:
				contains.append(node)
	return contains

def find(arr, val):
	try:
		return arr.index(val)
	except:
		return -1

def condition_paths(node, paths, contexts=[], debug=False):
	cond_paths = []
	
	loop = None
	for i in range(len(contexts)-1, -1, -1):
		if issubclass(type(contexts[i]), SingleExitLoop):
			loop = contexts[i]
			break

	for path in paths:
		if (node_index := find(path, node)) != -1:
			c_path = path[node_index + 1:]
			if c_path not in cond_paths:# and len(c_path) > 1:
				cond_paths.append(c_path)

	if_paths = []
	else_paths = []
	exit = None

	if debug:
		print(f"From paths:")
		for path in paths:
			print(path)
		print(f"Unique path for condition after node:{node.id}")
		for path in cond_paths:
			print(path)

	for path_node in cond_paths[0]:
		in_every_path = True
		for path in cond_paths:
			last_node = path[-1]
			path_contains_loop = len(path) - 1 == path.index(last_node)
			if loop is None or loop.get_entry_node() != path[-1] or not path_contains_loop:
				if path_node not in path:
					in_every_path = False
					break

		if in_every_path:
			exit = path_node
			break

	if exit is None:
		raise Exception("Couldn't exit node for this condition")

	if debug:
		print(f"exit:{exit.id}")

	node_links = node.get_links()

	if debug:
		print(f"node_links:{node_links}")

	for path in cond_paths:
		exit_index = find(path, exit)
		if debug:
			print(f"path:{path}")

		# if paths 
		if path[0] == node_links[1]:
			if exit_index == -1:
				if len(path) > 0 and path not in if_paths:
					if_paths.append(path)
			else:
				p = path[:exit_index+1]
				if len(p) > 0 and p not in if_paths:
					if_paths.append(p)

		# else paths
		elif path[0] == node_links[0]:
			if exit_index == -1:
				if path not in else_paths:
					else_paths.append(path)
			else:
				if path[:exit_index+1] not in else_paths:
					else_paths.append(path[:exit_index+1])

		# This is not supposed to happen
		else:
			raise Exception(f"Unsupported path: {path} for node: {node.id}")

	if debug:
		print(f"node: {node.id}")
		print(f"if_paths: {if_paths}")
		print(f"else_paths: {else_paths}")
		print(f"exit: {exit.__repr__()}")

	return (if_paths, else_paths, exit)