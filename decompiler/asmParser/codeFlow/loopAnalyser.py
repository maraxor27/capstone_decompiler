def is_loop(node, paths, debug=False):
	for path in paths:
		if path[-1] == node and path.index(node) != len(path) - 1:
			if debug:
				print("First loop path found:", path)
			return True
	return False

def loop_nodes(node, paths, debug=False):
	contains = []
	for path in paths:
		if path[-1] == node:
			for loop_node in path[path.index(node):-1]:
				if loop_node not in contains:
					contains.append(loop_node)
	contains.sort(key=lambda x: x.get_id())
	if debug:
		print(f"loop {node.get_id()} contains: {contains}")
	return contains

def loop_exits(node, contains, debug=False):
	exits = []
	for loop_node in contains:
		for link in loop_node.get_links():
			if link not in exits and link not in contains:
				exits.append(link)
	if debug:
		print(f"loop {node.get_id()} exits: {exits}")
	return exits

def loop_paths(node, paths, exit, debug=False):
	inner_paths = []
	for path in paths:
		if path[-1] == node:
			inner_path = path[path.index(node):]
			if inner_path not in inner_paths:
				inner_paths.append(inner_path)
		if exit in path and node in path and path.index(node) < path.index(exit):
			inner_path = path[path.index(node):path.index(exit)+1]
			if inner_path not in inner_paths:
				inner_paths.append(inner_path)

	if debug:
		print(f"loop {node.get_id()} paths:")
		for path in inner_paths:
			print(path)
	return inner_paths