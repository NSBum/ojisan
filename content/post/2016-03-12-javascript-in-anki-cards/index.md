---
title: JavaScript in Anki cards
date: 2016-03-12 05:25:05
aliases: [/2016/03/12/JavaScript-in-Anki-cards/]
tags:
- memorization
- programming
- javascript
- anki
- html
- css
categories:
- programming
---
_[N.B. 2016-03-26 Nathan Ifill pointed out that it is possible to use Anki's built-in [conditional replacement](http://ankisrs.net/docs/manual.html#conditional-replacement) feature to do what I'm illustrating. I'll have to work on another example!]_

[Anki](http://ankisrs.net) is a widely-used flashcard application. If you're learning a foreign language and you're not using Anki, you should be.

If you are using Anki and are picky about the appearance of the cards, you should know that JavaScript can be used in the card template. This opens up a number of possibilities for dynamic cards. I'm just touching on the technique here.

In my Russian deck, I sometimes have example sentences in Russian with an English translation. The fields are `sentence_ru` and `sentence_en`. Here's the catch, when a sentence is available, I want the card to display it. When there's not a sentence, I don't want any formatting artifacts on the card. Here's an example of a card with no example sentence:

{{< figure src="images/cardexample.png" title="Example card" >}}

The hyphen separating what should be the Russian and English sentences still appears on the card. Let's fix that. To do that will use JavaScript to detect if a sentence is present and modify the card's HTML if it's not. All of our work will be in the card template definition.

First, we'll define some CSS styling for the sentence fields.

{{< highlight css >}}
span.en {
	font-family: Courier;
	font-size: 16px;
	font-style: italic;
}

span.ru {
	font-family: CourierNew;
	font-size: 16px;
	font-weight: bold;
}
{{< /highlight >}}

Next we'll define the part of the card where the sentence (_if available_) should be displayed.

{{< highlight html >}}
<span id="ru" class="ru">{{sentence_ru}} - </span>   <span id="en" class="en">{{sentence_en}}</span>
{{< /highlight >}}
Now, if we have an example sentence pair, then we'll see a Russian sentence and the English translation separated by a hyphen. To deal with the case where no example sentence is available, we finally get to use some JavaScript. At the bottom of the card side HTML, add a script:

{{< highlight javascript >}}
var content = document.getElementById("ru").innerHTML;
if (content.length < 4) {
	document.getElementById("ru").innerHTML = "";
}
{{< /highlight >}}

This works by looking at the content of the Russian sentence tag. If the length isn't long enough, then we conclude that it's just the spaces and hyphen. So in that case, we just remove all of the content. You'll need to enclose the script in `<script></script>` tags, of course.

Here's what the card without example sentences looks like with our script applied:

{{< figure src="images/cardexample1.png" title="Fixed card" >}}

By adding a sentence pair, we can see that the styling is applied and that the script finds our content and ignores it:

{{< figure src="images/cardexample2.png" title="Fixed card with sentences" >}}

This is a simple example of how JavaScript can be used in an Anki card template. It looks like it could be a very useful way of dynamically styling cards.
