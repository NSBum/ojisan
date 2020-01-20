---
title: Automate hexo blogging tasks with Grunt
date: 2016-02-25 17:43:06
aliases: ['/2016/02/25/Automate-hexo-blogging-tasks-with-Grunt/','/hexogrunt']
tags:
- blogging
- hexo
- javascript
- grunt
- nodejs
- aws
category:
- programming
---
In my never-ending journey to find the optimal blogging platform, I wandered into the [hexo](https://hexo.io) camp. Among its many attributes is _speed_. Compared to Octopress, site generation is very fast. However, deployment has been tricky. Since I host my blogs from an Amazon S3 bucket, I tried to use the aws deployer commonly used with hexo; but I could never get it to install properly on OS X 10.11. So I [wrote my own](http://ojisanseiuchi.com/2015/11/25/A-new-hexo-deployer-for-Amazon-web-services/) deployer that essentially just runs an AppleScript that handles the synchronization task. It is __very slow__. So I'm always on the lookout for faster deployment schemes. It looks like a [Grunt](http://gruntjs.com)-based system is the ticket.

### Starting point for hexo automation

Chitrang Shah wrote a [series of articles](http://chitrangshah.com/tags/static-blog-setup/) on setting up a blog using hexo, Amazon S3 and Grunt. His piece on [automating deployment](http://chitrangshah.com/2014/03/13/static-blog-site-with-hexo-part-3/) with Grunt was the starting point that I needed. His solution relies on the `grunt-s3` plugin which unfortunately is no longer supported and doesn't work with current versions of Grunt. But the concept is sound.

First more about Grunt:

### About Grunt
As the [Grunt](http://gruntjs.com) page says, it's a JavaScript task runner, meant for automating repetitive tasks like testing, deploying, etc. It installs easily:

{{< highlight bash >}}
npm install -g grunt-cli
{{< /highlight >}}

The above will install grunt globally on the local machine. To use Grunt to automate your blogging tasks, you need to install the grunt shell plugin in the top level of your blog's directory.

{{< highlight bash >}}
npm install grunt-shell --save-dev
{{< /highlight >}}

### Install Grunt plugins for sitemap and robots.txt

Install two additional plugins `grunt-sitemap` and `grunt-robots-txt`.

{{< highlight bash >}}
npm install grunt-sitemap --save-dev
npm install grunt-robots-txt --save-dev
{{< /highlight >}}

### Install Grunt plugin for S3 deployment

Here is where this solution diverges from Chitrang Shah's. Instead of `grunt-s3`, I'm using [`grunt-aws`](https://github.com/jpillora/grunt-aws).

{{< highlight bash >}}
npm install --save-dev grunt-aws
{{< /highlight >}}

To use this plugin, you'll have to modify Shah's `Gruntfile.js`. Create the `Gruntfile.js` at the root level of your blog's local directory. This file specifies the actions that are available from the command line.

{{< highlight javascript >}}
module.exports = function(grunt){
	grunt.initConfig({
		pkg: grunt.file.readJSON('package.json'),
		aws: grunt.file.readJSON('grunt-aws.json'),
        // additional Configuration
    });
    // load and register tasks
};
{{< /highlight >}}

Loading the npm tasks is straightfoward:

{{< highlight javascript >}}
//Load NPM tasks
grunt.loadNpmTasks('grunt-shell');
grunt.loadNpmTasks('grunt-robots-txt')
grunt.loadNpmTasks('grunt-sitemap');
grunt.loadNpmTasks('grunt-aws');
{{< /highlight >}}

Then we just need to string the tasks together in logical sequence.

{{< highlight javascript >}}
//Grunt tasks
grunt.registerTask('default', ['shell:clean', 'shell:generate', 'sitemap:dev',
'robotstxt:dev', 'shell:server']);
//grunt.registerTask('staging', ['shell:clean','shell:generate','sitemap:staging',
'robotstxt:staging', 's3:staging']);
grunt.registerTask('deploy', ['shell:clean', 'shell:generate', 'sitemap:production', 'robotstxt:production',
's3']);
{{< /highlight >}}

I'm ambivalent about staging for a small blog; so I've left it out. YMMV.

Use a separate file that is not checked into version control for your AWS credentials. My `grunt-aws.json` looks like this:

{{< highlight json >}}
{
    "accessIdProduction" : "...,
    "accessKeyProduction" : "...",
    "bucketProduction" : "..."
}
{{< /highlight >}}

The complete `Gruntfile.js` for this blog [is available](https://gist.github.com/NSBum/5dd35074d17d93f0cf76) as a gist.

Finally, to use our new blog automation to clean, generate, and serve the blog locally, it's just `grunt`. To clean, generate and deploy, it's `grunt deploy`. This is a very straightforward way to automate your hexo blog and speedily deploy it to S3.
