#!/usr/bin/env python3

"""
Usage:
   prep_ojisan_css.py -s <source> -o <dest> -m <manifest>

Options:
    -s <source> --source <source>       Source path for template css files
    -o <dest> --out <dest>              Path for versioned css files
    -m <manifest> --manifest <manifest> Path for manifest css.json file
    - h, --help                         Show this help


"""

# Typical call:
#./prep_ojisan_css.py "/Users/alan/Documents/blog/ojisan/css_source" \
#    "/Users/alan/Documents/blog/ojisan/static/css" "/Users/alan/Documents/blog/ojisan/data/tonedeaf"

import os
import fnmatch
import subprocess
import json
import sys
import random
import re
from docopt import docopt
from shutil import copyfile

def fileHash(filePath):
    process = subprocess.run(['/usr/local/bin/git', 'hash-object',filePath], check=True, stdout=subprocess.PIPE, universal_newlines=True)
    output = process.stdout
    return output
    
def replaceIdentifier(fn,path):
    result = re.match(r'(.+)_[\d\D]{30}\.css', fn)
    try:
        baseName = result.groups()[0]
    except:
        result = re.search(r'(.+)\.css', fn)
        baseName = result.groups()[0]
    identifier = fileHash(os.path.join(path, fn)).strip('\n')
    return baseName + "_" + identifier + ".css"


arguments = docopt(__doc__, version='ruwordle 0.2')
try:
  path = os.path.abspath(arguments['--source'])
except KeyError:
  print('Error: no source path provided')
  sys.exit(0)

try:
  out_path = os.path.abspath(arguments['--out'])
except KeyError:
  print('Error: no output path provided')
  sys.exit(0)

try:
  j_data = os.path.abspath(arguments['--manifest'])
  j_data = os.path.join(j_data,"css.json")
except KeyError:
  print('Error: no manifest path provided')
  sys.exit(0)

data = {}
# the 1st argument `path` is the source path css_path
# path = os.path.abspath(sys.argv[1])
# # the 2nd argument `out_path` is the path to the actual css dir
# out_path = os.path.abspath(sys.argv[2])
# # the 3rd argument is the css.json manifest path
# j_data = os.path.abspath(sys.argv[3])
# j_data = os.path.join(j_data,"css.json")


# empty the primary css directory
for fname in fnmatch.filter(os.listdir(out_path), '*css'): 
    os.remove(os.path.join(out_path,fname))
    
# apply hash to css filename and move to primary css directory
for fname in fnmatch.filter(os.listdir(path), '*css'):
    newFilename = replaceIdentifier(fname,path)
    data[os.path.splitext(fname)[0]] = newFilename
    copyfile(os.path.join(path,fname), os.path.join(out_path,newFilename))
    
# write the manifest
with open(j_data,'w') as outfile:
    print("Generating css json data file.")
    json.dump(data, outfile, indent = 1)
    print("Done.")
    