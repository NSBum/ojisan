---
title: "Hedghog and interlinear lemmas"
date: 2022-05-15T06:37:22-04:00
draft: false
authorbox: false
sidebar: false
summary: "Starting a new devlog about Hedghog, a new language learning app and some thoughts about the interlinear display of lemmas."
tags:
- russian
- css
- nlp
- hedghog
categories:
- programming
---
I've been working on a side-project for a few weeks that I'm calling "Hedghog." Here's the _elevator pitch_.

> This is a tool to aid in learning foreign languages. Adults learn languages best by consuming comprehensible content whose context is relevant to the learner. Reading is one of the ways of acquiring foreign language content, including vocabulary, phraseology and so forth. Hedghog is a tool for acquiring and storing foreign language texts for the purposes of language learning. It helps the user track new words and phrases from these texts and provides translation, lemmatization and tagging features. It also can export lists of new words and phrases to the spaced-repetition program Anki.

One of the features of Hedghog is interlinear display of lemmas. Often, interlinear displays are used to display bilingual text. This is difficult when the word order differs significantly from the first-language word order. I'm also skeptical that this sort of display helps the learner efficiently acquire an understanding of the second-language ways of idiomatic writing. Instead, in Hedghog, the display will show the original text in large type with each word's _lemma_ beneath. For Russian, this solves one of the slowdowns in reading that I encounter - which is the momentary hesitation in recognizing the inflected form. It's particularly halting when I run into a participle in an oblique case. The term "interlinear" isn't exactly right here, but I'm struggling to think of something better. _Edit 2022-05-15: The better term is "interlinear gloss"_[^1]

It looks something like this:

{{< figure src="/images/2022/05/15/interlinear.png" width="500px" >}}

This is adapted from [an approach](https://jtauber.com/blog/2006/01/28/dynamic_interlinears_with_javascript_and_css/) demonstrated initially for reading classical Greek.

{{< highlight html >}}
<h3>Interlinear lemmas</h3>
<div class="unit"><p class="ru">В</p><p class="lemma">в</p></div>
<div class="unit"><p class="ru">этом</p><p class="lemma">этот</p></div>
<div class="unit"><p class="ru">контексте</p><p class="lemma">контехт</p></div>
<div class="unit"><p class="ru">комментаторы</p><p class="lemma">комментатор</p></div>
<div class="unit"><p class="comma">,</p></div>
<div class="unit"><p class="ru">журналисты</p><p class="lemma">журналист</p></div>
<div class="unit"><p class="ru">политики</p><p class="lemma">политик</p></div>
<div class="unit"><p class="ru">чувствуют</p><p class="lemma">чувствовать</p></div>
<div class="unit"><p class="ru">себя</p><p class="lemma">себя</p></div>
<div class="unit"><p class="ru">свободными</p><p class="lemma">свободный</p></div>
<div class="unit"><p class="ru">в</p><p class="lemma">в</p></div>
<div class="unit"><p class="ru">бряцании</p><p class="lemma">бряцание</p></div>
<div class="unit"><p class="ru">ядерным</p><p class="lemma">ядерный</p></div>
<div class="unit"><p class="ru">оружием</p><p class="lemma">оружие</p></div>
{{< /highlight >}}

And the CSS:


{{< highlight css >}}
div.unit {
  float: left;
  margin-bottom: 1em;
  color: black;
}

div.comma {
    float: left;
    margin-bottom: 1em;
    color: black;
    
}

p.comma {
  font-size: 16pt;
  font-family: serif;
  margin: 0em;
  padding: 0em 0em;
}

p.ru {
  font-size: 16pt;
  font-family: serif;
  margin: 0em;
  padding: 0em 0.5em;
}

p.lemma {
  font-size: 10pt;
  font-family: sans-serif;
  color: gray;
  margin: 0em;
  padding: 0em 1em;
}
h3 {
    font-family: "HelveticaNeue";
}
{{< /highlight >}}

Here's a [link](https://jsfiddle.net/OjisanSeiuchi/3rb5egu0/17/) to a JSFiddle to play around with this.

### More on interlinear text

- [Dynamic interlinears with CSS and HTML](https://jtauber.com/blog/2006/01/28/dynamic_interlinears_with_javascript_and_css/)
- [word-aligned interlinear glosses](https://github.com/parryc/interlinear)
- [liepzig.js - Interlinear glossing for the browser](https://github.com/bdchauvette/leipzig.js/) - this looks very promising. The example page linked from the repository is no longer live, but there's still an [archived version](https://web.archive.org/web/20190723212125/https://bdchauvette.net/leipzig.js/examples/). This may actually be the approach I take for this project.

[^1]: [Wikipedia - Interlinear gloss](https://en.wikipedia.org/wiki/Interlinear_gloss)