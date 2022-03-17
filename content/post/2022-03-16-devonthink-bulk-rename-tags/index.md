---
title: "Bulk rename tags in DEVONthink 3"
date: 2022-03-16T07:04:52-04:00
draft: false
authorbox: false
sidebar: false
tags:
- devonthink
- applescript
categories:
- programming
---
In DEVONthink, I tag _a lot_. It's an integral part of my strategy for finding things in my paperless environment. As I wrote about [previously](/2015/06/18/finding-things-with-devonthink/) hierarchical tags are a big part of my organizational system in DEVONthink. For many years, I tagged subject matter with tags that emmanate from a single tag named `topic_`, but it was really an unnecessary top-level complication. So, the first item on my to-do list was to get rid of the all tags with a `topic_` first level.

Also began to despise the underscore separator symbol. Instead, the `:` would take up less screen real estate. So the second item on my to-do list was to do a symbol replacement.

Complicating all of this is that we would have to do this all recursively because of my deeply-hierarchical tag tree. Since DEVONthink's AppleScript support is excellent, I put together a little program to take care of the tag reorganization for me. Aside from the recursive processing, the other interesting bit is how to use the `do shell script` command to easily use command line tools rather than resorting to the clumsy AppleScript syntax for text processing.

I've posted the script here. It's specific to my needs; but it's here partly to remind my future self of how I did this and partly to serve as a jumping-off point for others who may have similar needs.

{{< highlight applescript >}}
--
--   Created by: Alan Duncan
--   Created on: 2022-03-15
--
--   Copyright © 2022 OjisanSeiuchi, All Rights Reserved
--

use AppleScript version "2.4" -- Yosemite (10.10) or later
use scripting additions

global names
set names to {}

on processTag(thisTag)
   tell application id "DNtp"
      set db to the first database whose name is "leviathan"
      tell db
         set tagName to name of thisTag
         if tagName begins with "topic_" then
            -- remove the topic_prefix
            set cmd to "echo " & quoted form of tagName & " | " & ¬
               "sed -E 's/topic_//g'"
            set newName to do shell script cmd
            -- change "_" to ":"
            set cmd to "echo " & quoted form of newName & " | " & ¬
               "tr \"_\" \":\""
            set newName to do shell script cmd
            -- rename
            tell thisTag
               set name to newName
            end tell
            set names to names & newName
         end if
         -- perform recurrently as needed
         tell thisTag
            repeat with childRecord in children
               set tagType to (tag type of childRecord as string)
               if tagType is "ordinary tag" then
                  set tagName to (name of childRecord as string)
                  processTag(childRecord) of me
               end if
            end repeat
         end tell
      end tell
   end tell
end processTag

tell application id "DNtp"
   set theSelection to the selection
   repeat with topTag in theSelection
      processTag(topTag) of me
   end repeat
   names
end tell
{{< /highlight >}}
