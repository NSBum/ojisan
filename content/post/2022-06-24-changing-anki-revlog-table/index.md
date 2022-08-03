---
title: "Altering Anki's revlog table, or how to recover your streak"
date: 2022-06-24T04:47:32-04:00
draft: false
authorbox: false
sidebar: true
tags:
- sqlite
- sql
- database
- anki
categories:
- anki
---
Anki users are protective of their streak - the number of consecutive days they've done their reviews. Right now, for example, my streak is 621 days. So if you miss a day for whatever reason, not only do you have to deal with double the number of reviews, but you also deal with the emotional toll of having lost your streak.

You can lose your streak for one of several reasons. You could have simply been lazy. You may have forgotten that you didn't do your Anki. Or travel across timezones put you in a situation where Anki's clock and your clock differ. Others have described a procedure for resetting the computer's clock as a way of recovering a lost streak. It apparently works though I haven't tried it. Instead I'll focus on a technique that involves working directly with the Anki database.

First, I must warn you: if you don't know anything about sqlite, SQL or the like don't attempt this. It's very easy to do something that will wreck your collection's database. You've been warned.

### Locating the database

First of all, make any modifications to the Anki db with care; make backups, etc. Make sure Anki is closed.

On macOS the sqlite database file is at `~/Library/Application Support/Anki2/your_collection_name/collection.anki2`. On other platforms, the path is something else, I'm sure the manual says something about this. Or you can just search for `collection.anki2` and navigate there. That file is the Anki database.

### Moving a review

Let's say the goal is to move the latest review back to a different day. This query will find the latest review _(here I've restricted to a particular deck named Словарный запас...)_

{{< highlight sql >}}
SELECT * FROM revlog r 
INNER JOIN cards c ON c.id = r.cid 
INNER JOIN decks d ON c.did = d.id
WHERE d.name LIKE '%Словарный запас%'
   AND c.queue = 2
ORDER BY r.id DESC
LIMIT 1
{{< /highlight >}}

This query returns a single row. In that row, focusing on the `id` column, that will give us the timestamp in Unix epoch milliseconds. In my case it is `1656057796342`. That translates to _Fri Jun 24 2022 08:03:16 GMT+0000_, which checks out. 

Now we are going to need to move that row to an `id` with a different timestamp. But what should that timestamp be? Well, if we want to move it to yesterday, then we can subtract 86400 seconds (the number of seconds in one day) from the `id` above. Remember that the `id` field is in epoch _milliseconds_ so we have to divide by 1000 first → 1656057796. Now subtract 86400 → 1655971396, and multiply by 1000 → 1655971396000 which translates to _Thu Jun 23 2022 08:03:16 GMT+0000_. Bingo! One day earlier that our existing row.

Now we just need to move the row to our new computed `id`:

{{< highlight sql >}}
UPDATE revlog 
SET id = 1655971396000
WHERE id = 1656057796342
{{< /highlight >}}

As long as our new `id` is unique, this query should succeed.

Again, if you're not comfortable working with sqlite and SQL queries - this is **not a good idea**. At the very minimum backup your database in case of error.

### References

- [Anki database structure](https://github.com/ankidroid/Anki-Android/wiki/Database-Structure) - unofficial documentation of the tables in the Anki database