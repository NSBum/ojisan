---
title: "No sir, I do not want Big Sur"
date: 2021-04-24T05:49:09-04:00
draft: false
authorbox: false
sidebar: false
tags:
- computer
- macOS
categories:
- macOS
---
Maybe I'm just getting cranky after over a year of on-again-off-again pandemic lockdowns, but I've had it with Apple's heavy-handed attempts to get me to upgrade to Big Sur. Mind you, I have nothing against it. It's just an operating system. I don't particularly like it's translucent bubbly iOS look. But I could live with.

But I don't want it. I depend on a very unorthodox setup. I have a lot of infrastructure tools that depend on certain versions of Python to be in just the right place. Every single macOS major upgrade breaks all of this and I spend days picking up the pieces. I'm tired of Apple messing with it. So when my system launched into what seems like an unbidden upgrade process today, I lost it.

I'm not exactly sure how the upgrade got triggered today. In my frustration I may have hit the wrong button or was otherwise too hasty. But what follows is the documentation of my quest to never face this again.

First, in System Preferences → Software Update, uncheck "Automatically keep my Mac up to date". I already had this checked; so digging deeper there is an "Advanced..." button to deal with. Uncheck everything in the Advanced pane.

Next up, Terminal. In Terminal (or my preference, iTerm)

{{< highlight bash >}}
softwareupdate --ignore "macOS Big Sur"
{{< /highlight >}}

which should report:

{{< highlight bash >}}
Ignored updates:
(
)

Software Update can only ignore updates that are eligible for installation.
If the label provided to ignore is not in the above list, it is not eligible
to be ignored.

Ignoring software updates is deprecated.
The ability to ignore individual updates will be removed in a future release of macOS.
{{< /highlight >}}

There is a nuclear option known as _bigsurblocker_ that apparently does what it says on the tin. I'm holding that one in reserve but it can be downloaded from [Github](https://github.com/hjuutilainen/bigsurblocker) if needed.
