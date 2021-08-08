---
title: "Splitting a string on the command line - the search for the one-liner"
date: 2021-07-30T16:22:01-04:00
draft: false
authorbox: false
sidebar: true
tags:
- commandline
- programming
categories:
- programming
---
It seems like the command line is one of those places where you can accomplish crazy efficient things with one-liners. 

Here's a perfect use case for a CLI one-liner:

In Anki, I often add lists of synonyms and antonyms to my vocabulary cards, but I like them formatted as a bulleted list. My usual route to that involves Markdown. But how to convert this:

`известный, точный, определённый, достоверный`

to

{{< highlight markdown >}}
- `известный`
- `точный`
- `определённый`
- `достоверный`
{{< /highlight >}}

After trying to come up with a single text replacement strategy to make this work, the best I could do was this:

{{< highlight bash >}}
#!/bin/bash

words="известный, точный, определённый, достоверный";
echo $words | sed -E 's/, /\n/g'| sed -E 's/(.*)/- `\1`/g'

{{< /highlight >}}

Sometimes, if I get really irritated at `sed`, which is more often than I'd like, I'll switch to [`sd`](https://github.com/chmln/sd) which has more straightforward syntax.[^1] 

{{< highlight bash >}}
#!/bin/bash

words="известный, точный, определённый, достоверный";
echo $words | sd ", " "\n" | sd '(.*)\n' '\u002d \u0060$1\u0060\n';
{{< /highlight >}}

In both of these cases, the process requires two steps because of the way `sed` and `sd` work. First, we strip about the delimiters, then we capture what's left and format it.

[^1]: _Usually_. In the `sd` example, you'll see that I had to resort to Unicode in the replacement string, but it doesn't like the dash and back-tick symbols.