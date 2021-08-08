---
title: "A Keyboard Maestro macro to edit Anki sound file"
date: 2021-07-26T06:46:29-04:00
draft: false
authorbox: false
sidebar: true
tags:
- audacity
- keyboard-maestro
- anki
categories:
- anki
---
Often when I import a pronunciation file into Anki, from [Forvo](https://www.forvo.com) for example, the volume isn't quite right or there's a lot of background noise; and I want to edit the sound file. How?

The solution for me, as it often the case is a Keyboard Maestro macro.

### Prerequisites

- [Keyboard Maestro](https://www.keyboardmaestro.com/main/) - if you are a macOS power user and don't have KM, then your missing on a lot.
- [Audacity](https://www.audacityteam.org/) - the multi-platform FOSS audio editor

### Outline of the approach

Since Keyboard Maestro won't know the path to our file in Anki's `collection.media` directory, we have to find it. But the first task is to extract the filename. In the Anki note field, it's going to have this format:

{{< highlight bash >}}
[sound:forvo-e21a80cf-285b8575-3972ebd2-24eaa712-d8e5cc26.mp3]
{{< /highlight >}}

To extract the the filename `forvo-e21a80cf-285b8575-3972ebd2-24eaa712-d8e5cc26.mp3` we can just use `sed`:

{{< highlight bash >}}
sed -E 's/\[.*:(.*)\]/\1/g'
{{< /highlight >}}

And to find the file in the macOS file system:

{{< highlight bash >}}
mdfind -name $fn
{{< /highlight >}}

But we want to restrict our search to a `collection.media` directory because the file might be cached somewhere else. For example [Awesome TTS](https://ankiweb.net/shared/info/301952613) caches a copy of generated or downloaded files. Here, we can pipe our `mdfind` results to `grep`:

{{< highlight bash >}}
mdfind -name $fn | grep -E 'collection[^\0]media'
{{< /highlight >}}

Putting it all together, this is script we'll use in the KM macro:

{{< highlight bash >}}
#!/bin/bash

fn=$(pbpaste | sed -E 's/\[.*:(.*)\]/\1/g')
# open with Audacity but only if file is found in 
# a path with collection.media
open -a /Applications/Audacity.app \
     "$(mdfind -name $fn | grep -E 'collection[^\0]media')"
{{< /highlight >}}

Now we just just have to make sure that the field contents are on the clipboard for `pbpaste` to work. In KM, we will just add Select All and Copy actions (⌘A and ⌘C.)