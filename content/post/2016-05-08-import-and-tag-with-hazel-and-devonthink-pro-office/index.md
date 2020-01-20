---
title: Import and tag with Hazel and DEVONthink Pro Office
date: 2016-05-08 06:30:40
aliases: ['/2016/05/08/Import-and-tag-with-Hazel-and-DEVONthink-Pro-Office/']
tags:
- organization
- devonthink
- hazel
- osx
- mac
- applescript
categories:
- programming
---
[Hazel](https://www.noodlesoft.com/kb/) and [DEVONthink](https://www.google.ca/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=0ahUKEwjApMz67srMAhUHKx4KHfPyDfMQFggcMAA&url=http%3A%2F%2Fwww.devontechnologies.com%2Fproducts%2Fdevonthink%2Foverview.html&usg=AFQjCNHBkDoottuKS5_NujsjRTQSINDHpQ) make a great pair as I've [written before](/2015/10/17/working-with-devonthink-pro-office-and-hazel/). Using AppleScript, it's possible to take the import workflow even further by tagging incoming files automatically.

### Use case

I download a lot of mp3 files containing pronunciation of words in a language I've been learning. I keep a record of these words and tag them appropriately using my [hierarchical tagging](/2015/06/18/finding-things-with-devonthink/) system.

I'd like to download the files to a directory on the desktop. Keep them there for a few minutes until I'm done working with them, then import the file to DEVONthink Pro Office, tag the file there and delete the original.

Read on to see how the Hazel rule is written, including the AppleScript to make it happen.

<!-- more -->

### Hazel rule

{{< figure src="images/hazel_import_rule.jpg" title="" >}}

The Hazel rule is simple:

- Look in a directory called "mp3".
- Select files that have the mp3 extension.
- Allow the file to remain in place for 5 minutes
- Thereafter, execute the import and tagging script.
- Finally, delete the original file

Most of the action is in the AppleScript that provides a bridge from Hazel to DEVONthink.

### AppleScript import action

Hazel exposes a variable `theFile` that we can use as we import and tag the file. Here's the entire AppleScript with comments following.

{{< highlight applescript >}}
tell application id "com.devon-technologies.thinkpro2"
    launch
    open database "/Users/alanduncan/Documents/russian.dtBase2"
    set dbID to 7
    set theDatabase to get database with id dbID
    tell theDatabase
        set destGroup to first item of (records whose name is "reference")
        set theRecord to import theFile to destGroup
        tell theRecord
            set {od, AppleScript's text item delimiters} ¬
			   to {AppleScript's text item delimiters, ","}
            set tags to text items of "source_web, type_sound"
            set AppleScript's text item delimiters to od
        end tell
    end tell
end tell
{{< /highlight >}}

**Line 2-3** - Launch DEVONthink and open the receiving database.
**Line 4-5** - Reference the database by ID. There are other ways to do this. I just happened to find the ID in Script Debugger so I used it.
**Line 7** - Set a reference to the destination group. Mine is `reference`.
**Line 8** - Perform the import returning the imported record. You can import without the return but then you would have to do extra work to find the file you want to tag.
**Line 10** - Allow us to use a comma-delimited list of tags
**Line 12** - Set the incoming file's tags. Mine are as listed; yours would be something else.
**Line 13** Restore the original text delimiters

That's it! No you have a mechanism for automatically managing files from the Finder to DEVONthink.
