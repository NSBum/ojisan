---
title: Resizing of images for Anki with Hazel and ImageMagick
date: 2016-04-02 02:08:08
aliases: ['/2016/04/02/Resizing-of-images-for-Anki-with-Hazel-and-ImageMagick/']
tags:
- anki
categories:
- programming
---
I use [Anki](http://ankisrs.net) to study foreign language vocabulary. It's the _de facto_ spaced repetition software for memorization.^[Yes, I'm aware that others exist. I've tried many but always have come back to Anki.] When making flashcards for language learnings, I try to use imagery as much as possible. So a card may have a Russian word on one side and just an image on the opposite side. (Since I already know the English word that the image represents, why not try to engage a different part of the brain to help with memorization?)

If you use Anki on multiple devices, then synchronization is a key step. However, image size becomes a limiting factor for sync speed. Since only a small image is often necessary to convey the intended meaning, we can improve the sync efficiency by using them while not sacrificing any meaning. Bulk, efficient resizing of images for Anki cards is an important part of the process for me.

Here I'll describe a process of automatically processing images for use on Anki cards using [Hazel]() and [ImageMagick](). Sorry, PC and Linux users, this is OS X only.

<!-- more -->

### Hazel

[Hazel](https://www.noodlesoft.com/hazel.php) is an indispensable tool for OS X automation. It's a little hard to describe all of the things that it can do, but suffice it to say that it is a background application that watches folders and then performs rules on the contents of those folders. You will need to buy it for this process to work.

### ImageMagick

[ImageMagick](https://www.imagemagick.org/script/index.php) is a well-known Swiss army knife of image process. You will need to install it which you can do using [Homebrew](homebrewtalk) or [this installer](http://cactuslab.com/imagemagick/)

### The process

{{< figure src="images/directories.jpg" title="Image handling directories" >}}

I created two directories on the Desktop: `ankibound` and `ankidone`. Incoming images go into `ankibound`. The rule we create in Hazel will watch `ankibound`, convert the image to a smaller size, adjust the quality slightly, strip the unused metadata and move the processed file to `ankidone`.

### Hazel rule to process incoming images

{{< figure src="images/hazel1.jpg" title="Hazel rule list" >}}

If you are not familiar with creating Hazel rules, you first add the folder to be watched (`ankibound`) and add a new rules which we've cleverly named "Resize images for Anki." Then we just need to add the criteria and the steps for the rule.

{{< figure src="images/hazel2.jpg" title="Hazel criteria and actions" >}}

We've specified the type of file to be processed inside of `ankibound` and added two actions:

- resize incoming images using ImageMagick on the command line, and
- move the processed images to `ankidone`.

The code for image scaling is simple, it's just:

{{< highlight bash >}}
/usr/local/bin/convert "$1" -adaptive-resize 150x150 -quality 80\
 -density 72 -strip "$1"
{{< /highlight >}}

Now, any image that you save to `ankibound` will get resized to 150px in its largest dimension and moved to `ankidone`, ready to import into your Anki cards. Of course, you could also use the [ImageResizer](https://ankiweb.net/shared/info/1214357311) add-on for Anki but I like being in control of my own process and being able to deal with images without having to get them onto the clipboard. Either way works.

### References

- [Automatic image resize and ftp upload with Hazel 3.1](http://crateofpenguins.com/blog/2013-6-automatic-image-resize-and-ftp-upload-with-hazel-31) - original inspiration for the methodology
- [ImageMagick home page](http://www.imagemagick.org/script/index.php)
- [Adjusting size, resolution and quality using ImageMagick](https://imagemagick.org/discourse-server/viewtopic.php?t=24890)
- [Using -strip option in ImageMagick to remove metadata](http://www.imagemagick.org/discourse-server/viewtopic.php?t=20296)
- [Hazel](https://www.noodlesoft.com/index.php) - directory automation for OS X
- [Possible alternative to ImageMagick](http://apple.stackexchange.com/questions/106873/batch-processing-image-files-in-a-folder-using-a-folder-action-with-automator) - you could use `sips` on OS X in place of ImageMagick. It should work, but I haven't tried it. From a brief glance, it doesn't seem to support everything we are doing with ImageMagick, but I could be wrong.
- [sips man page](https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man1/sips.1.html) - this is the man(1) page for sips(1) on OS X.
- [Anki ImageResizer add-on](https://ankiweb.net/shared/info/1214357311) - another alternative leveraging the Anki plugin architecture
