---
title: Using AdBlock Plus to block YouTube comments
date: 2016-04-12 05:17:46
aliases: ['/2016/04/12/Using-AdBlock-Plus-to-block-YouTube-comments/']
tags:
- web
- privacy
categories:
- web
---
YouTube comments are some of the most offensive on the web. Even serious videos attract trolls bent on inscribing their offensiveness and cruelness on the web.

Here's one method of dealing with YouTube comments. Treat the comments block as an advertisement and block it.^[There are other ways of avoiding YouTube comments. I've used [ViewPure](http://viewpure.com) but it's hard to find content that way even though they seem to be working on making it more seamless to get from YouTube to ViewPure.]

### 1. Download AdBlock Plus

Download the [AdBlock Plus](https://adblockplus.org) extension for the browser you use and install it.

### 2. Create a custom ad filter

In this step you will create a filter that treats the entire comments section of a YouTube page as an advertisement.

- Navigate to YouTube and load any video page.
- Click on the AdBlock icon in the toolbar to bring up its contextual menu

{{< figure src="images/adblockmenu.png" title="AdBlock Plus contextual menu" >}}

- Choose "Block an ad on this page"
- Navigate to an area of the page just above the "COMMENTS" header where the ads are located. Once the entire ads area of the page is highlighted, click there.

{{< figure src="images/commentsdiv.jpg" title="Block YouTube comments" >}}

- AdBlock will ask you to confirm the block. If it looks right to you, agree.^[The `div` to be blocked is `<DIV id="watch-discussion" class="branded-page-box yt-card scrolldetect" >`. Don't be surprised if that changes and you need to update your filter as YouTube changes their page structure.]

If all goes well, you'll have comment-free YouTube pages now.
