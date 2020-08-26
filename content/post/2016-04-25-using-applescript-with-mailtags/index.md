---
title: Using AppleScript with MailTags
date: 2016-04-25 19:27:15
aliases: ['/2016/04/25/Using-AppleScript-with-MailTags/']
authorbox: false
tags:
- applescript
- mailtags
- tools
categories:
- programming
---
I'm a fan of using metadata to classify and file things rather than declarative systems of nested folders. Most of the documents and data that I store for personal use are in [DEVONthink](http://www.devontechnologies.com/products/devonthink/overview.html) which has robust support for metadata. On the email side, there's [MailTags](https://smallcubed.com) which lets you apply metadata to emails. Since MailTags also supports AppleScript, I began to wonder whether it might be possible to script workflows around email processing. Indeed it is, once you discover the trick of what dictionary to use.

The key is to use `MailTagsHelper` for the dictionary. To access the terms from that dictionary, you need to embed the code in the following block:

{{< highlight applescript >}}
using terms from application "MailTagsHelper"
    -- access MailTags properties here
end using terms from
{{< /highlight >}}

<!-- more -->

Here's a little script that fulfills a workflow need of mine. I try to assign incoming emails to projects and/or give them keywords right away either manually or via Mail rules. After being tagged I want them out of my Inbox and into a reference folder. This script moves any tagged message or one with a project assigned into the Reference folder after 2 days. You'll have to modify it to meet your needs and insert your account information.

{{< highlight applescript >}}
--  FileTaggedMessages

--  how long should message be allowed to remain
--  in the Inbox before being filed
property inboxDays : 2
set inboxSeconds to inboxDays * 86400

tell application "Mail"
    set msgs to every message in the inbox
    set referenceMailbox to mailbox "Reference" of account "duncan.alan@me.com"
    repeat with msg in msgs
        -- access the MailTags properties
        using terms from application "MailTagsHelper"
            set t to keywords of msg
            set tagCount to count of t
            set p to (project of msg)
        end using terms from
        if tagCount is not 0 or p is not missing value then
            -- found a message with keywords or a property
            set sentDate to date received of msg
            set thisDate to current date
            set delta to thisDate - sentDate
            if delta ≥ inboxSeconds then
                move msg to referenceMailbox
            end if
        end if
    end repeat
end tell
{{< /highlight >}}
