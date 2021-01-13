---
title: "Typing Russian stress marks on macOS"
date: 2020-10-19T05:06:59-04:00
draft: false
authorbox: false
sidebar: false
tags:
- linguistics
- macos
- russian
categories:
- russian
---
While Russian text intended for native speakers doesn't show accented vowel characters to point out the syllabic stress {{< russian >}}(ударение){{< /russian >}}, many texts intended for learners often do have these marks. But how to apply these marks when typing? 

Typically, for Latin keyboards on macOS, you can hold down the key (like long-press on iOS) and a popup dialog will show you options for that character. But in the standard Russian phonetic keyboard it doesn't work. Hold down the e key and you'll get the option for the letter {{< russian >}}ë{{< /russian >}} (yes, it's regarded as a separate letter in Russian - the essential but misbegotten {{< russian >}}ë{{< /russian >}}.)  

So there's the problem. Stress marks[^1] are occasionally needed but are nearly impossible to type.

### Solution

The solution is a little complicated and it requires some modifications to the instructions [noted here](https://ask.metafilter.com/248193/How-can-I-type-stress-marks-on-Mac-OS-using-the-Russian-keyboard) on Ask Metafilter. 

Here are the steps to follow:

1. [Download](https://www.dropbox.com/s/74vssudf98svya7/Russian%20-%20Phonetic%20Accents.keylayout) the `.keylayout` file `Russian - Phonetic Accents.keylayout` from this guy's public Dropbox. If the idea of that creeps you out and you trust me slightly more, or if that link goes down, you can [download it from my site](/attachments/2020/10/19/Russian-Phonetic-Accents.keylayout).
2. Move this `.keylayout` file to `~/Library/Keyboard Layouts`. You will need to authenticate as an Administrator for this computer. Alternatively, you can download the key layout modification application [Ukulele](http://scripts.sil.org/cms/scripts/page.php?site_id=nrsi&id=ukelele), install it and use it to open the "Russian - Phonetic Accents.keylayout" file that you downloaded in step one and then use Ukulele to install the keyboard. If you don't completely know your way around macOS then that might be a safer approach. Either way, you may have to restart or log out and log in for this to take effect.
3. Go to `System Preferences` > Keyboard > Input Sources
4. Click the (+) button to add a keyboard layout. Scroll down to the bottom of the list of languages to find "Others"
5. Click on "Others" and you'll see the new keyboard. Install it be clicking "Add".
6. If you type in both Russian and English, then you probably already have the input menu displayed in the menu bar, but if not, it's activated at `System Preferences` > Keyboard > Input Sources and select "Show Input menu in menu bar." Now you should be see all of your input sources in the keyboard and character menu bar item:

![](/images/2020/10/19/InputSource.png)

7. To type a character with stress marks, just type ⌥ + ', that's option-apostrophe followed by the Russian vowel that you when to mark.

### Alternative

There is a slightly more cumbersome alternative approach to going(nearly) straight to the Unicode character your intend to type. But if you only rarely need to input these stress-marked vowels, it might be worth exploring. Here are the steps:

1. If you don't have the input menu displayed in the menu bar, you'll need to activate it now by going to `System Preferences` > Keyboard > Input Sources and selecting "Show Input menu in menu bar."
2. Now from the Input menu, select "Show Emoji & Symbols."
3. Select the ⚙ button at the top left. > "Customize List..."
4. Select Code Tables > Unicode
5. Now when you want to add a stress mark on a vowel, return to the character menu (Input menu, select "Show Emoji & Symbols"), select `Unicode` > `00000300 Combining Diacritical Marks` and find row "0300". Drag glyph 0301 (the second one in on that row) to a location just _after_ the vowel you want to mark.



[^1]: I somewhat loosely interchange the terms _"accented characters"_ and _"stress marks"_. Although they change the pronounciation of vowels like accents in languages such as French, it's only because they indicate the syllabic stress location {{< russian >}}ударение{{< /russian >}} in the word and _that_ in turn changes the pronunciation. It's not an entirely pedantic point so I've used the terms interchangeably.

If you encounter any problems, feel free to [contact me](http://www.shortwhale.com/NSBum) and I can talk you through the process.

### References

- ["How can I type stress marks on Mac OS using the Russian keyboard?"](https://ask.metafilter.com/248193/How-can-I-type-stress-marks-on-Mac-OS-using-the-Russian-keyboard) - The second to last answer from pmdboi at 11:30 PM on September 9, 2013 has the outline of the first approach above.
- [Ukulele](http://software.sil.org/ukelele/) - Keyboard layout modification application.
- [Cyrillic script in Unicode](https://en.wikipedia.org/wiki/Cyrillic_script_in_Unicode) - this Wikipedia article notes the combining diacritical marks using `U+0301`.
- [Applying stress marks on macOS through morphological analysis](/2020/09/24/a-macos-text-service-for-morphological-analysis-and-in-situ-marking-of-russian-syllabic-stress/) - if you just want to take arbitrary text and mark the stress based on morphological analysis, then this piece that I wrote might help.
- [Stress (linguistics)](https://en.wikipedia.org/wiki/Stress_(linguistics)) - Everything that you wanted to know about linguistic stress. The section on [Spelling and notation for stress](https://en.wikipedia.org/wiki/Stress_(linguistics)#Spelling_and_notation_for_stress) is worth looking at because the linguistics convention and practice for marking stress in Russian, Ukrainian and Belarussian differs. This section also talks about how secondary stress is marked.