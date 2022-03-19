---
title: "Automating the handling of bank and financial statements"
date: 2022-03-19T06:57:23-04:00
draft: false
authorbox: false
sidebar: false
tags:
- applescript
- perl
- bash
- commandline
- cli
- hazel
- devonthink
categories:
- programming
---
In my perpetual effort to get out of work, I've developed a suite of automation tools to help file statements that I download from banks, credit cards and others. While my setup described here is tuned to my specific needs, any of the ideas should be adaptable for your particular circumstances. For the purposes of this post, I'm going to assume you already have [Hazel](https://www.noodlesoft.com). None of what follows will be of much use to you without it. I'll also emphasize that this is a macOS-specific post. Bear in mind, too, that companies have the nasty habit of tweaking their statement formats. That fact alone makes any approach like this fragile; so be aware that maintaining these rules is just part of the game. With that out of the way, let's dive in.

### Overview

The goal is to download a file from my bank and automatically rename the file in a consistent way with the month and year of the statment embedded in the filename. Then I'd like to apply DEVONthink tags and place the file into the right group in DEVONthink.

A caveat here is that this solution assumes there is text in the pdf. If you are working with an image-based pdf, there are additional steps that I'll describe in a future post. 

### Pre-requisites

You will need the Poppler library because the script relies on `pdftotext` in that library. You can use Homebrew or MacPorts. I use Homebrew:

{{< highlight bash >}}
brew install poppler
{{< /highlight >}}

### First Hazel rule - renaming the downloaded file

The statement download file from one of my banks is named _list.pdf_ which is a ridiculously ambiguous name, but the means we need to do a little extra work in the Hazel criteria to match the file. We can (and do) match on the extension `pdf` and on the name to contain _list_, but this will mean processing any unrelated stray file in `~/Downloads` that happens to have the same name.

So to add a margin of safety, we will add a criterion to match something from the content.

#### Matching pdf content in Hazel rule criteria

First, take a look at the pdf text content:

{{< highlight bash >}}
pdftotext "test.pdf" -
{{< /highlight >}}

This will give us all of the lines from the text of the file; and we can scroll through that content to find a suitable matching line.

Let's say that my bank is _Beaver Bank and Trust_. Then we should expect to find _Beaver_ in the text. From the command line, this would just be:

{{< highlight bash >}}
pdftotext "test.pdf" | grep -q "Beaver"
{{< /highlight >}}

If the word _Beaver_ appears in the text, then our return code is `0`, otherwise it's `1` - exactly what we need for a shell script-based Hazel criterion.

So our Hazel rule criteria will be:

1. Extension `is` pdf
2. Name `contains` list
3. Passes shell script → embedded script

The embedded script for the last criterion is just `pdftotext "$1" | grep -q "Beaver"`. (Of course, yours won't be "Beaver" but whatever you use to uniquely identify what kind of document you're dealing with.)

#### Processing the document in Hazel

Now that we've matched the document as our statement of interest, we can rename it.

First, we do a second check against another predictable piece of content. Let's say Beaver Bank and Trust offers some kind of reward points. So we expect to find "POINTS SUMMARY" somewhere in the text. The first part of our processing, then is to check for that in the content:

{{< highlight bash >}}
fn="$1"
unset flag; unset new_fn; shopt -s lastpipe;
flag=0
parentdir="$(dirname "$fn")"
pdftotext $fn - | while read -r line ; do
   if echo "$line" | grep -q 'POINTS SUMMARY'; then
      flag=1
      break
   fi
done

# exit if the required "POINTS SUMMARY" not found
[ $flag -ne 1 ] && exit -1
{{< /highlight >}}

A word about the `shopt -s lastpipe` directive: There is a slightly obscure issue with variable scope in the script above. The issue is that when we pipe the results of `pdftotext` to the `while` loop, that is executed in a separate shell[^1]; so `flag` in this new shell is a separate variable. Since we need `flag` in the outer scope, then we set the `lastpipe` option.

Next, we begin the work of actually extracting variable information - mainly the date - from the pdf content. Here, I can only point you to a generic approach because your content will differ.

{{< highlight bash >}}
# do this again but start looking for amount
# after "Opening/Closing Date"
flag=0
pdftotext $fn - | while read -r line ; do
   if echo "$line" | grep -q "Opening/Closing Date"; then
      flag=1
      idx=0
   fi
   # only start looking for amount after the line "Opening/Closing Date"
   ( [ $flag -eq 1 ] && [ $idx -eq 2 ] ) && break || ((idx++))
done
{{< /highlight >}}

This part is a little cumbersome. There are many dates in the content but we are looking for a specific date range that follows the line "Opening/Closing Date". Once again, we loop through the output of `pdftotxt`, this time looking for the "Opening/Closing Date" line. Once found, we set a `flag`. Now, there's always a blank line after the "Openinb/Closing Date" line, so we're not looking for _next_ line but for the one after that. So we keep looking for the line that appears after the flag is set and which has an index of 2 once we've found the target line. Now the `$line` contains the date range we are interested in, which is in the format _02/12/22 - 03/11/22_.

The rest of the script extracts the closing date from this range:

{{< highlight bash >}}
date=$(echo $line | cut -f2 -d'-' | xargs | tr '/' ' ')
read mo day yr<<<$date
std_day="20$yr-$mo-$day"

# derive month name from the integer month number
mo_name=$(date -jf %F $std_day '+%b')
title="20$yr$mo$day Beaver Bank - $mo_name 20$yr [38.01].pdf"

new_fn="$parentdir/$title"
#echo $new_fn; exit 0
mv "$fn" "$new_fn"
{{< /highlight >}}

The extraction of the closing data is the most interesting part of the script. There are possibly easier ways of doing this but the lines that follows are what came to mind:

{{< highlight bash >}}
date=$(echo $line | cut -f2 -d'-' | xargs | tr '/' ' ')
read mo day yr<<<$date
{{< /highlight >}}

The first `cut` saves everything after the '-' character. Then we strip the whitespace with `xargs`. Finally `tr` the '/' characters into spaces. The next line splits the `date` variable on the `IFS` into the data component variables.

The other interesting part about the last half of the script is the conversion of the month number to the month name which we do with a specific `date` incantation:

{{< highlight bash >}}
mo_name=$(date -jf %F $std_day '+%b')
{{< /highlight >}}

Finally, the `mv` changes the file name to our standardized meaningful name.

### Second Hazel rule - moving the file into DEVONthink Pro

Although this could be rolled into the first rule, I've kept them separate for ease of debugging.[^2] I won't go into all of the matching/criteria details this time, because we now have a pdf named with a controlled vocabulary that makes it easy to match.

The heart of this script is an AppleScript to move the pdf into a specific group into DEVONthink Pro. If you don't use this application, then you're done, and the pdf can just be handled/filed wherever you like.

If you _do_ use DEVONthink (DT3) then the next rule's action is for you. I'll present it without a lot of commentary.

{{< highlight applescript >}}
tell application id "DNtp"
   launch
   open database "/Users/alan/Documents/Databases/leviathan.dtBase2"
   set dbs to first database whose name is "leviathan"
   set groupPath to "/30-39 Finance/38 Credit cards/38.01 Beaver Bank/"
   set targetGroup to get record at groupPath in dbs
   set theFile to POSIX path of (theFile as alias)
   set theRecord to import theFile to targetGroup
   -- set the label to "to do" so we know to work with it in DT3
   set the label of theRecord to 1
end tell
{{< /highlight >}}

Lastly, once exported, one last shell script action gets rid of the now-imported file:

{{< highlight bash >}}
rm $1
{{< /highlight >}}

And that's it. I hope this has been helpful in showing how this sort of automation can be done. Having familiarity with `sed`, `grep`, `cut`, `awk`, `tr` and friends can definitely make your life easier when dealing with these sorts of tasks. And `pdftotext` is a great tool to have in the back pocket too. 

At some point I'll get around to how I deal with files that have no text. I promise, it's an interesting story.


[^1]: This is discussed in the `bash` `man` [page](https://linux.die.net/man/1/bash) under the section _"Pipelines"_.
[^2]: Debugging Hazel rules is not easy. Occasionally you can find interesting information in the logs, but often there's almost nothing to go on. "Caveman debugging" is often the only way to get anything useful.
