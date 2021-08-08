#!/bin/bash

til_path="/Users/alan/Documents/blog/ojisan/content/TIL"
title_date=`date +"%Y-%m-%d"`
fn="$til_path/$title_date.md"
touch $fn
long_date=`date +"%A, %B %d, %Y"`
tz=$(date +"%z" | sd '(\d{2})(\d{2})' '$1:$2')
md_date=`date +"%Y-%m-%dT%H:%M:%S"`
echo "---" >> $fn
echo "title: \"$long_date\"" >> $fn
echo "date: $md_date$tz" >> $fn
echo "draft: false" >> $fn
echo "authorbox: false" >> $fn
echo "sidebar: true" >> $fn
echo "tags:" >> $fn
echo "- til" >> $fn
echo "- someothertag" >> $fn
echo "categories:" >> $fn
echo "- somecat" >> $fn
echo "---" >> $fn
exit