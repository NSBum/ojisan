---
title: "Cleaning up Zettelkasten WikiLinks in DEVONthink Pro"
date: 2020-12-03T05:19:50-05:00
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
Organizing and reorganizing knowledge is one my seemingly endless tasks. For years, I've used [DEVONthink](https://www.devontechnologies.com/) as my primary knowledge repository. Recently, though I began to lament the fact that while I seemed to be collecting and storing knowledge in a raw form in DEVONthink, that I wasn't really processing and engaging with it intellectually.[^1] In other words, I found myself collecting content but not really synthesizing, personalizing and using it. While researching note-taking systems in the search for a better way to process and absord the information I had been collecting, I discovered the [Zettelkasten](https://zettelkasten.de/posts/overview/) method. I'm not going to go into it here because it has been exhaustively described elsewhere. But I'll just say that:

- The Zettelkasten method is an effective way of organizing, learning, processng and refactoring knowledge. 
- Maintaing a Zettelkasten becomes a central component of converting _passive_ collection of material to the active _use_ of the material.
- DEVONthink Pro is an effective and flexible tool for implementing the Zettelkasten method.

One methodological detail that I need to explain about Zettelkasten is the linkage between notes. Since every note gets a unique identifier (for me, just a date/timestamp), then notes get linked together in logical ways by the user. For example, I have a Zettel with the title `20201202204635 Present passive participle -авать verbs`. Its unique identifier is `20201202204635`. Now in DEVONthink, notes can be linked with WikiLinks. If you begin typing _[[_ followed by the title of a note you get a popup list of matching selections. It's a fast way of inserting a link to another Zettel.

The problem is this: I don't want the entire title of the linked note in the WikiLink. Using the example above, I want my link to look like `[[20201202204635]]` not like `[[20201202204635 Present passive participle -авать verbs]]`

The solution is two-part

- Create a document alias in DEVONthink by extracting just the unique ID from the title
- Parse notes for outgoing WikiLinks and reformat them to use just the aliased unique ID

### Extracting unique identifier as a document alias

This part of the solution belongs to Mark Honomichl. His post [Using Aliases in DEVONthink for Zettelkasten](https://austincloud.guru/2020/09/17/using-aliases-in-devonthink-for-zettelkasten/) describes a Smart Rule in DEVONthink that extracts the unique ID from the document title and uses that for the alias. 

### Parse and edit notes containing outgoing WikiLinks

The second part of the solution requires the first. In other words, every Zettel must have an alias formed from its unique ID.

Having established that, you can fix WikiLinks in existing Zettels to use the alias. Again, converting a WikiLink like `[[20201202204635 Present passive participle -авать verbs]]` to `[[20201202204635]]` Like the first part of the solution, this is implemented in AppleScript. For now, I've chosen to run it on demand, but it could easily be reconfigured as a Smart Rule in DEVONthink.

{{< highlight applescript >}}
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
use framework "Foundation"

property NSRegularExpressionCaseInsensitive : a reference to 1
property NSRegularExpression : a reference to current application's NSRegularExpression
property NSNotFound : a reference to 9.22337203685477E+18 + 5807 -- see http://latenightsw.com/high-sierra-applescriptobjc-bugs/


tell application id "DNtp"
   set theSelections to the selection
   if theSelections is {} then
      error localized string "Please select at least one document, then try again."
   end if
   repeat with theRecord in theSelections
      set recordText to (plain text of theRecord)
      set newText to fixLinks(recordText) of me as string
      set plain text of theRecord to newText
   end repeat
end tell

on fixLinks(theText)
   set linkPattern to "\\[\\[(\\d{14})\\s[^\\]]+\\]\\]"
   set replacementPattern to "\\[\\[$1\\]\\]"
   set theRegEx to NSRegularExpression's regularExpressionWithPattern:linkPattern options:NSRegularExpressionCaseInsensitive |error|:(missing value)
   set retString to theRegEx's stringByReplacingMatchesInString:theText options:0 range:[0, theText's length] withTemplate:replacementPattern
   return retString
end fixLinks
{{< /highlight >}}


To illustrate, here's a note before and after the conversion process:

![](/images/2020/12/03/prepost.png)

To use the script, just select one or more documents and run.

[^1]: This is the so-called [collector's fallacy](https://zettelkasten.de/posts/collectors-fallacy/) wherein we tend to feel fulfilled and successful solely by collecting lots and lots of information. But at some point, we begin to realize that knowledge work isn't a passive process at all. Anyone can _collect_ information. To be of use, we have to engage with it in an active ongoing way. Building mental models is an active, not passive proces.

### References

- [Using Aliases in DEVONthink for Zettelkasten](https://austincloud.guru/2020/09/17/using-aliases-in-devonthink-for-zettelkasten/)
- [How I use Wiki-Links and Aliases in DEVONthink to read Aristotle](https://medium.com/clássicos-digitais/how-i-use-wiki-links-and-aliases-in-devonthink-to-read-aristotle-e68d4dfc0409)
- [Zettelkasten Note-Taking Method With DEVONthink](https://www.stefanimhoff.de/zettelkasten-note-taking-devonthink/) - an overview of the methodology with some implementation-specific details for DEVONthink
- [Getting started with Zettelkasten](https://zettelkasten.de/posts/overview/) - an overview of the method. Start here if you're unfamiliar with this approach to information work.

### Notes

- 2020-12-08 04-44-56 A previous version of this script used a buggy regular expression. This has been corrected.