---
title: Resetting the Syncthing index
date: 2018-04-01 14:51:37
tags:
- technology
- tools
- organization
categories:
- software
---
I use [Syncthing](https://syncthing.net/)^[No, there's no iOS client. I'm OK with that.] to keep my laptop, desktop, and workshop computers in sync.^[Why don't I just use Dropbox like everyone else? I trust peer-to-peer syncing because I'm in control. I don't know what Dropbox is up to.] At least 99.9% of the time it works perfectly. Rarely, it seems to choke because of some edge case that I've never been able to sort out. But it never recovers on its own. Instead, it continues to report that a remote is 99% done syncing.

The workaround that I've learned is to simply reset the index. When the index gets rebuilt everything automagically works. You can't do it via the GUI; you have to execute a REST call against the server. It took me a while to find it.

{{< highlight bash >}}
curl -X POST -H "X-API-Key: abc123" http://localhost:8384/rest/system/reset?folder=default
{{< /highlight >}}

If you want to erase the entire index, execute the call without the `folder` parameter. Otherwise, provide the name of the folder. The API key isn't `abc123`; it's actually found in Actions > Settings > API key. Before executing the call, I pause syncing on both sides, rebuild the index, then start it up and let them go at it.

### Reference

- [POST /rest/system/reset](https://docs.syncthing.net/rest/system-reset-post.html)
