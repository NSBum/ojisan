---
layout: post
title: "Synchonizing DEVONthink databases across machines"
date: 2015-04-04 06:51:52 -0500
aliases: ['/2015/04/04/synchonizing-devonthink-databases-across-machines/']
categories:
- organization
tags:
- devonthink
- synchronization
---
### This is how I do it. YMMV.

I've used [DEVONthink](http://www.devontechnologies.com/products/devonthink/overview.html) since its early days. If you're unfamiliar with DEVONthink, it's a knowledge management tool that allows you to save information, tag it, cross-reference it and classify it. Since I use both a laptop and a desktop Mac Pro, I need to synchronize databases across machines. There are several ways to go about synchronization:

- __Direct connection__  This is not a bad option when both machines are turned on simultaneously and are connected to the same network.
- __Dropbox__ Obviously, you need a Dropbox account for this. Since databases can grow quite large, you may need a paid Dropbox account for it. I don't like having my personal information in the cloud; so I don't use this option.
- __WebDAV__ I don't run a WebDAV server, so that was out.
- __Local sync store__ This was the best option for me, since I use [BitTorrent Sync](https://www.getsync.com) to synchronize certain content between machines using peer-to-peer connections.

Here's how I do it.

1. __First and foremost, you need to have an identical copy of the database in the local filesystem of both machines that you are synchronizing.__ On the source machine, I copy the database to the directory that I'm synchronizing via BitTorrent Sync (BTS). _(Note that I don't use BTS as a vector for directly synchronizing databases between machines. I don't trust that it could faithfully synchronize the interal package structure.)_
2. Allow BTS to fully synchronize between machines.
3. On the destimation machine, copy the DEVONthink database from the directory that BTS is synchronizing to the directory where you want to store your databases. _(Again, note that I don't actually use BTS to sync the database itself. Right now, we're just using it to transfer an identical copy of the database from the source to destination machine. You could just as easily use a USB stick for this step.)_
4. Delete the database from the BTS-synced folder. Remember that it was just there to copy to the destination machine.
5. On the source machine, set up a local sync store: _DEVONthink Pro Office > Preferences > Sync_
{{< figure src="images/dtpo-sync-001.png" title="DEVONthink Pro Office synchronization" >}}
6. Select your database and choose _+_ > _Add new local sync..._. Choose a location in the __directory that BTS is syncronizing__.
7. Press _Sync Now_ to synchronize.
8. Now, on the destination machine, go to the sync preferences: _DEVONthink Pro Office > Preferences > Sync_.
9. Choose your database.
10. In the third column of the view, choose _+ > Add Existing Local Sync Store..._ and choose the sync store that you created on the source machine.
11. Setup synchronization schedules on both the source and destination machines.

The original idea for using this method came from [this post](http://basilsalad.com/how-to/devonthink-intranet-wiki/) and I modified it to use BitTorrent Sync.

Some other favorite posts about DEVONthink:

- [Organizing Your Research with DEVONthink Pro Office](http://at.blogs.wm.edu/organizing-your-research-with-devonthink-pro-office/) from [Academic Technology](http://at.blogs.wm.edu/) at the College of William and Mary
- [FAQs on DEVONthink](https://idlethink.wordpress.com/category/devonthink/)
