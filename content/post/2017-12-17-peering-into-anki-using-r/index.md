---
title: Peering into Anki using R
date: 2017-12-17 07:03:07
aliases: ['/2017/12/17/Peering-into-Anki-using-R/']
tags:
- programming
- anki
- R
categories:
- anki
---
{{< figure src="images/hrplot.png" >}}

Yet another diversion to keep me from focusing on actually using Anki to learn Russian. I stumbled on the R programming language, a language that focuses on statistical analysis.

Here's a couple snippets that begin to scratch the surface of what's possible. Important caveat: I'm an R novice at best. There are probably much better ways of doing some of this...

### Counting notes with a particular model type

Here we'll use R to do what we [did previously](/2017/12/03/Anki-database-adventures-Counting-notes-by-model-type/) with Python.

First load some of the libraries we'll need:

{{< highlight r >}}
library(rjson)
library(RSQLite)
library(DBI)
{{< /highlight >}}

Next we'll connect to the database and extract the model information:

{{< highlight r >}}
# connect to the Anki database
dbpath <- "path to your collection"
con = dbConnect(RSQLite::SQLite(),dbname=dbpath)

# get information about the models
modelInfo <- as.character(dbGetQuery(con,'SELECT models FROM col'))
models <- fromJSON(modelInfo)
{{< /highlight >}}

Since the model information is stored as JSON, we'll need to parse the JSON to build a data frame that we can use to extract the model ID that we'll need.

{{< highlight r >}}
names <- c()
mid <- names(models)
for(i in 1:length(mid))
{
  names[i] <- models[[mid[i]]]$name
}
models <- data.frame(cbind(mid,names))
{{< /highlight >}}

Next we'll extract the model ID (`mid`) from this data frame so that we can find all of the notes with that model ID:

{{< highlight r >}}
verbmid <- as.numeric(as.character(models[models$names=="Русский - глагол","mid"]))

# query the notes database for notes with this model
query <- paste("SELECT COUNT(id) FROM notes WHERE mid =",verbmid)
res <- as.numeric(dbGetQuery(con,query))
{{< /highlight >}}

And of course, close the connection to the Anki SQLite database:

{{< highlight r >}}
dbDisconnect(con)
{{< /highlight >}}

As of this writing, `res` tells me I have 702 notes with the verb model types (named "Русский - глагол" in my collection.)

### Counting hours per month in Anki

Ever wonder how many hours per month you spend reviewing in Anki? Here's an R program that will grab review time information from the database and plot it for you. I ran across the original idea in [this blog post](http://genedan.com/no-126-four-years-of-spaced-repetition/) by Gene Dan, but did a little work on the x-axis scale to get it to display correctly.

{{< highlight r >}}
library(RSQLite)
library(DBI)
library(rjson)
library(anytime)
library(sqldf)
library(zoo)
library(ggplot2)

dbpath <- "/Users/alan/Library/Application Support/Anki2/Alan - Russian/collection.anki2"
con = dbConnect(RSQLite::SQLite(),dbname=dbpath)
#get reviews
rev <- dbGetQuery(con,'select CAST(id as TEXT) as id
                  , CAST(cid as TEXT) as cid
                  , time
                  from revlog')

cards <- dbGetQuery(con,'select CAST(id as TEXT) as cid, CAST(did as TEXT) as did from cards')

#Get deck info - from the decks field in the col table
deckinfo <- as.character(dbGetQuery(con,'select decks from col'))
decks <- fromJSON(deckinfo)

names <- c()
did <- names(decks)
for(i in 1:length(did))
{
  names[i] <- decks[[did[i]]]$name
}

decks <- data.frame(cbind(did,names))
#decks$names <- as.character(decks$names)

cards_w_decks <- merge(cards,decks,by="did")
#Date is UNIX timestamp in milliseconds, divide by 1000 to get seconds
rev$revdate <- as.yearmon(anydate(as.numeric(rev$id)/1000))

# Assign deck info to reviews
rev_w_decks <- merge(rev,cards_w_decks,by="cid")
time_summary <- sqldf("select revdate, sum(time) as Time from rev_w_decks group by revdate")
time_summary$Time <- time_summary$Time/3.6e+6

ggplot(time_summary,aes(x=revdate,y=Time))+geom_bar(stat="identity",fill="#d93d2a")+
  scale_x_yearmon()+
  ggtitle("Hours per Month") +
  xlab("Review Date") +
  ylab("Time (hrs)") +
  theme(axis.text.x=element_text(hjust=2,size=rel(1))) +
  theme(plot.title=element_text(size=rel(1.5),vjust=.9,hjust=.5)) +
  guides(fill = guide_legend(reverse = TRUE))

dbDisconnect(con)
{{< /highlight >}}

You should get a plot like this the one at the top of the post.

I'm anxious to learn more about R and apply it to understanding my performance in Anki.
