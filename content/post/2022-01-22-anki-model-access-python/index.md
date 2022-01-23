---
title: "Accessing Anki collection models from Python"
date: 2022-01-22T08:05:38-05:00
draft: false
authorbox: false
sidebar: false
tags:
- anki
- python
- unicode
categories:
- programming
---
For one-off projects that target Anki collections, I often use Python in a standalone application rather than an Anki add-on. Since I'm not going to distribute these little creations that are specific to my own needs, there's no reason to create an add-on. These are just a few notes - nothing comprehensive - on the process.

One thing to be aware of is that there must be a perfect match between the Anki major and minor version numbers for the Python `anki` module to work. If you are running Anki 2.1.48 on your desktop application but have the Python module built for 2.1.49, it will not work. This is a huge irritation and there's no backwards compatibility; the versions must match precisely.

Anyway, here's a little application to illustrate the simple process of finding all of the moderls (also know as note types.)

{{< highlight python >}}
#!/usr/bin/env python3

import os
from anki.collection import Collection
from anki.models import ModelManager
import anki.errors

COLLECTION_PATH = os.environ.get('ANKI_RU_COL_PATH')

def anki_utf8_tr(ustr: str) -> str:
   try:
      return ustr.encode('latin1').decode('utf8')
   except UnicodeEncodeError:
      return ustr

if __name__ == "__main__":
   try:
      col = Collection(COLLECTION_PATH)
   except anki.errors.DBError:
      print("ERROR: Anki should be closed")
      quit()
   model_mgr = ModelManager(col)
   for m in model_mgr.all_names_and_ids():
      m_id = m.id
      m_name = anki_utf8_tr(m.name)
      print(f'{m_id} - {m_name}')
{{< /highlight >}}

An interesting caveat in reading the model names: if you've used names with character sets other than Latin, then the output of the `model.name` looks a little strnge, e.g. `name: "\320\240\321\203\321\201\321\201\320\272\320\270\320\271 enhanced"` which took a bit of time to figure out. It's actually just decimal UTF-8 codes. The function `anki_utf8_tr` function is meant to provide the translation to the original representation. I've [written](/2021/11/12/converting-cyrillic-utf-8-text-encoded-as-latin-1/) more about this previously.