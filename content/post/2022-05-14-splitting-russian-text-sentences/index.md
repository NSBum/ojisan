---
title: "Splitting text into sentences: Russian edition"
date: 2022-05-14T09:48:02-04:00
draft: false
authorbox: false
sidebar: false
summary: "Splitting text into sentences is one of those tasks that looks simple but on closer inspection is more difficult than you think. A common approach is to use regular expressions to divide up the text on punction marks. But without adding layers of complexity, that method fails on some sentences. This is a method using [spaCy](https://spacy.io)."
tags:
- russian
- nlp
categories:
- programming
---
Splitting text into sentences is one of those tasks that looks simple but on closer inspection is more difficult than you think. A common approach is to use regular expressions to divide up the text on punction marks. But without adding layers of complexity, that method fails on a sentence such as:

> _"Trapper John, M.D. was as fine as any Ph.D."_

It's obviously only one sentence, but try it with regex and the difficulty is obvious. 

[A solution](https://stackoverflow.com/a/66009264/134245) suggested on Stack Overflow is to use the [spaCy](https://spacy.io) natural language processing module along with its 'sentencizer' pipeline to do the heavy lifting. The recommended solutions are all based on English language processing; so I was anxious to see if it would work on Russian text. The short answer is "yes." This post is just to document the solution.

{{< highlight python >}}
from spacy.lang.ru import Russian

nlp_simple = Russian()
nlp_simple.add_pipe('sentencizer')

doc = nlp_simple(text)
sentences = [str(sent).strip() for sent in doc.sents]
{{< /highlight >}}