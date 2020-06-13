import sys
import os
import filecmp

arg_paths = []
file_paths = []
duplicates = {}

def check_if_subdir(path):
	rpath = os.path.realpath(path)
	for prev_path in arg_paths.copy():
			prev_rpath = os.path.realpath(prev_path)
			if rpath.startswith(prev_rpath):
				print("WARNING: argument '"+path+"' is a subdirectory or duplicate (ignoring)")
				return True
			elif prev_rpath.startswith(rpath):
				arg_paths.remove(prev_path)
				print("WARNING: argument '"+prev_path+"' is a subdirectory or duplicate (ignoring)")
	return False

def check_if_duplicate(file):
	file_size = os.path.getsize(file)
	for prev_file, prev_file_size in file_paths:
		if file_size == prev_file_size and filecmp.cmp(file, prev_file):
			if prev_file in duplicates:
				duplicates[prev_file].append(file)		
			else:
				duplicates[prev_file] = [prev_file, file]	
			return True
	return False
	
	

if len(sys.argv) < 2: exit("Usage: "+sys.argv[0]+" dir_path...");

for path in sys.argv[1:]: 
	if os.path.isdir(path): 
		if not check_if_subdir(path): arg_paths.append(path) 
	else: 
		print("WARNING: argument '"+path+"' is not a directory (ignoring)")

for arg_path in arg_paths:
	for root, _, files in os.walk(arg_path):
		for file in files: 
			file_path = os.path.join(root, file)
			check_if_duplicate(file_path)
			file_paths.append((file_path, os.path.getsize(file_path)))

for key, files in duplicates.items():
	print("duplicated: (size: {0})".format(os.path.getsize(files[0])))
	for file in files: print("\t{0}".format(file))