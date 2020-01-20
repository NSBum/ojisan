---
title: Fixing object caching headers in S3 buckets
date: 2016-03-17 04:55:33
aliases: ['/2016/03/22/Fine-tuning-caching-for-S3-hosted-static-blogs-using-AWS-CLI/']
draft: true
tags:
- programming
- blog
- blogging
categories:
- programming
---
This blog is served from an Amazon S3 bucket, a practice that has worked well for several years. With static blogs such as this, object caching is an important consideration. Since the blog is generated on the writer's client side then synced to the server rather than being generated dynamically on request, the browser caching practices are a consideration. I have a few comments about how I've dealt with caching for this blog. This isn't meant to be a definitive piece on caching.

Most importantly, I'd like images cached where possible so that I impose less demands on the server. But for the main `index.html` page, I don't want it to cache for very long at all because I may be updating it daily to a few times a day.

Since I use [grunt](http://gruntjs.com) to automate some of the blogging tasks as I've [written about]() before,
