---
title: "What's up with Pinboard? And an alternative"
date: 2022-05-03T07:41:32-04:00
draft: false
authorbox: false
sidebar: false
tags:
- web
- programming
categories:
- web
---
Beginning somewhere around April 2022, the bookmarking web application Pinboard began to suffer prolonged outages without really any substantive commentary from the developer. [Reports](https://news.ycombinator.com/item?id=31183419) on Hacker News reveal a pattern of frequently-broken functionality. As of this writing, the API is no longer functioning.

One of the great things about the HN community is that you can almost always find an open-source tool to get the job done. That's how I discovered [Espial](https://github.com/jonschoning/espial). It's a minimalist open-source self-hosted bookmarking tool that looks and works like Pinboard. It also imports the Pinboard export JSON format.

Espial installed readily for me on macOS and seems very usable. My advice is to export your Pinboard bookmarks while you can and spin-up an instance of Espial.