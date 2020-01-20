---
title: Managing classical music collections in iTunes in 2018
date: 2018-08-15 06:29:37
aliases: ['/2018/08/15/Managing-classical-music-collections-in-iTunes-in-2018/']
summary: "My approach to wrestling with iTunes to make it (barely) usable for classical music collections."
tags:
- itunes
- music
- software
categories:
- music
---
Like many, I use iTunes to manage my music library. Unlike most, I don't stream music^[Partly because we live in a rural setting with slow and unreliable internet access, partly because I don't trust that artists are getting properly compensated, and partly because I like to organize my music my own way.]. That means I have a large music collection - one that stretches the limits of iTunes' organizational system. The overwhelming majority of the music in our collection is classical; and this is the source of the difficulty.

## The problem

For background on why classical music is so poorly handled, read Robinson Meyer's piece in _The Atlantic_ ["The Tragedy of iTunes and Classical Music"](https://www.theatlantic.com/technology/archive/2015/07/the-tragedy-of-itunes-and-classical-music/399788/). Several issues make is difficult to organize classical works:

- iTunes regards all music as "songs". Of course, some classical works _are_ songs, but most are not.
- The mp3 metadata standard as originally released was incomplete and completely ignorant of organizational requirements beyond "song" and "album."
- And of course, much is driven by Apple's focus on profits. For every classical enthusiast, there must be 1000 popular music listeners. There's simply too little return on any investment in tailoring the software to meet the needs of classical music listeners.

## Naming and metadata standards

1. **Use Work/movement designation** - This considerably improves the organization of multi-movement works in iTunes.
2. **Use opus and number designations** - Both should be abbreviated, op. and no. respectively. That's lower case abbreviation followed by a period and a space. If the work is in a sequence, then No. is part of the title and should be capitalized as in “Piano Trio No. 1 in C minor" The _#_ symbol is never used. A slash _/_ is never used.
3. **If there is a catalogue number, then it should be used.** The catalogue number should be the last element in the name of the work, separated from the remainder by a comma and a single space. Köchel numbers and Deutsch should be abbreviated K. and D. respectively. However Bach-Werke-Verzeichnis catalogue numbers should not use periods.
4. **Add metadata in track comments** - Since iTunes does not yet have all of the metadata that I need to organize my music, I add additional metadata in the `Comments` field. Four elements comprise the metadata that I currently use: a) Musical form (symphony, concerto, sonata, etc.), b) Musical period (e.g. baroque, classical, etc.), c) Ensemble - solo, duet, trio, orchestra, etc. d) Highlighted instruments - a comma-delimited list of instruments that are featured. While iTunes provides a genre designation, I simply use "Classical" and apply my own period classification in my free-text metadata.

## Organizational approach

Since classical music isn't really organized by "song" and an album is much less important than the works it contains, I break down the album structure and reorganize it by work. In addition to using the work/movement designation in the track info, I create playlists for individual works and playlists folders for broader categories of works by the same composer.

{{< figure src="images/mozart.png" title="Organizing works as playlists and folders" >}}

The top-level folder is the composer followed by nested folders of category of works (e.g. sonatas, concerti, etc.) then instrument folders under that level. If I have multiple recordings of the same work, the work itself gets its own folder.

## What next for iTunes?

The work/movement designation in track info has been transformational; but iTunes still has a long way to go. Please don't suggest music to me. Don't show me a bunch of irrelevant album covers on the iTunes Store page; it's meaningless to me. On mobile devices, find a way of showing the entire track name. Classical track names are often very long. Sometimes on the phone, I can only see _"Piano Quartet No. 3 in..."_ Wait, is that the one in C minor or in G minor? No idea. iTunes still has a long way to go.
