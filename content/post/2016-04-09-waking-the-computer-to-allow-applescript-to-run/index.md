---
title: Waking the computer to allow AppleScript to run.
date: 2016-04-09 14:52:56
aliases: ['/2016/04/09/Waking-the-computer-to-allow-AppleScript-to-run/']
tags:
- osx
- mac
- programming
- applescript
categories:
- programming
---
I have a number of AppleScript applications that need to run at odd times. These maintenance tasks often attempt to run while the computer is sleeping. Particularly those that rely on UI scripting do not function during this period.

This most flexible way of dealing with this is to manipulate the power management settings directly via the [pmset(1)](https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man1/pmset.1.html) command.

The variety of options available using `pmset` is staggering and beyond the scope of this post. Here's what I do to wake the computer up at specific times so that scheduled AppleScripts can run:

{{< highlight bash >}}
~|⇒ sudo pmset repeat wakeorpoweron MTWRFSU 12:29:00
~|⇒ sudo pmset repeat wakeorpoweron MTWRFSU 23:49:00
{{< /highlight >}}

Now my 12:30 PM and 11:50 PM scripts will run just fine.

_Edit 2016-04-18: Actually my scripts don't run just fine because `pmset` does allow setting of multiple wakeorpoweron events like this. Only the last one set is retained. However, you can use the root's crontab to do that as long as you schedule the cron event to deliver the pmset schedule before it's needed. Here's the idea:_

{{< highlight bash >}}
@reboot pmset repeat wakeorpoweron MTWRFSU 23:49:00
00 12 * * * * pmset repeat wakeorpoweron MTWRFSU 12:01:00
02 12 * * * * pmset repeat wakeorpoweron MTWRFSU 23:49:00
{{< /highlight >}}
