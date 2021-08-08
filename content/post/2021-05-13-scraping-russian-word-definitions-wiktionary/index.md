---
title: "Scraping Russian word definitions from Wikitionary: utility for Anki"
date: 2021-05-13T06:40:45-04:00
draft: false
authorbox: false
sidebar: false
tags:
- anki
- russian
categories:
- programming
---
While my Russian [Anki]() deck contains around 27,000 cards, I'm always making more. (There are _a lot_ words in the Russian language!) Over the years, I've become more and more efficient with card production but one of the missing pieces was finding a code-readable source of word definitions. There's no shortage of dictionary sites, but scraping data from any site is complicated by the ways in which front-end developers spread the semantic content across multiple HTML tags arranged in deep and cryptic hierarchies. Yes, we can cut-and-paste, but my quest is about nearly completely automating quality card production. This is a quick post of a method for scraping word definitions from Wiktionary.

The project relies on the `wiktionaryparser` module available for Python. Although it's not feature complete, it's pretty good. With a little extra processing, it can do a lot of the heavy lifting of extracting word definitions.

{{< highlight python "linenos=table">}}
#!/usr/bin/env python3

from wiktionaryparser import WiktionaryParser
import re

parser = WiktionaryParser()
parser.set_default_language('russian')
wp = parser.fetch('картонный')
def_list = []
for parsed in wp:
   for definition in parsed['definitions']:
      for text in definition['text']:
         if not bool(re.search('[а-яА-Я]', text)):
            def_list.append(text)
print(', '.join(def_list))
{{< /highlight >}}

The code is largely self-explanatory; but I would just point out than line 13 is there to exclude any line that contains residual Cyrillic characters. Out-of-the-box, the `WiktionaryParser` module seems to capture the headword, IPA pronunciation, etc. so we need a way of excluding all of that before we compress the definition lines into a single string of comma-delimited text.
