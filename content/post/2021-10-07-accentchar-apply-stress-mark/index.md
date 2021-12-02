---
title: "accentchar: a command-line utility to apply Russian stress marks"
date: 2021-10-07T09:17:25-04:00
draft: false
authorbox: false
sidebar: false
tags:
- cli
- bash
- russian
categories:
- programming
---
I've [written](/2020/10/19/typing-russian-stress-marks-on-macos/) a [lot](/2021/08/04/stripping-russian-stress-marks-from-text-from-the-command-line/) about applying and removing syllabic stress marks in Russian text because I use it a lot when making Anki cards.

This iteration is a command line tool for applying the stress mark at a particular character index. The advantage of these little shell tools is that they can be composable, integrating into different tools as the need arises.


{{< highlight bash >}}
#!/usr/local/bin/zsh

while getopts i:w: flag
do
    case "${flag}" in
        i) index=${OPTARG};;
        w) word=${OPTARG};;
    esac
done

if [ $word ]; then
    temp=$word
else
    read temp
fi

outword=""
for (( i=0; i<${#temp}; i++ )); do
    thischar="${temp:$i:1}"
    if [ $i -eq $index ]; then
        thischar=$(echo $thischar | perl -C -pe 's/(.)/\1\x{301}/g;')
    fi
    outword="$outword$thischar"
done

echo $outword
{{< /highlight >}}

We can use it in a couple different ways. For example, we can provide all of the arguments in a declarative way:

{{< highlight bash >}}
➜  cli accentchar -i 1 -w 'кошка'
ко́шка
{{< /highlight >}}

Or we can pipe the word to `accentchar` and supply only the index as an argument:

{{< highlight bash >}}
➜  cli echo "кошка" | accentchar -i 1
ко́шка
{{< /highlight >}}