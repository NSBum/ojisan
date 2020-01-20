---
title: 'EC: An Environment Canada data plugin for Indigo'
date: 2016-05-30 05:37:06
aliases: ['/2016/05/30/EC-An-Environment-Canada-data-plugin-for-Indigo/']
tags:
- home automation
- programming
categories:
- home automation
---
![Environment Canada](http://www.public-domain-photos.com/free-cliparts-1/flags/america/national_flag_of_canada_.png)

[Indigo](http://www.indigodomo.com) is a well-known home automation controller software package for Mac OS X. I've written a plugin for Indigo 6 that allows you to create a virtual weather station from Environment Canada data. If you live in Canada, this will be a useful way of using weather data in your Indigo rules. For example, you could use wind and temperature data to adjust your irrigation schedule.

You can download the plugin from its [git repo](https://github.com/NSBum/EC/tree/master). After downloading the files, you'll just need to configure them as a plugin. To do this, create a new folder and rename it _EC.indigoPlugin_. Copy the _Contents_ folder that you just downloaded. Right-click on the _EC.indigoPlugin_ bundle and _Show Package Contents_. Paste the _Contents_ folder here. To install in Indigo, double-click the bundle file.
