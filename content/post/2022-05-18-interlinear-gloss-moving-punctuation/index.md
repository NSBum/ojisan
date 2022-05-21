---
title: "Interlinear glossing dealing with punctuation"
date: 2022-05-18T04:56:39-04:00
draft: false
authorbox: false
sidebar: false
tags:
- russian
- css
- html
- javascript
- jquery
- nlp
- hedghog
categories:
- programming
---
In a [previous post](/2022/05/17/three-line-though-non-standard-interlinear-glossing/) I presented a CSS-based solution to interlinear glossing that uses only CSS. It's a solution that may be preferrable others such as leipzig.js or interlinear.js because both of the latter assume a different annotation purpose than what I envision for my app. Whereas those libraries deal with punctuation gracefully, my CSS-only approach does not. So we end up with something like this:

{{< figure src="/images/2022/05/17/3line.png" width="600px" >}}

where the `PUNCT` nodes end up standing alone. These extra punctuation nodes add nothing to the understanding of the text and look ragged.

What I would really like is for the punctuation marks to live with the previous element and for the markup to go away. A little jQuery helps here. The basic strategy is this:

1. Find the `p.pos` nodes and select the ones containing _PUNCT_.
2. Loop over the `p.pos` punctuation nodes and find their parent node, which we're going to delete.
3. Find the previous sibling of the punctuation `div`.
4. Append the punctuation mark onto the `p.ru` of the previous sibling `div`.
5. Remove the punctuation `div` from the DOM.

The result looks like this:

{{< figure src="/images/2022/05/18/interlinear_punct.png" width="600px" >}}

The visual appearance is much better now, I think.

The CSS and HTML example code are as presented [previously](/2022/05/17/three-line-though-non-standard-interlinear-glossing/). Here's the jQuery code we use to move around the punctuation.

{{< highlight javascript >}}
$(function() {
    /* document ready code here */
    $('p.pos').filter(function() {
        return $(this).text().trim().toLowerCase() === 'punct';
    }).each(function(index) {
        /* these are each punctuation <p> */
        let punctDiv = $(this).parent();
        // get the exact punctuation mark in use
        let punctMark = punctDiv.children().filter('.ru').first().text();
        /*  find the previous div because
        	that's where we need to add back the
            punctuation mark
        */
        let punctPrevDiv = punctDiv.prev();
        // the p.ru child
        var punctRuP = punctPrevDiv.children().filter('.ru').first();
        // glom the punctuation mark onto previous p.ru
        punctRuP.append(punctMark);
        // remove the PUNCT div from the DOM
        punctDiv.remove()
    })
})
{{< /highlight >}}

There is a [JSFiddle](https://jsfiddle.net/OjisanSeiuchi/pj9ft6oh/48/) to play with if this is helpful. There's still much more to do in my project, integrating various pieces, but it's beginning to take shape.