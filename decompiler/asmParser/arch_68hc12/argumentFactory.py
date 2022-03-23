import re
# This should be moved from /decompiler/arch68hc12 into /decompiler
class ArgumentFactory:
	def __init__(self):
		self.arg_types = []

	def add_argument_type(self, new_type):
		if new_type not in self.arg_types:
			self.arg_types.append(new_type)

	def make_argument(self, string, repo):
		for arg_type in self.arg_types:
			if arg_type.regex.match(string):
				return arg_type(string, repo)

		raise Exception(f"couldn't make argument with {string}")
		
		return None


