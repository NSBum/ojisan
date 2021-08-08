---
title: "Refactoring Anki language cards"
date: 2021-03-20T06:47:44-04:00
draft: false
authorbox: false
sidebar: false
tags:
- anki
- russian
- linguistics
categories:
- anki
---
Regardless of how closely you adhere to the [20 rules for formating knowledge](http://super-memory.com/articles/20rules.htm), there are cards that seem destined to leechdom. For me part of the problem is that with languages, straight-up vocabulary cards take words out of the rich context in which they exist in the wild. With my maturing collection of Russian decks, I recently started to go through these resistant cards and figure out why they are so difficult.

### Why do some vocabulary cards resist learning?

1. **Rare words are rare in ordinary daily use, so they are not reinforced outside of Anki.** - Of course this is one of the reasons that some recommend just deleting or suspending leeches. I'm unwilling to that except in the rarest of cases. It feels like giving up. But the point stands, since you don't encounter the word frequently, if at all, outside of Anki reviews, the little hits of memory that would ordinarily prop up the forgetting curve don't occur.
2. **The card may be badly formatted.** - For example a card with an image on one side and a Russian word on the other side may be difficult simply because the meaning conveyed by the image is ambigous.
3. **Synonyms are tough.** - As you progress in the breadth of your vocabulary, you will accumulate words with similar meanings. When faced with an English → Russian card (a _production_ card) which variant is intended?
4. **Interference with similar words can be a problem.** - For example the two words {{< russian >}}угол{{< /russian >}} and {{< russian >}}уголь{{< /russian >}} are major interferers for me. Yes the spelling is different and yes, the pronunciation is somewhat different, but to the ears of a native English speaker, not different enough. So I might be close when I see one of them, but not absolute.

Finally, some cards fail regularly because of some inexplicable reason. For example, I have a vocabulary card for the verb pair {{< russian >}}полагаться/положиться{{< /russian >}} _"to rely (on)"_. There is no obvious reason why that should fail as often as it does for me. It's used frequently in speech and writing, but something about that aspect pair in isolation draws a blank for me.

### Bolstering vocabulary card performance

Before addressing how to improve card performance, I'll take a step back and address a way of finding resistant cards. The simplest approach in the card browser is to browse the deck of interest and sort by lapse count. This is a great start but I noticed that it also identifies cards that were resistant at one time, but have improved subsequently. If your goal is to order resistant cards by some metric of difficulty for the purpose of prioritizing them, then you need some metric. Since for any similar of difficulty, the lapse count will be greater for cards that have been around longer. Also cards with a higher ease factor are possibly cards that accumulated a lot of lapses early then stabilized (and thus recovered their ease.)

While completely arbitrary, the scoring formula that I'm using is given by:

![](/images/2021/03/19/formula_anki.png)

where _l_ is the number of lapses, _d_ is the number of days since card creation and _f_ is the ease factor of the card in the format it is stored in the database (so 250% = 2.50). The formula is nearly entirely arbitrary except for the idea of scaling the number of lapses by the age of the card to approximate a sort of _lapses per unit of time_ measurement. The factor by which the card ease influence the score was determined arbitrarily by finding the smallest integer that gave positive scores across a sample of cards with the most frequent lapses. I haven't yet come up with a better ways of objectively modelling this.

To implement this formula, I exported all cards with more than 10 lapses to a CSV file and exported it to Numbers. (Excel will work too.) After sorting by this score, I was able to get a better idea where my priorities should be. I was also able to make a more educated guess as to why the card was failing and implement strategies on a per-card (or per-note) basis.

#### Strategies for improving performance

1. **Ensure that there is at least one sample sentence card, preferably more.** - One of the lessons I've learned through years of using Anki for language learning is that context matters a lot. So before I do anything, I look through my sentence decks for any cards that contain the word in question. This in itself can be complicated in a highly inflected languaged like Russian. So I have a field `lemmas` on each sentence card that captures all of the relevant lemmas (uninflected root word forms) in the sentence. To lemmatize all of my several thousand sentence initially, I created a custom script that employs the natural language processing module `stanza` to extract all of the lemmas and load them into the `lemmas` field.[^1]
2. **Add a synonyms field to straight vocabulary cards** - The mapping between concepts in two languages, like Russian and English is not 1:1 so several Russian words may match an English prompt on a card. This ambiguity can be resolved by adding a field for synonyms on the card, so that you can at least see what the answer is _not_.
3. **Reduce the ambiguity of image cards.** - Since some images can be ambigous, using clarifying additions such as comments, arrows, and other callouts can add enough specificity to make the card more useful.
4. **Add monolingual definition cards.** - To make words appear more often in a different form, I've added a third card type that displays the Russian language definition of the Russian word. The adds memorability by piling on a little more context, albeit distributed in time.
5. **Add even more sentences that _you_ generate yourself.** - Sentences that are personally-relevant or have other _"interestingness"_ hooks[^2] can be valuable here. I use DeepL for translating English expressions into Russian.[^3]
6. **Add audio-only sentence cards.** - Create cards where the prompt is a spoken Russian sentence that employs the word in question. You can use the AwesomeTTS add-on in Anki to generate the audio for these cards. Several authentic text-to-speech providers are available. I use Microsoft Azure and Google Cloud TTS in addition to the built-in macOS text-to-speech system.
7. **Make certain that your language-learning "diet" is as diverse as possible.** - Since it is unreasonable to expect that the only time you're going to encounter a word is inside of Anki, don't rely solely on Anki. A language is much more than the sum of all of its words. Setting aside ample time for reading, listening to podcasts, reading fiction, reading news, speaking and so forth is more important than any intervention that you can implement inside of Anki.

### References

1. [Anki / Spaced Repetition Tip: Review your Weak Flashcards](http://www.marknagelberg.com/anki-spaced-repetition-tip-review-your-weak-flashcards/) - A similar post on refactoring weak Anki cards, how to detect weak cards, etc.

[^1]: I would post the script here but it is so deeply specific to my card setup that I can't imagine it would be very useful to anyone. But feel free to contact me if you are interested.
[^2]: This is one of the principles used in the Method of Loci for enhancing memory. The more raw, vivid, and odd the thing or situation being described, the stickier it is.
[^3]: I've found that DeepL translations are more natural-sounding than those from Google Translate and also allow you to choose alternate words in the resulting sentence.
