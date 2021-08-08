---
title: "Parsing Russian Wiktionary content using XPath"
date: 2021-02-13T05:45:41-05:00
draft: false
authorbox: false
sidebar: true
tags:
- python
- anki
- russian
categories:
- Programming
---
As readers of this blog know, I'm an avid user of [Anki](https://apps.ankiweb.net) to learn Russian. I have a number of sources for reference content that go onto my Anki cards. Notably, I use Wiktionary to get word definitions and the word with the proper syllabic stress marked. (This is an aid to pronunciation for Russian language learners.)

Since I'm lazy to the core, I came up with a system way of grabbing the stress-marked word from the Wiktionary page using `lxml` and `XPath`.

### Finding the XPath of the element

First, we need to find the XPath of the element we want. Right-click on the stress-marked word and select "Inspect Element" from the contextual menu in Safari. After confirming that the correct HTML is displayed, right-click again and select "Copy" > "XPath". 

Fortunately, the Wiktionary format is (relatively) consistent and stable enough, that I'll just tell you the XPath. It's `//*[@id="mw-content-text"]/div[1]/p[2]/strong`

### Prerequisites?

You will need the HTML/XML parsing module `lxml` so install with `pip3 install lxml`. While you're at it, you'll need BeautifulSoup later, so install that too `pip3 install beautifulsoup4`.

### Scraping the text of the element

{{< highlight python >}}
#!/usr/bin/env python3

from lxml import html
from lxml import etree
import requests
import sys

page = requests.get(sys.argv[1])
tree = etree.fromstring(page.content)
headword = tree.xpath('//*[@id="mw-content-text"]/div[1]/p[2]/strong')
try:
	print(headword[0].text)
except:
	headword = tree.xpath('//*[@id="mw-content-text"]/div[1]/p/strong')
	print(headword[0].text)
{{< /highlight >}}

And that's it - the script should print the headword - the accented word at the page. (Assumes the URL is the first script argument.)

### Scraping the definition(s)

It becomes a little more complicated to scrape the word definitions because Wiktionary makes extensive use of markup in the middle of the definition. But BeautifulSoup seems to do an admirable job of wading through the fluff to return just the text of the definition.

{{< highlight python >}}
#!/usr/bin/env python3

from lxml import html
from lxml import etree
import requests
import re
from bs4 import BeautifulSoup

page = requests.get('https://en.wiktionary.org/wiki/перерасти#Russian')
tree = etree.fromstring(page.content)
headword = tree.xpath('//*[@id="mw-content-text"]/div[1]/p[2]/strong')
try:
	print(headword[0].text)
except:
	headword = tree.xpath('//*[@id="mw-content-text"]/div[1]/p/strong')
	print(headword[0].text)

def_list = tree.xpath('//*[@id="mw-content-text"]/div[1]/ol')
def_text = ''
for li in def_list[0].iterchildren():
	soup = BeautifulSoup(etree.tostring(li), 'html.parser')
	def_text = def_text + '\n' + soup.get_text()
result = re.sub(r'\n\n', "\n", def_text)
print(result)
{{< /highlight >}}

That's the complete code to grab the headword and the definition list.

### References

- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - HTML parsing module
- [BeautifulSoup documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - all the gory details
- [Element to inner HTML in lxml](https://stackoverflow.com/questions/14896302/get-the-inner-html-of-a-element-in-lxml) - Some background on grabbing the inner HTML from an Element in lxml. It's the explanation for what's going on in `soup = BeautifulSoup(etree.tostring(li), 'html.parser')` above.