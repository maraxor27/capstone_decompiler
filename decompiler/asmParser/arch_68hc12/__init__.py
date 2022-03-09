# from ..miniArch import \
# 	Add as MiniAdd, Sub as MiniSub, Mult as MiniMult, Div as MiniDiv, \
# 	Compare as MiniCmp, And as MiniAnd, Or as MiniOr, \
# 	# Load as MiniLoad, Store as MiniStore, \
# 	Move as MiniMove, TempValue as MiniValue
	
from ..miniArch import *

from .. import arch, GenericReturn, GenericBranch
from .. import Instruction as BaseInstruction
from .. import GenericArgument 
from .argumentFactory import ArgumentFactory

ArgFactory = ArgumentFactory()

# load decorator for Instruction class
def load(c):	
	if issubclass(c, BaseInstruction):
		arch.addInstruction(c)
	elif issubclass(c, GenericArgument):
		ArgFactory.add_argument_type(c)
	return c

from .arguments import *

from .arithmetic import *
from .branch import *
from .compare import *
from .logic import *
from .memory import *
from .method import *
from .registerTransfer import *
from .subroutine import *
from .softwareInterrupt import SoftwareInterrupt

arch.parse_instuction__regex() 

