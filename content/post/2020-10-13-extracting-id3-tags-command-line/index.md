---
title: "Extracting ID3 tags from the command line - two methods"
date: 2020-10-13T15:24:24-04:00
draft: false
authorbox: false
sidebar: false
tags:
- bash
- shell
- mp3
categories:
- programming
---
As part of a [Hazel]() rule to process downloaded mp3 files, I worked out a couple different methods for extracting the ID3 `title` tag. Not rocket science, but it took a little time to sort out. Both rely on non-standard third-party tools, both for parsing the text and for extracting the ID3 tags.

### Extracting ID3 title with `ffprobe`

`ffprobe` is part of the `ffmpeg` suite of tools which on macOS can be installed with [Homebrew](https://brew.sh/). If you don't have the latter, go [install it](https://brew.sh/) now; because it opens up so many tools for your use. In this case, it makes `ffmpeg` available via `brew install ffmpeg`.

With that in place, extracting the title is just:

{{< highlight bash >}}
title=$(ffprobe -loglevel error -show_entries format_tags=title -of 
   default=noprint_wrappers=1:nokey=1 $file)
{{< /highlight >}}

### Extracting ID3 title with `id3info`

`id3info` is part of the `id3tool` suite of tools installed using - you guessed it - [Homebrew](https://brew.sh/). This solution also uses `sd` (`brew install sd`.) The latter is a more intuitive search and displace tool than the old stand-by `sed`.

{{< highlight bash >}}
IFS=$'\r\n'
tit2=""
for ln in $( id3info $file ); do
    if echo $ln | grep -q "TIT2"
    then
        tit2=$( echo $ln | sd '.*TIT2.*: (.*).*' '$1' );
        break;
    fi
done
{{< /highlight >}}

Or a one-liner using perl:

{{< highlight perl >}}
echo $( id3info $file ) | perl -ne 'print $1 if /TIT2.*?\:\s+(.*?)\s===/;'
{{< /highlight >}}

#### References

- [sd](https://github.com/chmln/sd) - intuitive search and displace - a `sed` replacement
- [ffmpeg](https://ffmpeg.org/) - play, record, convert, and stream audio and video
- [id3tool](http://nekohako.xware.cx/id3tool/) - ID3 editing tool
- [Bash `for` loop](https://linuxize.com/post/bash-for-loop/#break-and-continue-statements) - a short tutorial on the Bash `for` loop - something that I wasn't really proficient at. Always good to revist.