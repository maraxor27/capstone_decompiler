import re

from . import GenericReturn, load

@load
class SoftwareInterrupt(GenericReturn):
	name = "SWI"

	def __init__(self, line):
		super().__init__(line)
		return