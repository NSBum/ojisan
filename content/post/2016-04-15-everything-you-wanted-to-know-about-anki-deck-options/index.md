---
title: Everything you wanted to know about Anki deck options
date: 2016-04-15 17:37:49
draft: true
tags:
- anki
- memory
categories:
- anki
---
The spaced-repetition software system [Anki]() is my secret weapon in memorizing a massive number of Russian vocabulary words. Spaced repetition is probably the most effective way of memorizing material so long as the knowledge is well-structured. But several tweaks in the deck options can have a significant effect on the algorithm that Anki uses to schedule cards. In this post, I'll take you through the options and their effects. I'll also make some suggestions on how to set the options based on my experience with them.

## Card types

You have to understand that from the perspective of the scheduling algorithm, cards come in 3 flavors:

- **New** - these are cards that Anki hasn't yet presented to you. An entirely separate set of options governs the behavior of new cards.
- **Young** - these are cards that have been presented and are in review but the interval is less than 21 days.
- **Mature** - these are cards that are in review with an interval of 21 days or more.

The designations of "Young" and "Mature" are only for the purposes of statistics. The algorithm does not treat review cards differently based on whether they are Young or Mature. Instead, what matters is whether a given card is a new card or a review card.

## New card options

There are two separate tabs for options - one for new cards, the other for review cards. We'll start with the new card options first.

### Steps (in minutes)

A new card must go through a series of initial repetitions before it can graduate to being a young card. These steps are measured in minutes. If this field reads "1" then a card will be presented once, then again in one minute. If the second presentation passes, then the card will graduate to young status. On the other hand, if the field reads "1 5 10" then Anki will present a new card at intervals of 1 minute, 5 minutes, and 10 minutes. Once all of those "gates" are passed, then the card becomes a young review card.

There are two additional features to note. Anki also supports fractional steps. A step of 0.25 is an interval of 15 seconds. This can be used to force very tight initial repetitions. Second, the algorithm will show new cards up to 20 minutes early if you've exhausted everything else there is to do in a session. So if you set a 20 minute step and you finish everything else in a deck before 20 minutes, then Anki will perform the 20 minute step early.

It's worthwhile to read the section in the [Anki manual](http://ankisrs.net/docs/manual.html) about [new card deck options](http://ankisrs.net/docs/manual.html#deckoptions) to get an idea about how Anki treats steps that cross a day boundary.

### Order

You can set the order in which new cards are presented. In general, random order is better because there is less "state dependency" between cards. However, the manual points out that if you finish most of your new cards, then add additional new cards, the most recently added new cards are more likely to appear than the older new cards.

How Anki treats sibling cards with random presentation order is also important to understand. You may have some (or all) notes that create sibling cards. For example, one of my note types generates 3 cards: forward, reverse, and forward enhanced. Anki tries to keep all of the siblings together while respecting the new card presentation order.

### New cards/day

This value is like the spigot controlling the number of new cards entering the queue. The manual estimates that if you're studying 20 new cards daily then you should expect about 200 reviews a day. You can use the new card value as a means of controlling the review count.

### Graduating interval

The graduating interval is the number of days between the card graduating from new status to the next presentation as a review card measured in days.

### Easy interval

The easy interval is like the graduating interval but is applied when you answer Easy on a new card.

### Starting ease

Ease is an oddly named variable but the name is here to stay. I'd probably call it something like "Interval scaling factor." The ease is the amount by which the current interval is multiplied to get the next interval if you answered correctly. So if the last interval for a word was 10 days and you answered "good", then the new interval would be 15 days if its ease was 150%. The ease changes over time as you answer correctly or incorrectly. But it has to start somewhere - so that's the starting ease.

While we're on the subject of ease, it's worth taking a moment to think about how ease changes when the different buttons are pressed:

