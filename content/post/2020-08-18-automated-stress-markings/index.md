---
title: "Automated marking of Russian syllabic stress"
date: 2020-08-18T18:23:20-04:00
draft: true
authorbox: false
sidebar: false
tags:
- linguistics
- russian
- python
categories:
- programming
---
One of the challenges that Russian learners face is the placement of syllabic stress, an essential determinate of pronunciation. Although most pedagogical texts for students have marks indicating stress, practically no tests intended for native speakers do. The placement of stress is inferred from memory and context.

I was delighted to discover Dr. Robert Reynolds' work on natural language processing of Russian text to mark stress based on grammatical analysis of the text. What follows is a brief description of the installation and use of this work. The [project page](https://github.com/reynoldsnlp/udar) on Github has installation instructions; but I found a number of items that needed to be addressed that were not covered there. For example, this project (UDAR) depends on Stanza; which in turn requires a language-specific (Russian) model.

### Installation

The first step is to installation a few dependencies:

1. Install the [pexpect](https://stanfordnlp.github.io/stanza/) module:

{{< highlight bash  >}}
sudo pip3 install pexpect
{{< /highlight >}}

2. Install [stanza](https://stanfordnlp.github.io/stanza/)

{{< highlight bash  >}}
sudo pip3 install stanza
{{< /highlight >}}

3. Install Stanza's Russian model:

{{< highlight python  >}}
#!/usr/local/bin/python3
import stanza
stanza.download('ru')
{{< /highlight >}}

_Note the my python3 is the Homebrew version; so your hashbang may be different._

4. The project depends on hfst[^1] and vislcg3[^2] which can be installed by downloading the [following script, i.e.](https://apertium.projectjj.com/osx/install-nightly.sh). I had to download the script and run it in CodeRunner.

5. Install udar:

{{< highlight bash  >}}
sudo pip3 install --user git+https://github.com/reynoldsnlp/udar
{{< /highlight >}}

### Basic usage

See the [project page](https://github.com/reynoldsnlp/udar) on Github for more comprehensive details; but I was quickly able to create my own example following the documentation. For example:

{{< highlight python >}}
#!/usr/local/bin/python3
import udar
doc1 = udar.Document('Моя собака внезапно прыгнула на стол.')
print(doc1.stressed())
{{< /highlight >}}

which prints the correctly-marked {{< russian >}}Моя соба́ка внеза́пно пры́гнула на сто́л.{{< /russian >}}

I'm looking forward to exploring the capabilities of this NLP tool further.

### References

- Reynolds, Robert J. "Russian natural language processing for computer-assisted language learning: capturing the benefits of deep morphological analysis in real-life applications" PhD Diss., UiT–The Arctic University of Norway, 2016. https://hdl.handle.net/10037/9685
- [UDAR - NLP system for applying syllabic stress markings](https://github.com/reynoldsnlp/udar)

[^1]: Helsinki Finite-State Transducer.
[^2]: [Constraint grammar](https://en.wikipedia.org/wiki/Constraint_grammar) - implementation CG-3.
