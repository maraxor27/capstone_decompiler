from asmParser import *

if __name__ == '__main__':
	print("Test1:", BitSet("bset 12, %00000001"))
	print("Test2:", BitSet("bset $c, %00000001"))
	print("Test3:", BitSet("bset @14, %00000001"))
	print("Test4:", BitSet("bset %00001100, %00000001"))