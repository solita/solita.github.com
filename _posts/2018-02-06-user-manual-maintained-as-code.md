---
layout: post
title: User Manual Maintained Like Code
author: riikkanen
excerpt: The code is developed in feature branches. The user instruction documentation is not, which causes some trouble. Could the user manual be integrated tighter to the code? If so, could the manual still be easy to deliver to the customer?
tags:
- programming
- user manual
- asciidoctor
- maven
---

In our software project, we are dealing with an entire application family. Some of the applications are in maintenance phase, and some are in active development phase. However, new features emerge every now and then and old features are developed according to the feedback given by the users. This means that we need to update our user instruction documentation regularly.

# the Old Way

We have maintained our user instruction documentation as a few pages in Confluence. Confluence has offered a simple way to allow multiple editors, easy formatting and attaching images. When the software is delivered, the user instructions should be shipped with the new version. In our project, this meant converting the Confluence pages to html pages, which then could be saved in a dedicated web server location for the users to find via internet.

### Too much monkey business

The importing Confluence pages to html pages included a lot of manual work even the functionality is a basic feature of Confluence. The manual work included editing the generated html files, such as, removing unnecessary content from the header and footer, removing the list of attachments and so on. It is not a big deal once, but when you do it in every couple of weeks, it feels quite boring. We tried to find a way to customize look-and-feel of the html import but there were not enough tools to handle it. Confluence offers extensive support customizing the output when converting to pdf but not to html. Of course, some of the needs could have been handled with custom css.

### Outside the Natural Flow

The code is developed in feature branches, each branch corresponding to a Jira task defining the feature. In our project the feature branch is merged to the develop branch only after it is known for sure that the feature should and - even more important - is allowed to be included in the next release. This means that the user instructions can not be updated when the feature is developed, which otherwise is the natural moment to document the feature you have been working on. Unfortunately, we had to break the flow before we were certain that updating the instructions was ok. However, as you can guess, the updating of instructions was often forgotten when the feature was finally merged to the develop.

### Bad Traceability

There was also no easy way to check whether someone had updated the user manual or not. Confluence provides version history but it does not reflect the version history in the codebase. Being sure of whether a feature was documented or not was work for a detective. Text search proved to be the most powerful tool.

## Go with the flow

Our dream come true would have been a solution that integrates the code and the user manual more tightly to each other. Maybe the user manual could be maintained like code, even in the same repository, in the same commits. That way a feature branch could contain both the updates to the codebase and to the user instructions. Thus, the feature developed can similarly be documented to the user manual, and we can have different versions of the user manual at the same time. Using descriptive git commit messages including the Jira ticket ids, the updates to the user instructions can be traced as accurate as the code changes. 

Updating the user manual as we develop provides the updated instructions also for the fellow programmer testing our feature. How this feature should work? Are the instructions updated a) at all b) in adequate level? 

When the feature branch is finally merged to the develop, the different versions of the user manual are merged too. If there are conflicts, they can be resolved like any other conflicts in the codebase.

In addition to, it would be nice if generating the final html pages would be more fluent and more automated than in Confluence.

## Dream Come True


![code on screen](/img/programming-language/photo_koodia.JPG)
