---
title: "Hugo cache busting"
date: 2020-10-11T07:13:17-04:00
images:
- /images/2020/10/10/shortcut_01.jpg
description: An approach to cache busting CSS resources for Hugo static sites
draft: false
authorbox: false
sidebar: false
tags:
- blog
- hugo
categories:
- programming
---

## Justification

Although caching can make page loads notably faster, it comes with a cost. Browsers aren't always capable of taking note when a cached resource has changed. I've noticed recently that Safari utterly refuses to reload `.css` files even after emptying the browser cache and clearing the web history. 

## Background

With a lot of help from the a [pair](https://ukiahsmith.com/blog/hugo-static-asset-cache-busting/) of [articles](https://ukiahsmith.com/blog/hugo-improved-static-asset-cache-busting/) written by Ukiah Smith, I've developed a workflow for dealing with this problem during the deployment process. He describes two approaches to the problem of static asset caching, one an improvement on the other. I've implemented something like what he [describes](https://ukiahsmith.com/blog/hugo-improved-static-asset-cache-busting/) using the `git` file hash to modify the filename of the css files. When the client browser sees a new filename, it always reloads the resource. So the problem is to figure out how to only change the filename when the contents have changed. Let's say you tweak a css parameter and want to ensure that client browsers load the correct version. We can use the `git` file hash, and append it on the filename. Then the only remaining problem is to make sure that the page `head` template knows how to find the correct version to bake into the pages. Here, our approach is the same as Smith's.

Where we diverge in the approach described here relates to the fact that I'm using straight CSS and not a pre-processor. The main change is that I've moved my custom CSS files to a separate directory `css_source` at the top level of my site directoy. It's not parsed in the build process; but it serves as the canonical source of my custom css. During the build process, we run a script that process the contents of the `css_source` directory, appends the `git` hash to the filename and creates a JSON manifest that we use in the `head` template. 

### The process

First, I just clear the `public/css` directory of any prior versions of the css files:

{{< highlight python >}}
import os
import fnmatch

# Clean public/css directory of old CSS files before build process

public_css = "path to my public css directory"
for fname in fnmatch.filter(os.listdir(public_css), '*css'): 
    os.remove(os.path.join(public_css,fname))
{{< /highlight >}}


Then, we process the files and build the manifest:

{{< highlight python >}}
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
    identifier = fileHash(os.path.join(path, fn))
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
{{< /highlight >}}

Now in `site/data/tonedeaf/` I have a manifest file `css.json` that we can use to build the stylesheet links.

{{< highlight json >}}
 {
   "link-page": "link-page_10eb858a5c0a9e255aef9b40baf623d64ee2c29c\n.css",
   "russian-shortcode": "russian-shortcode_65be890c35a165f7ef13a61b1134c0888a0c384f\n.css",
   "photogallery": "photogallery_4d7b91630e0c31a2764ca52d61f3293438d752d0\n.css",
   "tag_page": "tag_page_121f9dc78b4180d309fbac735da704359c335921\n.css",
   "general": "general_191e79d04191f5dd1a8392b0904ee3c8fc4e9669\n.css",
   "hugo-easy-gallery": "hugo-easy-gallery_d78dfec854168b088b061544f8f01b20a5389efc\n.css"
}
{{< /highlight >}}

Using this data in my `head` template:

{{< highlight go >}}
<link href="{{ .Site.BaseURL }}css/{{ index .Site.Data.tonedeaf.css "general" }}" rel="stylesheet">
<link href="{{ .Site.BaseURL }}css/{{ index .Site.Data.tonedeaf.css "russian-shortcode" }}" rel="stylesheet">
<link href="{{ .Site.BaseURL }}css/{{ index .Site.Data.tonedeaf.css "photogallery" }}" rel="stylesheet">
<link href="{{ .Site.BaseURL }}css/{{ index .Site.Data.tonedeaf.css "link-page" }}" rel="stylesheet">
{{< /highlight >}}

Where Smith handles this all in a Makefile, I just use a Keyboard Maestro macro to link all of pieces together. I hope this helps solve caching problems when working with Hugo.

### References

- [Hugo static asset cache busting](https://ukiahsmith.com/blog/hugo-static-asset-cache-busting/) - using a random generated string to append to filenames.
- [Hugo: Improved static asset cache busting](https://ukiahsmith.com/blog/hugo-improved-static-asset-cache-busting/) - using git SHA1 file hash to append to filenames.
- [What is cache busting?](https://www.keycdn.com/support/what-is-cache-busting)
- [Revving Filenames: don’t use querystring](https://www.stevesouders.com/blog/2008/08/23/revving-filenames-dont-use-querystring/) - Query strings often fail to prompt client reloading.
