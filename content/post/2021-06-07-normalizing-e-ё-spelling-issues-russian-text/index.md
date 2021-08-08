---
title: "Normalizing spelling in Russian words containing the letter ё"
date: 2021-06-07T06:00:33-04:00
draft: false
authorbox: false
sidebar: false
tags:
- russian
categories:
- programming
- russian
---
The Russian letters {{< russian >}}ё{{< /russian >}} and {{< russian >}}e{{< /russian >}} have a complex and troubled relationship. The two letters are pronounced differently, but usually appear the same in written text. This presents complications for Russian learners and for text-to-speech systems. In several recent projects, I have needed to normalize the spelling of Russian words. For examples, if I have the written word {{< russian >}}определенно{{< /russian >}}, is the word **actually** {{< russian >}}определенно{{< /russian >}}? Or is it {{< russian >}}определённо{{< /russian >}}?

This was a larger challenge than I imagined. Apart from [udar](https://github.com/reynoldsnlp/udar)[^1], I failed to find any off-the-shelf solutions to what I call _normalizing_ the spelling of words that should be spelled with {{< russian >}}ё{{< /russian >}}. It turns out that the Russian language Wiktionary respects URLs whether spelled with {{< russian >}}ё{{< /russian >}} or {{< russian >}}e{{< /russian >}}. Therefore, one way of normalizing the spelling is to query Wiktionary and grab the headword from the page. Normally I don't like creating this sort of dependency; but it's the only solution that presented itself so far. Here's the approach I took:

{{< highlight python >}}
#!/usr/bin/env python3

from lxml import html
from lxml import etree
import requests
import re
from typing import Optional

word = 'еще'

def normalize(word:str) -> Optional[str]:
    # don't bother searching if there's no е or if
    # there *is* a ё
    if not bool(re.search(r'[её]', word)) or bool(re.search(r'[ё]', word)):
        return word
    url = f'https://ru.wiktionary.org/wiki/{word}'
    page = requests.get(url)
    content = page.content.decode()
    tree = etree.fromstring(content.replace('--lang--', ''))
    block = tree.xpath('//h1[@id="firstHeading"]')
    try:
        return block[0].text
    except:
        return word

if __name__ == "__main__":
    print(normalize(word))
{{< /highlight >}}


[^1]: [udar](https://github.com/reynoldsnlp/udar) can work but the installation is non-trivial and it has substantial dependencies that may make it less appealing in some applications.