- If you press __Good__, then the ease doesn't change. The last interval just gets multiplied by the current ease.
- If you press __Hard__, then the ease is decreased by 15 percentage points and the interval is multiplied by 1.2 (120% ease.)
- If you press __Again__, the ease is decreased by 20 percentage points and card goes into relearning mode. When the card exits the relearning mode, it's interval will current interval is multiplied by the value of the new ease.
- If you press __Easy__, the ease is increased by 15 percentage points and the new interval is given by the current interval x current ease x easy bonus. (More on that later.)

### Bury related

If you turn off this value, Anki will not bury siblings. If this sounds a little frightening, it shouldn't be. As mentioned earlier, some note types may have multiple cards. Ordinarily, Anki tries to separate siblings by burying them - that is by provisionally moving them to the next day. This only applies to new or review cards. Those that are currently in learning aren't buried.

So by turning off this feature, Anki will try to keep the siblings in the same session as long as the number of new cards per day value is high enough.

That's it for the new cards. Now on to the review card options.

## Review cards

### Maximum reviews per day

This number allows you to put a cap on the total number of review cards that will appear on a given day. You have to understand that when this is set too low relative to the total number of cards in the deck and the number of new cards per day, you will create a perpetual backlog. Watch for a message about this occurrence when you get to the end of your session and adjust the number accordingly.

### Easy bonus

Remember how the interval is calculated when you have answer "Easy"? One of the factors is the easy bonus. It is the factor that creates a spread between the "Good" and the "Easy" buttons. A value of 130% means that the interval will be 1.3x whatever the "Good" interval is.

### Interval modifier

The interval modifier is a global interval scaling parameter. It expands or contracts intervals by the value specified. The default value of 100% means that no scaling is applied and the intervals are simply what the calculations above determine they should be.

The manual has a [lengthy part](http://ankisrs.net/docs/manual.html#reviews) on using the interval modifier to fine-tune the optimal retention rate. The author suggests that you should be achieving a retention rate of 90% for mature cards. You can find this value by looking at the appropriate section of the answer buttons graph.

<img src="{% asset_path graph_retention_rate.jpg %}" alt="Retention rate data">

In my case, I have a retention rate of 88.83%. To achieve a 90% retention rate, I would have to contract the intervals somewhat to drive the retention rate higher. But by how much do we adjust the interval modifier? The answer is given by:

<img src="{% asset_path formula.png %}" alt="Interval modifier adjustment">

where `RR'` is the desired retention rate and `RR` is the current actual retention rate. So in my case, the modifier would be:

<img src="{% asset_path formula_answer.png %}" alt="Calculation of modifier">

So I should plug 99% into the interval modifier. I'd probably wait for even more mature cards before making any adjustment because I'm doing pretty well already.

### Maximum interval

The maximum interval is simply the highest interval that can ever be assigned to a card. The default is 36500 days or 10 years. Sounds about right.

### Bury related reviews

Remember how we could bury new siblings? This allows us to adjust the similar behavior for review cards rather than new cards.

## Lapses

Lastly, we have the lapses options. These options govern what happens with you forget a previously learned card. The default is for the algorithm to put the lapsed card into the learning queue in 10 minutes and set the interval to 1 day. But this can all be customized.

### Steps

As mentioned above the default behavior is to put a lapsed card back into the learning queue. This is done with a step of 10 minutes. __I like to have one additional step of 0.25 so I get a quick "hit" after forgetting.__

## New interval and minimum interval

The new interval and minimum interval only come into play when the steps are left blank. In that case, the new interval is determined by this factor. So if the previous interval were 10 days and the new interval value were 50%, then the new interval would be 5 days. The minimum interval sets a "floor" for this value.

## Leech threshold

You can set the number of lapses before a card becomes a leech. Leeches are cards that take an inordinately large amount of your review time without yielding any results. __For the leech settings, the defaults seem sensible to me.__

## Leech action

Here you can choose what you want Anki to do with the card once the leech threshold has been reached.
