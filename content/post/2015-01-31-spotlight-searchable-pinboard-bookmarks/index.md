---
title: "Spotlight-searchable pinboard bookmarks"
date: 2015-01-31T05:58:48-06:00
draft: false
authorbox: false
sidebar: false
categories:
- programming
tags:
- pinboard
- macos
---
I use the excellent, dependable [Pinboard](https://pinboard.in/u:LachmanBhatia) service for managing my bookmarks. A one-time fee gives you lifetime access to the service; and there is an API that has fostered an ecosystem of desktop and mobile apps that interact with the service. Of course, Safari can synchronize bookmarks among devices; but it doesn't allow tagging. Since tagging is a major part of my workflow, Safari bookmarks don't work for me.

So, here's where pinboardspotlight.py comes in. It's a relatively simple Python program that downloads your Pinboard bookmarks, writing them to local `.webloc` files and applying the tags you've used in the Pinboard metadata to the local files. Now you're Pinboard bookmarks are searchable locally.

### Usage ###

To use pinboardspotlight.py, you'll first need to install the command line app `tag` [here](https://github.com/jdberry/tag). Then you can download pinboardspotlight.py from [my github repository](https://github.com/NSBum/pinboardspot).

Calling the script is just a matter of supplying at least the following arguments:

    - `-u, --user`		Your Pinboard user name
    - `-p, --password`	Your Pinboard password
    - `-w, --webloc`	The path on your filesystem where the webloc files will be stored

    Optionally, you can specify the path to the sqlite3 database that the script uses.

    `-d, --database`	The path on your filesystem where the sqlite3 database is stored



