---
title: Automate iTunes for chorus repetitions of L2 pronunciation practice
date: 2018-01-11T06:20:50-05:00
draft: false
summary: Using AppleScript to automate chorus repetition practice
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
_N.B. This script [has been updated](/2020/07/04/scripting-apple-music-on-macos-for-chorus-repetition-practice/) to work with the new Music app on macOS 10.15 Catalina. 2020-07-04._

That title is a mouthful!

TL;DR: One approach to developing good second language pronunciation and rhythm is to repeat a sentence many times while simultaneously listening to a native speaker. If you do this while gradually reducing the source amplitude, you will be speaking on your own without help. This is an AppleScript that automates this process on the Mac platform.

## Background

For adult learners of a second language (L2), pronunciation and prosody (the rhythm and cadence of language) can be difficult. A method devised by Swedish linguist and medical doctor [Olle Kjellin](http://olle-kjellin.com/SpeechDoctor/) seeks to remedy this problem by applying a method of chorus repetitions of sentence in the L2. While listening to the sentence over and over, the learner repeats the same sentence aloud, attempting to match the native speaker's pronunciation and cadence. By gradually reducing the volume of the native speaker, the learner gradually hears more of his own voice. This shaping process has sound neurocognitive underpinnings and [Kjellin's explanation](https://www.researchgate.net/publication/285234145_Quality_Practise_Pronunciation_With_Audacity_-_The_Best_Method) of the method is definitely worth reading.

## Automating the process

One of the ideas that Kjellin discusses is gradual reduction in the native speaker's volume. That rationale is that as the learner begins to hear less of the native speaker's voice, he begins to hear more of his own. In this way, he learns to shape his pronunciation and developing prosody while the auditory stimulus is gradually withdrawn.

It is possible to do this automatically on the Mac plattorm.^[Sorry Windows and Linux users, this approach relies on AppleScript which of course doesn't run on these other platforms. Almost certainly there are platform-specific approaches there but that's for someone else to figure out!] For this approach, I use AppleScript to ask the user for the intended track duration in minutes and then it begins playing the current track, gradually reducing the volume over the course of the desired duration. To simplify the choices the user must make, the script only asks for the duration. The minimum volume is hard-coded as is the linear shape of the decay. With a little ingenuity, these choices could be modified. For example, the volume decay could be faster, leaving some of the remaining time at the minimum volume.^[Currently when the minimum volume is finally reached, playback stops.]

## Installing

You'll need to grab the [source code]() from Github and paste it into a new empty script in AppleScript Editor.app.^[You have it, it's just hard to find. Look in `/Applications/Utilities`.] From AppleScript Editor, you need to save it to the iTunes script directory which is located at `~/Library/Library/Scripts/Applications/iTunes`.^[You can access the iTunes scripts folder from the scripts menu when iTunes is the frontmost application by going to the scripts menu > Open Scripts Folder > Open iTunes Scripts Folder. That's where you need to save the script.] Sorry this is a little cumbersome but I can help you. Just send me a note via [my Shortwhale link](http://www.shortwhale.com/VladmrTrumpkin).

## Source code

For the intrepid and the techies, here's the source code for you:

{{< gist NSBum 4eb1e4171a012f6f7853305c4e637c25 >}}

I've found chorus repetitions to be an excellent way of honing one's pronunciation and prosody in L2 practice and I hope this approach of automating the process is helpful.
