import zipfile
import os

def package():
	file = "../package/imdb.zip"

	try:
	    os.remove(file)
	except OSError:
	    pass

	zip = zipfile.ZipFile(file, "w")
	zip.write("../lambda_function.py")
	zip.close()

	print("done")

if __name__ == '__main__':
	package()