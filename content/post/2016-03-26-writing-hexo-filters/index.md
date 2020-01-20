---
title: Writing Hexo filters
date: 2016-03-26 06:23:14
aliases: ['/2016/03/26/Writing-Hexo-filters/']
tags:
- hexo
- javascript
- programming
categories:
- programming
---
[Hexo](https://hexo.io/), the static blogging system that I use is very extensible and provides numerous hooks into generation pipeline.

While working on a Russian language blog that's coming online soon, I had the opportunity to write a filter to render Cyrillic text in a different font than the rest of the body text.

{{< figure src="images/blogpost.jpg" title="Markup filter use case" >}}

I wanted to set the Cyrillic text apart both in color, typeface, and font weight. Although I could have extended Hexo using a new tag, I decided to use a filter so that after rendering HTML anywhere on the blog, items demarcated by double pipes `||` would be replaced by a new `<span>`.

I used an [npm](https://www.npmjs.com/package/hexo-filter-russify) module to deploy the filter. You can find it on the [npm](https://www.npmjs.com/package/hexo-filter-russify) and at its [GitHub repo](https://github.com/NSBum/hexo-filter-russify)

Here's the very short code for the filter itself:

{{< highlight javascript >}}
hexo.extend.filter.register('after_render:html', function(str,data) {
    var re = /(\|{2}?)((.|\n)+?)(\|{2}?)/gm;
    var result = str.replace(re,'<span class="rsb">$2</span>');
    return result;
});
{{< /highlight >}}

The regex in the second line just identifies a block of text fenced by double pipes and replaces it with a span with the class that specifies the styling to be applied. In the future, I'd like to identify Cyrillic text with a regex and not have to use a fence at all.                               
