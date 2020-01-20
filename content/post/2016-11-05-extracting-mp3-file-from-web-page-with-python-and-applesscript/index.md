---
title: Extracting mp3 file from web page with Python and ApplesScript
date: 2016-11-05 15:49:45
aliases: ['/2016/11/05/Extracting-mp3-file-from-web-page-with-Python-and-ApplesScript/']
tags:
- programming
- python
- applescript
categories:
- programming
---
As I've mentioned before I use [Anki](http://ankisrs.net) extensively to memorize and practice Russian vocabulary. With language learning in particular, adding spoken pronunciations to the cards makes an enormous difference. Since I use [Open Russian](https://en.openrussian.org) extensively to provide information to built my Anki cards, it's a natural source of audio data, too. To optimize my learning time, I built two small scripts to grab and rename the audio files from the Open Russian site. First, I'll describe my workflow.

### My vocabulary workflow

Each morning, I pull 6 words from the a Russian word frequency list to add to my Anki deck. With each word, I use Open Russian to look up the complete definition, example sentences, syllabic stress, and other pieces of information that go on the flashcard. To facilitate OpenRussian.org opening in its own dedicate browser window, I built a [Fluid](http://fluidapp.com) application out of it. Having common workflow-related sites like this in their own dedication applications makes a lot of sense for task isolation.

Finally, for many words, I like to extract the audio from the site and add it to the card that I'm building. It turns out to be a cumbersome step because the audio doesn't play in a QuickTime or other player that allows me to save the file. The source sound files can be downloaded from [Shtooka](http://shtooka.net) but this is yet another step. This is where my enhanced workflow comes in.

### What should the enhanced workflow do?

Optimally, I should be able to grab the URL that is displayed in the Open Russian Fluid application. Using the content of that page, I should be able to obtain the URL of the mp3 file for that word and save it to the desktop using the Russian word as the filename.

### The solution

First is a Python application that grabs the URL from the Fluid app, extracts the audio file URL, and downloads it to the desktop.

{{< highlight python >}}
#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import urllib2
import urlparse
from os.path import expanduser, normpath, basename, join

""" Obtain the URL from the OpenRussian application,
which is just a Fluid browser application.
If obtaining URL from Safari:
	scpt = '''
	tell application "Safari"
		set theURL to URL of current tab of window 1
	end tell'''
"""
def getOpenRussianURL():
	from subprocess import Popen, PIPE


	scpt = '''
		tell application "OpenRussian"
			set theURL to URL of browser window 1
		end tell'''

	p = p = Popen(['osascript'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
	stdout, stderr = p.communicate(scpt)
	return stdout

""" Extract the audio file mp3 from
the content of the OpenRussian.org page.
"""
def audioURL(html):
	m = re.search("<audio.+(http.+mp3)", html)
	return m.group(1)

def saveMP3(url,path):
	mp3file = urllib2.urlopen(url)
	with open(path,'wb') as output:
		output.write(mp3file.read())

""" Fetch mp3 to which aURL points and save
it to the Desktop using the word as the filename
"""
def fetchMP3(aURL):
	response = urllib2.urlopen(aURL)
	content = response.read()

	url = audioURL(content)
	path = join(expanduser("~"),'Desktop',basename(normpath(url)))
	saveMP3(url, path)

url = getOpenRussianURL()
fetchMP3(url)

{{< /highlight >}}

To make this even faster, I assigned the script to a [Quicksilver](https://qsapp.com) keystroke trigger. It's that simple. Once little twist that I discovered was that difficulty in launching a Python application from a Quicksilver trigger. Although there must be an easier way, I haven't found it. Instead, I just wrote an AppleScript that runs the application in question and I used *that* as the triggered script in Quicksilver:

{{< highlight applescript >}}
--
--	Created by: Alan Duncan
--	Created on: 2016-11-05
--
--	Copyright (c) 2016 Ojisan Seiuchi
--	All Rights Reserved
--

use AppleScript version "2.4" -- Yosemite (10.10) or later
use scripting additions

do shell script "/Users/alan/Documents/dev/scripts+tools/fetchOpenRussianMP3.py"

{{< /highlight >}}

There may be a way to finish the process and add this to the Anki card in one step. I'll have to work on that.

---
