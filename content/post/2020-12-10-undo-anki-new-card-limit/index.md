---
title: "Undoing the Anki new card custom study limit"
date: 2020-12-10T13:30:18-05:00
draft: false
authorbox: false
sidebar: false
tags:
- sql
- programming
categories:
- anki
---
Recently I hit an extra digit when setting up a custom new card session and was stuck with hundreds of new cards to review. Desparate to fix this, I started poking around the Anki collection SQLite database, I found the collection data responsible for the extra cards. In the `col` table, find the `newToday` key and you'll find the extra card count expressed as a negative integer. Just change that to zero and you'll be good.

Later I discovered [another blogger](https://tahirhassan.blogspot.com/2018/06/anki-undo-increase-todays-new-card-limit.html) found it too! 