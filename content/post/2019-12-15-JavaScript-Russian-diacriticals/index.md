---
title: "Stripping diacriticals from Russian text"
date: 2019-12-15T05:08:09-05:00
draft: false
sidebar: false
summary: "A method for stripping diacritical markings from Russian text."
categories:
- programming
tags:
- russian
- javascript
---
While you seldom find diacritical markings in Russian text outside of that intended to help young readers or language learners, you occasionally have to deal with these markings. Here is a method to deal with it.

{{< highlight javascript >}}
const str = "Он горева́л по по́воду сме́рти лу́чшего дру́га."
var res = str.normalize("NFD").replace(/[\u0300-\u036f]/g, "")
document.getElementById("demo").innerHTML = `Original: ${str} | Stripped: ${res}`
{{< /highlight >}}

Output: Original: Он горева́л по по́воду сме́рти лу́чшего дру́га. | Stripped: Он горевал по поводу смерти лучшего друга.
