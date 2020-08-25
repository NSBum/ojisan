---
title: "Beginning to experiement with Stanza for natural language processing"
date: 2020-08-20T11:04:47-04:00
draft: false
authorbox: false
sidebar: false
tags:
- linguistics
- russian
- python
categories:
- programming
---
After installing [Stanza](https://stanfordnlp.github.io/stanza/) as dependency of [UDAR](https://github.com/reynoldsnlp/udar) which I recently [described](/2020/08/18/automated-marking-of-russian-syllabic-stress/), I decided to play around with what is can do.

### Installation

The installation is straightforward and is documented on the Stanza [getting started](https://stanfordnlp.github.io/stanza/#getting-started) page.

First,

{{< highlight bash  >}}
sudo pip3 install stanza
{{< /highlight >}}

Then install a model. For this example, I installed the Russian model:

{{< highlight python  >}}
#!/usr/local/bin/python3
import stanza
stanza.download('ru')
{{< /highlight >}}

### Usage

#### Part-of-speech (POS) and morphological analysis

Here's a quick example of POS analysis for Russian. I used `PrettyTable` to clean up the presentation, but it's not strictly-speaking necessary.

{{< highlight python  >}}
#!/usr/local/bin/python3
import stanza
from prettytable import PrettyTable

tab = PrettyTable()
tab.field_names = ["word","lemma","upos","xpos","features"]
for field_name in tab.field_names:
    tab.align[field_name] = "l"

nlp = stanza.Pipeline(lang='ru', processors='tokenize,pos,lemma')
doc = nlp('Моя собака внезапно прыгнула на стол.')
for sent in doc.sentences:
    for word in sent.words:
       tab.add_row([word.text, word.lemma, word.upos,
       word.xpos, word.feats if word.feats else "_"])
print(tab)
{{< /highlight >}}

![](/images/2020/08/20/terminal.jpg)

Note that `upos` are the universal parts of speech where `xpos` are language-specific parts of speech.

#### Named-entity recognition

Stanza can also recognize named entities - persons, organizations, and locations in the text it analyzes:

{{< highlight python  >}}
import stanza
from prettytable import PrettyTable

tab = PrettyTable()
tab.field_names = ["Entity","Type"]
for field_name in tab.field_names:
	tab.align[field_name] = "l"

nlp = stanza.Pipeline(lang='ru', processors='tokenize,ner')
doc = nlp("Владимир Путин живёт в Москве и является Президентом России.")
for sent in doc.sentences:
	for ent in sent.ents:
		tab.add_row([ent.text, ent.type])
print(tab)
{{< /highlight >}}

which, tells us:

![](/images/2020/08/20/named.jpg)

I'm excited to see what can be built from this for language-learning purposes.
