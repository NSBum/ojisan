---
title: "Creating year and month groups in DEVONthink Pro Office using AppleScript"
date: 2018-12-14T12:08:37-04:00
summary: "An AppleScript to create year and month groups in DEVONthink"
aliases: ['/2018/12/14/Creating-year-and-month-groups-in-DEVONthink-Pro-Office-using-AppleScript/']
tags:
- applescript
- programming
- devonthink
categories:
- programming
---
In [DEVONthink Pro Office](https://www.devontechnologies.com/apps/devonthink) I often organize certain content by year and month. To do that, I created a simple AppleScript to build year and month groups in the following format:

{{< figure src="/images/2018/12/14/yearmonth.png" title="DEVONthink year+month" >}}

To use the script, you select the parent group in which the year will reside.

{{< highlight applescript >}}
--
-- Created by: Alan Duncan
-- Created on: 2018-12-14
--
-- Copyright (c) 2018 Ojisan Seiuchi
-- All Rights Reserved
--

use AppleScript version "2.4" -- Yosemite (10.10) or later
use scripting additions

set theMonths to {"Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"}

tell application id "DNtp"
   try
      set theSelection to selection
      if theSelection is {} then error "Please select some contents."
      set theYear to display name editor "Year:"
      set theYearGroup to create record with {name:theYear, type:group} in current group
      repeat with i from 1 to 12
         set theMonth to item i of theMonths

         set theMonth to (my add_leading_zeros(i, 1)) & " - " & theMonth
         set theMonthGroup to create record with {name:theMonth, type:group} in theYearGroup
      end repeat
   on error
      display dialog "Error"
   end try
end tell

on add_leading_zeros(this_number, max_leading_zeros)
   set the threshold_number to (10 ^ max_leading_zeros) as integer
   if this_number is less than the threshold_number then
      set the leading_zeros to ""
      set the digit_count to the length of ((this_number div 1) as string)
      set the character_count to (max_leading_zeros + 1) - digit_count
      repeat character_count times
         set the leading_zeros to (the leading_zeros & "0") as string
      end repeat
      return (leading_zeros & (this_number as text)) as string
   else
      return this_number as text
   end if
end add_leading_zeros
{{< / highlight >}}