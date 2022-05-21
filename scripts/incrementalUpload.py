#!/usr/bin/env python3

import os
import sys
import hashlib
import sqlite3
import time
import subprocess
import re
from concurrent.futures import ThreadPoolExecutor


SRC_DIR = "/Users/alan/Documents/dev/ojisan/public"
BUCKET_URL = "s3://www.ojisanseiuchi.com"
DB_PATH = '/Users/alan/Documents/dev/ojisan/checksums.db'

def aws_copy(source: str, dest: str):
   cmd_list = ["aws","s3", "cp", source, dest ]
   subprocess.run(cmd_list)
   
def bucket_path_from_local(source_path: str) -> str:
   m = re.search(r'.*/public/(.*)', local_path)
   bucket_path = f"{BUCKET_URL}/{m[1]}"
   return bucket_path

def change_md5_query(changed: tuple) -> str:
   chg_query = f"UPDATE checksums SET md5 = '{changed[2]}' "
   chg_query += f"WHERE path = '{changed[0]}' AND fn = '{changed[1]}'"
   return chg_query

def select_md5_query(path: str, fn: str) -> str:
   query = f"SELECT md5 FROM checksums "
   query += f"WHERE path LIKE '{path}' "
   query += f"AND fn LIKE '{fn}' LIMIT 1"
   return query

def insert_md5_query(path: str, fn: str, checksum: str) -> str:
   query = f"INSERT INTO checksums (path, fn, md5) "
   query += f"VALUES ('{path}', '{fn}', '{checksum}')"
   return query
   
connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

changed_files = []
for root, subdirs, files in os.walk(SRC_DIR):
   for file in files:
      with open(os.path.join(root, file), 'rb') as _file:
         if file == ".DS_Store":
            continue
         file_md5 = hashlib.md5(_file.read()).hexdigest()
         cursor.execute(select_md5_query(root, file))
         row = cursor.fetchone()
         if row is None:
            # file md5 doesn't exist
            cursor.execute(insert_md5_query(root, file, file_md5))
            connection.commit()
            # since this is a new file, we need to
            # add it to the upload list
            changed_files.append((root, file, file_md5))
         else:
            # file md5 exists, is it changed?
            if row[0] != file_md5:
               print(f'changed db md5 = {row[0]} vs {file_md5}')
               changed_files.append((root, file, file_md5))
# process changed files
print(f"{len(changed_files)} files to upload")
with ThreadPoolExecutor(max_workers=16) as executor:
   for changed in changed_files:
      chg_query = change_md5_query(changed)
      cursor.execute(chg_query)
      connection.commit()
      local_path = f"{changed[0]}/{changed[1]}"
      bucket_path = bucket_path_from_local(local_path)
      future = executor.submit(aws_copy, local_path, bucket_path)
connection.commit()
connection.close()
print('done')