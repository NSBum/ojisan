---
title: "A comprehensive system for generating chorus repetition source material from Glossika sentence tracks"
date: 2020-07-22T14:37:29-04:00
draft: true
authorbox: false
sidebar: false
tags:
- language
- russian
- mac
- audacity
- programming
- applescript
categories:
- linguistics
---

## Generate iterated tracks at normal, 75% and 50% speeds

In [previous](/2020/07/13/audacity-macros-to-support-chorus-repetition-practice/) [posts](/2020/07/16/more-chorus-repetition-macros-for-audacity/) I described a group of Audacity macros that create iterated tracks for chorus repetition practice. As Dr. Kjellin [described](https://www.dropbox.com/s/g6hkeepygfsi5vi/Kjellin-Practise-Pronunciation-w-Audacity.pdf?dl=0) we use Audacity to create a total of six repetitions per track. 

## Automating the generation of tracks with AppleScript

On macOS, AppleScript is the core technology used to automate routine tasks. In this case, we make extensive use of UI scripting since Audacity is not a scriptable application.

## Move generated sentence tracks into place

The next requirement is to send the generated sentence tracks to a destination by `year → month`. I had hoped to do this by specifying a path in the save file dialog in Audacity, but the UI scripting of this macOS dialog is unreliable because of the default autocompletion on the folder path sheet that is invoked with the ⇧⌘G system-wide shortcut. But I also cannot accept whatever random path shows up by default. However, the "path to desktop" shortcut ⇧⌘D does work. So, a new idea emerged: save the file to the desktop, allow an existing Hazel rule to grab it an put it in an mp3 directory. Now, a rule on that directory, looks for some feature of _our_ mp3 file and takes care of moving the file into place.

What follows is a functional description of how this Python script works. In the following block, we just create an argument parsers that consumes the arguments `fn` and `destpath` with which Hazel will call our script.

{{< highlight python >}}
#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import os
import argparse
import re
import json
import datetime

# create argument parser
parser = argparse.ArgumentParser(description="Move GMS files by date.")

# add arguments to the parser
parser.add_argument("--fn")
parser.add_argument("--destpath")

# parse the arguments
args = parser.parse_args()
{{< /highlight >}}

Next, we ask the `ffmpeg` tool `ffprobe` to provide us with the ID3 tags in JSON format:

{{< highlight python >}}
cmd = "ffprobe -show_format -print_format json "
filename = args.fn 
destpath = args.destpath 

theCmd = cmd + "'%s'" % filename
mp3info = str(os.popen(theCmd).read())
{{< /highlight >}}

Then we extract some data from the returned JSON:

{{< highlight python >}}
mp3_json = json.loads(mp3info)
tags = mp3_json['format']['tags']
tag_year = tags['date']

m = re.search(r'GMS\s+(\d+)', tags['album'])
tag_group = m.group(1)
{{< /highlight >}}

Finally, if this file's comments are structured the way we expect (containing _Glossika GMS_) then we construct the destination path and move the file:

{{< highlight python >}}
#	check if this mp3 file is a Glossika-derived file
m = re.search(r'Glossika\s+GMS', tags['comment'])
if m is not None:
	# build destination path
	current_date = datetime.date.today()
	current_year = current_date.year
	current_month = current_date.month
	dest_path = os.path.join(destpath,str(current_year), "%02d" % current_month)
	dest_file_path = os.path.join(dest_path,os.path.basename(filename))
	os.replace(filename,dest_file_path)
{{< /highlight >}}

Then, we just need to construct a Hazel rule on our mp3 directory to execute the script: `python3 /Users/alan/Documents/dev/MoveMP3ByTags.py --fn $1 --destpath "/Users/my_user_name/path_to_destination"`

Now, whatever file Audacity saves to the Desktop that contains the text "Glossika GMS" in the comments ID3 tag is moved to a directory based on the current year and month.