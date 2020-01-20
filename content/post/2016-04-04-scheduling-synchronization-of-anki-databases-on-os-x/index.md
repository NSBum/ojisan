---
title: Scheduling synchronization of Anki databases on OS X
date: 2016-04-04 05:55:37
aliases: ['/2016/04/04/Scheduling-synchronization-of-Anki-databases-on-OS-X/']
tags:
- anki
- programming
- automation
categories:
- anki
---
While working on a project to automatically collect statistics on my [Anki](http://ankisrs.net) databases (stay tuned...) I worked out a system for scheduling synchronization from my desktop OS X machine.

### Prerequisites

- [LaunchControl](http://www.soma-zone.com/LaunchControl/) is a GUI application that lets you create and manage user services on OS X
- [Anki](http://ankisrs.net) is a spaced repetition memorization software system

The solution relies on Automator. Normally, I don't care much for Automator. It has too many limits on what tasks I can accomplish and workflows created with it are often fragile. However, in this case, we take advantage of its workflow recording feature. We're going to record the process of opening Anki, selecting the profile to sync, then quitting Anki. This sequence of events ensures that the database on the local system is synchronized with the remote version.

<!-- more -->

### Creating a new workflow

* Start Automator and create a new workflow document.
* Make sure that Anki resides in the OS X Dock because our workflow is going to look for it there.
* Click "Record" to begin recording the workflow.
* Click "Anki" in the Dock.
* After Anki launches, select the profile that you want to load. (I'm note sure whether you see this dialog when you have only a single profile. I have three so I see a dialog box asking which one to load. If you don't see this window, just skip this step.)
* Anki will synchronize. When it is done, select "Quit" from the menu bar. Anki will sync again. Since we didn't change any content this is an unnecessary step, but Anki does it automatically.
* After Anki has finished synchronizing, click the "Stop" button on the recording window.

{{< figure src="images/watchmedo.jpg" title="Watch Me Do Actions" >}}

### Saving the workflow

You should now have an unsaved sequence of actions in the Watch Me Do group as above.

1. Save the workflow _as a workflow_ first. This will allow you to edit the workflow in some way in the future if you need to.
2. Convert the workflow to an application. This will allow you to run it from the command line later on.
3. Save the converted workflow to an application file type. Name it anything you like. I called it `ankisync`.
4. Quit Automator

### Allowing the workflow to control the computer

The privacy and security features on OS X may not allow you to run the Automator workflow from the command line without adding it to the list of trusted application.

{{< figure src="images/securityprivacy.jpg" title="Add ankisync" >}}

1. Open the Security and Privacy section of the System Preferences
2. Click on the Privacy tab
3. Click on Accessibility in the source list
4. Drag the newly created workflow application into the list and grant it permission to control the computer.

This should be enough to allow the workflow to do its job.

### Test that you can launch the workflow from the command line

1. Open the Terminal or iTerm depending on your preference. I prefer iTerm but Terminal is pre-installed on OS X.
2. Launch the workflow as follows:

{{< highlight bash >}}
$ open /path_to_your_workflow_app/ankisync.app
{{< /highlight >}}

If this doesn't properly launch your workflow, check that the everything is authorized properly in System Preferences.

### Schedule the workflow to run using LaunchControl

{{< figure src="images/launchcontrol.jpg" title="Add ankisync to LaunchControl" >}}

* Add a new User Agent in LaunchControl by selecting _User Agents_ from the job types list and clicking the _+_ button at the bottom of the source list.
* Use the [reverse DNS]() standard for naming your job.
* Drag a "Start calendar interval" item on the job.
* Configure the calendar interval according to the time you would like the job to run.
* In the text box "Program to run" add `open` and the path of the workflow application.
* Save your job and that should be it!

You should be aware that this relies on a somewhat fragile set of UI actions; but when it works, you'll have a automated method for keeping your Anki collection in sync.
