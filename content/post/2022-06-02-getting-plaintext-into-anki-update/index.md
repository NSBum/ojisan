---
title: "Getting plaintext into Anki fields on macOS: An update"
date: 2022-06-02T12:20:03-04:00
draft: false
authorbox: false
sidebar: true
tags:
- programming
- cli
- applescript
- keyboard-maestro
categories:
- anki
---
A few years ago, I [wrote](/2019/12/13/getting-plain-text-into-anki-a-saga/) about my problems with HTML in Anki fields. If you check out that [previous post](/2019/12/13/getting-plain-text-into-anki-a-saga/) you'll get the backstory about my objection.

The gist is this: If you copy something from the web, Anki tries to maintain the formatting. Basically it just pastes the HTML off the clipboard. Supposedly, Anki offers to strip the formatting with Shift-paste, but I've point out to the developer specific examples where this fails. Basically, I only want plain text. Ever. I will take care of any and all formatting needs via the card templates. Period.

In the previous solution, I used ApplesScript that is triggered in Quicksilver. I've migrated from Quicksilver to Keyboard Maestro since then, so it was time for an update. And the good news is that it's simpler, it's literally a Bash one-liner:

{{< highlight bash >}}
#!/bin/bash
#
# Convert contents of clipboard to plain text.

pbpaste | textutil -convert txt -stdin -stdout -encoding 4 | pbcopy

exit 0
{{< /highlight >}}

In Keyboard Maestro, I just built a macro around this command line script. It's still triggered by ⇧⌘W and also includes a paste command to Anki so it's seamless compared to the previous solution. 

A brief note about `textutil`[^1] - it's a built-in text conversion utility on macOS. The script pipes the text to `textutil` which converts the format to text. The `-encoding` option with a value of 4 is the `NSUTF8StringEncoding` encoding format.[^2] Then the results are finally piped back to the clipboard.

[^1]: [textutil](https://ss64.com/osx/textutil.html) - manipulate text files in various ways.
[^2]: [NSStringEncoding enumeration](https://developer.apple.com/documentation/foundation/nsstringencoding) - constants are provided by `NSString` as possible string encodings