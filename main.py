from decompiler import decompileFiles

def main():
	folder = 'asm'
	file_name = 'test.asm'
	# try:
	decompileFiles(folder, file_name, debug=False)
	# except Exception as e:
	# 	print(str(e))
	return

if (__name__, '__main__'):
	main()