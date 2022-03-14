import re

from .. import GenericBranch, load

@load
class BranchBit(GenericBranch):
	name = "BR<SET, CLR>"

	def __init__(self, line, repo):
		super().__init__(line)

	def get_condition(self, var_name):
		return "<unkown bit branch>"