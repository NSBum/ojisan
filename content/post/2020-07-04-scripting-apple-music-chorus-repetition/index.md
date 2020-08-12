---
title: "Scripting Apple Music on macOS for chorus repetition practice"
date: 2020-07-04T21:09:57-04:00
draft: false
authorbox: false
sidebar: true
tags:
- language
- russian
- mac
- itunes
- programming
- applescript
categories:
- linguistics
---
This is an update to my [previous post](/2018/01/11/automate-itunes-for-chorus-repetitions-of-l2-pronunciation-practice/) on automating iTunes on macOS to support chorus repetition practice. You can read the original post for the theory behind the idea; but in short, one way of developing prosody and quality pronunciation in a foreign language is to do mass repetitions in chorus with a recording of a native speaker.

Because in macOS 10.15, iTunes is no more, I've updated the script to work with the new Music app. It turns out that it's a lot simpler. No need to dive into the application classes.

{{< highlight applescript >}}
--
--	Created by: Alan Duncan
--	Created on: 2020-07-04
--
--	Copyright (c) 2020 OjisanSeiuchu
--	All Rights Reserved
--

use AppleScript version "2.4" -- Yosemite (10.10) or later
use scripting additions

property trackDuration : 1
property minimumVolume : 10

--	initial volume, set by user
global volume0, trackRepeatMode0

on run
	
	tell application "Music"
		-- save original settings
		set trackRepeatMode0 to song repeat
		set song repeat to one
		set volume0 to sound volume
		
		play
		
		--	calculate the delay between fades
		set fadeDelay to (trackDuration * 60) / (volume0 - minimumVolume)
		repeat with i from minimumVolume to volume0
			delay fadeDelay
			set sound volume to sound volume - 1
		end repeat
		
		pause
		-- restore original settings
		set song repeat to trackRepeatMode0
		set sound volume to volume0
	end tell
	
end run
{{< /highlight >}}