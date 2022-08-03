---
title: "Getting plain text into Anki: a saga"
date: 2019-12-13T03:59:55-05:00
draft: false
sidebar: true
authorbox: false
summary: "In Anki 2.1, it's practically impossible to get plain text from the web into note fields. A solution (on macOS, at least)..."
categories:
- Anki
tags:
- programming
- applescript
---

I've used Anki for many years as a core piece of my language learning. I love it.

With the version 2.1 upgrade, I've had to spend more and more time finding ways to work around its quirks. The following issue is particularly thorny and support inquiries have been met with a version of "that's just the way it is."

My issue is in how Anki 2.1 decides whether you want HTML or plain text in the receiving field when cut-and-pasting from a website. Let's say I want to snag part of the English definition from the [Wikitionary article](https://en.wiktionary.org/wiki/%D1%82%D0%B0%D0%B8%D1%82%D1%8C%D1%81%D1%8F#Russian) for the Russian word {{<russian>}}таи́ться{{</russian>}}. So I highlight "to conceal/hide one's feelings (from)" on the page, ⌘-C to copy. In Anki, ⌘V to paste. Visually, it looks fine in the editor window, other than the unwanted italic text:

{{<figure src="/images/2019/12/13/img1.png" >}}

so let's take a look at the HTML (⇧⌘X):


{{<figure src="/images/2019/12/13/img2.png" >}}

It's a mess. All I want is the **plain text**. Where do all of the `&nbsp;` elements come from? It must have been on the original page. So let's look at the source:

{{< highlight html >}}
<li>to <a href="/wiki/conceal" title="conceal">conceal</a>/<a href="/wiki/hide" title="hide">hide</a> <a href="/wiki/one" title="one">one</a>'s <a href="/wiki/feeling" title="feeling">feelings</a> <i>(from)</i>
{{< /highlight >}}

Meh, there's a lot markup but no &nbsp; Either Anki or macOS is adding these unwanted non-breaking spaces. Since I've never seen that behaviour anywhere but Anki, I'm blaming Anki. The problems I have with this are both philosophical and practical.

- Since Anki provides extensive capabilities to format your cards, why force users to accept Anki's space to non-breaking space conventions? If you want something to align in a certain way, do it yourself. Why assume that every user wants it that way.
- The practical issue is that the non-breaking spaces force words to break in strange ways at certain window widths.

Desperate for a solution (short of coding a full Anki Add-on) here's what I came up. I assume that Anki is looking to see if there's some HTML on the clipboard. If there is, it changes all the spaces to &nbsp; elements. So, what if I just scrapped the HTML from the clipboard before it gets to Anki? AppleScript to the rescue.

{{< highlight applescript >}}
use AppleScript version "2.4" -- Yosemite (10.10) or later
use scripting additions

property paste : 9

delay 0.25
tell application "Anki"
   activate
   delay 0.25
   my pasteWithDelay(the clipboard)
end tell

on pasteWithDelay(someText)
   set the clipboard to {text:(someText as string), Unicode text:someText}
   tell application "System Events"
      key code paste using command down
      delay 0.25
   end tell
end pasteWithDelay
{{< /highlight >}}

Now the remaining problem is how to launch the script easily. Here, I just added a [Quicksilver](https://qsapp.com/) trigger. So the key combination ⇧⌘W now takes the clipboard, turns it into plain text and uses UI automation to paste it into the field that currently has the focus. It works, but I'm left with the feeling that I'm missing a better way...

_EDIT 2022-06-02_: I've since come up with a variation on this approach which I've written about in [Getting plaintext into Anki fields on macOS: An update](/2022/06/02/getting-plaintext-into-anki-fields-on-macos-an-update/).
