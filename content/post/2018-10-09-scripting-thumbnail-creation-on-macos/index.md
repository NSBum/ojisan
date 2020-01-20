---
title: 'Scripting thumbnail image file creation on macOS'
date: 2018-10-09T09:18:23-04:00
tags:
- python
- macOS
categories:
- programming
---
One of the sites that I manage uses a [jQuery-based image gallery](http://miromannino.github.io/Justified-Gallery/getting-started/) to display images in a grid. The script decides which thumbnail to use based on how large and image is needed. A series of suffixes à la Flickr^[Well, sort of. I don't think this is exactly what Flickr uses; and I made up the `_q` suffix for the less than 500px image.] is used to signify classes of image size. I wrote the following script to automate the process of scanning a source folder and creating four thumbnail sizes to an output directory.

It's all pretty self-explanatory.

{{< highlight python >}}
#!/usr/bin/python
# encoding=utf8

import os
import argparse
import glob
import subprocess

# instantiate argument parser
parser = argparse.ArgumentParser(description='Create thumbnails for YAPCA site')
# arguments
parser.add_argument('srcdir', help='Source directory to search')
parser.add_argument('outdir', help='Thumbnail output directory')
# parse
args = parser.parse_args()

extensions = [ ('t',99), ('m',239), ('n',319), ('q', 499)]

for imgpath in glob.glob(os.path.join(args.srcdir,"*.jpg")):
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
			cmd = "sips --resampleHeightWidthMax {0} '{1}' --out '{2}'".format(dimension, imgpath,thumbpath)
			p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
			(output, err) = p.communicate()
			p_status = p.wait()
{{< / highlight >}}
