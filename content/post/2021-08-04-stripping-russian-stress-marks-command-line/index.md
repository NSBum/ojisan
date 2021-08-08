---
title: "Stripping Russian stress marks from text from the command line"
date: 2021-08-04T17:18:36-04:00
draft: false
authorbox: false
sidebar: false
tags:
- russian
- unicode
- utf8
categories:
- programming
---
Russian text intended for learners sometimes contains marks that indicate the syllabic stress. It is usually rendered as a vowel + a combining diacritical mark, typically the combining acute accent `\u301`. Here are a couple ways of stripping these marks on the command line:

First is a version using Perl

{{< highlight bash >}}
#!/bin/bash

f='покупа́ешья́';
echo $f | perl -C -pe 's/\x{301}//g;'
{{< /highlight >}}

And then another using the `sd` tool:

{{< highlight bash >}}
#!/bin/bash

f='покупа́ешья́';
echo $f | sd "\u0301" ""
{{< /highlight >}}

Both rely on finding the combining diacritical mark and removing it with regex.

_(Yes, I know the example word is nonsense Russian; it's just meant to illustrate stripping the stress marks from any vowel.)_