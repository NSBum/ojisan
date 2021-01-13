---
title: "URL-encoding URLs in AppleScript"
date: 2020-11-15T14:40:23-05:00
draft: false
authorbox: false
sidebar: false
tags:
- applescript
- russian
- cyrillic
categories:
- programming
---
The AppleScript Safari API is apparently quite finicky and rejects Russian Cyrillic characters when loading URLs.

For example, the following URL `https://en.wiktionary.org/wiki/стоять#Russian` throws an error in AppleScript. Instead, Safari requires URL's of the form `https://en.wiktionary.org/wiki/%D1%81%D1%82%D0%BE%D1%8F%D1%82%D1%8C#Russian` whereas Chrome happily consumes whatever comes along. So, we just need to encode the URL thusly:

{{< highlight applescript >}}
use framework "Foundation"

-- encode Cyrillic test as "%D0" type strings
on urlEncode(input)
   tell current application's NSString to set rawUrl to stringWithString_(input)
   -- 4 is NSUTF8StringEncoding
   set theEncodedURL to rawUrl's stringByAddingPercentEscapesUsingEncoding:4 
   return theEncodedURL as Unicode text
end urlEncode
{{< /highlight >}}

When researching Russian words for vocabulary study, I use the URL encoding handler to load the appropriate words into several reference sites in sequential Safari tabs.

{{< highlight applescript >}}
--
-- Created by: Alan Duncan
-- Created on: 2017-11-01
--
-- Copyright (c) 2017 Ojisan Seiuchi
-- All Rights Reserved
--

use AppleScript version "2.4" -- Yosemite (10.10) or later
use scripting additions
use framework "Foundation"

set searchTerm to the clipboard as text
set openRussianURL to "https://en.openrussian.org/ru/" & searchTerm
set wiktionaryURL to "https://en.wiktionary.org/wiki/" & searchTerm & "#Russian"
set forvoURL to "https://forvo.com/search/" & searchTerm & "/ru/"
set ruWiktionaryURL to "https://ru.wiktionary.org/wiki/" & searchTerm

tell application "Safari" to activate

-- load word definitions
tell application "Safari"
   activate
   set i to 0
   set tabList to every tab of window 1
   set tabCount to count of tabList
   repeat tabCount times
      tell window 1
         set i to i + 1
         set textURL to (URL of tab i) as text
         -- load the word in open russian
         if textURL begins with "https://en.openrussian.org" then
            set encodedURL to urlEncode(openRussianURL) of me
            
            set URL of tab i to encodedURL
            
         end if
         -- load the word in wiktionary
         if textURL begins with "https://en.wiktionary.org" then
            set URL of tab i to urlEncode(wiktionaryURL) of me
            -- make the wiktionary tab the active tab
            try
               set current tab of window 1 to tab i
            end try
            
         end if
         
         if textURL begins with "https://forvo.com" then
            set URL of tab i to urlEncode(forvoURL) of me
         end if
         
         if textURL begins with "https://ru.wiktionary.org" then
            set URL of tab i to urlEncode(ruWiktionaryURL) of me
         end if
      end tell
   end repeat
end tell

-- encode Cyrillic test as "%D0" type strings
on urlEncode(input)
   tell current application's NSString to set rawUrl to stringWithString_(input)
   set theEncodedURL to rawUrl's stringByAddingPercentEscapesUsingEncoding:4 -- 4 is NSUTF8StringEncoding
   return theEncodedURL as Unicode text
end urlEncode
{{< /highlight >}}