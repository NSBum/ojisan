---
title: "Fixing Knowclip .apkg files: one more thing"
date: 2021-04-12T05:00:59-04:00
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

[Fixing the Knowclip note files](/2021/04/05/fixing-knowclip-anki-apkg-creation-dates/) as I described previously, it turns out, is only half of the fix with the broken .apkg files. You also need to fix the `cards` table. Why? Same reason. The rows are number sequentially from 1. But since Anki uses the card id field as the date added, the added field is always wrong. Again, the fix is simple:

{{< highlight python >}}
#!/usr/bin/env python3

import sqlite3
import time
import datetime

db_path = '/path/to/knowclip/generated/apkg/collection.anki2'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

q = 'UPDATE cards SET id = nid + 10'
cursor.execute(q)
conn.commit()
conn.close()
{{< /highlight >}}

Here's an improved version of the previous script, one that incorporates changes to both the `notes` and the `cards` tables.

{{< highlight python >}}
#!/usr/bin/env python3

import sqlite3
import time
import datetime

# start date for new cards
dt = input("Creation date 2021-04-05: ")
(year,month,day) = [int(x) for x in dt.split('-')]
tm = input("Creation time 05:00: ")
(hr, minute) = [int(x) for x in tm.split(':')]
new_date = datetime.datetime(year, month, day, hr, minute)
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
qc = f'UPDATE cards SET id = nid +10'
cursor.execute(qc)
conn.commit()
for sql in note_chg_sql_cmds:
	cursor.execute(sql)


conn.commit()
conn.close()
{{< /highlight >}}
