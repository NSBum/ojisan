#!/Users/alan/.pyenv/shims/python3

import os
import fnmatch
import subprocess
import json
import sys
import random
import re
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

data = {}
path = os.path.abspath(sys.argv[1])
out_path = os.path.abspath(sys.argv[2])
j_data = os.path.abspath(sys.argv[3])
j_data = os.path.join(j_data,"css.json")


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
    