---
title: "Using Python and AppleScript to get notified if a site is down"
date: 2016-05-19 06:52:34
aliases: ['/2016/05/19/Using-Python-and-AppleScript-to-get-notified-if-a-site-is-down/']
authorbox: false
tags:
- python
- applescript
- web
categories:
- programming
---
I manage a handful of websites, like this one. Having built a few on other platforms, such as Drupal, I'm familiar with the dreaded error _"The website encountered an unexpected error. Please try again later."_ On sites that I don't check on frequently, it can be an embarrassment when people begin emailing you with questions about the site being down.

I wrote the following Python script to deal with the problem:

{{< highlight python >}}
#!/usr/bin/python

import urllib
from subprocess import Popen, PIPE

RECIPIENT = "your.recipient@me.com"
URL_TO_CHECK = "http://www.example.com"
ERR_MSG = "Your website is down."

def sendMessage(message):
	scpt = '''
	tell application "Messages" to send "{0}" to buddy "{1}" of (service 1 whose service type is iMessage)
	'''.format(message,RECIPIENT)
	args = []
	p = Popen(['osascript', '-'] + args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	stdout, stderr = p.communicate(scpt)

try:
	fh = urllib.urlopen(URL_TO_CHECK)
except IOError:
	sendMessage(ERR_MSG)
else:
	# handle database type errors from Drupal sites
	site_content = fh.read()
	target_str = "The website encountered an unexpected error. Please try again later."
	if site_content.find(target_str) != -1:
		sendMessage(ERR_MSG)
	else:
		print "No error"

{{< /highlight >}}

I run this as a scheduled job using `launchd` and as long as I have a Messages-capable device with me, I'll get notifications of issues with the site.
