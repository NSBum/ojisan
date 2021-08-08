---
title: "Dynamically loading Javascript in Anki card templates"
date: 2021-04-22T14:49:45-04:00
draft: false
authorbox: false
sidebar: false
tags:
- javascript
- programming
categories:
- anki
---
The ability to execute Javascript in Anki card templates offers users flexibility in displaying data. In Anki 2.1, though, the asynchronous execution of Javascript means that user script functionality is not entirely predictable. [This post](https://www.reddit.com/r/Anki/comments/bk82ov/how_to_load_external_javascript/) on r/Anki discusses an approach for dynamically loading Javascript resources and ensuring that they are available when the card is displayed. Since I modularize my Javascript code so that it can be flexibly deployed to different card types, I extended this method to allow the template developer to load multiple scripts in one `<script>` block.

{{< highlight javascript >}}
<script>
    var fn = [
       "_fix_cloze_anything_sentence.js",
       "_expression_cloze_back_pos.js",
    ];
    fn.forEach(path => {
        var script = document.createElement('script');
        script.src = path;
        script.async = false;
        document.head.appendChild(script);
    });
</script>
{{< /highlight >}}

The template developer simply needs to store the scripts prepended with an underscore in the collection.media directory.[^1] Then enumerate the script filenames in the `fn` variable.

[^1]: This scheme prevents Anki from attempting to remove the files when it detects that they are not referenced in any notes.
