---
title: "Scraping Forvo pronunciations"
date: 2022-11-07T05:58:29-05:00
draft: false
authorbox: false
sidebar: false
tags:
- russian
- anki
- python
- webprogramming
- scraping
categories:
- programming
---
Most language learners are familiar with [Forvo](https://www.forvo.com), a site that allows users to download and contribute pronunciations for words and phrases. For my Russian studies, I make daily use of the site. In fact, to facilitate my Anki card-making workflow, I am a paid user of the Forvo API. But that's where the trouble started.

When the [Forvo API](https://api.forvo.com) works, it works _OK_, often extremely slow. But lately, it has been down more than up. In an effort to patch my workflow and continue to download Russian word pronunciations, I wrote this little scraper. I'd prefer to use the API, but experience has shown now that the API is slow and unreliable. I'll keep paying for the API access, because I support what the company does. And as often as not when a company offers a free service, it's likely to be involved in surveillance capitalism. So I'd rather companies offer a reliable product at a reasonable price. 

There are other such projects out in open-source. This project incorporates one interesting feature in that it attempts to rank pronunciations in a scoring system that relies on whether the contributing user is a favourite and how many votes that the pronunciation has gained.[^1]

If you just want to get started with the scraper, it's up on [GitHub](https://github.com/NSBum/forvo_scraper_example). I'm open to pull requests if you have something interesting to contribute, or honestly, you can do whatever you would like with it. I'd appreciate a little acknowledgement if you adopt the code in your own work. 

If you want to stick around and see how I did things, feel free to follow along.

### Approach

This scaper uses [Selenium](https://selenium-python.readthedocs.io) for Python which loads a browser head in order to capture the HTML that we're going to scrape. The idea is to future-proof the script against attempts on behalf of the company to detect script-based access. It was also a chance to learn how to integrate Selenium with [Beautiful Soup 4](https://beautiful-soup-4.readthedocs.io/en/latest/), my go-to scraping technology for Python. First, we're going to need to import those dependencies:

{{< highlight python >}}
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait

from bs4 import BeautifulSoup, element
{{< /highlight >}}

We use command-line arguments in the script, so we will need the `argparse` infrastructure to get our download destination and the word we're researching:

{{< highlight python >}}
import argparse

if __name__ == "__main__":
   prog_desc = "Download pronunciation file from Forvo"
   parser = argparse.ArgumentParser()
   parser = argparse.ArgumentParser(prog=prog_desc)
   parser.add_argument('--dest',
                        help="The directory for download",
                        type=str)
   parser.add_argument('--word',
                        help="Word to research",
                        type=str)

   args = parser.parse_args()
   word = args.word
   dest = args.dest
{{< /highlight >}}

#### Capturing the Forvo page

We're using Selenium to capture the HTML content of the pronunciation list page so that we can analyze it:

{{< highlight python >}}
def get_forvo_page(url: str) -> BeautifulSoup:
   """Get the bs4 object from Forvo page
   
   url: str - the Forvo pronunciation page

   Returns
   -------
   BeautifulSoup 4 object for the page
   """
   driver = webdriver.Safari()
   driver.get(url)
   driver.implicitly_wait(30)
   agree_button = driver.execute_script("""return document.querySelector("button[mode='primary']");""")
   try:
      agree_button.click()
   except AttributeError:
      pass
   try:
      close_button = driver.execute_script("""return document.querySelector("button.mfp-close");""")
      close_button.click()
   except AttributeError:
      pass
   time.sleep(1)
   soup = BeautifulSoup(driver.page_source, 'html.parser')
   return soup
{{< /highlight >}}

_Note that this uses Safari; obviously I'm on macOS, so you can use a different driver if you are on another platform._

Note that that we have to try to respond to privacy and other pop-ups that try to ruin our day. We could probably do it without the JavaScript, but that's what came to me in the moment.

{{< highlight html >}}
<ul class="pronunciations-list pronunciations-list-ru" id=
   "pronunciations-list-ru">
   <li class="pronunciation li-active">
      <!-- detail for this pronunciation -->
   </li>
{{< /highlight >}}

All of the Russian language pronunciations are in the unordered list with the id `pronunciations-list-ru`, so our next task is to find that `ul` element and enumerate it. Fortunately, Beautiful Soup makes that incredible easy:

{{< highlight python >}}
ru_pronunciation_list = soup.find("ul", {"id": "pronunciations-list-ru"})
if ru_pronunciation_list is None:
   exit('ERROR - this word may not exist on Forvo!')
{{< /highlight >}}

Then we can loop over `ru_pronunciation_list` to find all of the pronunciation list items (`li`) and accumulate them as our custom `Pronunciation` objects:

{{< highlight python >}}
pronunciations = []
for li in ru_pronunciation_list.find_all("li"):
   pronunciation = pronunciation_for_li(li)
   pronunciations.append(pronunciation)
{{< /highlight >}}

Next, we'll take a look at what `pronunciation_for_li` does with each of those `<li>` elements:

{{< highlight python >}}
def pronunciation_for_li(element: element.Tag) -> Optional[Pronunciation]:
   """Pronunciation object from its <li> element

   Returns an optional Pronunciation object from a
   <li> element that contains the required info.

   Returns
   -------
   Pronunciation object, or None
   """
   info_span = element.find("span", {"class": "info"})
   if info_span is not None:
      user = user_from_info_span(info_span)
   votes = num_votes_from_li(element)
   url = audio_link_for_li(element)
   if url is not None:
      pronunciation = Pronunciation(user, votes, url)
      return pronunciation
   return None
{{< /highlight >}}

Here we're just extracting vote, username and audio file link from the deeper levels of the hierarchy, which is left as an exercise for the reader. One detail that bears mentioning is how we extract the link to the `.ogg` file. Each pronunciation has a play button with an `onclick` attribute. The JavaScript code provides a base64-encoded value that we can extract. The value is a component of the audio file path that we extract.

#### Ranking pronunciations

As mentioned, we rank pronunciations by two variables - username and the number of votes. But we need a method for ordering them in the `list` of pronunciations. We use `functools.total_ordering` for this.

{{< highlight python >}}
from functools import total_ordering

@total_ordering
class Pronunciation(object):
   def __init__(self, uname:str, positive: int, path: str):
      self.user_name = uname
      self.positive: int = positive
      self.path: str = path
{{< /highlight >}}

By decorating the `Pronunciation` class, we can later use `max` against our list of pronunciations to select that highest rated item. But we do have to implement certain functions required by `total_ordering`:

{{< highlight python >}}
@property
def score(self) -> int:
   subscore = 0
   if self.user_name in FAVS:
      subscore = 2
   return self.positive + subscore
   
def __eq__(self, other):
   if not isinstance(other, type(self)): return NotImplemented
   return self.score == other.score
   
def __lt__(self, other):
   if not isinstance(other, type(self)): return NotImplemented
   return self.score < other.score
{{< /highlight >}}

The scoring algorithm is entirely arbitrary. If you want to give a higher weight to favourite users, that's something you can certainly implement.

#### Selecting a pronunciation

Having implement the comparison functions in the `Pronunciation` class, we can select the one with the highest score:

{{< highlight python >}}
use_p  = max(pronunciations) if len(pronunciations) > 1 else pronunciations[0]
{{< /highlight >}}

And that's it! I hope this example is helpful to you. If you have the means, and if the Forvo API improves _a lot_ using that would be the most ethical way to automate the process of grabbing pronunciations. But until then, here's an alternative. If you have questions, I'm not on Twitter[^2] so please just use my [contact page](http://www.shortwhale.com/NSBum).

[^1]: Of course the later variable is not entirely reliable because the oldest pronunciations will have had the longest opportunity to garner votes; but the idea is that we can at least look to our favourites as a way of nudging the choice in the desired direction.
[^2]: I refuse to be part of Elon Musk's attempt to impose his authoritarian world-view through his acquisition of Twitter. I have no accounts on the platform.