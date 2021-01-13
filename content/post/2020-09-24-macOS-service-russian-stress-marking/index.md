---
title: "A macOS text service for morphological analysis and in situ marking of Russian syllabic stress"
date: 2020-09-24T19:36:10-04:00
draft: false
authorbox: false
sidebar: false
tags:
- linguistics
- russian
- python
categories:
- programming
---
Building on my [earlier explorations](/2020/08/18/automated-marking-of-russian-syllabic-stress/) of the [UDAR](https://github.com/reynoldsnlp/udar) project, I've created a macOS Service-like method for in-situ marking of syllabic stress in arbitrary Russian text. The following video shows it in action:

{{< youtube 4bBPe3cjWaA >}}

The Keyboard Maestro is simple; we execute the following script, bracketed by `Copy` and `Paste`:

{{< highlight python >}}
#!/Users/alan/.pyenv/shims/python3
import xerox
import udar
import re

rawText = xerox.paste()
doc1 = udar.Document(rawText, disambiguate=True)
searchText = doc1.stressed()
result = re.sub(r'( ,)', ",", searchText)
xerox.copy(result)
{{< /highlight >}}

This presumes that `udar` and its prerequisites have already been installed, of course.

So why not build out this idea as an _actual_ macOS text service? In theory, it should be possible. Maybe even ideal but for Python version management I use [pyenv](https://github.com/pyenv/pyenv). Because some of the UDAR dependencies will not run under my current system Python version of 3.8.5, I use 3.7.4 under pyenv and it appears that the correct Python version run under whatever environment the service launches. Someone with deeper system knowledge could undoubtedly figure it out; but instead I accomplished the same effect via a Keyboard Maestro macro.
