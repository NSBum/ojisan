
#!/usr/bin/python
# encoding=utf8

import os
import argparse
import glob
import subprocess
import fnmatch
import re

def unifyExtensions():
	'''Attempts to unify all of the jpg files to a single '*.jpg' extension
	'''
	rename_list = []
	for ext in ('*.JPG', '*.jpeg', '*.JPEG'):
		rename_list.extend(glob.glob(os.path.join(args.srcdir,ext)))
	for rename_file in rename_list:
		base = os.path.splitext(rename_file)[0]
		os.rename(rename_file, base + ".jpg")

def findfiles(which, where='.'):
	'''Returns list of filenames from `where` path matched by 'which'
	   shell pattern. Matching is case-insensitive.'''
	
	# TODO: recursive param with walk() filtering
	rule = re.compile(fnmatch.translate(which), re.IGNORECASE)
	return [name for name in os.listdir(where) if rule.match(name)]

# instantiate argument parser
parser = argparse.ArgumentParser(description='Create thumbnails for YAPCA site')
# arguments
parser.add_argument('srcdir', help='Source directory to search')
parser.add_argument('outdir', help='Thumbnail output directory')
# parse
args = parser.parse_args()

extensions = [ ('t',99), ('m',239), ('n',319), ('q', 499), ('z',639), ('b',1023)]

unifyExtensions()

for imgpath in findfiles("*.jpg",args.srcdir):
#for imgpath in glob.glob(os.path.join(args.srcdir,"*.jpg")):
	imgpath = os.path.join(args.srcdir, imgpath)
	print "imgpath = {0}".format(imgpath)
	imgname = os.path.basename(imgpath)
	imgbase = os.path.splitext(imgname)[0]
	for e in extensions:
		thumbbase = imgbase + '_' + e[0]
		thumbname = thumbbase + ".jpg"
		thumbpath = os.path.join(args.outdir,thumbname)
		if os.path.isfile(thumbpath):
			print "File: {0} exists".format(thumbname)
		else:
			# this thumbsize doesn't exist, so we must create it
			dimension = e[1]
			print "File: {0} does NOT exist. Creating for dimension {1}\n".format(thumbname,dimension)
			#cmd = "sips -s formatOptions 100 --resampleHeightWidthMax {0} '{1}' --out '{2}'".format(dimension, imgpath,thumbpath)
			cmd = "convert {0} -resize {1}x{1} -unsharp 1.5x1+0.7+0.02 {2}".format(imgpath, dimension, thumbpath)
			p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
			(output, err) = p.communicate()
			p_status = p.wait()