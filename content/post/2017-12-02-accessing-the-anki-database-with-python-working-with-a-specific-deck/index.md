---
title: 'Accessing the Anki database with Python: Working with a specific deck'
date: 2017-12-02 04:29:36
aliases: ['/2017/12/02/Accessing-the-Anki-database-with-Python-Working-with-a-specific-deck/']
tags:
- python
- programming
- anki
categories:
- anki
---
I [previously wrote](/2017/12/01/Working-with-the-Anki-database-on-mac-OS/) about accessing the Anki database using Python on mac OS. Extending that post, I'll show how to work with a specific deck in this short post.

To use a named deck you'll need its deck ID. Fortunately there's a built-in method for finding a deck ID by name:

{{< highlight python >}}
col = Collection(COLLECTION_PATH)
dID = col.decks.id(DECK_NAME)
{{< /highlight >}}

Now in queries against the `cards` and `notes` tables we can apply the deck ID to restrict them to a certain deck. For example, to find all of the cards currently in the learning stage:

{{< highlight python >}}
query = """SELECT COUNT(id) FROM cards where type = 1 AND did = dID"""
learningCards = col.db.scalar(query)

print 'There are {:.5g} learning cards.'.format(learningCards)
{{< /highlight >}}

And close the collection:
{{< highlight python >}}
col.close()
{{< /highlight >}}

### See also:
- [Working with the Anki database on mac OS](/2017/12/01/Working-with-the-Anki-database-on-mac-OS/)
- [Open the Anki database from Python](https://eshapard.github.io/anki/)
- [Anki database structure](https://github.com/ankidroid/Anki-Android/wiki/Database-Structure) - A thorough explanation of all the tables and fields
- [All of my articles about Anki](/categories/anki/)
