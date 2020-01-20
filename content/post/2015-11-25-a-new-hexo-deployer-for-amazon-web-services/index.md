---
title: A new hexo deployer for Amazon web services
date: 2015-11-25 05:06:26
aliases: ['/2015/11/25/A-new-hexo-deployer-for-Amazon-web-services/']
tags:
- programming
- blogging
categories:
- programming
---
I recently migrated this and [my other blog](htttp://www.suzukiexperience.com) to [Hexo](https://hexo.io/) which is a very fast static blogging framework built on node.js. As when I used Octopress, this blog is still hosted from an AWS S3 bucket. However the deployers that I tried with Hexo failed because of dependencies that were incompatible with the OS X version I was running. Not being a node.js expert, and having no time to delve into node.js internals, I wrote a new deployer:

[hexo-deployer-awstransmit](https://www.npmjs.com/package/hexo-deployer-awstransmit)

It relies on [Transmit](https://panic.com/transmit/) to upload the `public` directory of a Hexo baked blog to the S3 bucket that hosts the site. You can find it [on npm](https://www.npmjs.com/package/hexo-deployer-awstransmit) and [Github](https://github.com/NSBum/hexo-deployer-awstransmit).
