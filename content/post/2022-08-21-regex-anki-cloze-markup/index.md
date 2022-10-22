---
title: "A regex to remove Anki's cloze markup"
date: 2022-08-21T12:00:49-04:00
draft: false
authorbox: false
sidebar: true
tags:
- regex
- anki
categories:
- programming
---
Recently, someone asked [a question](https://www.reddit.com/r/Anki/comments/wtvijv/how_to_use_cloze_note_types_as_basic/) on [r/Anki](https://www.reddit.com/r/Anki/) about changing and existing cloze-type note to a regular note. Part of the solution involves stripping the cloze markup from the existing cloze'd field. A cloze sentence has the form `Play {{c1::studid}} games.` or `Play {{c1::stupid::pejorative adj}} games.`

To handle both of these cases, the following regular expression will work. Just substitute for `$1`.
{{< highlight regex >}}
\{\{c\d::([^:\}]+)(?:::+[^\}]*)*\}\}
{{< /highlight >}}

However, the Cloze Anything markup is different. It uses `(` and `)` instead of curly braces. If we want to flexibly remove both the standard and Cloze Anything markup, then our pattern would look like:

{{< highlight c >}}
[\{\(]{2}c\d+::([^:\}\)]++)(?:::[^:\}\)]+)?[\}\)]{2}
{{< /highlight >}}