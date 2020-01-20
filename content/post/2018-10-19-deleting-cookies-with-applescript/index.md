---
title: "Deleting cookies with AppleScript"
date: 2018-10-19T10:39:54-04:00
aliases: ['/2018/10/19/Deleting-cookies-with-AppleScript/']
tags:
- programming
- privacy
- applescript
categories:
- programming
---
A couple years ago I [wrote about a method](/2016/01/25/Stop-Facebook-tracking/) for deleting cookies from Safari on macOS by employing AppleScript. Now I have a new script that works on OS X 10.14 Mojave. There are ways of surgically removing cookies, but honestly most sites leave so many cookies on my machine that I have no idea what any of them do and to what extent they use them to track me.

### Safari

Here's the script for Safari. Install it in `~/Library/Scripts/Applications/Safari` (or really, wherever you like.) When launched from the scripts menu in the menu bar, it will close all current tabs and delete every cookie that Safari has saved. Since it employs UI scripting, you'll need to give it accessibility permissions when asked.

{{< highlight applescript >}}
--
--	Created by: Alan Duncan
--	Created on: 2018-10-19
--
--	Copyright (c) 2018 Ojisan Seiuchi
--	All Rights Reserved
--

use AppleScript version "2.4" -- Yosemite (10.10) or later
use scripting additions

tell application "Safari"
    activate
end tell

tell application "System Events" to tell process "Safari"
    click button 1 of window 1
    delay 0.5
    keystroke "," using command down
    delay 1
    click button "Privacy" of toolbar 1 of window 1
    delay 0.5
    click button "Manage Website Data…" of group 1 of group 1 of window "Privacy"
    delay 3
    if button "Remove All" of sheet 1 of window "Privacy" is enabled then
        try
            click button "Remove All" of sheet 1 of window "Privacy"
            delay 0.5
            keystroke tab
            delay 0.5
            keystroke return
            delay 2
            click button "Done" of sheet 1 of window "Privacy"
            delay 0.5
        on error errMsg
            click button "Done" of sheet 1 of window "Privacy"
        end try
    else
        click button "Done" of sheet 1 of window "Privacy"
    end if
    click button 1 of window 1
end tell
{{< / highlight >}}

### Chrome

In the case of Chrome, it seems to store its cookies in a SQLite database. There, I just delete the database using AppleScript:

{{< highlight applescript >}}
--
--	Created by: Alan Duncan
--	Created on: 2018-10-19
--
--	Copyright (c) 2018 MyCompanyName
--	All Rights Reserved
--

use AppleScript version "2.4" -- Yosemite (10.10) or later
use scripting additions

tell application "Google Chrome" to quit
do shell script "rm '/Users/alan/Library/Application Support/Google/Chrome/Default/Cookies'"
delay 2
tell application "Google Chrome" to activate
{{< / highlight >}}
