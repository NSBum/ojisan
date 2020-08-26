---
title: 'anki_tool: low level manipulation of Anki databases'
date: 2016-03-12 15:16:00
authorbox: false
tags:
- anki
- programming
- python
- learning
categories:
- anki
---
Speaking of [Anki](http://ankisrs.net), here's a Swiss Army knife of database utilities that provides searching, moving and renaming functions from the command line.

On [GitHub](https://github.com/repolho/anki_tool).

You can do things like this to rename and collect tags:

{{< highlight bash >}}
$ anki_tool mv_tags '(dinosaur|mammal)' animal
{{< /highlight >}}

Looks cool.
