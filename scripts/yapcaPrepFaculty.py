#!/usr/bin/python
# encoding=utf8

import yaml
import os
import re

datadir = '/Users/alan/blogs/YAPCA/data/'
outputdir = '/Users/alan/blogs/YAPCA/content/faculty'
facultydirs = ['faculty','extended_faculty', 'guest_artists']
for faculty_type in facultydirs:
	dirpath = os.path.join(datadir,faculty_type)
	for fn in os.listdir(dirpath):
		stream = open(os.path.join(dirpath,fn),"r")
		docs = yaml.load_all(stream)
		for doc in docs:
			content = "+++\n"
			#print doc
			for k,v in doc.items():
				if k == 'name':
					#print """{0}""".format(v)
					faculty_name = v
					content += "title = \"{0}\"\n".format(v)
					content += "description = \"YAPCA faculty\"\n"
					content += "type = \"faculty\"\n"
					content += "+++\n"
					faculty_fn = re.sub("^(\\D)\\D+\\s(\\D+)", "\\1\\2", v).lower() + ".md"
					
				if k == 'biophoto':
					imgpath = v
				if k == 'bio':
					bio = v
			content += "{{< figure src=\"" + imgpath + "\" class=\"faculty-biophoto\" >}}"
			content += "\n" + bio
			
			writepath = os.path.join(outputdir,faculty_fn)
			print writepath
			wr = open(writepath,'w')
			wr.write(content.encode('utf-8').strip())