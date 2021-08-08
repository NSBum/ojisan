---
title: "Querying the Anki database when the application is running"
date: 2021-07-13T05:50:53-04:00
draft: false
authorbox: false
sidebar: true
tags:
- anki
- sql
categories:
- Anki
---
When the Anki application is open on the desktop, it places a lock on the sqlite3 database such that it can't be queried by another process. One workaround is to try to open the database and if it fails, then make a temporary copy and query that. Of course, this only works with read-only queries. Here's the basic strategy:

{{< highlight python >}}
#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# requires python >= 3.8 to run because of anki module

from anki import Collection, errors

if __name__ == "__main__":
    try:
        col = Collection(path_to_anki_db)
    except (errors.DBError:
        # anki is open, copy to temp file
        import tempfile
        import shutil
        import os

        with tempfile.TemporaryDirectory() as tmpdir:
            dst = os.path.join(tmpdir, 'collectiontemp.anki2')
            shutil.copy(COLLECTION_PATH, dst)
            col = Collection(dst)
            # do something with Anki db
{{< /highlight >}}

Note that the `tempfile` context manager will discard the database, if there are actions on the collection that are common to the Anki-is-open and Anki-is-not-open paths then those should be abstracted to separate function.
