---
title: "Fixing CodeRunner jQuery injection"
date: 2021-04-17T11:02:55-04:00
draft: false
authorbox: false
sidebar: false
tags:
- javascript
- coderunner
categories:
- programming
---
CodeRunner is one of my favourite development environments on macOS. I use it for small one-off projects or for testing concepts for integration into larger projects. But in version 4.0.3, jQuery injection in a custom HTML page is broken, giving the error:

{{< figure src="images/2021/04/17/error.png" >}}

It's probably due to some unescaped bit of code in their minified jQuery, but I didn't have time to work that hard. Instead I reported the error to the developer an fixed it myself. The original (default) run script for jQuery is:

{{< highlight bash >}}
echo "<script>$(cat "$CR_SCRIPTS_DIR/jquery.min.js")</script><script src=\"file://$PWD/$filename\"></script>"
{{< /highlight >}}

Instead, I just pointed the jQuery source path to a local file on my drive. It also has the advantage of allowing me to use whatever version of jQuery that I want. So the new run script is:

{{< highlight bash >}}
echo "<script src=\"file:///Users/alan/Documents/dev/jquery.min.js\"></script><script src=\"file://$PWD/$filename\"></script>"
{{< /highlight >}}

Problem solved and back to work.
