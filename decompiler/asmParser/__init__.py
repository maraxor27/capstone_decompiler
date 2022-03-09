from .preProcessorValueRepository import PreProcessorValueRepository

pre_proc = PreProcessorValueRepository()

from .instruction import Instruction
from .genericReturn import GenericReturn
from .genericBranch import GenericBranch
from .genericArgument import GenericArgument
from .label import Label
from .instructionRepository import InstructionRepository
from .includeRepository import IncludeRepository

from .miniArch import *

arch = InstructionRepository()
includes = IncludeRepository()

from .arch_68hc12 import *
from .parser import *

arch.setLabel(Label)

from .codeGraph import CodeGraph
from .codeFlow import analyse_code_path

from .composer import compose