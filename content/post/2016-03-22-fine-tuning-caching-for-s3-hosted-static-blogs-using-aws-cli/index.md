---
title: Fine-tuning caching for S3-hosted static blogs using AWS CLI
date: 2016-03-22 11:02:33
aliases: ['/2016/03/22/Fine-tuning-caching-for-S3-hosted-static-blogs-using-AWS-CLI/']
tags:
- blogging
- programming
categories:
- programming
---
Because the blogging system that I use doesn't apply finely grained object-level caching rules, I end up with objects such as images that cache appropriately but an `index.html` page that does not. I don't want client browsers to hang on to the main `index.html` page for more than an hour or so because it should update much more frequently than that as its content changes.

It's possible that I could dig around under the hood of [hexo](https://hexo.io) and create a version that applies customized caching rules. Instead, I make a second pass over the content, adjusting the Cache-Control and other metadata according to my needs. For this task I use the Amazon Web Services command line interface [AWS-CLI](http://docs.aws.amazon.com/cli/latest/reference/index.html#cli-aws).

### Installation

Installing the AWS CLI is straightforward. On the platform I use (OS X), it's just:

{{< highlight bash >}}
$ curl "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip" -o "awscli-bundle.zip"
$ unzip awscli-bundle.zip
$ sudo ./awscli-bundle/install -i /usr/local/aws -b /usr/local/bin/aws
{{< /highlight >}}

After installation, you will want to [configure AWS CLS](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html). Installing the credentials for AWS is an important step which you can do via the `aws configure` command:

{{< highlight bash >}}
AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
Default region name [None]: us-west-2
Default output format [None]: ENTER
{{< /highlight >}}

Once installed, you can use the AWS CLI to perform a variety of options on your S3 buckets. It's worth reading [documentation](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-using.html) to get familiar with the command structure which is very detailed.

### Using AWS CLI to adjust image caching

To compute new Cache-Control header dates for the `aws` command, I used Python for a little script to do the job. For images, I want to maximize caching in the request/reply chain. Since images are the heaviest objects traveling on the wire, I want minimize how many of them I need to reload. So I want to set a long cache time for these objects. Here's how I compute new dates and build up the `aws` command:

{{< highlight python >}}
#!/usr/bin/python

import datetime
from dateutil.relativedelta import relativedelta
import subprocess

weeks = 2
seconds = weeks * 7 * 24 * 60 * 60

today = datetime.datetime.now()
new_date = today + relativedelta(weeks=weeks)

command = '''aws s3 cp s3://ojisanseiuchi.com/ s3://ojisanseiuchi.com/ --exclude "*" '''
command += '''--include *.jpg '''
command += '''--include *.jpg '''
command += '''--recursive '''
command += '''--metadata-directive REPLACE '''
command += '''--expires {0} '''.format(new_date.isoformat())
command += '''--acl public-read '''
command += '''--content-encoding "gzip" '''
command += '''--cache-control "public, max-age={0}"'''.format(seconds)

subprocess.call(command,shell=True)
{{< /highlight >}}

This will build and execute the following command:

{{< highlight bash >}}
aws s3 cp s3://ojisanseiuchi.com/ s3://ojisanseiuchi.com/ --exclude "*" --include *.jpg --include *.jpg --recursive --metadata-directive REPLACE --expires 2016-04-05T11:37:16.181141 --acl public-read --content-encoding "gzip" --cache-control "public, max-age=1209600"
{{< /highlight >}}

This will recursively manipulate the metadata for all jpg and png files in the bucket. The `weeks` parameter can be adjusted to any duration you would like.

### Using AWS CLI to adjust the `index.html` caching

The main index page should get reloaded frequently. Otherwise users have no idea that the page has been changed. For this part, I'll drop down to the lower level `s3api` command for illustration. Here's the Python script to make this work:

{{< highlight python >}}
hours = 1
seconds = hours * 60 * 60   # seconds in hours
new_date = today + relativedelta(hours=hours)
command = '''aws s3api copy-object  --copy-source ojisanseiuchi.com/index.html --key index.html --bucket ojisanseiuchi.com '''
command += '''--metadata-directive "REPLACE" '''
command += '''--expires {0} '''.format(new_date.isoformat())
command += '''--acl public-read '''
command += '''--content-type "text/html; charset=UTF-8" '''
command += '''--content-encoding "gzip" '''
command += '''--cache-control "public, max-age={0}"'''.format(seconds)

subprocess.call(command,shell=True)
{{< /highlight >}}

When run, this will build and execute the following command:

{{< highlight bash >}}
aws s3api copy-object  --copy-source ojisanseiuchi.com/index.html --key index.html --bucket ojisanseiuchi.com --metadata-directive "REPLACE" --expires 2016-03-22T12:42:44.706536 --acl public-read --content-type "text/html; charset=UTF-8" --content-encoding "gzip" --cache-control "public, max-age=3600"
{{< /highlight >}}

This will ensure caching only for 1 hour.

### Automating the post-processing

As I've written before, I use Grunt to automate blogging tasks. To run the post-processing I've described about, I simply add it as a task in the `Gruntfile.js`

To initialize the post-processing task:

{{< highlight javascript >}}
grunt.initConfig({
    shell: {
        fixImageCacheHeaders: {
            options: {
                stdout: true,
                execOptions: {
                    cwd: '.'
                }
            },
            command: 'python fixCacheHeaders.py'
        }
    }
    //  etc...
}
{{< /highlight >}}

To register the task:

{{< highlight javascript >}}
grunt.registerTask('deploy', ['shell:clean', 'shell:generate', 'sitemap:production', 'robotstxt:production', 's3']);
grunt.registerTask('logpre', function() {
    grunt.log.writeln('*** Fix metadata ***');
});
grunt.registerTask('logpost', function() {
    grunt.log.writeln('*** Fixed metadata ***');
})
grunt.registerTask('deployf', function() {
    grunt.task.run(['shell:clean', 'shell:generate', 'sitemap:production', 'robotstxt:production', 's3']);
    grunt.task.run('logpre');
    grunt.task.run('shell:fixImageCacheHeaders');
    grunt.task.run('logpost');
})
{{< /highlight >}}

Now I can deploy the blog and run the post-processing using `grunt deployf`.

The entire metadata post-processing script is [available](https://gist.github.com/NSBum/0c379edcb9cf778ce6dd) as a gist. My updated [Gruntfile.js](https://gist.github.com/NSBum/72b6627e44565fb0712d) is too.
