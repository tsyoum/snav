#!/usr/local/bin/python3

import glob
import os
import sys
import pickle

index_path = '.snav.db'

def traverse(dir, result):
	new_dir = [ dir ];

	for obj in glob.glob(dir + '/*'):
		if os.path.isdir(obj):
			traverse(obj, result)
		elif os.path.isfile(obj):
			# add specific types of file
			ext = os.path.splitext(obj)[1].lower()
			if ext == '.c' or ext == '.cpp' or ext == '.h' or ext == '.java' or ext == '.aidl':
				new_dir.append(os.path.basename(obj))
		else:
			print('unknown node: ' + os.getcwd() + '/' + obj)

	result.append(new_dir)

def save_index(index):
	f = open(index_path, 'wb')
	pickle.dump(index, f)
	f.close()

def load_index():
	# FIXME: find index file first
	path = index_path;

	f = open(path, 'rb')
	index = pickle.load(f)
	f.close()
	return index

def find_index_file(path):
	if os.path.isfile(path):
		return path
	else:
		if len(path) > 100:
			return None
		return find_index_file('../' + path)

def search_file(index, filename):
	match = []
	for obj in index:
		cnt = len(obj)
		dir = obj[0]
		for idx in range(1, cnt):
			if filename == obj[idx]: # exact match!
				return [dir + '/' + obj[idx]]
			elif obj[idx].lower().find(filename.lower()) >= 0:
				match.append(dir + '/' + obj[idx])

	if len(match) == 0:
		return None
	else:
		return match

def build_file_list(index):
	f = open('.files.tmp', 'w')
	for obj in index:
		cnt = len(obj)
		dir = obj[0]
		for idx in range(1, cnt):
			f.write(dir + '/' + obj[idx] + '\n')
	f.close()

	return '.files.tmp'

def usage():
	print('\nsnav - simple source navigation tool\n')
	print('    Usage: snav <command> [arg]');
	print('          command - build, find, grep, vi, ctags, cscope, diff, p4, git\n')


if __name__ == '__main__':
	
	if len(sys.argv) < 2:
		usage()
		exit()

	cmd = sys.argv[1]
	if cmd == 'build':
		index = [];
		traverse(('.'), index)
		#print(index)
		# save index file
		save_index(index)

	elif cmd == 'vi':
		filename = sys.argv[2]
		print('Opening ' + filename)

		index = load_index()
		# run vi

		match = search_file(index, filename)
		if match == None:
			print('Not found')
		elif len(match) == 1:
			print('opening ' + match[0]+ ' using vi...')
			os.execlp('vi', 'vi', match[0])
		else:
			print('Matches:')
			i = 1
			for item in match:
				print('    ' + str(i) + ') ' + os.path.basename(item) + '   (' + os.path.split(item)[0] + ')')
				i = i + 1

			key = 0
			while key < 1 or key > len(match):
				try:
					key = int(input('>> '))
				except:
					exit()

			print('opening ' + match[key-1] + ' using vi...')
			os.execlp('vi', 'vi', match[key-1])

	elif cmd == 'ctags':
		index = load_index()
		file_list = build_file_list(index)
		os.execlp('ctags', 'ctags', '-L', file_list)
		os.unlink(file_list)

	elif cmd == 'cscope':
		index = load_index()
		file_list = build_file_list(index)
		os.execlp('cscope', 'cscope', '-b', '-i', file_list)
		os.unlink(file_list)

	elif cmd == 'find':
		print('Not supported.')

	elif cmd == 'grep':
		print('Not supported.')

	elif cmd == 'diff':
		print('Not supported.')

	elif cmd == 'p4':
		print('Not supported.')

	elif cmd == 'git':
		print('Not supported.')

	else:
		usage()
		
