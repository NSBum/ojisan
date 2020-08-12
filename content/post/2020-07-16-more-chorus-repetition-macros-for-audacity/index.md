---
title: "More chorus repetition macros for Audacity"
date: 2020-07-16T08:35:57-04:00
draft: false
authorbox: false
sidebar: false
tags:
- language
- russian
- mac
- audacity
- programming
categories:
- linguistics
---

[In a previous post](2020/07/13/audacity-macros-to-support-chorus-repetition-practice/) I described macros to support certain tasks in generating source material for L2 chorus repetition practice. Today, I'll describe two other macros that automate this practice by slowing the playback speed of the repetition.

### Background

I've [described the rationale](2020/07/13/audacity-macros-to-support-chorus-repetition-practice/) for chorus repetition practice in previous posts. The technique I describe here is to slow the sentence playback speed to give the learner time to build speed by practicing slower repetitions. By applying the `Change Tempo...` effect^[[Change tempo effect](https://manual.audacityteam.org/man/change_tempo.html) in the Audacity manual] in [Audacity](https://www.audacityteam.org/). In my own practice, I will often begin complex Russian sentences at -50% speed and progress to -25% speed before practicing the pronunciation at native-level speed. By practicing at slow speeds, it gives the learner time to appreciate how syllables are connected to each other. The prosody is more apparent.

### Technique

| Num | Command | Explanation |
|-----|---------|-------------|
| 01  | SelectAll: | Select the entire source sentence |
| 02  | ChangeTempo:Percentage="-50" SBSMS="1" | Change the tempo (without altering pitch) by -50% |
| 03  | Select:End="-0.65" Mode="Set" RelativeTo="SelectionEnd" Start="0" | Create an empty 0.65 second region |
| 04  | Silence:Use_Preset="User Preset:650ms" | Add 0.65 seconds of silence |
| 05  | SelectAll: | Select the original clip + the silence |
| 06  | CursSelEnd: | Move the cursor to the end of the new selection |
| 07  | Repeat:Count="5" | Repeat 5 times for a total of six iterations on the track. |

You can see that we've just add a single additional step (02) to the previous iteration generator macro - in this case, reducing the tempo by 50%.

If you want to reduce the speed by only 25%, then you just need to alter the corresponding command 02:

| Num | Command | Explanation |
|-----|---------|-------------|
| 02  | ChangeTempo:Percentage="-25" SBSMS="1" | Change the tempo (without altering pitch) by -25% |

Download the files [Kjellin sentences 50.txt](/attachments/2020/07/16/Kjellin\ sentences\ 50.txt) and [Kjellin sentences 25.txt](/attachments/2020/07/16/Kjellin\ sentences\ 25.txt) and on macOS install them at `~/Library/Application Support/Audacity/Macros`.