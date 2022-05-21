---
title: "Bash variable scope and pipelines"
date: 2022-03-20T04:13:35-04:00
draft: false
authorbox: false
sidebar: false
tags:
- bash
- commandline
- cli
categories:
- programming
---
I alluded to this nuance involving variable scope in my [post](/2022/03/19/automating-the-handling-of-bank-and-financial-statements) on [automating pdf processing](/2022/03/19/automating-the-handling-of-bank-and-financial-statements), but I wanted to expand on it a bit.

Consider this little snippet:

{{< highlight bash >}}
i=0
printf "foo:bar:baz:quux" | grep -o '[^:]\+' | while read -r line ; do
   printf "Inner scope: %d - %s\n" $i $line
   ((i++))
   [ $i -eq 3 ] && break;
done
printf "====\nOuter scope\ni = %d\n" $i;
{{< /highlight >}}

If you run this script - not in interactive mode in the shell - but as a script, what will `i` be in the outer scope? And why?

Unless you look carefully, you would think that `i` should be 3. After all, the `while` loop exits on a test for equality of `i` and 3, right? But no, `i` remains 0 in the outer scope; and this is because each command in a pipeline runs in its own subshell. From the GNU `bash` manual [section on pipelines](https://www.gnu.org/software/bash/manual/html_node/Pipelines.html):


> Each command in a pipeline is executed in its own _subshell_, which is a _separate process_. (Emphasis is mine.)

The last command in the pipeline in the above example is the `while` loop, so it's merrily executing in its own subshell modifying its own `i` while the outer scope is unaware of what's happening in this shell. This explains why `i` remains 0 in the outer scope.

But what are we to do if we want the inner scope to modify `i`? The key is to set the `lastpipe` option with `shopt -s lastpipe`. This option introduced in `bash` 4.2 forces the last command in the pipeline to run in the outer shell environment. So now if we modify the script with this option:

{{< highlight bash >}}
shopt -s lastpipe

i=0
printf "foo:bar:baz:quux" | grep -o '[^:]\+' | while read -r line ; do
   printf "Inner scope: %d - %s\n" $i $line
   ((i++))
   [ $i -eq 3 ] && break;
done
printf "====\nOuter scope\ni = %d\n" $i;
{{< /highlight >}}

what is `i` in the outer scope? Right, it's 3 this time because the `while` loop is executing in the shell environment, not in its own subshell.
