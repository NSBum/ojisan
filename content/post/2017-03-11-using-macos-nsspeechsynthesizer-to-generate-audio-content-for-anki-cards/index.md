---
title: Using macOS NSSpeechSynthesizer to generate audio content for Anki cards
date: 2017-03-11 14:12:28
aliases: ['/2017/03/11/Using-macOS-NSSpeechSynthesizer-to-generate-audio-content-for-Anki-cards/']
tags:
- macOS
- dev
- anki
categories:
- anki
---
As I've written before, I use [Anki](https://apps.ankiweb.net/) for Russian language learning. One of the skills to master in learning a foreign language is to quickly speak and recognize numbers. With a little help from macOS, I've developed a way of rapidly creating audible content of spoken numbers for my Anki cards.

That's the good news. The bad news is that as of right now, you'll have to have Xcode and build the app yourself. Someday, I'll deal with all the official certificate stuff again (I've not developed apps seriously for iOS or macOS for several years now.)

But, here it is anyway on Github: [RussianNumberGenerator](https://github.com/NSBum/RussianNumberGenerator).

The operating principal is that it generates spoken numbers in a user-specified range. You can choose to generate numbers sequentially or randomly within a range. `NSSpeechSynthesizer` generates .aiff files, but to make the audio content more widely usable, the application converts these files to .mp3 using `ffmpeg` which, by the way, you will need to have installed.

![RussianNumberGenerator](http://i.imgur.com/R8waGlJ.png)

There's much more to do, but there's the idea.
