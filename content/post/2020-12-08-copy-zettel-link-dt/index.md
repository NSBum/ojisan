---
title: "Copy Zettel as link in DEVONthink"
date: 2020-12-08T05:16:36-05:00
draft: false
authorbox: false
sidebar: false
tags:
- zettelkasten
- devonthink
- applescript
categories:
- zettelkasten
---
Following up on my [recent article](/2020/12/03/cleaning-up-zettelkasten-wikilinks-in-devonthink-pro/) on cleaning up [Zettelkasten](https://zettelkasten.de/) WikiLinks in [DEVONthink](https://www.devontechnologies.com/), here's another script to solve the problem of linking notes.

Backing up to the problem. In the Zettelkasten (or _archive_) - Zettel (or _notes_) are stored as list of [Markdown](https://www.markdownguide.org/) files. But what happens when I want to add a link to another note into one that I'm writing? Since DEVONthink recognizes WikiLinks, I can just start typing but then I have to remember the exact date so that I can pick the item out of the contextual list that DEVONthink offers as links. Also, if I took that approach I would end up with the same problem of excessive text in the link that I would then have to clean up with the [previous script](/2020/12/03/cleaning-up-zettelkasten-wikilinks-in-devonthink-pro/).

Instead, the easier approach is to use AppleScript again, triggered by a [Keyboard Maestro](http://www.keyboardmaestro.com/main/) macro to extract the UID from the title and put it on the clipboard, ready to go into the note I'm writing. Simple, but small inconveniences amplied over time become impediments to efficient learning and writing.

{{<  highlight applescript >}}
(*
Copyright © 2020 Alan Duncan

Permission is hereby granted, free of charge, to any person obtaining a copy of this 
software and associated documentation files (the “Software”), to deal in the Software 
without restriction, including without limitation the rights to use, copy, modify, merge, 
publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons 
to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies 
or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE 
FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, 
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
DEALINGS IN THE SOFTWARE.
*)

use AppleScript version "2.4" -- Yosemite (10.10) or later
use scripting additions

tell application id "DNtp"
   set theSelections to the selection
   if theSelections is {} then
      error localized string "Please select at least one document, then try again."
   end if
   repeat with theRecord in theSelections
      set theTitle to name of theRecord
      set the clipboard to "[[" & extractLink(theTitle) of me & "]]"
   end repeat
end tell

on extractLink(theText)
   return do shell script "echo " & quoted form of theText & " | grep -Eo '[0-9]{14}'"
end extractLink
{{< /highlight >}}

_N.B._ In order to effectively use links in the form of `[[20201207215041]]`, you'll need to store the 14 digit timestamp as an alias for the actual Zettel tile. See the [previous article](/2020/12/03/cleaning-up-zettelkasten-wikilinks-in-devonthink-pro/) that discusses it further or [this article](https://austincloud.guru/2020/09/17/using-aliases-in-devonthink-for-zettelkasten/) by Mark Honomichl on using aliases in a DEVONthink-based Zettelkasten.

### References:

- [Zettelkasten Note-Taking Method With DEVONthink](https://www.stefanimhoff.de/zettelkasten-note-taking-devonthink/) - an overview of the methodology with some implementation-specific details for DEVONthink
- [Getting started with Zettelkasten](https://zettelkasten.de/posts/overview/) - an overview of the method. Start here if you're unfamiliar with this approach to information work.
