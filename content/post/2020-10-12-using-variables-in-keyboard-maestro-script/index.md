---
title: "Using variables in Keyboard Maestro scripts"
date: 2020-10-12T07:02:58-04:00
draft: false
authorbox: false
sidebar: false
tags:
- macos
- automation
categories:
- programming
---
Having fallen in love with [Keyboard Maestro](https://www.keyboardmaestro.com/main/) for its flexibility in macOS automation, I began experimenting with scripting in various languages, like my old favourite Perl. That's when the fun began. How do we access KM variables inside a Perl script.

Let's see what the [documentation says](https://wiki.keyboardmaestro.com/action/Execute_a_Shell_Script):

![](/images/2020/10/11/km_variables_doc.png)

So the documentation clearly states that this script

{{< highlight perl >}}
#!/usr/bin/perl

print scalar reverse $KMVAR_MyVar;
{{< /highlight >}}

should work if I have a KM variable named `MyVar`. But, you guessed it - it does not.

After digging around in the [Keyboard Masestro forums](https://forum.keyboardmaestro.com/latest), I found an [obscure post](https://forum.keyboardmaestro.com/t/how-to-call-a-km-macro-from-a-shell-or-perl-script/16550/4) that pointed the way. It turns out that the Perl access to KM variables is completely different from what the documentation claims, the format **is not** `$KMVAR_MyVar`, it is actually:

{{< highlight perl >}}
$ENV{KMVAR_MyVar}
{{< /highlight >}}

so the above script works if the variable is accessed from Perl that way:

{{< highlight perl >}}
#!/usr/bin/perl

print scalar reverse $ENV{KMVAR_MyVar};
{{< /highlight >}}