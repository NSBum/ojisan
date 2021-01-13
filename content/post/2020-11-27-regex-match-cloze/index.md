---
title: "Regex to match a cloze"
date: 2020-11-27T11:04:13-05:00
draft: false
authorbox: false
sidebar: false
tags:
- regex
- anki
categories:
- programming
---
Anki and some other platforms use a particular format to signify cloze deletions in flashcard text. It has a format like any of the following:

- `{{c1::dog::}}`
- `{{c2::dog::domestic canine}}`

Here's a regular expression that matches the content of cloze deletions in an arbitrary string, keeping only the main clozed word (in this case _dog_.)

{{< highlight regex >}}
{{c\d::(.*?)(::[^:]+)?}}
{{< /highlight >}}

To see it in action, here it is in action in a Python script:

{{< highlight python >}}
import re

def stripCloze(searchText):
    return re.sub(r'{{c\d::(.*?)(::[^:]+)?}}', r"\1", searchText)

print(stripCloze("The {{c1::passengers::tourist riders}} spotted a breaching {{c2::whale}}."))
{{< /highlight >}}

It should return `The passengers spotted a breaching whale.`