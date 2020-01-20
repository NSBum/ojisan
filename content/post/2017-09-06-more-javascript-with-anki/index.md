---
title: More Javascript with Anki
date: 2017-09-06 20:56:24
aliases: ['/2017/09/06/More-Javascript-with-Anki/']
tags:
- javascript
- anki
- memorization
- css
categories:
- anki
---
I [wrote a piece](/2016/03/12/JavaScript-in-Anki-cards/) previously about using JavaScript in Anki cards. Although I haven't found many uses for employing this idea, it does come up from time-to-time including a recent use-case I'm writing about now.

After downloading a popular [French frequency list deck](https://ankiweb.net/shared/info/893324022) for my daughter to use, I noticed that it omits the gender of nouns in the French prompt. In school, I was always taught to memorize the gender along with the noun. For example, when you memorize the word for law, _"loi"_ you should mermorize it with either the definite article _"la"_ or the indefinite article _"une"_ so that the feminine gender of the noun is inseparable from the noun itself. But this deck has only the noun prompt and I was afraid that my daughter would fail to memorize the noun's gender. JavaScript to the rescue.

Since the gender _is_ encoded in a field, we can capitalize on that to insert the right article. My preference is to use the definite articles _"le"_ or _"la"_ where possible. But it gets increasingly complex from there. Nouns that begin with a vowel such as _"avocat"_ require _"l'avocat"_ which obscures the gender. In that case, I'd prefer the indefinite article _"un avocat"_. Then there's the _"h"_. Most words beginning with _"h"_ behave like those with vowels. But some words have [_h aspiré_](https://en.wikipedia.org/wiki/Aspirated_h). With those words, we keep the full definite article without the apostrophe.

So we start with a couple easy preliminaries, such as detecting vowels:

{{< highlight javascript >}}
//	returns true if the character
//	is a vowel
function vowelTest(s) {
   return (/^[aeiou]$/i).test(s);
}
{{< /highlight >}}

Now we turn our attention to whether a words _would_ need an apostrophe with the definite article. I'm not actually going to use the apostrophe. Instead we'll fall back to the indefinite article _"un/une"_ in this case.

{{< highlight javascript >}}
// returns true if the word would need
// an apostrophe if used with the
// definite article
function needsApostrophe(str) {
    if(str[0]=='h') {
        //	h words that do not need apostrophe
        var aspire = ["hache","hachisch","haddock","haïku",
            "haillon","haine","hall",
            "halo","halte","hamac",
            "hamburger","hameau","hammam",
            "hampe","hamster","hanche",
            "hand-ball","handicap","hangar",
            "harde","hareng","hargne",
            "haricot","harpail","harpon",
            "hasard","hauteur","havre","hère",
            "hérisson","hernie","héron",
            "héros","herse","hêtre",
            "hiatus","hibou","hic",
            "hickory","hiérarchie","hiéroglyphe",
            "hobby","Hollande","homard",
            "Hongrie","honte","hoquet",
            "houe","houle","hooligan",
            "houppe","housse","houx",
            "houblot","huche","huguenot"
            ];
        return (aspire.indexOf(str) == -1);
    }
    return vowelTest(str[0]);
}
{{< /highlight >}}

Now we can wrap this up into a function that adds an article, either definite or indefinite to the noun:

{{< highlight javascript >}}
//	adds either definite or indefinite article
function addArticle(str,genderstr) {
    if( needsApostrophe(str) ) {
       return (genderstr == "nm" ) ? "un " + str : "une " + str;
    }
       return (genderstr == "nm") ? "le " + str : "la " + str;
}
{{< /highlight >}}


The first step is to make sure that the part of speech field is visible to the script. We do this by inserting it into the card template.

{{< highlight html >}}
<span id="pos">{% raw %}{{Part of Speech}}{% endraw %}</span>
{{< /highlight >}}

Don't worry, we'll hide it in a minute.

Then we can obtain the contents of the field and add the gender-specific article accordingly.

{{< highlight javascript >}}
var content = document.getElementById("pos").innerHTML;
var fword = document.getElementsByClassName("frenchwordless")[0].innerHTML;
artword = addArticle(fword,content);
document.getElementsByClassName("frenchwordless")[0].innerHTML=artword;
{{< /highlight >}}

And we can hide the gender sentinel field:

{{< highlight javascript >}}
var content = document.getElementById("pos").style.visibility = "hidden";
{{< /highlight >}}

Ideally, French Anki decks would be constructed in such a way that the gender is embedded in the noun to be memorized, but with a little creative use of JavaScript, we can retool it on-the-fly.
