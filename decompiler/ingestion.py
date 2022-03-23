import re
import time
import threading

from .asmParser import *


def is_letter(value):
	char = ord(value)
	return ord('A') <= char <= ord('Z') or ord('a') <= char <= ord('z')

def extract_instructions(folder, file):
	instructions = []
	while True:
		line = file.readline()
		if not line:
			break

		# remove any space at the front or the end of the line.
		striped = line.strip()

		if not striped:
			continue

		# skip lines that are only comments
		if not is_letter(striped[0]):
			continue

		striped = striped.replace("\t", " ")
		striped = re.sub(' +', ' ', striped)
		
		if includes.match_and_add(striped):
			filename = includes.get_filename_to_include()
			print("Including", filename)
			included_file = open(folder + "/" + filename, 'r')
			instructions += extract_instructions(folder, included_file)
			print("Finished including", filename)

		#check for pre processor value def
		if pre_proc.match_and_add(striped):
			continue
		
		instuction = arch.matchInstruction(striped)
		instructions += instuction

	return instructions

def read_file_with_include(folder, filename, depth=0, debug=False, do_include=True):
	""" read_file_with_include(folder, filename, depth=0, debug=False, do_include=True) -> list
	Return value:
	list of string which represent the whole assembly code.

	Arguments:
	folder -- String of the base folder of the asm code.
	filename -- String of the filename that needs to be read.
	depth -- Use on recursive call for debugging.
	debug -- Must be a boolean. True to enable debug.
	do_include -- When True and an include command is found, will read the included file 
				  and append its line at the current position in the list.
	"""
	lines = []
	file = open(folder + "/" + filename, 'r')

	if debug:
		print(" " * depth + "Including", filename)

	while True:
		line = file.readline()
		if not line:
			break

		striped = line.strip()
		if not striped:
			continue

		# skip lines that are only comments
		if not is_letter(striped[0]):
			continue

		striped = striped.replace("\t", " ")
		striped = re.sub(' +', ' ', striped)

		if includes.match_and_add(striped):
			if do_include: 
				next_filename = includes.get_filename_to_include()
				lines += read_file_with_include(folder, next_filename, depth + 1, debug)
			continue

		lines.append(striped)

	if debug:
		print(" " * depth + "Finished including", filename)

	return lines

def decompileLines(lines, debug=False):
	finish_reading_files = time.time()
	normalization_pass(lines)
	finish_normalization_pass = time.time()
	print(f"{(finish_normalization_pass - finish_reading_files) * 1000} ms taken to normalize the lines")
	
	pre_proc_repo = PreProcessorValueRepository()
	inst_repo = arch
	
	# This pass will parse lines of the following format
	# offset 0
	# FN_varN DS.L 1
	# ...
	# FN_var1 DS.B 4
	# FN_STACK
	# ... other registers that are pushed on the stack in the function
	# FN_REGX DS.W 1
	# FN_REGA DS.B 1
	# FN_RETURN_ADDR DS.W 1
	stack_parser(lines, repo=pre_proc_repo)
	finish_stack_pass = time.time()
	print(f"{(finish_stack_pass - finish_normalization_pass) * 1000} ms taken to analyse all function stack")
	
	# This pass will parse line of the following format
	# NAME_bin EQU %10101010
	# NAME_hexa EQU $FF
	# NAME_oct EQU @377
	# NAME_int EQU 255
	# and other format
	pre_processor_value_parser(lines, repo=pre_proc_repo)
	finish_pre_processor_pass = time.time()
	print(f"{(finish_pre_processor_pass - finish_stack_pass) * 1000} ms taken to analyse all pre processor value definition")
	

	# This pass will parse line of the following format
	# - Global var example
	# NAME_var DS.W 2
	# 
	# - Global const var example
	# NAME_const_var DC.B 1
	global_var_parser(lines, repo=pre_proc_repo)
	finish_global_var_pass = time.time()
	print(f"{(finish_global_var_pass - finish_pre_processor_pass) * 1000} ms taken to analyse all global variable")
	
	# This pass parses all the instruction in the lines
	# 
	instruction_parser(lines, architecture=inst_repo, repo=pre_proc_repo)
	finish_instruction_pass = time.time()
	print(f"{(finish_instruction_pass - finish_global_var_pass) * 1000} ms taken to analyse all instructions")
	if debug:
		for line in lines:
			print(line)

	# Create a code graph for each function in the lines. The name of the 
	# function is defined as the string of the first label of a function.
	# The end of the function is the first rts, swi found.
	cgs = []
	program = []
	functions = []
	program += lines
	while len(program) > 0:
		cg = CodeGraph()
		cg.input(program)
		found = cg.parse_instruction_buffer()
		if found:	
			cgs.append(cg)
		program = cg.remove_extra_instructions()

	if debug:
		if len(cgs) > 0:	
			for cg in cgs:
				print(f"Found: {cg.functionName}",flush=True)
		else:
			print('No Function found!',flush=True)

	finish_code_graph_gen = time.time()
	print(f"{(finish_code_graph_gen - finish_instruction_pass) * 1000} ms taken to create all code graphs")
	
	for code_graph in cgs:
		mini_arch_func = MiniFunction(code_graph)

		show_thread = False
		t = threading.Thread(target=CodeGraph.show, args=(code_graph,), kwargs={"id":True,"debug":False,})
		if show_thread:
			t.start()
			time.sleep(1)
		

		functions.append((mini_arch_func, analyse_code_path(mini_arch_func.code_blocks, debug=debug)))

		if show_thread:
			t.join()	
	
	end = time.time()
	print(f"{(end - finish_reading_files) * 1000} ms for decompilation",flush=True)

	return compose(functions, pre_proc_repo, debug)

