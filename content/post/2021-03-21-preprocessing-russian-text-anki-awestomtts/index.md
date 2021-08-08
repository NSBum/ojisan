---
title: "Pre-processing Russian text for the AwesomeTTS add-on in Anki"
date: 2021-03-21T20:36:52-04:00
draft: false
authorbox: false
sidebar: false
tags:
- anki
- russian
- linguistics
categories:
- anki
---
The Anki add-on [AwesomeTTS](https://ankiweb.net/shared/info/1436550454) has been a vital tool for language learners using the Anki application on the desktop. It allows you to have elements of the card read aloud using text-to-speech capabilities. The new developer of the add-on has added a number of voice options, including the Microsoft Azure voices. The neural voices for Russian are quite good. But they have one major issue, syllabic stress marks that are sometimes seen in text intended for language learners cause the Microsoft Azure voices to grossly mispronounce the word.

For example, the sentence {{< russian >}}Цензу́ра потака́ет извращённому уму́ больше, чем сло́во из трёх букв само́ по себе.{{< /russian >}} is incorrectly pronounced because it has stress marks _and_ because the letter {{< russian >}}ë{{< /russian >}} is _correctly_ displayed. Apparently Microsoft Azure doesn't like it when {{< russian >}}ë{{< /russian >}} is correctly rendered.

Fortunately, there's a text pre-processor built into the plugin. Here is how to use this pre-processor to change the text that's fed to the TTS provider:

![](/images/2021/03/22/settings.png)

In the add-on configuration view, navigate to Text → Advanced and add two rules:

1. The first rule basically just strips the Unicode accent grave character (U+0301) from any vowels.
2. The second rule transliterates {{< russian >}}ë{{< /russian >}} to {{< russian >}}e{{< /russian >}}. Yes, it offends me to do this because they are two different letters in the Russian alphabet, but it appears that the models were trained on text written in the way that's often encountered, unfortunately.

With those two rules in place, the pronounciations going to Microsoft Azure should be correct.
