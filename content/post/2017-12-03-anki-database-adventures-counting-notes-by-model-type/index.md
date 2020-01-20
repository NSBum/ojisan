---
title: 'Anki database adventures: Counting notes by model type'
date: 2017-12-03 06:48:16
aliases: ['/2017/12/03/Anki-database-adventures-Counting-notes-by-model-type/']
tags:
- python
- programming
- anki
categories:
- anki
---
Continuing my series on accessing the Anki database outside of the Anki application environment, here's a piece on accessing the note type model. You may wish to start [here](/2017/12/01/Working-with-the-Anki-database-on-mac-OS/) with the first article on accessing the Anki database. This is geared toward mac OS. (If you're not on mac OS, then start [here](https://eshapard.github.io/anki/) instead.)

### The note type model

Since notes contain flexible fields in Anki, the model for a note type is in JSON. The best guess definition of the JSON is:

{{< highlight json >}}
{
    "css": "CSS, shared for all templates",
    "did":
        "Long specifying the id of the deck that cards are added to by default",
    "flds": [
       "JSONArray containing object for each field in the model as follows:",
       {
         "font": "display font",
         "media": "array of media. appears to be unused",
         "name": "field name",
         "ord": "ordinal of the field - goes from 0 to num fields -1",
         "rtl": "boolean, right-to-left script",
         "size": "font size",
         "sticky": "sticky fields retain the value that was last added \
                    when adding new notes"
      }
    ],
    "id": "model ID, matches cards.mid",
    "latexPost": "String added to end of LaTeX expressions",
    "latexPre": "preamble for LaTeX expressions",
    "mod": "modification time in milliseconds",
    "name": "model name",
    "req": [
      "Array of arrays describing which fields are required \
       for each card to be generated",
      [
        "array index, 0, 1, ...",
        "? string, all",
        "another array",
        ["appears to be the array index again"]
      ]
    ],
    "sortf": "Integer specifying which field is used for sorting (browser)",
    "tags": "Anki saves the tags of the last added note to the current model",
    "tmpls": [
      "JSONArray containing object of CardTemplate for each card in model",
      {
        "afmt": "answer template string",
        "bafmt": "browser answer format: used for displaying answer in browser",
        "bqfmt": "browser question format: \
                  used for displaying question in browser",
        "did": "deck override (null by default)",
        "name": "template name",
        "ord": "template number, see flds",
        "qfmt": "question format string"
      }
    ],
    "type": "Integer specifying what type of model. 0 for standard, 1 for cloze",
    "usn": "Update sequence number: used in same way as other usn vales in db",
    "vers": "Legacy version number (unused)"
}
{{< /highlight >}}

Our goal today is to count all of the notes that have a given note type. Fortunately, there's a built-in method for this:

{{< highlight python >}}
verbModel = col.models.byName(u'Русский - глагол')
{{< /highlight >}}

Here we find the model object (a Python dictionary) named 'Русский - глагол' (that's Russian verb, by the way.) To access its `id`:

{{< highlight python >}}
modelID = verbModel['id']
{{< /highlight >}}

Now we just have to count:

{{< highlight python >}}
query = """SELECT COUNT(id) from notes WHERE mid = {}""".format(verbModel['id'])
verbNotes = col.db.scalar(query)

print 'There are {:.5g} verb notes.'.format(verbNotes)
{{< /highlight >}}

And that's it for this little adventure in the Anki database.

### See also:

- [Working with the Anki database on mac OS](/2017/12/01/Working-with-the-Anki-database-on-mac-OS/)
- [Accessing the Anki database with Python: Working with a specific deck](/2017/12/02/Accessing-the-Anki-database-with-Python-Working-with-a-specific-deck/)
- [Open the Anki database from Python](https://eshapard.github.io/anki/)
- [Anki database structure](https://github.com/ankidroid/Anki-Android/wiki/Database-Structure) - A thorough explanation of all the tables and fields
- [Anki Scripting 101](https://www.juliensobczak.com/tell/2016/12/26/anki-scripting.html#AlookinsidetheAnkimodel) - the motherlode of information about scripting Anki outside the add-on environment.
- [All of my articles about Anki](/categories/anki/)
