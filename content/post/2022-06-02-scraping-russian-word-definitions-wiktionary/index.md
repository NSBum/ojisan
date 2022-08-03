---
title: "A tool for scraping definitions of Russian words from Wikitionary"
date: 2022-06-02T13:33:44-04:00
draft: false
authorbox: false
sidebar: false
tags:
- programming
- russian
- python
categories:
- anki
---
In my perpetual attempt to make my language learning process using Anki more efficient, I've written a tool to extract English-language definitions from Russian words from Wiktionary. I wrote about the idea previously in [Scraping Russian word definitions from Wikitionary: utility for Anki](/2021/05/13/scraping-russian-word-definitions-from-wikitionary-utility-for-anki/) but it relied on the `WiktionaryParser` module which is _good_ but misses some important edge cases. So I rolled up my sleeves and crafted my own solution. As with `WiktionaryParser` the heavy-lifting is done by the Beautiful Soup parser. Much of the logic of this tool is around detecting the edge cases that I mentioned. For example, the underlying HTML format changes when we're dealing with a word that has multiple etymologies versus those with a single etymology. Whenever you're doing web scraping you have to account for those sorts of variations.

### Code

{{< highlight python >}}
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen, Request
import urllib.parse
from http.client import HTTPResponse
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem, HardwareType
import copy
import re
import sys
from bs4 import BeautifulSoup, element

def remove_html_comments(html: str) -> str:
    """
    Strips HTML comments. See https://stackoverflow.com/a/57996414
    :param html: html string to process
    :return: html string with comments stripped
    """
    result = re.sub(r'(<!--.*?-->)|(<!--[\S\s]+?-->)|(<!--[\S\s]*?$)', "", html)
    return result

def extract_russian_soup(response: HTTPResponse) -> BeautifulSoup:
   new_soup = BeautifulSoup('', 'html.parser')
   # remove HTML comments before processing
   html_str = response.read().decode('UTF-8')
   cleaner_html = remove_html_comments(html_str)
   soup = BeautifulSoup(cleaner_html, 'html.parser')
   # get rid of certain tags to make it lighter
   # to work with
   [s.extract() for s in soup(['head', 'script', 'footer'])]
   for h2 in soup.find_all('h2'):
      for span in h2.children:
         try:
            if 'Russian' in span['id']:
               new_soup.append(copy.copy(h2))
               # capture everything in the Russian section
               for curr_sibling in h2.next_siblings:
                  if curr_sibling.name == "h2":
                     break
                  else:
                     new_soup.append(copy.copy(curr_sibling))
               break
         except:
            pass
   return new_soup
   
def check_excluded_ids(span_id: str) -> bool:
   excluded = ['Pronunciation', 'Alternative_forms', 'Etymology']
   for ex in excluded:
      if re.search(ex, span_id, re.IGNORECASE):
         return True
   return False

def remove_dl_ul(li: element.Tag) -> element.Tag:
   try:
      dl_extract = li.dl.extract()
   except AttributeError:
      pass
      # sometimes citations are presented in <ul> so remove
   try:
      ul_extract = li.ul.extract()
   except AttributeError:
      pass
   return li

def url_from_ru_word(raw_word:str) -> str:
   # strip syllabic stress diacritical marks
   raw_word = re.sub(r'\u0301|\u0300', "", raw_word)
   raw_word = raw_word.replace(" ", "_").strip()
   word = urllib.parse.quote(raw_word)
   return f'https://en.wiktionary.org/wiki/{word}#Russian'

def request_headers() -> dict:
   hn = [HardwareType.COMPUTER.value]
   user_agent_rotator = UserAgent(hardware_types=hn,limit=20)
   user_agent = user_agent_rotator.get_random_user_agent()
   return {'user-agent': user_agent}

if __name__ == "__main__":
   __version__ = 1.0
   
   # accept word as either argument or on stdin
   try:
      raw_word = sys.argv[1]
   except IndexError:
      raw_word = sys.stdin.read()
      
   url = url_from_ru_word(raw_word)
   headers = request_headers()
   
   try:
      response = urlopen(Request(url, headers = headers))
   except urllib.error.HTTPError as e:
      if e.code == 404:
         print("Error - no such word")
      else:
         print(f"Error: status {e.code}")
      sys.exit(1)
   
   # first extract the Russian content because
   # we may have other languages. This just
   # simplifies the parsing for the headword
   new_soup = extract_russian_soup(response)
            
   # use the derived soup to pick out the headword from
   # the Russian-specific content
   definitions = []
   
   # there are cases (as with the word 'бухта' where there are
   # multiple etymologies. In these cases, the page structure is
   # different. We will try both structures.
   
   for tag in ['h3', 'h4']:
      for h3_or_h4 in new_soup.find_all(tag):
         found = False
         for h3_or_h4_child in h3_or_h4.children:
            if h3_or_h4_child.name == 'span':
               if h3_or_h4_child.get('class'):
                  span_classes = h3_or_h4_child.get('class')
                  if 'mw-headline' in span_classes:
                     span_id = h3_or_h4_child.get('id')
                     # exclude any h3 whose span is not a part of speech
                     if not check_excluded_ids(span_id):
                        found = True
                     break
         if found:
            ol = h3_or_h4.find_next_sibling('ol')
            if ol is None:
               continue
            lis = ol.children
            for li in lis:
               # skip '\n' children
               if li.name != 'li':
                  continue
               # remove any extraneous detail tags + children, etc.
               li = remove_dl_ul(li)
               li_def = li.text.strip()
               definitions.append(li_def)
   definition_list = '; '.join(definitions)
   # if a definition has a single line, remove the ;\s
   definition_list = re.sub(r'^(?:;\s)+(.*)$', '\\1', definition_list)
   # remove "see also" links
   definition_list = re.sub(r'\(see also[^\)]*\)+', "", definition_list)
   print(definition_list)
{{< /highlight >}}

### Usage

The script works flexibly accepting a Russian language word either from `stdin` or as the first argument. For example

{{< highlight bash >}}
echo "собака" | ruendef # or
ruendef "собака"
{{< /highlight >}}

Both print out:

> dog; hound; (derogatory, figuratively) mongrel, cur, bastard (a detestable person); (colloquial, figuratively) fox (a clever, capable person); (Internet) @ (at sign); (computing slang) watchdog timer