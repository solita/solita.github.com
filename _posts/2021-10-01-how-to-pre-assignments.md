---
layout: post
title: TBA
author: noora & aija
excerpt: >
tags:
---

# Working title: Do's and Dont's of Dev Academy Pre-assignments

## README

If your project is published in github, the first thing the reviewer will see of your pre-assignment is README. With good README the reviewer gets a clear picture of your project even without looking at the code or running it. 

Good README includes following things:

- Prequisites. Are there some things that need to be installed on reviewers computer before they can compile and run the project? Is the project working only on windows or only on linux? List things that need to be done before trying to run the project. If versions are important, remember to include those as well.
- Configurations. Do you have to config for example database connections locally? Provide clear instructions what needs to be changed and where.
- How to run the project? Do you have to install some packages or compile the code? If you have separate services for example for backend and frontend, remember to write instructions for all needed services.
- Tests. If your project has tests include instructions how to run them. 
- Description of the project. What is the purpose of the project and what features it has? 
- Technology choices. List chosen technologies. It's also nice to know, why you ended up with those technologies.
- TODO. If there are some things missing or not working, you can list them to README. That way the reviewer knows that you thought of them and also doesn't waste time looking for them or trying to figure out if something works or not. 

## Make sure that code is compiling and tests are passing

Make sure that your instructions on how to run the project are working. If you have tests, they should all be passing or at least you should have some explanation for failing tests. 

## Clear project structure

Try to keep the project structure clear and filenames descriptive. It's easier to review smaller components that do only one thing that is described on the filename than to review files that are hundreds or even thousands of lines long. 

## Clean up unused code

In many cases there is a deadline for pre-assignment and that might lead to that you won't finish everything you have started. You might have some functions and components that you don't use at all, that should be cleaned up before submitting. Unused code distracts the reviewer and the general feeling of the codebase could seem unclear. 

If you have used some boilerplate as base for the project, remember to also clean up unused boilerplate. For example create-react-app adds a default e2e-test as a template, that really doesn't test anything. If you don't have any e2e-tests remove all boilerplate related to e2e-tests and so on. 

It's of course okay to leave some unused code to your project, but before submitting go through your code. Consider adding a comment if you end up leaving some unused code to your project to help the reviewer. 

## Focus on getting features complete

Pre-assignment can consist of many requirements and features. Some of them can be required and some optional. For this fall Solita Academy pre-assignment we didn't have any must do's and the applicant's could choose what they wanted to focus on.

If you think that you can't finish everything, it's better to do some things thoroughly and leave the others undone than to do everything half-way. Choose your focus points and what you want showcase, then start with those and do other things afterwards. It is easier to review complete things than to try to figure if something is almost done or almost not done.

## Your Git History

Knowing how to use version control (nowadays analogous to git) is one of the most essential skills of a developer. To make your project look more professional make sure your git history is neat and informative. 

Your git history is also something that we will look nto in when we are checking your hobby projects or pre-assignment as part of a recruiting process. We want to see how you've created your project incrementally. From your git history we can get a glimpse of your development process: where you started, in which order you did things, which parts were refactored during the process, etc.

// vai

Your git history is the collection of your commits. So, you should always have several. In the context of an recruitment pre-assignment project, its purpose is, in addition of being helpful to you, to give some insight on how you created your project. Like what you did first and how you incrementally added features. 

During the Dev Academy recruitment process we saw many git histories that had basically two commits. One containing all the application code and the second updating readme. Please try to have more commits

How to go about creating an informative git history? 

First, think about the content of your commit. A good rule of thumb is to have one commit per one major change in your code. A major change could be:
* initialising a React project with create-react-app
* creating a new component/class and connecting it with the rest of your code
* adding a new library and doing something with it
* creating a new api endpoint and creating database queries and application code needed to fetch and handle the data needed by that endpoint
* adding tests

Remeber that you don't have to stage and commit all the chages in one commit but you can stage and commit only selected files or even parts of files. So, if you did several major changes and forgot to commit in between, or maybe you just worked on several things concurrently. We will not go into detail of any specific git commands here but there are GUI tools (e.g. VS Code and Intelli J Idea include such) that allow you to select which parts of file you want to stage and if you are using git from command line `git add --patch` is the command you want to explore.  However, when committing only parts of your files, always try to keep your application somewhat functional, for example don't commit code where you use an external library before committing the installation of that library or don't commit a file where you import a component before you have committed that component.

A good commit message describes your changes your commit makes to the repository. Try to be concise but yet descriptive, not easy, we know :) Try to think what is the one main thing you did in this commit, if there are several, then maybe that is an indication that you should have several commits instead of one.

Examples of good commit messages:

init project with create-react-app
added unit tests for vaccination info component
configured proxy for front-end
installed cypress
added logger middleware
fixed footer margin
updated readme with list of scripts

When looking beyond individual commit message, it also matters how your commit messages look together. For instance, one "update readme" is an ok message but if you have several "update readme" commit messages in a row, it does't look so good.

It often happens that despite your best efforts your git history starts to look cluttered and you have several commits like 'bug fixes', 'fix typos' 'update readmes' and 'some more of the same stuff as the previous commit'.

It is possible to amend and clean your git history afterwards. This is already somewhat advandec stuff and again we won't go into details how these git commands work but here are some pointers on which commands you should learn:

* To add stuff to your previous commit and change the commit message: `git commit --amend`.
* To add stuff to your previous commit without changing the commit message: `git commit --amend --no-edit`.
* Undo some commits (e.g. to be able commit those things again in a different way): `git reset <..>`.
* Reorganise, squash and edit several commits at once: `git rebase -i <..>`.

NB! If you have already pushed your local changes to the remote, you have to push with force after using any of these commands. Always be careful when using `push --force` and maybe use `push --force-with-lease` instead to be on the safe side.

An excellent material for practicing git branches: https://learngitbranching.js.org
https://gitexplorer.com


# Code formatting

Always try to make your code look good and clean. For instance make sure that you always use the same indentation across your project and remove any unused variables and functions. Use linters and code formatters to automatise this process. When installed and configured these tools can visually highlight problems in your code and you can enable format on save feature, which can for instance add missing semicolons and remove extra white space.

Good tools are Eslint and Prettier for JavaScript, Pylint for Python and Detekt for Kotlin. These tools often include some default formatting configuration which you can customise to your needs. For some languages there are also other often more opiniated configurations you can use such as Airbnb config for Eslint.

When using linters make sure to fix all problems before submitting your project. For instance for React projects it doesn't look good if there are a bunch of linter errors in the browser console.

# Code quality & comments

A good rule of thumb is to never use comments unless you really really have to.

Ideally your code should be easily understandable without any comments.
* use descriptive names for your variables and functions, for instance instead of adding a comment that tells what your function does, try to name your functions in such a way that its purpose can be understood from its name
* don't mix English and Finnish (or any other language), unless you have an excellent reason

When to use comments:
* it is ok to add TODO comments when there are some things in your code that you want to fix later
* You know that some part of your code is not working correctly but you don't want to delete it altogether, you can add a comment explaining this. This is a good practice in any kind of recruitment pre-assignments where it may be almost as important that you have attempted to implement something and have tried to debug why it is not working as an actual working solution.
