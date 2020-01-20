---
title: How I use Anki to learn Russian
date: 2016-03-08 06:35:53
draft: true
tags:
- memorization
- learning
- russian
- languages
- anki
categories:
- russian
---
Learning the vocabulary of a non-native language is a daunting task. The Russian vocabulary encompasses an [estimated](http://www.lingholic.com/how-many-words-do-i-need-to-know-the-955-rule-in-language-learning-part-2/) 200,000 words. Facing the task of learning this massive vocabulary for a foreign speaker is a Herculean task.^[Fortunately, many words are rare or obsolete and my experience with other languages is that you can make yourself understood with far less than the complete vocabulary.] The average adult English speaker is said to use about 20,000 words. Presumably Russian speakers can get by with about number too. Nonetheless, it remains an enormous task, one that can't be conquered solely by brute force.

## Spaced repetition system

On of the most effective methods of memorizing large quantities of information is by applying a spaced repetition system (SRS). Spaced repetition of information takes advantage of the observation that repeated exposure to information at gradually increasing intervals is known to increase the retention rate. A single exposure to a piece of information is associated with a predictable rate of decay. After a repeat exposure a few days later, the rate of decay is somewhat less and for each subsequent interval, the rate of loss is much less. So SRS "pulses" information at predictable intervals to optimize its retention. If it sounds like the perfect task for a computer, it is!

### Software for spaced repetition

A number of software application implement forms of spaced repetition, mainly in the form of flash cards. I did not review each of these in enough detail to make a definitive comparison. Instead, I've evaluated Mental Case (a native Mac OS X and iOS application) and SuperMemo fairly cursorily. SuperMemo is not a great option for me because it is available only on Windows. I wanted to like Mental Case but I felt like the interface got in the way and I didn't want to take the time to learn the unusual ways that it organizes knowledge in the application. For several years now I've used [Anki](http://ankisrs.net). It is available on multiple platforms and has a spartan user interface. Since it is not a native OS X application it takes some getting used to. This particularly true for accented languages because you cannot use the native OS X keyboard input scheme for accents.^[For example, all of the "e" accents are accessible by holding the "E" key.] There are, of course, workarounds and you just have to get used to them. Anki is also available on iOS and syncs very well between devices. There is a robust community of users, a mechanism for sharing decks, and many plugins to enhance the functionality of the application.

### Organizing the work

As with any large task, devising a strategy in advance will help make it easier. Before downloading a shared deck or jumping in head-first, consider some [basic rules](https://www.supermemo.com/en/articles/20rules) for organizing knowledge. One of the most important heuristics to consider is that context is important.

Anki has a large deck exchange. On Anki's deck sharing site, I found 269 Russian decks that users have shared. It is certainly possible to begin by downloading a large deck and plowing through it. But presumably you are using other means of learning Russian. The context of your work in those methods should provide a steady supply of vocabulary to feed your Anki lists.

Data entry is a formidable barrier for many users. However, the act of entering the card into Anki has some learning value itself. It's up to you to evaluate the pros and cons of using pre-built decks.

| Pros                               | Cons                                     |
|------------------------------------|------------------------------------------|
| Users have vetted and rated decks  | Words are unrelated to learning context  |
| Many pre-built decks are available | Quality control is variable              |
| Some decks are very comprehensive  | Decks aren't personalized for your needs |

I've tried using shared decks, but the lack of immediate relevance to what I'm learning elsewhere in my self-studies is a significant impediment. Instead, I have a system for getting words into my Anki lists as I encounter them.

- If I have time, I make cards for the words while I'm learning them.
- Otherwise I add a to-do item in my to-do application of choice [OmniFocus](https://www.omnigroup.com/omnifocus).
- If I'm working on a mobile device where it's inconvenient to switch back and forth between applications, I will take a screenshot of what I'm working on (e.g. Duolingo.)

### Overall structure

I have a profile for all of my Russian cards and another for other types of knowledge I'm memorizing. This cleanly separates the metadata that I use for tagging cards and it eliminates Anki's perpetual nagging about having too many decks. Within that profile, I have single deck called "Every card". Given Anki's flexibility to create [filtered decks]() that can behave in customizable ways, there's no compelling reason to create multiple decks.

### Speaking of metadata

{{< figure src="images/tag_hierarchy.jpg" title="Tag hierarchy in Aniki" class="left" >}}

I use tagging to organize my cards in Anki. Out-of-the box, Anki has a tagging system that you can use to build filtered decks of related knowledge. However, its built-in tagging system consists of a single-layer hierarchy. Since I think in terms of nested hierarchies, I installed the HierarchicalTags plug-in. This allows you to build sensible layers of metadata about cards.

Consistent use of tagging adds a little time to the process of entering the cards, and periodic review, pruning and joining of tags is necessary as the system grows. But the effort is worth it. For example, if I want to review the declension of all of the singular personal pronouns, it is very easy for me to construct a special filtered deck to do that. Otherwise, the knowledge is scattered haphazardly in the database.

My top-level tags are:

- grammar _(What part of speech is this word?)_
- source _(Where did I encounter this word?)_
- type _(What knowledge domain does this live in?)_



### Types of cards

The richer, more varied the learning experience the better. Although some shared decks consist of simple word pairs, I don't find them particularly useful. Instead, I try to approach the vocabulary from multiple angles. My decks are pretty redundant for that reason.

Before jumping into using Anki heavily, a cursory review of the manual is very helpful. In particular understanding the relationship between _cards_, _notes_, _fields_, and _decks_ is helpful. A __card__ is just a question/answer pair: "Q: собака, A: dog." That's it. A __deck__ is a collection of __cards__. This is the simplest example. Since [context is important](https://www.supermemo.com/en/articles/20rules#Context%20cues) and not every piece of knowledge can be reduced to a question/answer pair, Anki embraces the context of a __note__ which is a set of information related to a single fact of knowledge. Each of these notes, in turn comprises __fields__ which are the elements of this piece of knowledge. Finally, the blueprint that maps notes with their respective fields to individual cards is the __card type__. Each note can have more than one card type so that knowledge can be presented in multiple ways.

This lengthy introduction is necessary because I use Anki in a way that leverages them considerably.
