---
title: "Partitioning a large directory into subdirectories by size"
date: 2020-08-11T22:28:10-04:00
draft: false
authorbox: false
sidebar: false
tags:
- bash
- shell
- macos
- mac
- filesystem
categories:
- programming
---
Since I'm not fond of carrying around all my photos on a cell phone where they're perpetually at list of loss, I peridiocally dump the image and video files to a drive on my desktop for later burning to optical disc.[^1] Saving these images in archival form is a hedge against the bet that my existing backup system won't fail someday.

I'm using Blue-Ray optical discs to archive these image and video files; and each stores 25 GB of data. So my plan was to split the iPhone image dump into 24 GB partitions. H

{{< highlight bash  >}}
#!/bin/bash      
                                                               
directory=${1:-testdir}                                                         
sizelimit=${2:-1000} # in MB                                                    
sizesofar=0                                                                     
dircount=1                                                                      
du -s -m "$directory"/* | while read -r size file                  
do                                                                              
	if ((sizesofar + size > sizelimit))                                           
	then                                                                          
		(( dircount++ ))                                                            
		sizesofar=0                                                                 
	fi                                                                            
	(( sizesofar += size ))                                                       
	mkdir -p -- "$directory/sub_$dircount"                                           
	mv -- "$file" "$directory/sub_$dircount"                                           
done
{{< / highlight >}}

We call the script with `./dump-split.sh dir_to_split your_size_limit`. In my case, the size limit (in MB) was 2400. This script is modified slightly from a version for Unix.[^2] The `du` tool differs between these two platforms. This script doesn't optimize the packing of the discs, but over the many files being archived, it all evens out.

### See also

- [macOS/OS X man page for du](https://ss64.com/osx/du.html) - take note of the differences from the Unix variant.


[^1]: Yes, I could probably go through many if not most of them and delete nearly the entire lot since the best of them have already been moved over to my Lightroom catalogue.
[^2]: [How to split a large folder into smaller folders of equal size](https://unix.stackexchange.com/questions/490124/how-to-split-a-large-folder-into-smaller-folders-of-equal-size) - Note that --block-size parameter isn't available on macOS. Intead, the `-m` flag serves the same purpose as `--block-size=1M`