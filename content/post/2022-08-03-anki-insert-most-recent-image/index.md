---
title: "Anki: Insert the most recent image"
date: 2022-08-03T16:37:21-04:00
draft: false
authorbox: false
sidebar: true
tags:
- anki
- cli
- programming
categories:
- anki
---
I make a _lot_ of [Anki](https://apps.ankiweb.net) cards, so I'm on a constant quest to make the process more efficient. Like a lot of language-learners, I use images on my cards where possible in order to make the word or sentence more memorable.

### Process

When I find an image online that I want to use on the card, I download it to `~/Documents/ankibound`. A [Hazel](https://www.noodlesoft.com) rule then grabs the image file and converts it to a `.webp` file with relatively low quality and a maximum horizontal dimension of 200px. The size and low quality allow me to store lots of images without overwhelming storage capacity, or more importantly, resulting in long synchronization times.

But, getting the "done" image into Anki is a hole in the process. Yes, I could click the paperclip "insert media" button and browse to the file. Or I could open a Finder window and drag the file into the image field. But a faster solution is to use [AnkiConnect](https://foosoft.net/projects/anki-connect/) to store the image file and then just insert an `<img>` tag into the field HTML, then close up. If we set this up as a [Keyboard Maestro](https://www.keyboardmaestro.com/main/) macro, it's just a quick keystroke combination.

Here's how it works:

#### Finding the most recent file

We're going to use `bash` for this because the composability of its tools make this kind of filesystem work _so_ easy. Here's the first part of our script.

{{< highlight bash >}}
#!/bin/bash

DIR="$HOME/Documents/ankidone"
fn=$(ls -lt $DIR | head -2 | tail -1 | awk '{print $9}')
{{< /highlight >}}

`lt -lt` gives us a list of files in `$DIR` ordered by modification date. Then `head -2` returns the first two lines. Why 2 lines? Well `ls` insists on printing out a `total _n_` line first, so we need to grab _that_ line and the one we want which is next. We find our most recent file line with a call to `tail -1`. Finally `awk` splits the line into space-separate fields. The filename is the ninth field. So `$fn` now has our filename and extension.

#### Storing the file in `collection.media`

We will use AnkiConnect to store the file for us.

{{< highlight bash >}}
ip="http://localhost:8765/"
action="storeMediaFile"
json=$(jo -p version=6 action=$action params[filename]=$fn params[path]="$DIR/$fn")
r=$(curl -s -XPOST "$ip" \
   -H 'Content-Type: application/json' \
   -d "$json"
)
{{< /highlight >}}

The hard-coded `$ip` address is just the standard address of the AnkiConnect server running inside of Anki. The API action we're interested in is `storeMediaFile`, for obvious reasons. Next we use the excellent `jo` tool[^1] to build the required JSON payload for the POST API call.

#### Inserting the image into the editor

In our Keyboard Maestro macro, we set the Execute Shell Script action to same the result on the clipboard. The last part of our shell script formats an `<img>` HTML tag for us to insert. That's what's on the clipboard when the shell script exits.

The macro assumes the cursor is sitting in the image field. So with a command+shift+X we can open the HTML field editor. Then just a paste keystroke, and repeat the command+shift+X and the image should appear. Done!

There are definitely other ways we could go about this, that don't involve AnkiConnect. It's possible that just moving the image into `collection.media` would suffice. But then we would have to hard-code the proper path to that directory and if you use multiple collections, you'd be out of luck.

For reference, here's the whole script:

{{< highlight bash >}}
#!/bin/bash

DIR="$HOME/Documents/ankidone"
fn=$(ls -lt $DIR | head -2 | tail -1 | awk '{print $9}')

ip="http://localhost:8765/"
action="storeMediaFile"
json=$(jo -p version=6 action=$action params[filename]=$fn params[path]="$DIR/$fn")
r=$(curl -s -XPOST "$ip" \
   -H 'Content-Type: application/json' \
   -d "$json"
)
echo "<img src=\"$fn\">"
{{< /highlight >}}

Happy studying!

[^1]: `jo` is non-standard on my system. On macOS you can install via `brew install jo`. If you work frequently with JSON on the command line, it saves a lot of time. More about the `jo` [here](https://jpmens.net/2016/03/05/a-shell-command-to-create-json-jo/).
