---
title: "A folder-based image gallery for Hugo"
date: 2020-01-11T04:59:54-05:00
draft: false
authorbox: false
sidebar: false
categories:
- programming
tags:
- blog
- hugo
---
[Hugo](https://gohugo.io/) is the platform I use to publish this weblog. Occasionally I have the need to include a collection of images in a post. Mostly this comes up on other sites that I publish. [Fancybox](http://fancyapps.com/fancybox/3/) can do this; but it wasn't immediately clear how to direct Fancybox to create a gallery of images in a page based on images in a directory. Previously, I've solved this in different ways, but I was anxious to find a simple shortcode-based method.

Eventually I settled on [this shortcode](https://greekdeveloper.com/2018/folder-based-gallery-for-hugo/) `foldergallery` but I quickly discovered that it must be based on a site configuration that is different from mine. Furthermore, the way it configures paths into the image source directory seems to be localized to Windows. If you run Windows, it undoubtedly works fine, but I had to do some modifications to get it to work on macOS, mostly changing the code that constructs the paths to the source directory of the images.

{{< highlight html >}}
<!-- /layouts/shortcodes/foldergallery.html -->

<style>
    div.gallery {
        display: flex;
        flex-wrap: wrap;
    }

    div.gallery a {
        flex-grow: 1;
        object-fit: cover;
        margin: 2px;
        display: flex;
    }

    div.gallery a img {
        height: 200px;
        object-fit: cover;
        flex-grow: 1;
    }
</style>

<div class="gallery">
    {{ $path := print "static/img/" (.Get "src")  }}
    {{ $url  := print (.Get "src") }}
    {{ range (readDir $path)  }}
        {{/* don't try to display .DS_Store or directories */}}
        {{ if and (ne .Name ".DS_Store") (not .IsDir)  }}
            {{ $src := print "/img" "/" $url "/" .Name }}
            {{/*
                troubleshoot the $src variable as needed
                <!-- <p>{{ $src }}</p> -->
                */}}
            <a data-fancybox="gallery" href="{{ $src }}">
                <img src="{{ $src }}">  <br/>
            </a>
        {{ end }}
    {{ end }}
</div>
{{< /highlight >}}

I've also published this as a [gist](https://gist.github.com/NSBum/56a3779ee62793a3597f9aa2e29ec47c).

In order to use the `foldergallery` shortcode, you'll need to install it in /layouts/shortcodes. You will also need the following in your head partial:

{{< highlight html >}}
<!-- IMPORTANT: Remove any references in older versions of jquery -->
<script src="https://code.jquery.com/jquery-3.3.1.min.js" integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/fancybox/3.4.0/jquery.fancybox.min.js"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/fancybox/3.4.0/jquery.fancybox.min.css" />
{{< /highlight >}}

Now, in order to publish a gallery of images from a directory we just need:

{{< gist NSBum e0bccddc82874d05d5d61ad7eca45ac6 >}}

which will pull images from `static/img/news/asi`.
