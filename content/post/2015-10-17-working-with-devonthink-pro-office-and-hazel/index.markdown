---
title: "Working with DEVONthink Pro Office and Hazel"
date: 2015-10-17 03:33:30 -0700
aliases: ['/2015/10/17/working-with-devonthink-pro-office-and-hazel/']
categories:
- organization
tags:
- devonthink
- organization
- Mac OS
- Hazel
- applescript
---
My main organizational tool [DEVONthink Pro Office](http://www.devontechnologies.com/products/devonthink/devonthink-pro-office.html), a tool I've used for many years. I've [written previously](/blog/categories/devonthink) about it and how I use it [to find things](/blog/2015/06/18/finding-things-with-devonthink/) and how I [synchronize databases](/blog/2015/04/04/synchonizing-devonthink-databases-across-machines/) across machines.

I'm a relative newcomer to [Hazel](https://www.noodlesoft.com/hazel.php) though. Hazel's tagline is "automated organization for your Mac." Hazel works as an agent to keep folders organized on the Mac. It's an engine that applies per-folder rules to take actions on files and folders. Actions can include tagging files, moving them to other folders, running AppleScripts, deleting them, etc.

Since DEVONthink is the centerpiece of my organizational tools on the Mac, I wondered if Hazel and DEVONthink might be able to work together in a productive way. It's an experiment that turned out well. I'll describe two cases where I'm using them together. Read more after the break.

<!-- more -->

### Using Hazel to clear the DEVONthink global inbox.

Because the global inbox in DEVONthink doesn't synchronize across machines, I keep a separate database for my collection point. That way, I can keep sorting items collected on my desktop computer at home while I'm on the road with my laptop. Hazel can help us by watching the Inbox and running an AppleScript that moves items from the Inbox to a database of my choice. First, the AppleScript:

{{< highlight applescript >}}
-- move global inbox items to collection inbox

tell application id "com.devon-technologies.thinkpro2"
	set inboxItems to every record of the inbox
	repeat with inboxItem in inboxItems
		repeat 1 times
			if the name of inboxItem is "Tags" then exit repeat
			if the name of inboxItem is "Trash" then exit repeat
			set collectionDb to database "Collection inbox"
			set cib to get record at "/Inbox" in collectionDb
			move record inboxItem to cib
		end repeat
	end repeat
end tell
{{< /highlight >}}

{{< figure src="images/hazel_clear_inbox.png" title="Hazel rule to clear inbox" >}}

The script iterates over all of the records in the Inbox, skipping items that shouldn't be copied (Tags and Trash) then moves them to the inbox in my database called "Collection inbox".

To have the script run, we have to create a Hazel rule to make it happen. The trick is to find the right folder to watch. The path that you want is `~/Library/Application Support/DEVONthink Pro 2/Inbox.dtBase2/Files.noindex` Once you've drilled down to the correct directory for Hazel to watch, create the as shown in the figure. The trick here is to make sure that Hazel traverses the directory hierarchy inside `Files.noindex`. We do this by setting the rule criterion of `Kind is Folder`. With that criterion, Hazel will watch all of the folders beneath `Files.noindex` and trigger the embedded AppleScript on demand.

### Using Hazel to save images to DEVONthink

I collect a lot of images for projects that I work on. In fact, I squirrel away so many images that I keep a separate database for them. When need for a particular project, I can move images to the proper database. But having a DEVONthink database for the images, insures that I have a centralized collection point so that I don't have to look all over my file system for images.

For this task, I have a pair of Hazel rules that work in tandem. The first is simple and I'll describe only cursorily. It works like this: any image that gets downloaded onto the Desktop or to Downloads, gets slurped up to a Desktop folder called "images". That's it.

The second task is to get the images into DEVONthink. In particular, I want the images to go to the `images` database in DEVONthink. Like the first example above, we use Hazel to execute an AppleScript when its criteria are met. In this case, the script is quite simple:

{{< highlight applescript >}}
tell application id "com.devon-technologies.thinkpro2"
	set img_ib to get record at "/Inbox" in database "Images"
	import theFile to img_ib
end tell
{{< /highlight >}}

{{< figure src="images/hazel_move_images.png" title="Hazel rule to move images" >}}

Note that `theFile` is provided by Hazel so we have a file object to work with in the AppleScript. One of the items that I had to tweak a bit was to make sure that images didn't not get slurped up too quickly into DEVONthink. If I am downloading an image to use in a presentation, I want the image readily available in the file system long enough to use it on a slide. After that, Hazel is free to send it over to DEVONthink. To do that, I set the criterion to `Date Added is not in the last 15 minutes`. This gives me long enough to work actively with the image before it is archived in DEVONthink.

These use cases barely touch on the capability of automating your workflow with the pairing of DEVONthink Pro Office and Hazel. Much of the heavy lifting comes from the deep accessibility to DEVONthink internals through AppleScript. What use cases have you found for Hazel and DEVONthink?
