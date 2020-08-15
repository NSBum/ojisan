---
title: "Speaking of regex: sd - a tool to search and displace"
date: 2020-08-15T09:32:57-04:00
draft: true
authorbox: false
sidebar: true
tags:
- sed
- regex
- bash
categories:
- programming
---
With all its peculiarities of syntax, `sed` leaves a bit to be desired. That's why I was pleased to find `sd`, or "Search and Displace", a tool that does what `sed` does but with less arcane syntax.

For example:

{{< highlight bash  >}}
# prints "Corruption" (W.Barr)
echo "\"Corruption\" by W.Barr" | sd '(.+)\sby\s(.+)' '$1 ($2)'
{{< /highlight >}}

Or just leave out the `\s` metacharacter in favour of a literal string:

{{< highlight bash  >}}
sd '(.+) by (.+)' '$1 ($2)'
{{< /highlight >}}

It does all the tricks you'd expect from a `sed` replacement. For example, named capture groups:

echo "The U.S. president is Donald Trump" | sd '.+\s(?P<evilhuman>\w+ \w+)$' '$evilhuman is a liar.'
{{< highlight bash  >}}
# prints Donald Trump is a liar.
echo "The U.S. president is Donald Trump" | sd '.+\s(?P<evilhuman>\w+ \w+)$' '$evilhuman is a liar.'
{{< /highlight >}}

The published benchmarks suggest that it is comparably performant, if not superior to `sed`.

It's work checking out - [chmln/sd](https://github.com/chmln/sd). Installation on macOS is simple, just `brew install sd` if you're using Homebrew.