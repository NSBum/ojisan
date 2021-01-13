---
title: "Removing stress marks from Russian text"
date: 2020-11-27T09:10:26-05:00
draft: false
authorbox: false
sidebar: false
tags:
- russian
- python
- nlp
- linguistics
- python
- cyrillic
categories:
- programming
---
Previously, I wrote about [adding syllabic stress marks]() to Russian text. Here's a method for doing the opposite - that is, removing such marks (ударение) from Russian text. 

Although there may well be a more sophisticated approach, regex is well-suited to this task. The problem is that 

{{< highlight perl >}}
def string_replace(dict,text):
   sorted_dict = {k: dict[k] for k in sorted(dict)}
   for n in sorted_dict.keys():
      text = text.replace(n,dict[n])
   return text

dict = { "а́" : "а", "е́" : "е", "о́" : "о", "у́" : "у",
      "я́" : "я", "ю́" : "ю", "ы́" : "ы", "и́" : "и",
      "ё́" : "ё", "А́" : "А", "Е́" : "Е", "О́" : "О",
      "У́" : "У", "Я́" : "Я", "Ю́" : "Ю", "Ы́" : "Ы",
      "И́" : "И", "Э́" : "Э", "э́" : "э"
   } 
   
print(string_replace(dict, "Существи́тельные в шве́дском обычно де́лятся на пять склоне́ний."))
{{< /highlight >}}

This should print: {{< russian >}}Существительные в шведском обычно делятся на пять склонений.{{< /russian >}}