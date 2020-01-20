---
layout: post
title: "Finding things with DEVONthink"
date: 2015-06-18 05:59:24 -0500
aliases: ['/2015/06/18/finding-things-with-devonthink/']
categories:
- organization
tags:
- devonthink
- organization
---
I've been a DEVONthink user for many years; it's an amazing piece of software. Currently I'm using DEVONthink Pro Office because I use all of the higher level capabilities. Over the years, my database structure and workflow have gone through many changes. In this post I'll describe my approach to finding things in DEVONthink.

### Databases

At first, I dumped everything into a single database. Over time, however, I realized that finding things was difficult because of the number of false positives when searching. I roughly divide my databases between areas of responsibility. For example, I'm a director at two local music organizations; so I have separate databases for each of those groups. However, most of my material goes into a single database. It's where all of the items of daily living go - bills, receipts, bookmarks, web clips, etc.

I do have an archive database. Although I don't systematically move items into the archive, when I find items that I'm sure I won't wish to see in my searches, I move them across to the archive.

### Tags

Tags are among the most powerful feature of DEVONthink Pro Office. In fact, because of the way tags are implemented in DTPO, I have begun to dump most of my folder hierarchy. There are two main ways of storing items in DTPO: groups and tags. The problem with groups is that they allow items to exist only in a single area.[^1] Sometimes it's hard to determine in advance where an item should go. For example, our health care provider sends monthly statements. Should they go in a bills folder, a folder for the provider, a medical folder?

{{< figure src="images/dtpo_tag_location.png" title="" alt="DEVONthink Pro Office location tags" class="left" >}}

Instead of building deep structures of groups, I've become disciplined at building a hierarchical tag list and tagging every item systematically. The choice of tags is dictated by how I want to find things.[^2] To be an item, I should be able to ask a series of questions about it, the answers to which will narrow the field. Typical question words help me construct a hierarchy. _Where_ becomes a location hierarchy. Now everything gets tagged with a location that lets me find items geographically. _What_ is the largest tree; and it evolves constantly over time as I add new items and try to classify them. _Who_ has two trees, a Vendor tree and a Person tree. I use either depending on which is appropriate to the item. _When_ is answered by the file data metadata. _Why_ becomes a Purpose tree which has branches for entities such as _action_, _reference_, etc. The _how_ question is represented by a Source tree with items such as web, note, scan, email, etc.

| Question | Tag tree      | Example                                  |
|----------|---------------|------------------------------------------|
| Where    | location      | location_us_mn_rochester                 |
| What     | topic         | topic_financial_tax_2015                 |
| When     | none          | file creation date                       |
| Why      | purpose       | purpose_reference                        |
| Who      | vendor person | topic_vendor_verizon, person_crustyclown |
| How      | source        | source_scan                              |

<br />

### Workflow

Every item that I collect goes into the global inbox. I make no attempt to tag or categorize the file at the initial collection point. In order to make collection even easier, I hae a folder on the Desktop titled "DT". Anything that is saved there triggers a [Hazel](http://www.noodlesoft.com/hazel.php) rule that moves the item to the DTPO global inbox. I check the global inbox daily and move items into destination databases according to the content. Most items go into the general purpose database that I call _Leviathan_.[^3]

{{< figure src="images/dtpo_inbox_counts.png" title="" alt="DEVONthink Pro Office inbox counts" class="left" >}}
Once an item is in the database inbox, the count of items shows up in the sidebar, acting as a trigger for me to get busy tagging items. Right now, almost every item will go into a reference group after tagging. Importantly, nothing gets out of the database inbox without being tagged.

Although everything goes into one large reference group, I still need to organize materials by project. That's where my _project_ tag tree comes into play. I create project tags for items that relate to a particular project. When materials come into the database that are related to that project, I tag them either directly in the information dialog or by dragging the items onto the tag in question. Finally, I create project smart groups based on the particular tag for that project.

This is my system for using DEVONthink Pro Office. In particular, it's how I _find_ things. HTH.

[^1]: That's not completely true. You can duplicate (copy) and replicate (create aliases of) items between groups.

[^2]: Hierarchical tags are a killer feature in DTPO because when you search against a tag, the entire hierarchy below it, if any, will also be taken into account. For more about hierarchical tags, see [this post](http://www.organizingcreativity.com/2012/07/quick-hierarchical-tagging-in-devonthink/) on the excellent [Organizing Creativity blog](http://www.organizingcreativity.com) blog.

[^3]: Leviathan (לִוְיָתָן) is a sea monster mentioned in the Tanakh. It has come to mean any large creature. My general purpose database fits that description pretty well.
