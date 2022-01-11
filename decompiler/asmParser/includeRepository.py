import re

class IncludeRepository:
	regex = re.compile('^INCLUDE\\s+"{0,1}([A-Z0-9_]+\\.(asm|inc))"{0,1}', re.I)

	def __init__(self):
		self.included_files = []
		self.to_include = None
		return

	def match_and_add(self, line):
		match = self.regex.match(line)
		if match is None:
			return False
		return self.try_include(match.group(1))

	def try_include(self, filename):
		if filename in self.included_files:
			return False
		self.included_files.append(filename)
		self.to_include = filename
		return True

	def get_includes(self):
		return self.included_files

	def get_filename_to_include(self):
		filename = self.to_include
		self.to_include = None
		return filename