from .parser import StackPreProcessorOffset

def compose_code_blocks(blocks, debug=False):
	function = ""
	if len(blocks) > 0:
		function = f"void {blocks[0].label}() {{\n"
		for block in blocks:
			function += block.compose()
		function += "\n}"
	else:
		raise Exception("Empty function!")
	return function


def compose(functions, global_vars, debug=False):
	code = ""
	for global_var in global_vars.getAll():
		if not issubclass(type(global_var), StackPreProcessorOffset):
			code += f"{global_var.compose()}\n"

	for func in functions:
		code += "\n/*\nStack layout of the function\n"
		code += f"{func[0].code_graph.get_stack()}"
		code += """
This function may or may not have arguments.
It is your job to figure this out with the stack and other information.
*/
"""
		code += f"{compose_code_blocks(func[1])}"

	print("\n---OUTPUT---\n")

	print(code)
	print("\n---END OUTPUT---\n")