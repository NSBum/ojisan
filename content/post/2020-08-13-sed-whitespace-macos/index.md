---
title: "sed matching whitespace on macOS"
date: 2020-08-13T22:15:47-04:00
draft: false
authorbox: false
sidebar: true
tags:
- macos
- commandline
- unix
categories:
- programming
---

sed is such a useful pattern-matching and substitution tool for work on the command line. But there's a little quirk on macOS that will trip you up. It tripped me up. On most platforms, `\s` is the character class for whitespace. It's ubiquitous in regexes. But on macOS, it doesn't work. In fact, it silently fails.

Consider this bash one-liner which looks like it should work but doesn't:

{{< highlight bash  >}}
# should print I am corrupt (W.Barr)
# instead it prints I am corrupt by W.Barr
echo "I am corrupt by W.Barr" | sed -E 's|^(.+)\sby\s(.+)|\1 (\2)|g'
{{< /highlight >}}

What _does_ work is the character class `[:space:]`:

{{< highlight bash  >}}
# prints I am corrupt (W.Barr)
echo "I am corrupt by W.Barr" | sed -E 's|^(.+)[[:space:]]by[[:space:]](.+)|\1 (\2)|g'
{{< /highlight >}}

Or just a space without a character class seems to work:

{{< highlight bash  >}}
# prints I am corrupt (W.Barr)
sed -E 's|^(.+) by (.+)|\1 (\2)|g'
{{< /highlight >}}

The `[:blank:]` character class works also:

{{< highlight bash  >}}
sed -E 's|^(.+)[[:blank:]]by[[:blank:]](.+)|\1 (\2)|g'
{{< /highlight >}}

### Bracket expressions in sed

It turns out that if you RTFM for `sed`, the explanation is clear. There are several character classes documented in the `sed` [manual](https://www.gnu.org/software/sed/manual/html_node/Character-Classes-and-Bracket-Expressions.html) and each must be enclosed in brackets `[]`. Pertinent to our issue, the `[:space:]` character class matches the following: tab, newline, vertical tab, form feed, carriage return, and space. On the other hand `[:blank:]` is more restrictive, matching only space and tab. The manual is definitely worth looking at because there are other metacharacter classes that are simply not available. For example `\w` is unusable, requiring `[:alnum:]` instead, as in:

{{< highlight bash  >}}
# prints foobar
echo "foo        bar" | sed -E 's|^([[:alnum:]]+)[[:space:]]+([[:alnum:]]+)$|\1\2|g'
{{< /highlight >}}

### References

- macOS [man page for sed](https://ss64.com/osx/sed.html) - no mention of `\s` though.
- [This question](https://superuser.com/questions/112834/how-to-match-whitespace-in-sed) about whitespace and `sed` on Superuser is worth reviewing.
- The [sed manual](https://www.gnu.org/software/sed/manual/html_node/Character-Classes-and-Bracket-Expressions.html) section on character classes and bracket expressions is a must-read. (Or the [contents](https://www.gnu.org/software/sed/manual/html_node/index.html#SEC_Contents) page of the sed manual.)