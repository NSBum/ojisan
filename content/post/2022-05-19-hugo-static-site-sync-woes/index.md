---
title: "Hugo static site upload woes and a way forward"
date: 2022-05-19T18:44:12-04:00
draft: false
authorbox: false
sidebar: false
tags:
- hugo
- blog
- python
- aws
- s3
categories:
- programming
---
As much as I love the static website concept in general and Hugo in particular, there is one part of the Hugo/S3 infrastructure that I despise which is the lack of incremental uploads and the fact that no matter whether I use the `--noTimes=false` flag to compile my sites with `hugo`. It seems to touch every single file, every single time. Therefore, whatever sync utility I chose sees every file as new and in need of upload. For this blog, that takes about 10 minutes.

Since I only sporadically see people complaining about this online, the problem is either that I haven't figured out the magical incantation to stop `hugo` from touching unchanged files, or I just have really slow upload speeds (I do.) or something else. In any case, I've decided to take matters into my own hands and force the upload process to respect the MD5 hash of each file. We store these hashes in a database and then walk the `/public` directory examining comparing hashes. Only if the hashes differ, or if it's a new file will we add it to the upload list.

All we need is a sqlite database stored in the project root and a simple script. First the database has the following structure:

{{< highlight sql >}}
CREATE TABLE "checksums" (
   "id" INTEGER PRIMARY KEY AUTOINCREMENT,
   "path" TEXT,
   "fn" TEXT,
   "md5" TEXT
);
{{< /highlight >}}

And the script:

{{< highlight python >}}
#!/usr/bin/env python3

import os
import sys
import hashlib
import sqlite3
import time
import subprocess
import re
from concurrent.futures import ThreadPoolExecutor


SRC_DIR = "/path/to/public/dir"
BUCKET_URL = "s3://your.bucket.com"
DB_PATH = /path/to/checksums.db'
   
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
   
connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

changed_files = []
for root, subdirs, files in os.walk(SRC_DIR):
   for file in files:
      with open(os.path.join(root, file), 'rb') as _file:
         file_md5 = hashlib.md5(_file.read()).hexdigest()
         query = f"SELECT md5 FROM checksums \
                   WHERE path LIKE '{root}' \
                   AND fn LIKE '{file}' LIMIT 1"
         cursor.execute(query)
         row = cursor.fetchone()
         if row is None:
            # file md5 doesn't exist
            add_query = f"INSERT INTO checksums (path, fn, md5) \
                          VALUES ('{root}', '{file}', '{file_md5}')"
            cursor.execute(add_query)
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
with ThreadPoolExecutor(max_workers=16) as executor:
   for changed in changed_files:
      chg_query = change_md5_query(changed)
      cursor.execute(chg_query)
      
      local_path = f"{changed[0]}/{changed[1]}"
      bucket_path = bucket_path_from_local(local_path)
      future = executor.submit(aws_copy, local_path, bucket_path)
connection.commit()
connection.close()
{{< /highlight >}}

For simple posts only two files might be changed - the root index page and the post page itself. But if new tags or categories are required, or pagination gets shuffled around, a larger number of files may be affected. That's why I've divided the work in a thread pool. With informal testing that strategy seems to provide about 10x performance improvement over just a singular serial execution on the main thread. The greatest savings in efficiency comes from avoiding uploading images repeatedly.

Just build the site normally and run the script to upload and you're good to go. Enjoy! If you have questions, you can reach me through my [contact page](http://www.shortwhale.com/NSBum)

### Prerequisites

The AWS command-line interface tool is required. Install whatever release is compatible with your system. 

### Alternatives

I've explored many of these options for deploying Hugo static sites to AWS S3. Each has some limitations which I won't go into in detail. But I will note that I had problems with each of them "over-syncing" files that had not actually changed.

- [s3deploy](https://github.com/bep/s3deploy)
- [s3sync](https://github.com/larrabee/s3sync)
- [AWS S3 cli](https://docs.aws.amazon.com/cli/latest/reference/s3/) - under-the-hood my sync option uses this interface but in a non-standard way.
