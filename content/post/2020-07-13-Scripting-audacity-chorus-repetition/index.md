---
title: "Audacity macros to support chorus repetition practice"
date: 2020-07-13T09:20:59-04:00
draft: false
authorbox: false
sidebar: true
tags:
- language
- russian
- mac
- audacity
- programming
categories:
- linguistics
---

Achieving fluid, native-quality speech in a second language is difficult task for adult learners. For several years, I've used Dr. Olle Kjellin's method of "chorus repetition" for my Russian language study. In this post, I'm presenting a method for scripting Audacity to facilitate the development of audio source material to support his methodology.

## Background

For detailed background on the methodology, I refer you to Kjellin's [seminal paper](https://www.dropbox.com/s/g6hkeepygfsi5vi/Kjellin-Practise-Pronunciation-w-Audacity.pdf?dl=0) _"Quality Practise Pronunciation with Audacity - The Best Method!"_ on the subject of chorus repetition practice. The first half of the paper outlines the neurophysiologic rational for the method and the second half describes the practical use of the cross-platform tool [Audacity](https://www.audacityteam.org/) to generate source material for this practice.

## Rationale for this project

Preparing source material (sentences of about 2 seconds duration) for this method is not difficult, but the steps are repetitive. Fortunately Audacity offers the ability to script its behaviour through macros (`Tools → Macros...`). Two macros are described here. Neither are complex, but they do chain common commands in Audacity, making it faster to produce material for chorus repetition. The first macro just trims silence from the clip and compresses its dynamic range. The second takes a clip, ideally a single sentence, adds 0.65 seconds of silence at the end, then replicates the clip + the silence 5 times for a total of 6 repetitions.

## Macros

### Truncate and compress

| Num | Command          | Parameters                                                                                                    |
|-----|------------------|---------------------------------------------------------------------------------------------------------------|
| 01  | Select All       |                                                                                                               |
| 02  | Truncate Silence | Action="Truncate Detected Silence" Compress="50" Independent="0" Minimum="0.5" Threshold="-20" Truncate="0.5" |
| 03  | Compressor       | AttackTime="0.2" NoiseFloor="-40" Normalize="1" Ratio="2" ReleaseTime="1" Threshold="-12" UsePeak="0"         |

To install this macro, [download](https://gist.github.com/NSBum/c12aaf6a17edfba5b44fb5948f6ba809) the file (`Download ZIP`.) On macOS, you can move the file to `~/Application Support/audacity/Macros`. I'm not sure where it goes on other platforms; check the manual.

To use the macro, start with the sentence clip you want to process and invoke `Tools → Apply Macro → TruncateAndCompress`. 

You can play around with different parameters if you need to trim more or less silence or if you want to change the compressor settings.

### Kjellin Sentences

This macro will take a prepared clip, ideally a single sentence and create six total iterations with 650 ms of silence between each iteration.


| Num | Command | Explanation |
|-----|---------|-------------|
| 01  | SelEnd: | Move the selection point to the end |
| 02  | Select:End="-0.65" Mode="Set" RelativeTo="SelectionEnd" Start="0" | Create an empty 0.65 second region |
| 03  | Silence:Use_Preset="User Preset:650ms" | Add 0.65 seconds of silence |
| 04  | SelectAll: | Select the original clip + the silence |
| 05  | CursSelEnd: | Move the cursor to the end of the new selection |
| 06  | Repeat:Count="5" | Repeat 5 times for a total of six iterations on the track. |

To install the macro, download it from the [following location](https://gist.github.com/NSBum/1bca6b07926a3cc3cea353e980c9b15d) using `Download ZIP`, decompress and place in the `Macros` directory as above.

You will need one additional step before this is usable. You will need to create a user preset for the Generate silence tool. Navigate to `Generate → Silence...` and create a preset named "_650ms_" so that the macro can use it.

Again, to use it, just prepare a track with a single sentence you wish to use and then `Tools → Apply Macro → KjellinSentences`.

Enjoy and keep practicing!
