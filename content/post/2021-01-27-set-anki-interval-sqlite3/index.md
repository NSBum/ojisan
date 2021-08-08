---
title: "Directly setting an Anki card's interval in the sqlite3 database"
date: 2021-01-27T21:17:18-05:00
draft: false
authorbox: false
sidebar: true
tags:
- anki
- sql
categories:
- Anki
---
It's always best to let Anki set intervals according to its view of your performance on testing. That said, there are times when directly altering the interval makes sense. For example, to build out a complete representation of the entire Russian National Corpus, I'm forced to enter vocabulary terms that should be obvious to even elementary Russian learners but which aren't yet in my nearly 24,000 card database. Therefore, I'm entering these cards gradually. When they come up as new cards, I pass them as "Easy" on the first appearance, converting them to review cards. But ideally, I'd like to send them away for years.

I'm sure it's possible to do this with an add-on or such inside of Anki, but it's easy enough to do in sqlite3 if you know the card ID's. If you have a group of card ID's, make sure you can find them:

{{< highlight sql >}}
SELECT * FROM cards where id IN (1611799204625, 1611799014001, 1611755571885, 1611755486486)
{{< /highlight >}}

and  to reset the interval `ivl`:

{{< highlight sql >}}
UPDATE cards SET ivl = 1825 WHERE id IN (1611799204625, 1611799014001, 1611755571885, 1611755486486)
{{< /highlight >}}
