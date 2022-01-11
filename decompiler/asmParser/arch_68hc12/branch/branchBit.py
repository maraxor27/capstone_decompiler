import re

from .. import GenericBranch, load

@load
class BranchBit(GenericBranch):
	name = "BR<SET, CLR>"

	def __init__(self, line):
		super().__init__(line)

	def get_condition(self, var_name):
		return "<unkown bit branch>"