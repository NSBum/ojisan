#!/Users/alan/.pyenv/shims/python3

import os
import fnmatch

# Clean public/css directory of old CSS files before build process

print("*** Clear ojisan css files")
public_css = "/Users/alan/Documents/blog/ojisan/public/css"
for fname in fnmatch.filter(os.listdir(public_css), '*css'): 
	os.remove(os.path.join(public_css,fname))
	
print("*** Done clearning ojisan css files")

