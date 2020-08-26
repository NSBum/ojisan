---
title: Stop Facebook tracking
date: 2016-01-25 06:37:50
aliases: ['/2016/01/25/Stop-Facebook-tracking/']
authorbox: false
tags:
- technology
- culture
categories:
- technology
---
{{< figure src="/images/2016/01/25/web.jpg" alt="network" >}}

Although I understand Facebook's business model and I (basically) understand how money is made on the internet, I have no compunction about blocking ads, trackers, beacons and all manner of scripts. The current system creates layers upon layers of networks that exist to track one's activities on the internet and market products and services more specifically. The problem is that unless I take specific action, I don't get to choose what I reveal to companies that want to track me. Some have argued that using services like Facebook constitutes an implied contract between you - the user, and the internet application provider. It's a ridiculous argument because I could make a similar argument that my use of their service implies a contract not to track.

Here's how I block tracking. Some is specific to Mac OS X and Safari and some is general.

### Register your advertising preference

The Digital Advertising Alliance allows you register your advertising preference with participating companies and ad networks. After turning off any ad blockers and after setting your browser preferences to accept third-party cookies, visit [their page](http://youradchoices.com/choices) and opt our of all participating companies. When I ran it on my computer, it blocked 123 companies from behavioural tracking.

### Use Ghostery

{{< figure src="/images/2016/01/25/trackers.png" caption="Ghostery blocks trackers" class="left" >}}

The browser extension Ghostery works with a number of different browers to block scripts that provide information about your browsing to third parties (and fourth, fifth, and sixth...) For example, I visited the theverge.com, a technology-oriented site ahd Ghostery reported at 11 trackers, beacons, and widgets. Mind you, perhaps the previous step of registering with the Digital Advertising Alliance is sufficient to block many of these scripts. But since participation by the companies is voluntary, I would prefer to block them on my end also. Ghostery is very easy to use and has the ability to whitelist a site that you trust and to pause blocking as some sites have scripts that are essential to their functionality.

### Browser privacy settings

Check your privacy settings in your browser. For Safari, it's _Safari_ > _Preferences..._. Make sure that you set the _Cookies and website data_ to "Allow from current website only." And check the feature to block website tracking.

For Chrome, it's _Chrome_ > _Preferences_. Search for "cookies" in the settings search field. I set my cookies preferences to "Keep local data only until you quit your browser" and "Block third-party cookies and site data."

### Close Facebook when you're done

When you're done with your session on Facebook, logout (FB menu far right) and close its window or tab.

### Clear Facebook cookies

After I've finished using Facebook, I clear any cookies that it has set on my computer. You can do this manually:

- __Safari__: _Safari_ > _Preferences..._ > Cookies and website data > Details... Search for facebook.com and delete its cookies.

- __Chrome__: _Chrome_ > _Preferences..._. Search the settings for cookies and clear browsing data. I cannot find a function that allows you to delete cookies in a more granular way.

On Mac, I use a script that I borrowed and modified from [Dr. Drang](http://www.leancrew.com/all-this/2013/03/deleting-safari-cookies-via-applescript/) that automates the deletion of specific cookies in Safari. I set it up to run using a key combination that I press whenever I close down Facebook. Here's the script, if you're interested:

{{< highlight applescript >}}
set deCookie to {"facebook.com"}

tell application "Safari" to activate

tell application "System Events"
   tell process "Safari"
      keystroke "," using command down
      delay 1
      tell window 1
         click button "Privacy" of toolbar 1
         delay 3
         repeat with d in deCookie
            click button "Details…" of group 1 of group 1
            try
               keystroke d
               delay 1
               select row 1 of table 1 of scroll area 1 of sheet 1
               click button "Remove" of sheet 1
            end try
            click button "Done" of sheet 1
         end repeat
      end tell
      keystroke "w" using command down
   end tell
end tell
{{< /highlight >}}

### Use an ad blocker

[Download](https://adblockplus.org/) Ad Block Plus to block advertisements on web pages. It's spectacular how many ads that it blocks. I don't know that it stops tracking completely; but the aesthetic result of blocking ads is spectacular. Again, I don't regard this as an ethical issue in the least. Services that I use regularly that wish to charge me money are free to do so. If I see value in the service I'll use it. Monetizing the use of a site by tracking one's users and selling the information to other parties is hardly a way to build trust.

### See also

- [Business Week: How to Stop Facebook from Tracking You](http://www.businessinsider.com/heres-how-to-stop-facebook-from-tracking-you-2012-9?op=1) - has some information about other browsers and techniques to use.^[Interestingly, Business Week itself runs 15 trackers, beacons and other suspicious scripts on its site...]
- [iMore: How to Stop Facebook from Constantly Tracking and Recording Your Location](www.imore.com/how-stop-facebook-constantly-tracking-yo…) - this article is more specific to iOS; but very useful.^[Again, another site that condemns tracking but itself runs 14 trackers...]
