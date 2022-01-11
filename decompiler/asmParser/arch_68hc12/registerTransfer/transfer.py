import re

from .. import BaseInstruction, load

@load
class Transfer(BaseInstruction):
	name = "T<AB,BA,AP,PA,FR,SX,SY,XS,YS>"
	regex = re.compile("^T(AB|BA|AP|PA|FR|SX|SY|XS|YS)$", re.I)

	def __init__(self, line):
		super().__init__(line)