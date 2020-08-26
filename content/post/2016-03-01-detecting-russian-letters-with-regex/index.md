---
title: Detecting Russian letters with regex
date: 2016-03-01 04:51:52
aliases: ['/2016/03/01/Detecting-Russian-letters-with-regex/']
authorbox: false
tags:
- russian
- regex
- php
categories:
- programming
---
How to identify Russian letters in a string? The short answer is: `[А-Яа-яЁё]` but depending on your regex flavor, `[\p{Cyrillic}]` might work. What in the word does this regex mean? It's just like `[A-Za-z]` with a twist. The `Ёё` at the end adds support for ё ("yo") which is in the Latin group of characters.

See [this question](http://stackoverflow.com/questions/3212266/detecting-russian-characters-on-a-form-in-php) on Stack Overflow.
