---
title: "Dynamic DNS - auto-updating from macOS"
date: 2021-05-06T11:02:22-04:00
draft: false
authorbox: false
sidebar: false
tags:
- macos
- tutorial
categories:
- programming
---
To run a little project (that I'll describe at some point in the future) I have to run a small web server from my home computer, one that happens to run macOS. More than anything else, this is just a reply of what I did to get it running in case: a) I have to do it again, or b) Someone else can find it useful.

### Sign up for dynamic DNS service

I signed up for service with [dynv6](https://dynv6.com) because I saw it recommended elsewhere and it didn't look creepy like some of the other options. I just signed up with email - through an email proxy anonymizer, because I'm paranoid. After verifying my email, I was able to create a new "zone", basically a record of my public IP address linked to custom DNS.

### Updating the IP address.

Most of us don't have static public IP addresses, so some mechanism is required to keep the custom DNS and your public IP address linked.

I used the `ddclient` tool [Github](https://github.com/ddclient/ddclient) to keep my dynamic DNS up-to-date. The Homebrew install works well:

{{< highlight bash >}}
brew install ddclient
{{< /highlight >}}

Now we need to configure the ddclient tool with a `ddclient.conf` file. This is a little struggle because the syntax offered when you create a zone on dynv6 is not correct. Here is the syntax that works:

{{< highlight bash >}}
# ddclient configuration for dyndns
#
# /usr/local/etc/ddclient/ddclient.conf
syslog=yes
ssl=yes
use=web, web=checkip.dyndns.com/, web-skip='Current IP Address'
server=dynv6.com
protocol=dyndns2
login=none
password='YOUR PASSWORD'
YOUR_ZONE
{{< /highlight >}}

`YOUR_PASSWORD` is the password key that you obtain from dynv6. `YOUR_ZONE` is the full zone name.

To check that the updater is working:

{{< highlight bash >}}
sudo /usr/local/opt/ddclient/sbin/ddclient -verbose -noquiet
{{< /highlight >}}

If that succeeds, then you can set it up on a schedule:

{{< highlight bash >}}
sudo cp -fv /usr/local/opt/ddclient/*.plist /Library/LaunchDaemons
sudo chown root /Library/LaunchDaemons/homebrew.mxcl.ddclient.plist

sudo launchctl load /Library/LaunchDaemons/homebrew.mxcl.ddclient.plist
{{< /highlight >}}
