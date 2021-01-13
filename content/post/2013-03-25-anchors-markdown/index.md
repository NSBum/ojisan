---
title: "Markdown anchors"
date: 2013-03-25T05:45:09-05:00
draft: false
authorbox: false
sidebar: false
tags:
- blog
- markdown
categories:
- programming
---
TIL how to use anchors in [Markdown](http://daringfireball.net/projects/markdown/) documents.  I needed to use this in a long blog post in my [Octopress](http://octopress.org) blog and was stymied. 

As usual, I found the [answer](http://stackoverflow.com/questions/5319754/cross-reference-named-anchor-in-markdown/7335259#7335259) on Stack Overflow.

{{< highlight html >}}
Beam me [up](#enterprise), Scotty

<a id="enterprise"></a>
{{< /highlight >}}

It's a great way to move around in longer content.

_2014-03-03: I no longer publish using Octopress; but this should work in most cases where Markdown is used.  Bitbucket is a notable exception.  For Github wiki, you'll need something like:_

{{< highlight html >}}
# <a name="heading1" /> Heading 1 #
{{< /highlight >}}

and for the link to that anchor:

{{< highlight html >}}
[link to heading1](#heading1)
{{< /highlight >}}
