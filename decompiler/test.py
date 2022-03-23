from asmParser import *

if __name__ == '__main__':
	repo = PreProcessorValueRepository()
	repo.add_new_value(GlobalVar("array", "b", "1,2,3,4,5", True))
	repo.add_new_value(PreProcessorValue("N", "20"))
	print("Test1:", BitSet("bset 12, %00000001", repo))
	print("Test2:", BitSet("bset $c, %00000001", repo))
	print("Test3:", BitSet("bset @14, %00000001", repo))
	print("Test4:", BitSet("bset %00001100, %00000001", repo))
	print("Test5:", RegLoad("LDD #42", repo))
	print("Test6:", RegLoad("leax b,x", repo))
	regload = RegLoad("ldx #array", repo)
	print("Test6:", regload)
	print(Compare("cmpb #N", repo))
	print([str(s) for s in AddReg("ABA", repo).to_mini_arch()])
	print([str(s) for s in AddMem("ADDD #N", repo).to_mini_arch()])


	#print(Store._regex.pattern)