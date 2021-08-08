---
title: "Fixing Knowclip Anki apkg creation dates"
date: 2021-04-05T06:09:30-04:00
draft: false
authorbox: false
sidebar: false
tags:
- anki
- russian
- video
categories:
- anki
---
_(N.B. A much-improved version of this script is published in a [later post](/2021/04/15/complete-fix-for-broken-knowclip-.apkg-files/))_

Language learners who want to develop their listening comprehension skills often turn to YouTube for videos that feature native language content. Often these videos have subtitles in the original language. A handful of applications allow users to take these videos along with their subtitles and chop them up into sentence-length bites that are suitable for Anki cards. Once such application is [Knowclip](https://github.com/knowclip/knowclip). Indeed for macOS users, it's one of the few viable options.[^1]

As expected, as of version 0.10.2-beta, it has a few rough edges, one of which is that notes it generates have the incorrect date. All of the creation dates are 1969-12-31, which of course is the zero date in the Unix epoch date-keeping world. As far as I can tell, it doesn't cause in problems once the Knowclip-generated `apkg` file is imported into Anki, but it's an irritating bug.

To fix this issue, it's important to recognize that an `apkg` file is just a regular `zip` file in disguise. So the first step is to rename the file that Knowclip generates to `something.zip`, then decompress it. Inside the decompressed directory, you'll see a number of file, including a `collection.anki2` file. That's the SQLite file we'll be targeting.

We'll need to correct both the `notes` and `cards` tables. For convenience, we can do this in a script:

{{< highlight python >}}
#!/usr/bin/env python3

import sqlite3
import time
import datetime

# start date for new cards
new_date = datetime.datetime(2021,4,5,5,0)
new_epoch = int(new_date.timestamp() * 1000)
print(f'Will begin create date with epoch ms {new_epoch}.')

db_path = '/path/to/knowclip/generated/apkg/collection.anki2'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
q = 'SELECT id FROM notes'
cursor.execute(q)
note_rows = cursor.fetchall()
note_chg_sql_cmds = []
for note_row in note_rows:
	qn = f'UPDATE notes SET id = {new_epoch} WHERE id = {note_row[0]}'
	note_chg_sql_cmds.append(qn)
	qc = f'UPDATE cards SET nid = {new_epoch} WHERE nid = {note_row[0]}'
	new_epoch = new_epoch + 100
	cursor.execute(qc)
conn.commit()
for sql in note_chg_sql_cmds:
	cursor.execute(sql)
conn.commit()
conn.close()
{{< /highlight >}}

Just run this script against the collection.anki2 file before importing, and you'll have the correct date inside of Anki.

[^1]: [subs2srs](http://subs2srs.sourceforge.net) is frequently featured and offers similar features, but it Windows-only.
