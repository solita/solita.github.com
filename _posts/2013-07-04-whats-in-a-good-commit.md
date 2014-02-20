---
layout: post
title: What's in a Good Commit?
author: noidi
excerpt: These tips can help you turn your VCS from a backup system into a valuable tool for communication and documentation.
---
<p></p>
Let's begin with a horror story.

You hear that issue `FOO-123` has been fixed. The bug had something to do with a subsystem you know well, so you have your own hunch about what might have caused it. To confirm your suspicion, you decide to take a look at how the bug was fixed. You spend quite some time rummaging through the revision history until you manage to narrow the fix down to four consecutive revisions, described in their commit messages as "dao tweaks", "moar", "Fixes." and "remove debug stuff". Each changeset looks huge. There are hundreds of lines of changes spread over a dozen of files. "What the...", you begin but pause, unable to choose just one of the myriad of profanities racing through your mind. "The fix shouldn't be more than a three-line change!"

![My Mind is Full of Profanity](/img/whats-in-a-good-commit/jackie.jpg)

Does this sound familiar? All too many developers use their version control system as nothing more than a haphazard pile of backups. The resulting history is useless for anything other than retrieving the files' contents at a given point in time. The following tips can help you turn your VCS from a backup system into a valuable tool for communication and documentation.

## 1. Only make one change per commit

If you fix `FOO-123` as well as `FOO-234`, refactor a couple of classes, add a button or two to the UI, and change tabs to spaces throughout the project, all in one commit, it's simply impossible for anyone to review the fix to `FOO-123`. You are the only one who knows which of your changes are part of the fix. In a week even you'll forget that.

What if a week later it turns out that your fix caused a new bug that's even worse? You can't undo the change using `backout` (Hg) or `revert` (Git), because that would mean stripping out all those other changes you made and a week's worth of work depends on them.

The solution is to only make one change in each commit. There are no hard and fast rules about what constitutes a single change, but if you can describe everything you did in a single sentence without using the word "and", you're probably in the clear.

One of the cool things about distributed version control systems is that if you end up with a working directory full of unrelated changes, you can [clean up the mess you've made](http://tomayko.com/writings/the-thing-about-git), but it's better not to make a mess in the first place. Before jumping into changing the code, decide what it is that you want to do and how you want to do it. Then focus on making that one change only.

It seems impossible to work on a piece of code without coming up with ideas on how it could be improved. You notice bugs, poorly factored code, and curious things that you'd like to investigate. No matter how tempting they seem, do not get sidetracked! These findings are valuable, so [jot them down](http://antirez.com/news/51) in a notebook or a TODO-file, but don't return to them until you current task is finished.

This is not just about better commits. When you're immersed in a programming problem, your head is full of little details related to the code you're working on. You lose all that if you start thinking about something else, and getting back into the flow takes time. To maximize your productivity you need to [minimize task switches](http://www.joelonsoftware.com/articles/fog0000000022.html).

Of course there are times when you find out that there's no way to finish your current task without first making some other change. The easiest way to keep the two changes separate is to `shelve` (Hg) or `stash` (Git) your current, unfinished change, make and commit the change that you depend on, and then return to your original task.

## 2. Make the whole change in one commit

A change is also hard to review and undo if it's spread over several commits. Typically this is a side effect of working on too many things at once. If you bite off more than you can chew, most of your changes will be unfinished by the time you want to save some of them. Focusing on one task at a time takes you a long way towards committing complete changes.

Some changes take so much time that you can't afford to start all over again if you make a mistake, so you need to save work-in-progress versions of your work. Luckily DVCSs allow you to save WIP versions for your own use while still publishing a single changeset to the central repository. You can make as many WIP commits as you want and then use [`histedit`](http://mercurial.selenic.com/wiki/HisteditExtension) (Hg) or [`rebase`](http://gitready.com/advanced/2009/02/10/squashing-commits-with-rebase.html) (Git) to fold/squash them into a single changeset when you're done.

Another approach, which I prefer because it keeps WIP changes clearly separated from permanent changesets, is to use Git's index or a patch in [Mercurial Queues](http://stevelosh.com/blog/2010/08/a-git-users-guide-to-mercurial-queues/) to store the latest known-good WIP version, which you update every time you make progress. If you make a mistake, you can restore your working directory to the version in the index/patch. I like to think of it as a one-slot quicksave for version control.

## 3. Document what you have changed

The commit message "Fixes" contains very little useful information. "Commit" contains none whatsoever. If someone is interested in the revision history, messages like this force them to read through the changes, and reading code is both slow and mentally taxing. By writing a gibberish commit message you save a minute but can waste hours of other people's time.

A good commit message tells the reader what part of the codebase was changed and how without them having to look at the code:

    SomeClass: use bleh instead of xyzzy in someMethod (fixes FOO-123)

## 4. Document why you made the change

Presumably there's always a good reason for every change made to a codebase. If that reason is not documented, the codebase becomes exposed to the following risks:

* The other developers do not understand why the code was written the way it was. When they change the code, they introduce problems that the original author had identified and avoided.

* The other developers assume that the code was written the way it was for a Good Reason&trade; so it's best left untouched. They treat it as a black box and add complex workarounds to avoid changing it. As a consequence the codebase becomes bloated and hard to understand.

If you need to break the project's conventions, or if there's a subtle reason why your code must be the way it is, document the reason in the code with a comment:

    -  xyzzy(bars);
    +  // Our bars are already sorted, so bleh is much faster than xyzzy
    +  bleh(bars);

If your code adheres to conventions and there are no subtleties to it, there's no need for inline documentation. It's still valuable to know why the new code is preferred over the old (especially if the change happens to introduce a new problem), so document the reason in the commit message:

    SomeClass: Don't flush caches in someMethod

    The caches are flushed automatically at the end of each request.

If the change fixes a reported issue, make sure you mention the ticket's number in the commit message so that a developer looking at the revision history can better understand the context in which the change was made.

## 5. Never commit code that's been commented out

I've never understood the reasoning behind committing code that's been commented out. I assume it's to keep old versions of the code around just in case the new code doesn't work, but that's just bizarre. Keeping track of old versions is the reason we use a version control system in the first place!

Why was the code commented out? Does it work? Should it work? Has it ever worked? Is it something we should strive towards or run away from? Code that's been commented out is worse than useless, because every time it's read, it raises questions like these without providing any answers. It only serves to confuse and distract from the code in use.

There's only one rule when it comes to committing commented-out code: ![NO!](/img/whats-in-a-good-commit/no.gif)

