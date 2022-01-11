from .value import Value
from .register import Register
from .fixMemory import FixMemory
from .relativeMemory import RelativeMemory
from .relativeMemoryPointer import RelativeMemoryPointer

registers = [
	Register('A', 8), 
	Register('B', 8), 
	Register('D', 16), 
	Register('X', 16), 
	Register('Y', 16), 
	Register('SP', 16, var=False),
	Register('PC', 16, var=False),
]