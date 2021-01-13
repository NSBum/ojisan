---
title: "More on integrating Hazel and DEVONthink"
date: 2021-01-05T04:00:25-05:00
draft: false
authorbox: false
sidebar: false
tags:
- hazel
- devonthink
- perl
- applescript
categories:
- programming
---
Since DEVONthink is my primary knowledge-management and repository tool on the macOS desktop, I constantly work with mechanisms for efficiently getting data into and out of it. I [previously wrote](/2016/05/08/import-and-tag-with-hazel-and-devonthink-pro-office/) about using [Hazel and DEVONthink](/2016/05/08/import-and-tag-with-hazel-and-devonthink-pro-office/) together. This post extends those ideas about and looks into options for preprocessing documents in Hazel before importing into DEVONthink as a way of sidestepping some of the limitations of Smart Rules in the latter. I'm going to work from a particular use-case to illustrate some of the options.

### Use case

While preparing for tax season, I download all of my bank statements because I have to deal with foreign accounts for FATCA compliance. (Thanks a lot, U.S.!) It would be ideal if I could analyze the document content and rename the statement based on dates in the PDF. While Smart Rules in DEVONthink are quite robust, I have two problems with them:
1. They don't reliably trigger automatically. Often I find that the matching process works, but the actions aren't triggered. Instead, they "accumulate" in the Smart Rule group and I have to select them and "Apply Rules" to get the actions started. Sometimes it works; sometimes it doesn't.
2. Options for extracting content from the PDF are limited. Specifically, I've not found a way to pull content on the OCR'd text of the PDF. Certainly, it's possible to _match_ against content; but extracting fields and using that data to, say, rename the document seems impossible.

Turning to Hazel, then, I can do much of the required pre-processing of the PDF document before it hits DEVONthink. In our particular use-case, I want to extract the statement end date from the PDF content and use those data to rename the document before it reaches DEVONthink. Otherwise, all of the statements have the same gibberish names as they come from the bank.

### Using CAM::PDF to inspect the PDF

I like to work in Perl when I can because:
- It plays nicely with the lower levels that we're working in here.
- I understand its regex model well
- Rarely having to deal with versioning issues is a place over Python.

There are a fer Perl packages that can inspect and manipulate PDF documents. Out of familiarity, I chose `CAM::PDF`. The first step is to dive into the text content of the PDF and see what's there.

{{< highlight perl >}}
#!/usr/bin/perl

use CAM::PDF;
use Data::Dumper; 
$Data::Dumper::Indent = 1; $Data::Dumper::Sortkeys = 1;

my $filename = "/Users/alan/blah2.pdf";
my $pdf = CAM::PDF->new($filename);
my $content = $pdf->getPageText(1);
print Dumper($content);
{{< /highlight >}}

Now I can sort through the text and find the data of interest:

{{< highlight txt >}}
Account
No.
OCT
30/20
-
NOV
30/20
0026
0026-7247238
{{< /highlight >}}

_Don't worry, I've obfuscated the account information here._

To extract `NOV`, `30` and `20`, I can use regex to pull them out of the content. Ideally, the content will remain stable between statements. To tune the regular expression, I use the excellent [Patterns]() application on macOS, but there are many others. Here's the extraction process laid out with a little more detail:

{{< highlight perl >}}
#!/usr/bin/perl

use CAM::PDF;
use Data::Dumper; 
$Data::Dumper::Indent = 1; $Data::Dumper::Sortkeys = 1;

my $filename = "/Users/alan/blah2.pdf";
my $pdf = CAM::PDF->new($filename);
my $content = $pdf->getPageText(1);

if ($info) {
   if( $content =~ m/-\n(\D+)\n(\d+)\/(\d+)\n\d+\n0026-7247238/ ) {
      my ($month_str,$day,$year) = (lc($1), $2, $3);
      my %month_dict = (
         jan =>  1, feb =>  2, mar =>  3,
         apr =>  4, may =>  5, jun =>  6,
         jul =>  7, aug =>  8, sep =>  9,
         oct => 10, nov => 11, dec => 12
      );
      my $month_num = $month_dict{$month_str};
      my $fn = sprintf("20%d-%02d-%d Acme Bank business statement.pdf", $year, $month_num, $day);
      my @f = split('/',$filename);
      splice @f, -1;
      push @f, $fn;
      $ff = join "/",@f;
      print $ff;
      #  rename($filename, $ff);    # rename the original file 
   }
   else { print "No match\n"; }
}
exit $?;
{{< /highlight >}}

If implementing this script as part of an actual Hazel rule, then you'll want to uncomment the `rename` line, remove the `print $ff` and the final `else` condition. Of course, you'll need to adjust the regex and so forth since this is specific to my use case.

### Importing to DEVONthink

Now that we've dived in the PDF text, extracted the information needed to rename the file and have done so, we can tag and import the file into desired DEVONthink group. This we'll do via AppleScript:

{{< highlight applescript >}}
tell application id "DNtp"
   -- whatever your db name is, mine is leviathan
   set dbs to first database whose name is "leviathan" 
   set myGroup to get record at "/path/to/your/group" in dbs
   set myRecord to import (POSIX path of theFile) to myGroup
   set tags of myRecord to {"main", "topic_financial", "topic_financial_banking", "topic_financial_content", "topic_financial_content_statement", "vendor", "vendor_acmebank"}
end tell
{{< /highlight >}}

### References

- [Import and tag with Hazel and DEVONthink Pro Office](/2016/05/08/import-and-tag-with-hazel-and-devonthink-pro-office/)
- [Working with DEVONthink Pro Office and Hazel](/2015/10/17/working-with-devonthink-pro-office-and-hazel/)
