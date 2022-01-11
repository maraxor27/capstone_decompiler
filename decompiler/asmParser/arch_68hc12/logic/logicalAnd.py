import re

from .. import BaseInstruction, load

@load
class LogicalAnd(BaseInstruction):
	name = "AND<A,B,CC>"
