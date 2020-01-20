---
title: "A Simple Styling Shortcode for Hugo"
date: 2019-09-15T05:15:29-04:00
draft: false
summary: "A Hugo shortcode used to style inline text in a post. I use it here to style Russian text in my posts."
categories:
- programming
tags:
- blog
- hugo
---
I've always had a preference for serif fonts when writing in Russian. Since some of my posts here are written in Russian I needed a quick way of marking up the formatting for the Russian portion of my post, as in [this post](/2019/09/13/russian-tk-constructions/). Just a simple shortcode specifying a CSS class:

{{< highlight html >}}
<span class="russian">{{ .Inner | markdownify }}</span>
{{< /highlight >}}

In action, applying the desired CSS for the `russian` class, we have:

{{< figure src="images/illustrate.png" title="Russian shortcode in action" >}}