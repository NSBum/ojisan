"""incrementalUpload.py

Usage:
   incrementalUpload.py db create (--dbpath=<dbpath>)
   incrementalUpload.py site transfer (--src=<srcdir>) (--bucket=<bktaddr>) (--dbpath=<dbpath>) [-d | --dryRun]
   incrementalUpload.py (-h | --help)
   incrementalUpload.py (-v | --version)

Options:
   -h --help               Show this help info
   -v --version            Show the script version
   -i --forceExcludeMedia  Do not include media even if checksum differs
   -d --dryRun             Simulate upload, but make no file transfers
   --src=<srcdir>          Path to /public directory of site
   --bucket=<bktaddr>      Bucket address
   --dbpath=<dbpath>       Path to checksum database
"""
   
import os
import sys
import hashlib
import sqlite3
import time
import subprocess
import re
from concurrent.futures import ThreadPoolExecutor
from docopt import docopt
import shlex

SRC_DIR = "/Users/alan/Documents/dev/ojisan/public"
BUCKET_URL = "s3://www.ojisanseiuchi.com"
DB_PATH = '/Users/alan/Documents/blog/ojisan_incremental_upload.db'

def aws_copy(source: str, dest: str):
   cmd = f'aws s3 cp {source} {dest}'
   subprocess.run(shlex.split(cmd))
   
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

def uri_strip_protocol(uri: str) -> str:
   m = re.search(r'^.*://(.*)$', uri)
   if m:
      uri = m[1]
   return uri

def bucket_exists(bpath: str) -> bool:
   bpath = uri_strip_protocol(bpath)
   
   cmd = f'aws s3api head-object --bucket {bpath} --key index.html'
   cmd_list = shlex.split(cmd)
   resp = subprocess.run(cmd_list, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
   return (resp.returncode == 0)
   
   
if __name__ == '__main__':
   connection = None
   arguments = docopt(__doc__, version='incrementalUpload.py 0.9')
   print(arguments)
   if arguments['create'] and arguments['db']:
      # docopt insures that we have a --dbpath
      # does the db file already exist?
      dbpath = arguments['--dbpath']
      connection = sqlite3.connect(dbpath)
      cursor = connection.cursor()
      q = """CREATE TABLE "checksums" (
               "id" INTEGER PRIMARY KEY AUTOINCREMENT,
               "path" TEXT,
               "fn" TEXT,
               "md5" TEXT
               );"""
         
      cursor.execute(q)
      print('database created')
      sys.exit(-1)
         
      print("create db")
   else:
      if arguments['site'] and arguments['transfer']:
         BUCKET_PATH = arguments['--bucket']
         if not bucket_exists(BUCKET_PATH):
            print('ERROR: bucket does not exist')
            connection.close()
            sys.exit(-1)
         SRC_DIR = arguments['--src']
         # exit if source directory doesn't exist
         if not os.path.exists(SRC_DIR):
            print('ERROR: src directory does not exist')
            sys.exit(-1)
         DB_PATH = arguments['--dbpath']
         if not os.path.exists(DB_PATH):
            print('ERROR: db path does not exist')
            sys.exit(-1)
   changed_files = []
   if connection is None:
      dbpath = arguments['--dbpath']
      connection = sqlite3.connect(dbpath)
      cursor = connection.cursor()
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
   if not arguments['--dryRun']:
      with ThreadPoolExecutor(max_workers=16) as executor:
         for changed in changed_files:
            chg_query = change_md5_query(changed)
            cursor.execute(chg_query)
            connection.commit()
            local_path = f"{changed[0]}/{changed[1]}"
            bucket_path = bucket_path_from_local(local_path)
            future = executor.submit(aws_copy, local_path, bucket_path)
   else:
      print('--dryRun option selected - nothing will be transferred')
   connection.commit()
   connection.close()
   print('done')