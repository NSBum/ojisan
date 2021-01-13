---
title: "My macOS and iOS security setup - Update 2020"
date: 2020-10-04T06:55:51-04:00
draft: false
authorbox: false
sidebar: false
tags:
- privacy
- security
categories:
- macos
---
_(N.B. I am not a security expert. I've implemented a handful of reasonable measures to prevent cross-site tracking and limit data collection about my preferences and actions online.)_

[Surveillance capitalism](https://en.wikipedia.org/wiki/Surveillance_capitalism) is a [real and destructive force](https://www.thesocialdilemma.com/) in contemporary economics, politics and culture. Whatever utopian visions that Silicon Valley may have had about the transformative power of ubiquitous network technologies have been overwhelmed by the pernicious and opaque forces that profit from amplifying divisions between people. While I can't change the system, I can change _my own_ practices and reduce the degree to which surveillance capitalists, state actors and others who have no rights to my data.

### macOS privacy practices

First the easy parts:

#### Browser choice

I do not use **Chrome** unless forced to do so because I do not trust what Google does with my information. Although I use **Safari** as my usual browser, I'm wary of Apple too. If you are going to use Safari on macOS, I highly recommend applying the macOS 10.15.6 update which includes Safari 14.0 as of October 4, 2020. This version of Safari blocks cross-site tracking by default. For some secure transactions, I use the [Tor](https://www.torproject.org/) browser which connects to a convoluted network whose purpose is to deliberately conceal the originator of the request. However, many sites break when using Tor. 

#### General browsing practices

Regardless of your choice of browser, the following browser practices are recommended:

- Logout of any sites you've logged into, close its tab and either clear the _specific_ cookies set by that site or all cookies, whichever is easier.
- Review your privacy settings in all social media services that you use. It isn't much; but it's something.
- Set your browser search engines to DuckDuckGo. In macOS Safari, that's done at **Safari → File → Preferences... → Search engine → "DuckDuckGo"** On the iOS side, it's **Settings → Safari → Search Engine → "DuckDuckGo"**. 

#### Safari browsing practices

Safari has the ability to block cross-site tracking if enabled. So enable it: **Safari → Preferences → Privacy** and select "Prevent cross-site tracking". 

![](/images/2020/10/04/safari_privacy.png)

By default I use private windows in Safari (or any other browser, if the feature is available.) In Safari, that's **Safari → File → New Private Window**. In private windows, the history and any cookies are not stored when the window or tab is closed. For extra security, if I've used any service that requires a login, I logout of the service, and close the private window. If I use any kind of social media or commercial site, I clear all cookies after closing out the tab or window. To clear cookies, go to **Safari → Preferences → Privacy** and select "Manage Website Data..." 

![](/images/2020/10/04/safari_cookies.png)

If you want to remove everything (recommended) then click "Remove All". Otherwise, you can search for and remove any specific cookies. I've automated the process using AppleScript, so that I can just select "Clear cookies" from the menu bar script menu. I've written about [how to do this](/2018/10/19/deleting-cookies-with-applescript/) ap few years ago.

I also try to do one thing at a time and "sanitize" my browser before using services that are riskier for tracking. 

In summary, I use private windows, login and logout of services and regularly clear cookies from Safari.

#### Ad blocking
r
I block ads. Some people turn themselves into human pretzels obsessing about "good ads" and "bad ads." They wonder about the ethics of blocking ads and how it disrupts the very foundations of the internet. 

**I don't care.** 

I didn't ask Google and Facebook and the rest to monetize themselves using advertising. They've chosen to go all-in with surveillance capitalism without my consent; so I blocks ads without their consent. I manage several sites and I've never used advertising.

How to block ads? I use the AdBlock for Safari extension. To install, go to the **Mac App Store → search AdBlock → Install → Open**. 

#### Email practices

Email is a another frequent vector for surveillance and for phishing attacks. My first line of defense is to avoid giving out my email address to anyone that I don't want to hear from.

##### Don't give away your information

 Every single time I go in certain stores, the clerk asks for email and/or my cell phone number. **Never give it to them.** Sometimes they up the ante by telling you that you can't access discounted prices today unless you give them your data. Tough luck, you're not getting it. Sometimes, of course, you're forced to give out an email address for some online transaction. For that, I have a throw-away email address that I never look at. It's some cruddy yahoo.com email address that is probably brimming with garbage right now. But I don't care. It goes without saying to never sign up for newsletters. If I can't get your content on-demand at your site, then too bad for you. Surely you, a user, can remember or prompt yourself periodically to look for the content. Or better yet, use their RSS feed.

##### Aggressive spam filtering

So the first line of defense is to simply be suspicious of anyone who wants your email address. The second line of defense is to be very aggressive about spam. On the macOS side, I use the amazing [Spam Sieve](https://c-command.com/spamsieve/), a Bayesian spam filtering extension for macOS mail. It scans incoming emails and filters those that are considered spam by assigning it a probability based on source and content features. What makes it particularly effective is that it learns over time as you train it. I've used it for over a decade;so my rulesets are very accurate and robust. 

##### Avoid email pixel tracking

You may not be aware that images and other small files in email messages are used to track individual users. So I block remote content unless I absolutely need to see it. To do that, go to **Mail → Preferences → Viewing → Load remote content in messages → uncheck**. To learn more about pixel trackers in email, I recommend an article originally published in Fast Company ([PDF capture](/attachments/2020/10/04/pixel_trackers.pdf)).

![](/images/2020/10/04/mail_preferences.png)

* * *

### macOS traffic blocking

The last component of my protection on the macOS side is to selectively block traffic to and from entities that I know are adverse to my privacy or that I don't recognize. This is not simple to implement; but worthwhile learning about. I use [Little Snitch 4](https://www.obdev.at/products/littlesnitch/index.html). This application runs on macOS and sits on top of the networking layer of the OS to intercept traffic in and out of your computer. It allows you to implement rules that govern how it handles traffic. You can also setup profiles that allow you to apply the rules in specific circumstances. For example, I'm an administrator of a group on Facebook; so I need to access it periodically. But I don't want Facebook spying on me when I'm not using it. Removing Facebook cookies helps; but but many sites contain code that attempts to transmit information back to Facebook. Browser fingerprinting can make it possible for Facebook to continue to track you even when logged out via these means.


### iOS privacy practices

Starting with basic principles, I don't use mobile applications for social networking. Period. Until recently, I had been using Instagram; but since Instagram is just another arm of Facebook, I can't support having it on my phone any longer. So, gone. I also don't use Twitter or Facebook on my phone.

So how to block trackers, beacons, social pingers of various sorts? I block these on my phone by routing my traffic through a proxy server on my Mac at home. Outside of home, I don't really bother surfing the web; so I'm mostly protected.

#### iOS connection through proxy server


{{< figure src="/images/2020/10/04/squidman.png" caption="SquidMan macOS proxy server" class="left" >}}

By direct internet traffic through a proxy server running on a Mac, you can use Little Snitch to regulate traffic on the phone in the same manner as with traffic directly to and from the Mac itself. For this, I use [SquidMan](https://squidman.net/squidman/) which is a GUI front-end for the Squid proxy cache. On the Mac side, it's just a matter of downloading and installing SquidMan, then noting the IP address of this new proxy server (the LAN address of your Mac) and its port (8080 by default). This sort of proxy server arrangement is a lot easier if you can reserve an IP address for at least the server, if not both the server and the client.

After installing SquidMan, you can consult [this tutorial](https://howchoo.com/mac/how-to-set-up-a-proxy-server-on-mac) for the remaining setup instructions on the Mac side and [this tutorial on the iOS side](https://howchoo.com/iphone/how-to-configure-a-proxy-on-your-iphone).

Back in Little Snitch, if everything is working as intended, once my iPhone is connected through the proxy server, I should begin to see traffic under `squid`:

{{< figure src="/images/2020/10/04/little_snitch_squid.png" caption="Traffic from iPhone routed through squid" >}}

Now within **Little Snitch → `squid`** you can create allow/block rules for traffic passing through the proxy server.

#### Conclusion

I hope this article gives you ideas for actions you can take to reduce your exposure to surveillance capitalism. Utlimately this neo-feudal economic system must be dismantled through collective action. But ironically, and almost certainly by design, the surveillance capitalists are actively dividing the very bodies who would seek to regulate them. 

