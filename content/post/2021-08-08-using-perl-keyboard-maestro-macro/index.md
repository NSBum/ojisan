---
title: "Using Perl in Keyboard Maestro macros"
date: 2021-08-08T09:36:41-04:00
draft: false
authorbox: false
sidebar: true
tags:
- keyboard-maestro
- perl
- anki
- programming
categories:
- programming
---
One of the things that I love about Keyboard Maestro is the ability to chain together disparate technologies to achieve some automation goal on macOS.

In most of my previous posts about Keyboard Maestro macros, I've used Python or shell scripts, but I decided to draw on some decades-old experience with Perl to do a little text processing for a specific need.

### Background

I want this text from Wiktionary:

{{< figure src="images/2021/08/08/wikisnippet.png">}}

to look like this:

{{< highlight markdown >}}
- `по проше́ствии пяти́ лет` - after five years had elapsed; five years later
{{< /highlight >}}

so that I can then render this Markdown into HTML on my Anki cards.

That's it. Simple; I would just highlight the block in the browser, copy, and allow Keyboard Maestro to reformat the text.

### Splitting the text into lines

Not knowing how the lines were split, I started by analyzing the string on the clipboard character-by-character.

{{< highlight perl >}}
my @chars = split("", $str);
foreach (@chars) {
   printf("%02x ", ord($_));
}
{{< /highlight >}}

which shows:

{{< figure src="images/2021/08/08/consoleout.png">}}

With that information in hand, we know that the line separator is `\x0A`.

No we can easily split the string on that character and reformat. So the core of the macro will be:

{{< highlight perl >}}
#!/usr/bin/perl

my $str = $ENV{KMVAR_ruword};
my @lines = split("\x0A", $str); 
printf("- `%s` - %s", $lines[0], $lines[2]);
{{< /highlight >}}

No we just need to get the clipboard into the variable `ruword` and pass the results of the Perl script back to the clipboard, and paste.