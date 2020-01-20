---
title: Working with the Anki database on mac OS using Python
date: 2017-12-01 06:16:29
aliases: ['/2017/12/01/Working-with-the-Anki-database-on-mac-OS/']
tags:
- python
- programming
- anki
categories:
- anki
---
Not long ago I ran across [this post](https://eshapard.github.io/anki/) detailing a method for opening and inspecting the Anki database using Python _outside_ the Anki application environment. However, the approach requires linking to the Anki code base which is inaccessible on mac OS since the Python code is packaged into a Mac app on this platform.

The solution I've found is inelegant; but just involves downloading the Anki code base to a location on your file system where you can link to it in your code. You can find the Anki code [here on github](https://github.com/dae/anki/).

Once that's done, you're ready to load an Anki collection. First, the preliminaries:

{{< highlight python >}}
#!/usr/bin/python

import sys

#   paths
ANKI_PATH = 'path to where you downloaded the anki codebase'
COLLECTION_PATH = "path to the Anki collection"

sys.path.append(ANKI_PATH)
from anki import Collection
{{< /highlight >}}

Now we're ready to open the collection:

{{< highlight python >}}
col = Collection(COLLECTION_PATH)
{{< /highlight >}}

And execute a simple query to print out the total number of cards in the collection:
{{< highlight python >}}
query = """SELECT COUNT(id) from cards"""
totalCards = col.db.scalar(query)

print 'There are {:.5g} total cards.'.format(totalCards)
{{< /highlight >}}

Then close the collection:
{{< highlight python >}}
col.close()
{{< /highlight >}}

That's it. Ideally, we'd be able to link to the Anki code bundled with the Mac application. Maybe there's a way. In the meanwhile, here's the entire little app:

{{< highlight python >}}
#!/usr/bin/python

import sys

#   paths
ANKI_PATH = '/Users/alan/Documents/dev/projects/PersonalProjects/anki'
COLLECTION_PATH = "/Users/alan/Documents/Anki/Alan - Russian/collection.anki2"

sys.path.append(ANKI_PATH)
from anki import Collection

col = Collection(COLLECTION_PATH)

query = """SELECT COUNT(id) from cards"""
totalCards = col.db.scalar(query)

print 'There are {:.5g} total cards.'.format(totalCards)

col.close()
{{< /highlight >}}
