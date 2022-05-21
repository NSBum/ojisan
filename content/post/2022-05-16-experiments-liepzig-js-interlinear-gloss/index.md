---
title: "Experimenting with leipzig.js for interlinear gloss"
date: 2022-05-16T05:36:03-04:00
draft: false
authorbox: false
sidebar: false
tags:
- russian
- css
- nlp
- hedghog
categories:
- programming
---
One of the key features of my language learning app [Hedghog](/2022/05/15/hedghog-and-interlinear-lemmas/) is the display of source text with interlinear gloss. This is of huge benefit in understanding highly-inflected languages. Right now I'm playing around with different ways of achieving this sort of display. I stumbled on [leipzig.js](https://github.com/bdchauvette/leipzig.js) which is a library for formatting interlinear gloss according to the [Leipzig Rules](https://www.eva.mpg.de/lingua/pdf/Glossing-Rules.pdf).

I like what I see, but my first inclination is to get under the hood and fix some of the CSS. For example, the original text is displayed in italic. This is fine, and it may be the convention in linguistics circles, but some Russian letters are a little confusing to Russian learners when displayed in oblique type. It's not difficult to fix.

Here's what it looks like:

{{< figure src="/images/2022/05/16/leipzig.png" width="500px" >}}

I just needed to apply some of my own CSS to achieve the desired appearance - Leizig Rules or not.

{{< highlight css >}}
.gloss__line--0 {
    font-family: "Georgia";
    font-size: 20px;
}

.gloss__line--1 {
    color: gray;
}

.gloss__word .gloss__line:first-child {
    font-style: normal !important;
}
{{< /highlight >}}

And the minimal example in Russian:

{{< highlight html >}}
<html>

  <head>
    <link rel="stylesheet" href="//cdn.jsdelivr.net/npm/leipzig@latest/dist/leipzig.min.css">
  </head>

  <body>
    <div data-gloss>
      <p>Дональд Трамп - нелепый болван, который был избран президентом.</p>
      <p>дональд трамп - нелепый болван который был избрать президент.</p>
      <p>‘Donald Trump is a ridiculous moron who was elected president.’</p>
    </div>
    <script src="//cdn.jsdelivr.net/npm/leipzig@latest/dist/leipzig.min.js"></script>
    <script>
      document.addEventListener('DOMContentLoaded', function() {
        var glosser = Leipzig();
        glosser.gloss();
      });
    </script>
  </body>
</html>
{{< /highlight >}}

This minimal example as a [JSFiddle](https://jsfiddle.net/OjisanSeiuchi/6tvpbwmx/39/)

### More on interlinear gloss

- [leipzig.js GitHub repository](https://github.com/bdchauvette/leipzig.js/)
- [leipzig.js examples - archived](https://web.archive.org/web/20190723212125/https://bdchauvette.net/leipzig.js/examples/)
- [Wikipedia - interlinear gloss](https://en.wikipedia.org/wiki/Interlinear_gloss)
