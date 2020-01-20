---
title: "Sunday, September 16, 2018"
date: 2018-09-16T08:03:55-04:00
aliases: ['/2018/09/16/Sunday-September-16-2018/']
tags:
- programming
- regex
- anki
- russian
categories:
- programming
---
[Regex 101](https://regex101.com/) is a great online regex tester.

 ---
 Speaking of regular expressions, for the past year, I've used an [automated process](/2017/11/03/Process-automation-in-building-Anki-vocabulary-cards/) for building Anki flash cards. One of the steps in the process is to download Russian word pronunciations from Wiktionary. When Wiktionary began publishing transcoded mp3 files rather than just ogg files, they broke the URL scheme that I relied on to download content. The new regex for this scheme is: `(?:src=.*:)?src=\"(\/\/.*\.mp3)`

 Edit 2018-09-17: Nope, still not right. This is the new working version:
 `data-.+\s?/?><source\s+src=\"(\/\/.*\.mp3)`

---

Gina Loudon is a [liar and an idiot](https://twitter.com/TheContemptor/status/1037521368542322688/video/1). She claims in her recent book proclaiming the sanity of Donald Trump that she has a Ph.D. in psychology. In fact, she does not. Her degree is from an online "school."