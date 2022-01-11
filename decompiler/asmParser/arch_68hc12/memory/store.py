import re

from . import load
from .. import BaseInstruction

@load
class Store(BaseInstruction):
	name = "ST<AA,AB,D,S,X,Y>"
	regex = re.compile("^ST(AA|AB|D|S|X|Y)$", re.I)

	def __init__(self, line):
		super().__init__(line)
		return