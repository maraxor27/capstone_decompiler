def is_condition(node, debug=False):
	return len(node.get_links()) == 2

def condition_exit(node, contains, debug=False):
	exit = None
	
	return exit

def condition_nodes(node, paths, debug=False):
	contains = []
	
	if debug:
		print(f"loop {node.get_id()} contains: {contains}")
	return contains

def condition_paths(node, paths, exit, debug=False):
	
	if debug:
		print(f"loop {node.get_id()} paths:")
		for path in inner_paths:
			print(path)
	return inner_paths