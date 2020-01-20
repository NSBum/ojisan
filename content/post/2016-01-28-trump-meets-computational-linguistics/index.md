---
title: Trump meets computational linguistics
date: 2016-01-28 04:40:39
aliases: ['/2016/01/28/Trump-meets-computational-linguistics/']
tags:
- politics
- technology
- trump
- programming
categories:
- politics
---
{{< figure src="images/trump.jpg" title="Trump orating" >}}

_"I actually called her, and she never mentioned my name. You know, I - when I sold - oh, did I get a call from one of the Environmental Protection Agency, they couldn't find it because it comes out in big globs, right, and you say to yourself, 'How does that help us?'"_

Trump is one of the most amusing orators in the history of presidential politics in the the U.S. But I wondered what would happen I took the text of a few of his speeches and fed it into a algorithm that uses [Markov chains](https://en.wikipedia.org/wiki/Markov_chain) to shake things up a bit.

A Markov Chain is a process in which states undergo random transitions in which the probability of the next state depends only on the current state. This is a characteristic often called "memorylessness." In statistical modeling, Markov Chains have serious applications. But I've used it here to analyze and distort Trump speeches so that they sound even more rambling than in reality. This results in such keepers as:

> _"Well, they couldn’t find it because then it comes out in big globs, right, and you had Iraq and you know, China comes over and they say, we can't believe it or not. I’m doing it. Number two, I’m a free trader._

The algorithm takes a "snapshot" of the preceding two words in a sentence, scans the text for those two words, generating a table of words that follow those couplets. It then chooses a random word based on the probabilities.

> _"We have wounded warriors, incredible people. And you know, we are doing a big problem, Russia’s a problem, China’s a problem. We’ve got a lot of things. We are rebuilding China. We’re rebuilding many countries. The Euro, China is going to be repealed and replaced. It will die in ’17 anyway."_

Some of the sentences are grammatically correct; many are not. But they have similar cadence and "feel" as a real Trump speech.

> _"“Mr. Trump, where are those hats made?” I said. I had no choice, because I don’t want me to refute his statement. How dare you say that. They don't know what they’re saying — that nobody believes. So you have a presidential election coming up. We have $2 trillion and we are going to move the plant back to the ceiling, $500 billion is?"_

I used a [Python implementation](http://agiliq.com/blog/2009/06/generating-pseudo-random-text-with-markov-chains-u/) of the Markov text generator described above. You can read the [full text of a run](pdf/trump_output.pdf). The source text comes from three different speeches given by Mr. Trump.
