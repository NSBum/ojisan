---
title: "Stripping Russian syllabic stress marks in Python"
date: 2022-01-23T05:06:06-05:00
draft: true
authorbox: false
sidebar: false
tags:
- russian
- nlp
- regex
- programming
- unicode
- utf8
- python
categories:
- programming
---
I [written previously](h/2021/08/04/stripping-russian-stress-marks-from-text-from-the-command-line/) about stripping syllabic stress marks from Russian text using a Perl-based regex tool. But I needed a means of doing in solely in Python, so this just extends that idea.

{{< highlight python >}}
#!/usr/bin/env python3

import re

def strip_stress_marks(text: str) -> str:
   b = text.encode('utf-8')
   # correct error where latin accented ó is used
   b = b.replace(b'\xc3\xb3', b'\xd0\xbe')
   # correct error where latin accented á is used
   b = b.replace(b'\xc3\xa1', b'\xd0\xb0')
   # correct error where latin accented é is used
   b = b.replace(b'\xc3\xa0', b'\xd0\xb5')
   # correct error where latin accented ý is used
   b = b.replace(b'\xc3\xbd', b'\xd1\x83')
   # remove combining diacritical mark
   b = b.replace(b'\xcc\x81',b'').decode()
   return b

text = "Том столкну́л Мэри с трампли́на для прыжко́в в во́ду."

print(strip_stress_marks(text))
# prints "Том столкнул Мэри с трамплина для прыжков в воду."
{{< /highlight >}}

The approach is similar to the Perl-based tool we constructed before, but this time we are working working on the `bytes` object after encoding as utf-8. Since the `bytes` object has a `replace` method, we can use that to do all of the work. The first 4 replacements all deal with edge cases where accented Latin characters are use to show the placement of syllabic stress instead of the Cyrillic character plus the combining diacritical mark. In these cases, we just need to substitute the proper Cyrillic character. Then we just strip out the "combining acute accent" `U+301` → `\xcc\x81` in UTF-8.