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

