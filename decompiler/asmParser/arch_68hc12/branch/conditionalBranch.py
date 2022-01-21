import re

from .. import GenericBranch, load

@load
class ConditionalBranch(GenericBranch):
	name = "<L, >B<CC,CS,EQ,NE,MI,PL,RCLR,RSET,VC,VS,GT,GE,LT,LE,HI,HS,LS,LO>"
	regex = re.compile("^L{0,1}B(CC|CS|EQ|NE|MI|PL|VC|VS|GT|GE|LT|LE|HI|HS|LS|LO)$", re.I)
	n_path = 2

	def __init__(self, line):
		super().__init__(line)
		return

	def get_condition(self, var_name):
		op = self.operation.upper()
		if op == "BCC":
			raise Exception("Branch if carry clear not implemented for decompilation")
		elif op == "BCS":
			raise Exception("Branch if carry set not implemented for decompilation")
		elif op == "BEQ":
			minus = var_name.index("-")
			return var_name[:minus] + "==" + var_name[minus+1:]
			#return f"{var_name} == 0"
		elif op == "BNE":
			minus = var_name.index("-")
			return var_name[:minus] + "!=" + var_name[minus+1:]
			# return f"{var_name} != 0"
		elif op == "BMI":
			minus = var_name.index("-")
			return var_name[:minus] + "<" + var_name[minus+1:]
			#return f"{var_name} < 0"
		elif op == "BPL":
			minus = var_name.index("-")
			return var_name[:minus] + ">=" + var_name[minus+1:]
			#return f"{var_name} >= 0"
		elif op == "BVC":
			raise Exception("Branch if overflow clear not implemented for decompilation")
		elif op == "BVS":
			raise Exception("Branch if overflow clear not implemented for decompilation")
		elif op == "BGT":
			minus = var_name.index("-")
			return var_name[:minus] + ">" + var_name[minus+1:]
			#return f"{var_name} > 0"
		elif op == "BGE":
			minus = var_name.index("-")
			return var_name[:minus] + ">=" + var_name[minus+1:]
			#return f"{var_name} >= 0"
		elif op == "BLT":
			minus = var_name.index("-")
			return var_name[:minus] + "<" + var_name[minus+1:]
			#return f"{var_name} < 0"
		elif op == "BLE":
			minus = var_name.index("-")
			return var_name[:minus] + "<" + var_name[minus+1:]
			#return f"{var_name} < 0"
		elif op == "BHI":
			minus = var_name.index("-")
			return var_name[:minus] + ">" + var_name[minus+1:]
			#return f"{var_name} > 0"
		elif op == "BHS":
			minus = var_name.index("-")
			return var_name[:minus] + ">=" + var_name[minus+1:]
			#return f"{var_name} >= 0"
		elif op == "BLS":
			minus = var_name.index("-")
			return var_name[:minus] + "<=" + var_name[minus+1:]
			#return f"{var_name} <= 0"
		elif op == "BLO":
			minus = var_name.index("-")
			return var_name[:minus] + "<" + var_name[minus+1:]
			#return f"{var_name} < 0"
		else:
			return None

	def __str__(self):
		return f"Conditional Branch: [operation: {self.operation}, line: '{self.line}']"