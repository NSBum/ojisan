---
title: "A deep dive into my Anki language learning: Part III (Sentences)"
date: 2022-06-08T06:33:23-04:00
draft: false
authorbox: false
sidebar: false
tags:
- russian
- anki
categories:
- anki
---
Welcome to Part III of a deep dive into my Anki language learning decks. In [Part I](2022/06/03/a-deep-dive-into-my-anki-language-learning-part-i-overview-and-philosophy/) I covered the principles that guide how I setup my decks and the overall deck structure. In the lengthy [Part II](/2022/06/04/a-deep-dive-into-my-anki-language-learning-part-ii-vocabulary/) I delved into my vocabulary deck. In this installment, Part III, we'll cover my sentence decks.

### Principles

First, sentences (and still larger units of language) should eventually take precedence in language study. What help is it to know the word for _"tomato"_ in your L2, if you don't know how to _slice a tomato_, how to _eat a tomato_, how to _grow a tomato plant_? Focus on larger units of language increases your success rate in integrating vocabulary into daily use.

Second, I don't want sentence learning to require a lot of extra effort. If I'm learning a new word, I don't want to have to create a separate sentence card while I'm making a vocabulary card. (Fortunately I have a solution for that!)

### Types of sentence cards

#### Cloze deletion cards

My sentence cards are almost all have a cloze deletion format.

{{< figure src="/images/2022/06/08/sentence1front.png" width="600px" >}}

Above is the front side of a typical cloze deletion card. The card is asking to recall the bracketed word(s) and the back will reveal them.


{{< figure src="/images/2022/06/08/sentence1back.png" width="600px" >}}

On the back, we reveal the clozed text and also expose any notes, such as usage notes, alternative translations and so forth. And that's the essence of the cloze deletion card.

### Two methods of generating cloze deletion cards

There are two ways that cloze deletion cards come about. The standard method relies on Anki's built in cloze mechanism. The other way uses a script [Anki Cloze Anything](https://github.com/matthayes/anki_cloze_anything) that simulates a cloze card. The outcome looks the same but the generation mechanism differs. 

#### Straight cloze deletion cards

My straight cloze deletion cards use a version of the built-in cloze deletion note type. I've added several fields that are specific to my purposes, but it's basically a cloze deletion note. To designate a block of text to be clozed out, the format looks like this:

{{< figure src="/images/2022/06/08/cloze1fields.png" width="600px" >}}

#### Anki Cloze Anything cards

I hinted at this idea when I wrote about vocabulary cards in [Part II](/2022/06/04/a-deep-dive-into-my-anki-language-learning-part-ii-vocabulary/). The problem that this solves is the need to use a cloze deletion note type in order to access cloze deletion functionality. Since Anki notes are capable of generating multiple different card types, this seems an unnecessary distinction. Anki Cloze Anything (ACA) is a JavaScript that allows you to bypass this limitation by simulating a cloze deletion card in any standard note type.

In this way, I can add a sentence cloze deletion inside my standard vocabulary cards.

{{< figure src="/images/2022/06/08/acafields.png" width="600px" >}}

Note that the format that ACA uses is slightly different from the built-in cloze. Instead of curly braces, it uses parentheses. But the outcome is the same; the resulting cards look exactly like a built-in cloze deletion card!

There are two important issues with the ACA mechanism: the appearance of the sentence on non-ACA cloze, and the pronunciation of the sentence when using AwesomeTTS. Both can be solved, but they require some work.

##### ACA sentences and display on non-cloze cards

If you try to display an example sentence that has ACA markup on a non-cloze card, it shows the markup still in place:

{{< figure src="/images/2022/06/08/acafail.png" width="600px" >}}

Fortunately, we can solve this easily by applying some text manipulation using a regular expression in JavaScript:

{{< highlight javascript >}}
 /*

_fix_cloze_anything_example_sentence.js

2022-06-04

On any card that shows an example sentence that has
Cloze Anything markup and is in a span
that has rusentence class, strip that markup from it.

*/

function fix_cloze_anything_example_sentence() {
   document.querySelectorAll('span.rusentence').forEach((el, idx) => {
      let text = el.textContent;
      let re = /\(\(c\d::([^\)\(:]+)(?:::[^\):]+)?\)\)/g;
      text = text.replace(re, "$1");
      text = text.replace(new RegExp('`', 'g'),"");
      el.textContent = text;
   });
}
{{< /highlight >}}

When this is wrapped in a `<script></script>` block in the card template, the marked-up sentence will appear normal.

##### ACA sentences and AwesomeTTS

The harder problem to solve is with TTS. The pronunciation file seems to be generated before the Anki Cloze Anything script has a chance to process and strip the markup. As a result, AwesomeTTS pronounces the sentence with the markup in place. Needless to say, that won't work.

The only solution I've found is to create a separate copy of the sentence _without_ the ACA markup and use that for the pronunciation. Not ideal, but I've written a Keyboard Maestro macro that ingests the original marked up sentence, removes the formatting and pastes in a dedicated pronounceable field on my template. It could be worse...

### Parting words on sentences

A few miscellaneous thoughts that have informed my use of sentence cards:

1. You don't have to cloze single words. Prepositional phrases, whole clauses, even entire sentences are excellent candidates for cloze deletion and pushes you in the direction of larger and larger units of language.
2. Sentences can come from anywhere. The best source is real life or whatever you're reading in the target language; that's where a majority of mine come from. But [Tatoeba](https://tatoeba.org/en/) is a great source of sentences that are verified by native speakers.
3. Text-to-speech (TTS) is excellent. There are several ways to go about this. I use AwesomeTTS. The developers now are saying that it is being phased out in favour of HyperTTS. As of this writing, I haven't made the transition. 
4. I've begun adding images to my sentence cards. Anything to reinforce the learning using different sensory modalities.

That's what I have on sentence cards. In the next article in the series, I'll describe my grammar cards. In the meanwhile, if you would like to contact me about something in this article or any of my Anki-related posts, you can use this [contact form](http://www.shortwhale.com/NSBum).

