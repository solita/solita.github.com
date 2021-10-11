---
layout: post
title: Do's and Dont's of Dev Academy Pre-assignments
author: noora & aija
excerpt: >
  The fall 2021 Solita Dev Academy applicants were required to submit a pre-assignment as part of the recruitment process. We were part of the team reviewing the pre-assignments and wanted to share some insights gained from the experience.
tags:
- academy
- pre-assignment
- recruitment
---

# Do's and Dont's of Dev Academy Pre-assignments

## Introduction
The applicants to fall 2021 Solita Dev Academy were required to submit a [pre-assignment](https://github.com/solita/vaccine-exercise-2021) as part of the recruitment process. We were part of the team reviewing the pre-assignments and wanted to share some insights gained from the experience.

The purpose of this blog is to give some general feedback to the Dev Academy applicants and to act as a guide for any future applicants on how to make your project stand out as more professional. These tips can, of course, be applied to any other pre-assignments as well.

## README
If your project is published in Github, the first thing we will see of your pre-assignment is README. With good README we get a clear picture of your project even without looking at the code or running it. 

A good README includes following things:
- Prerequisites. Should the reviewer install something on their computer before they can compile and run the project? Does the project only work on Windows or on Linux? List clearly all steps that need to be done before trying to run the project. If versions are important, remember to mention those as well.
- Configurations. Do you have to configure for example database connections locally? Provide clear instructions on what needs to be changed and where. In case you have an .env file which you, of course, should not add to GitHub, you can send that file to the reviewers by other means.
- How to run the project? Do you have to install some packages or compile the code? If you have separate services for example for backend and frontend, remember to write instructions for all needed services.
- Tests. If your project has tests, include instructions on how to run them.
- Description of the project. What is the purpose of the project and what features it has?
- Technology choices. List chosen technologies. It's also nice to know why you chose those technologies.
- TODO. If there are some things missing or not working, you can list them in README.

## Git History
Knowing how to use version control (nowadays analogous to git) is one of the most essential skills of a developer. To make your project look more professional make sure your git history is neat and informative. 

Your git history is also something that we will often look into before digging deeper into your code. We want to see how you've created your project incrementally. From your git history we can get a glimpse of your development process: where you started, in which order you did things, which parts were refactored during the process, etc.

During the Dev Academy recruitment process we saw many git histories that had basically two commits. One containing all the application code and the second updating readme. Please try to have more commits than that.

### How to create an informative git history? 
First, think about the content of your commit. A good rule of thumb is to have one commit per one major change in your code. A major change could be:
- initialising a React project with create-react-app
- creating a new component/class and connecting it with the rest of your code
- adding a new library and doing something with it
- creating a new api endpoint and creating database queries and application code needed to fetch and handle the data needed by that endpoint
- adding tests
- 
A good commit message describes your changes your commit makes to the repository. Try to be concise but yet descriptive, not easy, we know :) Try to think what is the one main thing you did in this commit, if there are several, then maybe that is an indication that you should have several commits instead of one.

Examples of good commit messages:
![Git history](/img/pre-assignments/git-history.png)

When looking beyond individual commit messages, it also matters how your commit messages look together. For instance, one "update readme" is an ok message but if you have several "update readme" commit messages in a row, it doesn't look so good.

It often happens that despite your best efforts your git history starts to look cluttered and you have several commits like 'bug fixes', 'fix typos', 'update readmes' and 'some more of the same stuff as the previous commit'. There are ways to clean your git history by e.g. amending or squashing your commits, but that is a rather advanced feature and we will not go into that in more detail in this post.

An excellent material for practicing git commands: https://learngitbranching.js.org https://gitexplorer.com

## Make sure that code compiles and tests pass
Make sure that the instructions on how to run the project actually work. The reviewer checking out your project does not want to fix stuff to make it work. If you have tests, they should all pass or at least you should have some explanation for failing tests. 

## Focus on getting features complete
Pre-assignment can consist of many requirements and features. Some of them can be required and some optional. For this fall’s Solita Dev Academy pre-assignment we didn't have any must dos and the applicant's could choose what they wanted to focus on.

If you think that you can't finish everything, it's better to do some things thoroughly and leave the others undone than to do everything half-way. Choose your focus points and what you want to showcase, then start with those and do other things afterwards.

## Write good quality code
Good quality code is easy to read and looks nice. For instance make sure that you always use the same indentation across your project and remove any unused variables and functions. Use linters and code formatters to automatise this process, because otherwise you will miss a lot of stuff. These tools can visually highlight problems in your code and you can enable format on save, which can for instance add missing semicolons and remove extra white space.

When using linters make sure to fix all problems before submitting your project. It doesn't look good if your application runs with a bunch of linter errors in the console.

Try to make your code easily understandable without using any comments: Organise your code in a logical manner both into different files and within a single file. Use descriptive names for your variables and functions, for instance instead of adding a comment that tells what your function does, try to name your functions in such a way that its purpose can be understood from its name
Also, don't mix English and Finnish (or any other language) in your code. If you want to use some other language than English, then everything but the programming language commands should be in that language.

## Clean up unused code
In many cases there is a deadline for pre-assignment and you might not have time to finish up everything you have started. You might have some functions and components that you don't use at all, and those should be cleaned up before submitting. Unused code distracts the reviewer and the general feeling of the codebase could seem unclear. If you are using any linter tools, they will often show error messages for things such as unused imports and variables.
If you have used some boilerplate as base for the project, remember to also clean up unused boilerplate. 

It's of course okay to leave some unused code to your project, but before submitting go through your code. Consider adding a comment if you end up leaving some unused code to your project to tell the reviewer that it was done on purpose.

## To conclude
We hope you found these insights useful. There are, of course, a lot of things that are taken into consideration when reviewing the pre-assignments and applications to the Solita Dev Academy and this is by no means an exhaustive list. These are some of the general things we would like to see in the pre-assignment projects and these could be applied to any project regardless of the assignment or the technologies used. Even though your application might be very simple and you could not implement all the features, you can still have an excellent readme and git history.