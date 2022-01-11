from decompiler import decompile

def main():
	folder = 'asm'
	file_name = 'keyPad.asm'
	decompile(folder, file_name, debug=False)
	return

if (__name__, '__main__'):
	main()