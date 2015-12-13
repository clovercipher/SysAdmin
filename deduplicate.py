#!/usr/bin/env python
'''
Notes:
Script removes duplicate files within specified directory and its subdirectories.
Takes commandline input and outputs removed.txt containing deleted files.
'''

import os, sys, hashlib

manifest = {}
removed = []

if len(sys.argv) < 2:
	sys.exit("Usage: Please provide directory.")
else:
	basedir = sys.argv[1]

f = open('removed.txt', 'w')

def additem(digest, path):

	manifest.update({digest:path})

'''
Build dictionary contianing each unique file found
Key: Hash | Value: Full Pathname
'''
def build_manifest():

	for dir, subdir, file in os.walk(basedir):
		for name in file:
			fileobj = open(os.path.join(dir,name))
			content = fileobj.read()
			hash = hashlib.md5(content).hexdigest()
			additem(hash, os.path.join(dir,name))
			fileobj.close()

'''
Search the manifest for duplicate key,value pairs
Remove file is the key,value pair is not found.
'''
def cleanup():

	for dir, subdir, file in os.walk(basedir):
		for name in file:
			fileobj = open(os.path.join(dir,name))
			content = fileobj.read()
			hash = hashlib.md5(content).hexdigest()
			if manifest[hash] != os.path.join(dir,name):
				os.remove(os.path.join(dir,name))
				removed.append(str(os.path.join(dir,name)))
			fileobj.close()

'''
Build text file containing all removed files.
'''
def create_del_file():
	f.write("Total files removed:\t" + str(len(removed)))
	f.write("\n")

	for item in removed:
		f.write(item)
		f.write("\n")
	f.close()
	

def main():
	build_manifest()
	cleanup()
	create_del_file()

if __name__=="__main__":
	main()




