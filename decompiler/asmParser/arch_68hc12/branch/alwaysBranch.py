import re

from .. import GenericBranch, load

@load
class AlwaysBranch(GenericBranch):
	name = "<L, >BRA"
	regex = re.compile("^L{0,1}BRA$", re.I)
	n_path = 1

	def __init__(self, line, repo):
		super().__init__(line)
		return

	def get_condition(self, var_name):
		return "true"

