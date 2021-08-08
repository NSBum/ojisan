---
title: "Extending the Anki Cloze Anything script for language learners"
date: 2021-04-16T03:45:33-04:00
draft: false
authorbox: false
sidebar: false
tags:
- anki
- russian
- programming
- javascript
categories:
- anki
---
It's possible to use cloze deletion cards within standard Anki note types using the Anki Cloze Anything setup. But additional scripts are required to allow it to function seamlessly in a typical language-learning environment. I'll show you how to flexibly display a sentence with or without Anki Cloze Anything markup and also not break AwesomeTTS.

### Anki's built-in cloze deletion system

The built-in cloze deletion feature in Anki is an excellent way for language learners to actively test their recall. For example, a cloze deletion note type with the following content requires the learner to supply the missing word:

{{< figure src="images/2021/04/16/note_fields.jpg">}}

This will render the front side as:

{{< figure src="images/2021/04/16/cloze_render_front.jpg">}}

and the reverse side will be rendered as:

{{< figure src="images/2021/04/16/cloze_render_back.jpg">}}

But the greatest weakness of the built-in cloze deletion feature is that the only way to generate cloze deletion cards is to use the cloze deletion note type; and it is not possible to generate cloze deletion cards from other note types. This introduces an inefficiency for language learners. Often we use example sentences in straight vocabulary notes as an aid to using the word in context. I use example sentences that appear on the back side of the card. It would be ideal if I could create a card type within my standard vocabulary notes that generates a cloze card with the example sentence. Otherwise, I am forced to create a separate cloze deletion note for my example sentence if I want to also test on that sentence. This is the problem that Anki Cloze Anything solves.

### Anki Cloze Anything

In its simplest form, this is a script that allows you to use cloze deletion card types in a regular note. Instead of Anki's typical `{{c1:somecloze}}` markup, it uses `((c1::somecloze))` style markup, but in most respects works the same as the built-in system. Anki Cloze Anything also has an add-on that addresses some workflow efficiency needs; but it will work just fine with only the Javascript on the card template.

However, because Anki Cloze Anything requires that I use a particular markup for the sentences, I can no longer display the same sentence on another card type. Using the example above, if I have a vocabulary card for {{< russian >}}перевязать{{< /russian >}} then I'd like to have an illustrative sentence on the the back of my card, {{< russian >}}Она перевяза́ла упако́вку шпагатом.{{< /russian >}}. But Anki Cloze Anything requires me to commit to something like: {{< russian >}}Она ((c1::перевяза́ла)) упако́вку шпагатом.{{< /russian >}} if I also want to use the same sentence in a cloze-type note. Unless I modify my standard card template, then my sentence will display with the Anki Cloze Anything markup.

Essentially, what Anki Cloze Anything does for me is that it allows me to use a single illustrative sentence as both an example sentence on the back of a standard vocabulary card _and_ to be a cloze sentence at the same time. It saves time by not requiring me to add sentences twice (once to my standard vocabulary card and again to a cloze deletion card.)

{{< figure src="images/2021/04/16/dual_use.png" >}}

But this idea only works if I can display (and pronounce) the sentence in the correct way on the correct card. This is where the two-fold solution described below comes into play.

### Enhancing the Anki Cloze Anything template

If I want to display a sentence containing Anki Cloze Anything markup on a standard (non-cloze) card type, then I have to strip out the markup. Fortunately, jQuery makes this easy. Assume I have the following on my standard card template:

{{< highlight html>}}
<!-- if an example sentence is available, show it -->
{{#sentence_ru}}
   <hr/>
   <div style="padding-left:10px;, padding-right:10px;">
      <span class="rusentence">
         {{sentence_ru}}
      </span> - <span class="ensentence smaller">{{sentence_en}}</span>
   </div>
{{/sentence_ru}}
{{< /highlight >}}

If the `span` class `rusentence` contains a sentence with Anki Cloze Anything markup, then I need to strip away the markup when the standard card displays; so I just need a script to address that:

{{< highlight javascript >}}
$('span.rusentence').each(function() {
   var text = $(this).text();
   text = text.replace(/\({2}c\d::([^\0]+)\){2}/g, "$1");
   text = text.replace(new RegExp('`', 'g'),"")
   $(this).text(text);
});
{{< /highlight >}}

If you enclose this between `<script>...</script>` tags in the standard note template, then the sentence will display normally, while still allowing you to use the same sentence in a different Anki Cloze Anything card type.

### But what about AwesomeTTS

Many language learners use AwesomeTTS, an add-on that provides text-to-speech capabilities to Anki cards. However, using AwesomeTTS on an Anki Cloze Anything card doesn't work as intendeded, because it just reads the text with the markup. How to fix this?

Fortunately, AwesomeTTS has a text preprocessor that allows you to apply regular expressions (regex) to the text before it feeds the text to the TTS service. The functionality is at Toos → AwesomeTTS → Configuration → Text → Advanced. From there, add a text replacement rule:

{{< figure src="images/2021/04/16/atts.png" >}}

The rule `\({2}c\d::(.+)\){2}` → `\1` is very similar to the Javascript we used above in the template. With this text-replacement rule in place, AwesomeTTS now reads the sentence correctly even if it contains Anki Cloze Anything markup.

### Caveats

The regex described here doesn't account for the hint markup feature of Anki Cloze Anything. I'll have to work on that at some point.

### References

- [Anki Cloze Anything - Github repository](https://github.com/matthayes/anki_cloze_anything)
- [Anki Cloze Anything - instructions](https://github.com/matthayes/anki_cloze_anything/blob/master/docs/INSTRUCTIONS.md) - Incorporating Anki Cloze Anything in your own custom notes.
- [Cloze deletion - Anki manual](https://docs.ankiweb.net/#/editing?id=cloze-deletion) - Anki's built-in cloze deletion system
