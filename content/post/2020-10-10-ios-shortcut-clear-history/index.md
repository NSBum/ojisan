---
title: "iOS shortcut to clear Safari"
date: 2020-10-10T04:34:33-04:00
images:
- /images/2020/10/10/shortcut_01.jpg
description: Sanitizing mobile Safari using iOS shortcuts.
draft: false
authorbox: false
sidebar: true
tags:
- privacy
- security
categories:
- ios
---
_(N.B. The next installment in my obsessional interest in thwarting surveillance capitalism. Read Shoshana Zuboff's seminal work on the subject and you'll see._)

### Justification

Last week I [outlined](/2020/10/04/my-macos-and-ios-security-setup-update-2020/) my evolving comprehensive approach to thwarting surveillance capitalism - that is the extraction, repurposing and selling of online behavioural surplus for the purposes of altering future behaviour. 

This is a simple iOS shortcut to the embedded Safari setting for clearing Safari history and website data. It turns out that when iOS Safari is presented with a URL in a certain format, it will execute preference settings on the device. After a little trial and error, I noted that the setting _Settings → Safari → Clear History and Website Data_ has its own URL:  `prefs:root=SAFARI&path=prefs:root=SAFARI&path=CLEAR_HISTORY_AND_DATA`. By loading that URL through an iOS Shortcut, you can quickly sanitize iOS Safari.

In short, the justification for this Shortcut is simply to make it easier to clear mobile Safari's cookies and cached web data to minimize tracking. If you're curious about why tracking is so creepy, consider this: how often have you seen ads in Instagram for things you've browsed on Amazon? Now, imagine it's not ads but content related to a particular political persuasion. Now it's possible to turn the dial on political beliefs by amplifying slight tendencies. How? Because surveillance capitalists have a surplus of behavioural data at their disposal and an excess of capital to put it to use.

### Installing the iOS "Clear Safari" Shortcut

![](/images/2020/10/10/shortcut_01.jpg)

It looks more difficult than it actually is.

1. Launch the Shortcuts application on your iPhone. (This all applies to iPad, too; but I'm just going to write _"iPhone."_)
2. Tap + in the top navigation bar.
3. Tap "+ Add Action" → Web → URL
4. Type _exactly_ the following for the _URL_: `prefs:root=SAFARI&path=CLEAR_HISTORY_AND_DATA` 
5. Tap "+ Add Action" → "Apps" on the next view → "Safari"
6. Choose "Open URLs"
7. Give the Shortcut a name and tap the three dots near the top of the screen to give it an icon for installation on the home screen.

When you're done building the Shortcut, it should look something like this on the home screen:

![](/images/2020/10/10/homescreen.jpg)

### References

- [Comprehensive list of settings links](https://www.macstories.net/ios/a-comprehensive-guide-to-all-120-settings-urls-supported-by-ios-and-ipados-13-1/) - This list on MacStories is current as of iOS 13. I have only verified a handful on iOS 14; but haven't found a similar list for iOS 14. 
- [My anti-surveillance practices](/2020/10/04/my-macos-and-ios-security-setup-update-2020/)
- [How to Destroy Surveillance Capitalism (Cory Doctorow)](/attachments/2020/10/10/destroy_surveillance.pdf) - Cory Doctorow's book on the subject, captured from Medium. 