---
title: AppleScript and iTerm2
date: 2017-02-02 06:40:30
aliases: ['/2017/02/02/AppleScript-and-iTerm2/']
tags:
- applescript
- mac
- macOS
- programming
- iterm2
categories:
- programming
---
Among the many reasons I use [iTerm2](https://www.iterm2.com) in lieu of the macOS Terminal is its [AppleScript support](https://www.iterm2.com/documentation-scripting.html).

I recently had the need to automate some tasks on my Amazon Web Services EC2 server in a way that takes advantage of iTerm2 AppleScript functionality.

### Use case

I've found recently, that my `screen` sessions were disappearing. Although I haven't completely excluded other causes, some have suggested that infrequently-reconnected sessions can be cleaned up. Since I'm not a Unix sysadmin, I'm not sure about this. However, I decided to test the hypothesis by writing an AppleScript that logs into my EC2 server, attaches to each `screen` session, detaches and closes the connection.

### `screen` escape sequence implementation

The trickiest bit to solve was the `^A` escape sequence that `screen` uses. Here's how I solved that part:

{{< highlight applescript >}}
key code 0 using {control down}
delay 1
keystroke "d"
{{< /highlight >}}

By wrapping that in a subroutine, I was able to automate the detachment from the current screen.

### Full implementation

The complete implementation just loops over the `screen` session ID's, attaches and detaches then finally logs out and closes the window. I use [LaunchControl](http://www.soma-zone.com/LaunchControl/) to have the AppleScript run every 2 hours.

{{< highlight applescript >}}
--
--	Created by: Alan Duncan
--	Created on: 2017-02-02
--
--	Copyright (c) 2017 OjisanSeiuchi
--	All Rights Reserved
--

use AppleScript version "2.4" -- Yosemite (10.10) or later
use scripting additions

set screenIDs to {5546, 5208, 5129, 5580}

tell application "iTerm"
	set newWindow to (create window with profile "OjisanSeiuchi EC2")
	tell current session of current window
		delay 3
		repeat with screenID in screenIDs
			-- attach to this screen session
			set screenCommand to "screen -r " & (screenID as string)
			write text screenCommand
			delay 2
			--	detach from the session
			my detach()
			delay 1
		end repeat
		write text "logout"
		delay 1
	end tell
	close newWindow
end tell

--	detaches from the current screen session
on detach()
	tell application "iTerm" to activate
	tell application "System Events"
		tell process "iTerm2"
			key code 0 using {control down}
			delay 1
			keystroke "d"
		end tell
	end tell
end detach
{{< /highlight >}}

We'll see if this solves the problem of `screen` sessions disappearing.
