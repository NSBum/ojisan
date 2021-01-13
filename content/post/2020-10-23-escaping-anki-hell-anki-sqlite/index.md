---
title: "Escaping \"Anki hell\" by direct manipulation of the Anki sqlite3 database"
date: 2020-10-23T06:07:56-04:00
draft: false
authorbox: false
sidebar: false
tags:
- programming
- russian
- linguistics
categories:
- anki
---
There's a phenomenon that verteran [Anki]() users are familiar with - the so-called "Anki hell" or "ease hell." 

### Origins of ease hell

The descent into ease hell has to do with the way Anki handles correct and incorrect answers when it presents cards for review. Ease is a numerical score associated with every card in the database and represents a valuation of the difficulty of the card. By default, when cards graduate from the learning phase, an ease of 250% is applied to the card. If you continue to get the card correct, then the ease remains at 250% in perpetuity. As you see the card at its increasing intervals, the ease will remain the same. All good. Sort of.

But what happens if you fail the card at some point in the review process, then the ease becomes 250% minus 15% or 235%. Then, say, you relearn the card and the ease has stablized at 235% percent again. Then later you miss the card. Now you get another 15% hit to the ease. For older cards, you can see where this is going. Eventually the ease bottoms out at 130% and you will see the card frequently forever...

Unless you intervene in one of a handful of ways. The simplest approach is to keep track of the ease values and use the "Easy" button on the card to recover the 15% that was deducted when you missed the card previously. The logical problem behind all of this is that getting a card wrong leaves you with 15% less ease, but getting a card correct has no effect. 

### A blunt force approach to fixing ease hell

I was skeptical of the concept of ease hell until I ran a search on all my 22,000 Russian cards. Sure enough thousands were stuck at an ease of 130%. My solution was to identify these cards in ease hell and put them back to the starting point of 250%. Here's the process I used:

1. Quit Anki so that you can manipulate the database behind its back.
2. Find the location of the database. On macOS, it's `~/Application Support/Anki2/name_of_collection/collection.anki2`
3. Open the database using [Base](https://apps.apple.com/us/app/base-sqlite-editor/id402383384) sqlite3 database editor, or you can just use sqlite3 straight from the Terminal or iTerm. The advantage of using the GUI application Base is that it's easier to see the results of your actions; but either way works. If you're using Base, skip to step 5, otherwise go to step 4
4. In Terminal or iTerm (I use the latter.) open the Anki collection database: `sqlite3 path_to_your_db`. To illustrate how SQL queries work, you can execute a quick query against the `cards` table: `SELECT * FROM cards LIMIT 2;` The query should return some data with fields delimited by '|' characters.
5. In Base find the SQL tab. In the text box, you can input a SQL query and press "Execute".
6. To target all cards in ease hell, those having an ease factor of 130 (or 1300) as it's encoded in the database, you would issue the SQL query: 

{{< highlight sql >}}
UPDATE cards SET factor = 2500 WHERE factor = 1300 AND factor > 0
{{< /highlight >}}

Save the database and exit. Now Anki should reflect that ease factor changes.

### Alternative approach

You can also accomplish this same feat using an add-on. For example, ResetEZ.py discussed on [Mass Immersion Approach](https://massimmersionapproach.com/table-of-contents/anki/low-key-anki/low-key-anki-summary-and-installation/) will reset all of the ease factors. The same page also features other components of the low-key Anki approach that will maintain the ease factors at 250%.

### Maintenance after climbing out of Anki hell

One approach is to simply abuse the Easy button which will repeatedly boost the ease and, in time, build up a buffer against potential future incorrect responses. Another approach to maintenance is to adopt the "straight reward" approach while adds ease bonuses for several correct responses in a row.

### Conclusion

Anki hell, also known as ease hell is a real phenomenon, one that defeats the effciencies that could otherwise be gained through spaced repetition.

### References

- [Staight Reward add-on](https://ankiweb.net/shared/info/957961234) - I haven't used this one because I'm stuck on an earlier version of Anki due to incompatibilities with other add-ons. But it is widely used.
- [Low-key Anki](https://massimmersionapproach.com/table-of-contents/anki/low-key-anki/low-key-anki-summary-and-installation/) - this site has a suite of add-ons available in a zip file. Together, they correct and prevent ease hell by resetting and keeping all of the ease factors at 2500.
- [Explanation of ease hell](https://www.youtube.com/watch?v=roR8S9zjUh8) - AnKing explains the phenomenon.