def decompileFiles(folder, filename, debug=False):
	decompilation_start = time.time()
	lines = read_file_with_include(folder, filename, debug=debug, do_include=True)
	finish_reading_files = time.time()
	print(f"{(finish_reading_files - decompilation_start) * 1000} ms taken to read all the required files")

	decompileLines(lines, debug)

def decompile(folder, filename, debug=False):
	decompilation_start = time.time()
	lines = read_file_with_include(folder, filename, debug=debug, do_include=True)
	finish_reading_files = time.time()
	print(f"{(finish_reading_files - decompilation_start) * 1000} ms taken to read all the required files")

	normalization_pass(lines)
	finish_normalization_pass = time.time()
	print(f"{(finish_normalization_pass - finish_reading_files) * 1000} ms taken to normalize the lines")
	
	# This pass will parse lines of the following format
	# offset 0
	# FN_varN DS.L 1
	# ...
	# FN_var1 DS.B 4
	# FN_STACK
	# ... other registers that are pushed on the stack in the function
	# FN_REGX DS.W 1
	# FN_REGA DS.B 1
	# FN_RETURN_ADDR DS.W 1
	stack_parser(lines)
	finish_stack_pass = time.time()
	print(f"{(finish_stack_pass - finish_normalization_pass) * 1000} ms taken to analyse all function stack")
	
	# This pass will parse line of the following format
	# NAME_bin EQU %10101010
	# NAME_hexa EQU $FF
	# NAME_oct EQU @377
	# NAME_int EQU 255
	# and other format
	pre_processor_value_parser(lines)
	finish_pre_processor_pass = time.time()
	print(f"{(finish_pre_processor_pass - finish_stack_pass) * 1000} ms taken to analyse all pre processor value definition")
	

	# This pass will parse line of the following format
	# - Global var example
	# NAME_var DS.W 2
	# 
	# - Global const var example
	# NAME_const_var DC.B 1
	global_var_parser(lines)
	finish_global_var_pass = time.time()
	print(f"{(finish_global_var_pass - finish_pre_processor_pass) * 1000} ms taken to analyse all global variable")
	
	# This pass parses all the instruction in the lines
	# 
	instruction_parser(lines)
	finish_instruction_pass = time.time()
	print(f"{(finish_instruction_pass - finish_global_var_pass) * 1000} ms taken to analyse all instructions")
	if debug:
		for line in lines:
			print(line)

	# Create a code graph for each function in the lines. The name of the 
	# function is defined as the string of the first label of a function.
	# The end of the function is the first rts, swi found.
	cgs = []
	program = []
	program += lines
	while len(program) > 0:
		cg = CodeGraph()
		cg.input(program)
		if cg.parse_instruction_buffer():
			cgs.append(cg)
		program = cg.remove_extra_instructions()

	finish_code_graph_gen = time.time()
	print(f"{(finish_code_graph_gen - finish_instruction_pass) * 1000} ms taken to create all code graphs")
	
	for code_graph in cgs:
		if True and code_graph.functionName == "copy":
			# code_graph.print_asm_function()
			mini_arch_func = MiniFunction(code_graph)

			show_thread = False
			t = threading.Thread(target=CodeGraph.show, args=(code_graph,), kwargs={"id":True,"debug":False,})
			if show_thread:
				t.start()
				time.sleep(1)
				
			#code_graph.print_asm_function()
			analyse_code_path(mini_arch_func.code_blocks, debug=debug)
			if False:
				code_graph.show(id=True, debug=debug)
			elif False:
				input()

			if show_thread:
				t.join()
			

	end = time.time()
	print(f"{(end - decompilation_start) * 1000} ms for decompilation",flush=True)
	