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

The purpose of this blog is to give some general feedback to the Dev Academy applicants and to act as a guide for any future applicants on how to make your project a bit better. The most important thing in your pre-assignment project is, of course, that you have been able to implement (at least some of) the required features. When you have that covered, these tips should help your project to stand out as more professional.

![A person sitting in front of a laptop](/img/pre-assignments/image.png)

## README
If your project is published in Github, the first thing we will see of your pre-assignment is README. With good README we get a clear picture of your project even without looking at the code or running it. 

A good README includes the following things:
- Prerequisites. Should the reviewer install something on their computer before they can compile and run the project? Does the project only work on Windows or Linux? List all steps that need to be done before trying to run the project. If versions are important, remember to mention those as well.
- Configurations. Do you have to configure for example database connections locally? Provide clear instructions on what needs to be changed and where. In case you have an .env file which you, of course, should not add to GitHub, you can send that file to the reviewers by other means.
- How to run the project? Do you have to install some packages or compile the code? If you have separate services for example for backend and frontend, remember to write instructions for all needed services.
- Tests. If your project has tests, include instructions on how to run them.
- Description of the project. What is the purpose of the project and what features it has?
- Technology choices. List chosen technologies. It's also nice to know why you chose those technologies.
- TODO. If some things are missing or not working, you can list them in README.

## Git History
Your git history is also something that we will often look into before digging deeper into your code. From your git history, we can get a glimpse of your development process: where you started, in which order you did things, which parts were refactored during the process, etc. Knowing how to use version control (nowadays analogous to git) is one of the most essential skills of a developer. To make your project look more professional you should pay some attention to how your git history looks. 

During the Dev Academy recruitment process we saw many git histories that had practically two commits. One that contained all the application code and the second that updated readme. Please try to have more commits than that. A good rule of thumb is to have one commit per one major change in your code. A good commit message describes the changes your commit makes to the repository. Try to be concise but yet descriptive, not easy, we know :) Try to think what is the one main thing you did in this commit, if there are several, then maybe that is an indication that you should have several commits instead of one.

Some people like to keep their git history extra neat by amending and squashing their commits. In a recruitment pre-assignment, it is usually enough to just commit frequently enough and in reasonably sized chunks.

Examples of good commits:
![Git history](/img/pre-assignments/git-history.png)

## Make sure that code compiles and tests pass
Make sure that the instructions on how to run the project work. The reviewer checking out your project does not want to fix stuff to make it work. If you have tests, they should all pass or at least you should have some explanation for failing tests. 

## Focus on getting features complete
Pre-assignment can consist of many requirements and features. Some of them can be required and some optional. For this fall’s Solita Dev Academy pre-assignment we didn't have any mus- dos and the applicants could choose what they wanted to focus on.

If you think that you can't finish everything, it's better to do some things thoroughly and leave the others undone than to do everything halfway. Choose your focus points and what you want to showcase, then start with those and do other things afterwards.

## Write good quality code
Good quality code is easy to read and looks nice. For instance, make sure that you always use the same indentation across your project and remove any unused variables and functions. Use linters and code formatters to automate this process, because otherwise, you will miss a lot of stuff. These tools can visually highlight problems in your code and you can enable format when saving, which can for instance add missing semicolons and remove extra white space.

When using linters make sure to fix all problems before submitting your project. It doesn't look good if your application runs with a bunch of linter errors in the console.

Try to make your code easily understandable without using any comments: Logically organise your code both into different files and within a single file. Use descriptive names for your variables and functions, for instance instead of adding a comment that tells what your function does, try to name your functions in such a way that their purpose can be understood from its name.

Also, don't mix English and Finnish (or any other language) in your code. If you want to use some other language than English, then everything but the programming language commands should be in that language.

## Clean up unused code
In many cases, there is a deadline for pre-assignment and you might not have time to finish up everything you have started. You might have some functions and components that you don't use at all, and those should be cleaned up before submitting. Unused code distracts the reviewer and the general feeling of the codebase could seem unclear. If you are using any linter tools, they will often show error messages for things such as unused imports and variables.

If you have used some boilerplate as a base for the project, remember to also clean up unused boilerplate. 

It's of course okay to leave some unused code to your project, but before submitting go through your code. Consider adding a comment if you end up leaving some unused code to your project to tell the reviewer that it was done on purpose.

## To conclude
We hope you found these insights useful. There are, of course, a lot of things that are taken into consideration when reviewing the pre-assignments and applications to the Solita Dev Academy and this is by no means an exhaustive list. These are just some of the general things we would like to see in the pre-assignment projects and these could be applied to any project regardless of the assignment or the technologies used. Even though your application might be very simple and you could not implement all the features, you can still pay attention to your README, git history and overall code quality.

## Some links to check out
[Solita Careers](https://www.solita.fi/en/careers/)
[Solita Academy](https://www.solita.fi/en/academy/)
[SolitaTech Videos playlist on YouTube](https://www.youtube.com/watch?v=bYeJ3xfwjjg&list=PLsaEf6-Yla5oOMz04xXQ-NsVnYqPCcmZH)