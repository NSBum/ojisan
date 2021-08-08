---
title: "Generating HTML from Markdown in Anki fields"
date: 2021-03-24T06:19:38-04:00
draft: false
authorbox: false
sidebar: false
tags:
- markdown
- keyboard-maestro
- python
- programming
- ankiweb
- html
categories:
- anki
---
I write in Markdown because it's much easier to keep the flow of writing going without taking my hands off the keyboard.

I also like to write content in Anki cards in Markdown. Over the years there have been various ways in of supporting this through add-ons:

- The venerable [Power Format Pack](https://ankiweb.net/shared/info/162313389) was great but no longer supports Anki 2.1, so it became useless.
- [Auto Markdown](https://ankiweb.net/shared/info/1030875226) worked for a while but as of Anki version 2.1.41 does not.
- After `Auto Markdown` stopped working, I installed the supposed fix [Auto Markdown - fix version](https://ankiweb.net/shared/info/15061497) but that didn't work either.
- It's possible that the [Mini Format Pack](https://ankiweb.net/shared/info/295889520) will work, but honestly I'm tired of the constant break-fix-break-fix cycle with Anki.

### The problem

The real problem with Markdown add-ons for Anki is the same as every other add-on. They are all hanging by a thread. Almost every minor point upgrade of Anki breaks at least one of my add-ons. It's nearly impossible to determine in advance whether an Anki upgrade is going to break some key functionality that I rely on. And add-on developers, even prominent and prolific ones come and go when they get busy, distracted or disinterested. It's one of the most frustrating parts of using Anki.

---

### The solution

The broad solution to the break-fix-break cycle is to find solutions that don't rely on the underlying codebase. In other words, where possible, I'll code my own functionality and use GUI scripting either through AppleScript or Keyboard Maestro to accomplish what I need.

The only functionality I need is to allow me to write my own Markdown code in a note field, press a keystroke and have it render the Markdown to field HTML.

#### Install Python `markdown` module

It's as simple as `pip3 install markdown` in the Terminal.

#### Keyboard Maestro macro

The strategy for the Keyboard Maestro macro is straightforward: Select the text → Copy the text → Render the Markdown to HTML → Paste the HTML code into the HTML field view → Close the HTML field view. The core of the macro is the Python script to generate HTML code from the Markdown. It's nothing fancy.

{{< highlight python >}}
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import markdown
import os

md_text = os.environ['KMVAR_ruword']
print(markdown.markdown(md_text))
{{< /highlight >}}

You can access the entire macro _Create Anki field markdown.kmmacros_ [here](/attachments/2021/03/24/CreateAnkifieldMarkdown.kmmacros).
