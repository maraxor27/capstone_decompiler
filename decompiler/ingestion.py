import re

from .asmParser import * # arch, pre_proc, CodeGraph, includes
from .asmParser import normalization_pass, stack_parser, \
	pre_processor_value_parser, global_var_parser, instruction_parser, \
	analyse_code_path, MiniFunction

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

def decompile(folder, filename, debug=False):
	lines = read_file_with_include(folder, filename, debug=debug, do_include=True)
	normalization_pass(lines)
	stack_parser(lines)
	pre_processor_value_parser(lines)
	global_var_parser(lines)
	instruction_parser(lines)
	if debug:
		for line in lines:
			print(line)

	cgs = []
	program = []
	program += lines
	while len(program) > 0:
		cg = CodeGraph()
		cg.input(program)
		cg.parse_instruction_buffer()
		program = cg.remove_extra_instructions()
		
		if True and cg.functionName == "readKey":
			# cg.print_asm_function()
			mini_arch_func = MiniFunction(cg)
			analyse_code_path(mini_arch_func.code_blocks, debug=debug)
			if True:
				cg.show(id=True, debug=debug)
			else:
				input()
		cgs.append(cg)