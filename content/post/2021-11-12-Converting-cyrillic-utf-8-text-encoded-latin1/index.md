---
title: "Converting Cyrillic UTF-8 text encoded as Latin-1"
date: 2021-11-12T11:36:02-05:00
draft: false
authorbox: false
sidebar: false
tags:
- cli
- bash
- russian
- utf8
- unicode
categories:
- programming
---
This may be obvious to some, but visually-recognizing character encoding at a glance is not always obvious. 

For example, pronunciation files downloaded form Forvo have the following appearance:

`pronunciation_ru_Ð¾ÑÐ±ÑÐ²Ð°Ð½Ð¸Ðµ.mp3`

How can we extact the actual word from this gibberish? Optimally, the filename should reflect that actual word uttered in the pronunciation file, after all.

### Step 1 - Extracting the interesting bits

The gibberish begins after the `pronunciation_ru_` and ends before the file extension. Any regex tool can tease that out.

This is what I did in the shell:

{{< highlight bash >}}
echo $fn | perl -CSD -pe 's/pronunciation_ru_(.*)\.mp3/$1/gm;'
{{< /highlight >}}

Now we have are left with `Ð¾ÑÐ±ÑÐ²Ð°Ð½Ð¸Ðµ` and the question of what kind of strange encoding this is.

### Step 2 - Figuring out character encoding

Obviously, this uses some Latin character set. Since the Russian language does not, we have some work to do. The task of unraveling this is easier when you can visualize the hex character codes laid out. A simple Python script makes that easy:

{{< highlight python >}}
#!/usr/bin/env python3

word = 'Ð¾ÑÐ±ÑÐ²Ð°Ð½Ð¸Ðµ'

print(":".join("{:02x}".format(ord(c)) for c in word))
{{< /highlight >}}

Running this little script, we see `d0:be:4e:303:82:d0:b1:4e:303:8b:d0:b2:d0:b0:d0:bd:d0:b8:d0:b5`.

Immediately we can begin to discern a pattern - lots of `D0` codes followed by something else. It's beginning to look like Unicode. So, on macOS, I fired up the character viewer from the menu bar and drilled down to the Cyrillic (or Unicode) section. Lookup any Cyrillic character, for example {{< russian >}}ж{{< /russian >}}:

{{< figure src="images/2021/11/12/unicode_something.png" class="left" >}}

Aha! The Cyrillic range in includes characters whose first byte is `D0`, so now it's just a matter of lining up 2 byte groups and reading it as UTF-8. So the first character would be `D0 BE` - which, according to the table, is a lower case Cyrillic {{< russian >}}o{{< /russian >}}

However, one complication remains. What is happening when the sequence is broken? There is an interruption in the two-byte reading frame that begins with the sequence `4e:303:82` then happens again with the sequence `4e:303:8b`? The first step is to figure out the common portion `4e:303`. Back to the character viewer table, we find `4E` is the Latin capital letter N. So what about 303? Using the search feature of the Character Viewer, we easily see that U+0303 is a combining tilde. It's a symbol that combines with the character that immediately precedes it. So what we have is not just Cyrillic UTF-8 characters encoded in Latin symbols, but with the additional oddity of a composed `Ñ` character. It we search for _that_ character, we find that it is `D1`. So, the sequence isn't really interrupted; it's just an issue of how `Ñ` is comprised.

### Step 3 - Reading `N` + combining tilde as `u'\u00D1'`

This just requires substituting one UTF-8 sequence for another. In Python, this will work:

{{< highlight python >}}
# strange issue where Ñ (\u00D1) is intended
# but is encoded as N + tilde. Obviously this 
# is meaningless in terms of UTF-8 encoding
# but we have to deal with it before the decoding
# takes place.
word = word.replace(u'\u004E\u0303',u'\u00D1')
{{< /highlight >}}

### Step 4 - Putting it all together

After correcting the odd `Ñ` composition, we can simple decode the text as UTF-8, but we have one little twist first. `.decode('utf8')` requires a sequence of bytes (`class <bytes>`) not a string. So we have to make a trip through encoding in 'latin1' first, then decode it to UTF-8.

{{< highlight python >}}
tr_word = word.encode('latin1').decode('utf8')
{{< /highlight >}}

#### rfndecode - a Python script to decode this form of encoding

{{< highlight python >}}
#!/usr/bin/env python3

# 
# rfndecode
#
# When downloading files from Forvo, we get file
# names that look like: .ÐºÐ¾Ñ.mp3
# This puts the text into ordinary utf-8
#
# Input: Text to translate as argument or 
#        on stdin
# Output: Re-encoded text
#

import sys

# accept word as either argument or on stdin
try:
   word = sys.argv[1]
   except IndexError:
      word = sys.stdin.read()

      # check if this word is in the expected encoding
      if word.find(u'\u00D0') == -1:
         print(word.strip())
            exit()

               # strange issue where Ñ (\u00D1) is intended
               # but is encoded as N + tilde. Obviously this 
               # is meaningless in terms of UTF-8 encoding
               # but we have to deal with it before the decoding
               # takes place.
               word = word.replace(u'\u004E\u0303',u'\u00D1')

               # convert string to bytes in latin script
               # then decode it as UTF-8
               tr_word = word.encode('latin1').decode('utf8')
               print(tr_word.strip())
{{< /highlight >}}

#### Shell script to extract the unencoded text and rename

Now it's just a matter of connecting all the components, which I did in a small shell script.


{{< highlight bash >}}
#!/usr/local/bin/zsh

# extract the really messed-up name of the 
# pronunciation file
if [ "$#" -gt 0 ]; then
  fn=$1
else
  read fn
fi

tr_fn=$(echo $fn | perl -CSD -pe 's/pronunciation_ru_(.*)\.mp3/$1/gm;' | rfndecode ).mp3
tr_fn=$(basename $tr_fn)
printf "*** tr_fn = %s\n" $tr_fn >> $HOME/wtf.txt
mv $fn $HOME/Documents/mp3/$tr_fn
{{< /highlight >}}

Undoubtedly, the mysterious encoding might have been obvious to some, but for me it was an illustration of how to approach technical problems by taking them apart into the smallest discernible piece then applying what you know - even if limited in scope - to assemble the pieces into a comprehensive solution.