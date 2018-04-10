---
layout: post
title: User Manual Maintained Like Code
author: riikkanen
excerpt: 'Unlike our code, we don't develop our user manual in feature branches, which causes some trouble for us. Could the user manual be integrated tighter to the code? If so, could the manual still be easy to deliver to the customer?
tags:
- documentation
- maven
---

In our software project, we are dealing with an entire application family. Some of the applications are already in maintenance phase, and some are in active development phase. However, new features are introduced every now and then in the applications. In addition to this, old features are developed according to the feedback given by the users. This means that we need to update our user manual regularly.

![user manual](/img/user-manual/user_manual.jpg)

## The Old Way

We have maintained our user manual as a few enormous pages in Confluence. Confluence has offered a simple way to allow multiple editors, easy formatting and attaching images. When the software is delivered, the manual should be shipped with the new version. In our project, this has meant converting the Confluence pages to an HTML format, which then could be saved in a dedicated web server location for the users to find via internet.

### Too much monkey business

Importing turned out to be a lot of work despite being a basic functionality of Confluence. The manual work included editing the generated HTML files, such as, removing unnecessary content from the header and footer, removing the list of attachments and so on. Doing it once is not a big deal, but when you do it in every couple of weeks, it feels quite boring. We tried to find a way to customize the look-and-feel of the HTML import but there were not enough tools to handle it. Confluence offers extensive support customizing the output when converting to PDF but not when converting to HTML. Of course, some of the needs could have been handled with custom CSS, but it seemed not to be a long-lasting solution.

### Outside the Natural Flow

Our code is developed in feature branches, each branch corresponding to a Jira task defining the feature. A feature branch is merged to the development branch only after it is known for sure that the feature should and - even more important - is allowed to be included in the next release. This means that the user manual can not be updated when the feature is developed, which otherwise is the natural moment to document the feature you have been working on. However, as you can guess, the updating of instructions was often forgotten when the feature was finally merged to the development.

### Bad Traceability

There was also no easy way to check whether someone had updated the user manual or not. Confluence provides version history but it does not map to the version history in the codebase. Being sure of whether a feature was documented or not was work for a detective. Text search proved to be the most powerful tool.

## Go with the flow

Our dream-come-true solution would have one that integrates the code and the user manual more tightly to each other. Maybe the documentation could be maintained like code, even in the same repository, in the same commits. That way a feature branch could contain both the updates to the codebase and to the user manual. Thus, the feature developed can similarly be documented to the user manual, and we can have different versions of the user manual at the same time. Using descriptive git commit messages and including the Jira ticket ids, the updates to the user manual can be traced as accurately as the code changes. 

Updating the user manual as we develop provides the updated instructions also for the fellow programmer testing our feature. How this feature should work? Are the instructions updated a) at all b) in adequate level? 

When the feature branch is finally merged to the develop, the different versions of the user manual are merged too. If there are conflicts, they can be resolved like any other conflicts in the codebase.

In addition to this, it would be nice if generating the final HTML pages would be more fluent and more automated than in Confluence.

![dream](/img/user-manual/dream.jpg)

## The Dream Come True

We asked our developer community for help and got a hint. [AsciiDoctor](https://asciidoctor.org/) might be our dream come true. AsciiDoctor reads and parses text written in a special AsciiDoc syntax, which can then be converted, for example, to HTML. This really sounded fine. The next step was to find out how to implement this in practice. The Confluence pages should somehow be converted to the AsciiDoc syntax, figure out the project structure, and automate the import process with maven.

### To AsciiDoc

At first, the Confluence pages were imported to HTML. After that, [HTMLToAsciiDoc](https://github.com/asciidocfx/HtmlToAsciidoc) converter was used to convert the HTML files to asciidoc files. The generated asciidoc files were not perfect, but at least they were in asciidoc format and the picture names were linked correctly. Furthermore, the asciidoc files needed to be groomed thoroughly by hand. Attachment lists, table of contents, meta information, and unnecessary formatting were removed. There were still plenty of issues that needed special attention: every inline icon link needed to be fixed, header notations corrected, bullet lists fixed, and internal links checked. Finally, the asciidoc files were imported to HTML and the new HTML pages were compared to the old HTML pages. This was done side by side with two browser windows. Was all the information there? Were the images, links and formatting correct? 

The laborious conversion from Confluence pages to asciidoc, and then to HTML, was really worth it. The asciidoc files were clean and simple, easy to read, easy to edit. In addition to this, the default CSS in AsciiDoctor utilized in the brand new user manual made our old user manual feel ancient.

![great sucess](/img/user-manual/excellent.jpg)

### Location

The documentation is located in the same repository as the software code in a dedicated directory. The user manual is distributed in subdirectiories reflecting the applications. The images are saved in image-subdirectories beneath. Thus, the changes in the user manual can be pushed to the repository in the same commits as the changes in software code providing better traceability to the user manual updates.

### Editing AsciiDoc

There is a [AsciiDoc plugin](https://plugins.jetbrains.com/plugin/7391-asciidoc) available to IntelliJ IDEA which is used in our project. The AsciiDoc plugin provides syntax highlighting and HTML preview as you edit the asciidoc-file.  

### Converting to HTML

[AsciiDoctor maven plugin](https://github.com/asciidoctor/asciidoctor-maven-plugin) provides a convenient way to convert the asciidoc documentation to HTML using maven. The plugin requires configuring the source and destination files for the documentation in a pom.xml. After that, the full user documentation in asciidoc can be converted to HTML with a single _mvn_ command. 

### Possibilities

Having the user manual as "code" offers further possibilities to automate or control the documentation process. We have already a script which checks that all image links refer to an existing image. And vice versa, we also have a script which removed all such images that are not referred by any link. This way the repository does not get overwhelmed with outdated images. Also, the converting and delivering the final HTML files to customer could be automated as some Jenkins build.

## Retrospective

The conversion process took some time, but we think it definitely was worth it. We had greenlight also from the customer to optimize and rationalize our documentation process. After all, the customer was pleased with the results. The new user manual is looks neat, and in addtion to this, the simplified delivery process relieves us to do something more sensible.
