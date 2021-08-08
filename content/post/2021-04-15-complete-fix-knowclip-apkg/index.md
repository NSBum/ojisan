---
title: "Complete fix for broken Knowclip .apkg files"
date: 2021-04-15T06:24:08-04:00
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
I think this is the last word on fixing Knowclip .apkg files. I've developed this in bits and pieces; but hopefully this is the last word on the subject. See my previous articles, [here](/2021/04/12/fixing-knowclip-.apkg-files-one-more-thing/) and [here](/2021/04/05/fixing-knowclip-anki-apkg-creation-dates/), for the details.

This issue, again, is that Knowclip gives these notes and cards sequential `id` values starting at 1. But Anki uses the `note.id` and the `card.id` as the creation date. I logged it as an issue on Github, but as of 2021-04-15 no action has been taken.

This version takes the .apkg path as the script parameter and then does this rest. Instead of asking the user for the date and time for the first note (and card) it takes that information from the creation time of the .apkg file. Note that this has been tested only on macOS. Undoubtedly you will have to adapt this on other platforms.


{{< highlight python >}}
#!/usr/bin/env python3

import sqlite3
import time
import datetime
import zipfile
import os
import sys

def create_holding_dir(parent_path, name):
   path = os.path.join(parent_path, name)
   os.mkdir(path)
   return path

def delete_rogue_macosx_dir(target_dir):
   path = os.path.join(target_dir, '__MACOSX')
   os.rmdir(path)

def collection_path(target_dir):
   path = os.path.join(target_dir, 'collection.anki2')
   return path

def open_collection_db(target_dir):
   try:
      conn = sqlite3.connect(collection_path(target_dir))
      cursor = conn.cursor()
   except:
      exit("__UNABLE TO OPEN COLLECTION DB__")
   return (conn, cursor)

def restore_apkg(apkg_path, basename_with_path):
   # give apkg_path a unique name
   components = os.path.split(apkg_path)
   os.rename(basename_with_path, os.path.join(components[0], f'_{components[1]}'))

   # sys.argv[1] is the apkg to expand
try:
   apkg_path = sys.argv[1]
except:
   exit("__NO APKG PATH SPECIFIED__")
basename_with_extension = os.path.basename(os.path.normpath(apkg_path))
basename = basename_with_extension.rsplit( ".", 1 )[ 0 ]
basename_with_zip = basename + '.zip'
parent_dir = os.path.split(apkg_path)[0]
basename_with_path = os.path.join(parent_dir, basename_with_zip)
parent_path = os.path.abspath(os.path.join(basename_with_path, '..'))

# create a directory to hold the unzipped files
target_dir = create_holding_dir(parent_path, basename)

try:
   os.rename(apkg_path, basename_with_path)
except:
   print('ERROR - unable to rename file')
with zipfile.ZipFile(basename_with_path, 'r') as zip_ref:
   zip_ref.extractall(target_dir)

delete_rogue_macosx_dir(target_dir)
(conn, cursor) = open_collection_db(target_dir)

new_epoch = int(1000 * os.path.getctime(basename_with_path))

print(f'Will begin create date with epoch ms {new_epoch}.')

q = 'SELECT id FROM notes'
cursor.execute(q)
note_rows = cursor.fetchall()
note_chg_sql_cmds = []
for note_row in note_rows:
   qn = f'UPDATE notes SET id = {new_epoch} WHERE id = {note_row[0]}'
   note_chg_sql_cmds.append(qn)
   qc = f'UPDATE cards SET nid = {new_epoch}, id = {new_epoch} WHERE nid = {note_row[0]}'
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

# save a backup copy of the original apkg name
restore_apkg(apkg_path, basename_with_path)

# compress the altered collection directory into a zip
# and rename it as an .apkg file for Anki
dest_zip_file_path = os.path.join(parent_path, basename+'.zip')
zf = zipfile.ZipFile(dest_zip_file_path, 'w', zipfile.ZIP_DEFLATED)
for root, dirs, files in os.walk(target_dir):
   for file_name in files:
      zf.write(os.path.join(root, file_name))
os.rename(basename_with_path, apkg_path)
{{< /highlight >}}
