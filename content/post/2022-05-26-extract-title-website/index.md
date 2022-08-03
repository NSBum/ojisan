---
title: "Extracting title title of a web page from the command line"
date: 2022-05-26T05:26:35-04:00
draft: false
authorbox: false
sidebar: false
tags:
- web
- shell
- cli
categories:
- programming
---
I was using a REST API at https://textance.herokuapp.com/title but it seems awfully fragile. Sure enough this morning, the entire application is down. It's also not open-source and I have no idea who actually runs this thing.

Here's the solution:

{{< highlight bash >}}
#!/bin/bash

url=$(pbpaste)
curl $url -so - | pup 'meta[property=og:title] attr{content}'
{{< /highlight >}}

It does require `pup`. On macOS, you can install via `brew install pup`. 

There are other ways using regular expressions but no dependency on `pup` but parsing HTML with regex is not such a good idea.