---
title: Collapsing DEVONthink groups via AppleScript
date: 2015-11-23 04:48:30
aliases: ['/2015/11/23/Collapsing-DEVONthink-groups-via-AppleScript/']
tags:
- organization
- devonthink
- programming
- applescript
categories:
- organization
---
I've been moving to a tag-based system for organizing content in DEVONthink. All of my content for each database goes into a single group called "reference." If I want to find something, I search the hierarchical tag structure instead of diving into some arbitrary list of groups.

But I still have groups that I'd like to collapse into the reference group. So I wrote an AppleScript to perform this action. Notably, most of the action is in the `processGroup()` handler which is recursive because we do not know how deep the group hierarchy goes.

Here's the script if it's something you can use:

{{< highlight applescript >}}
-- collapse all groups into a single reference group
-- Created by Alan Duncan on 2015-11-23 03-15-56
-- Copyright (c) 2015 Alan K. Duncan.
-- Distributed under the terms of the MIT license

-- some error codes we might encounter
property InvalidRecordIndexError : -1719

-- warning string template
property ConfirmText : "Collapse all groups in database: "

-- name of groups that we don't want to move contents of
property ExcludedRecordNames : {"Inbox", "Tags", "Mobile Sync", "Trash", "reference"}

-- the reference group
global refGroup

-- list of groups to delete
global deleteGroups

tell application "DEVONthink Pro"
   set questionText to ConfirmText & name of current database & "?"
   set confirm to display dialog questionText buttons {"Yes", "No"} default button 2
   set answer to button returned of confirm
   if answer is equal to "Yes" then
      set deleteGroups to {}
      set refGroup to referenceGroup(current database) of me
      tell current database
         repeat with aRecord in (every record whose type is group)
            if name of aRecord is not in ExcludedRecordNames then
               -- this is a legitimate group to process
               processGroup(aRecord) of me
               -- this group has been processed; it can be deleted
               set end of deleteGroups to aRecord
            end if
         end repeat

         cleanupGroups() of me
      end tell
   end if
end tell

-- remove all groups that are marked for deletion
on cleanupGroups()
   tell application "DEVONthink Pro"
      repeat with deleteGroup in deleteGroups
         delete record deleteGroup
      end repeat
   end tell
end cleanupGroups

-- recursively process groups
on processGroup(aGroup)
   tell application "DEVONthink Pro"
      set theChildren to children of aGroup
      repeat with aRecord in theChildren
         -- if this child is a group, then enter recursively
         if type of aRecord is group then
            processGroup(aRecord) of me
         else
            move record aRecord to refGroup
         end if
      end repeat
   end tell
end processGroup

-- return the reference group, creating it if it doesn't exist
on referenceGroup(db)
   using terms from application "DEVONthink Pro"
      tell db
         try
            set referenceGroup to the first record whose name is "reference"
         on error error_message number error_number
            if error_number is InvalidRecordIndexError then
               -- try to create a group "reference"
               set refGroup to create record with {name:"reference", type:group} in root
            end if
         end try
      end tell
   end using terms from
end referenceGroup
{{< /highlight >}}
