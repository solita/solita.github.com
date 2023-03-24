---
layout: post
title: Do's and Don'ts of Dev Academy Pre-assignments - Revisited
author: aija
excerpt: >
  Insights from the spring 2023 Solita Dev Academy pre-assignment reviews.
tags:
- Dev Academy
- Pre-assignment
- Recruitment
---

## What is this blog about?
[Solita Dev Academy](https://www.solita.fi/en/academy/) is an intensive onboarding to Solita and at the same time a stepping stone to getting started with one’s career as a software developer. This year Solita is organising three Dev Academies starting in March, August and November, respectively. We recently finished the recruitment for the spring 2023 academy, which started in March and [the application period for the next Dev Academy is already open](https://www.solita.fi/positions/dev-academy-to-boost-your-software-developer-career-5202331003/).

As part of the Dev Academy application process, we ask the applicants to complete a pre-assignment project, which is a full-stack web application on a given topic using data provided by us ([currently we use this assignment](https://github.com/solita/dev-academy-2022-fall-exercise)). The purpose of the pre-assignment is to give applicants the opportunity to showcase their software development skills in practice as the Dev Academy is intended for people in the early stages of their careers who might not yet have any work experience in the field.

This time we received double the amount of applications than in the previous rounds, (over 300), and the number reviewed pre-assignment almost doubled to about 100 assignments. Applicants often ask us for feedback for their pre-assignments but due to the number of applications, it is just not possible for us to give individual feedback. This blog post is intended as general feedback for the applicants of the spring 2023 Dev Academy and as a guide for any future applicants applying to the Dev Academy. It is a retelling of a similar [blog post written in 2021](https://dev.solita.fi/2021/11/04/how-to-pre-assignments.html). Everything said in the previous blog post still applies, but we still see some of the same issues with the pre-assignments so we wanted to further highlight the importance of these things.

![Solitans sitting together at Helsinki office](/img/pre-assignments-2/Solitans-at-Helsinki-office.jpg)

## Always include local build instructions

In order to review the pre-assignment we need to run your project on our computers. Even though you have deployed your application to the internet, which is a big plus and facilitates the reviewing process, we still want to try it out locally as well. Therefore, your README must contain clear step-by-step instructions on how to set up and run the project locally. Don’t forget to mention all the tools and software (including their versions) that need to be installed for the build to work!

One important yet often overlooked aspect of the build instructions is the instructions for the local database setup. Too often the instructions are just something along the lines: ‘Set up a database and put the data in it’. However, the reviewer might not be familiar with the database you are using. So, we appreciate it if you can make the review process as smooth as possible with comprehensive documentation. Good documentation is also crucial in professional software development projects, where different people in the project might use different operating systems and tools for development, and where new people are joining the project in different stages of it. Your instructions should explain the database initialisation process step by step, including how to insert the initial data into the database. Pro tip: If the data files are too big to put into GitHub, you should, at least, include links to the data in your README, or you could also split the files into smaller chunks that can be uploaded to GitHub.

If you are looking for an extra challenge, you can dockerize your application or parts of it. This will make the local setup process so much smoother! Good resources to get started with docker are for example the following materials: [Aalto Fitech Web Software Development course](https://fitech101.aalto.fi/web-software-development/9-working-with-containers/), [DevOps with Docker MOOC](https://devopswithdocker.com). It's a good idea to also create some custom scripts so that your application can be set up and run with just one command instead of having to run several install and start commands separately.

Remember to make sure that the instructions work! You can for example ask a friend to test if they can get your project up and running following only the instructions. If you don’t want to bother your friends, you can also do it yourself: set up the project from scratch following only your instructions. Can you do it without having to look for additional guidance from the internet?

![A heap of Jigsaw puzzle pieces](/img/pre-assignments-2/hans-peter-gauster-252751-solita.jpg)

## We want more tests!
Writing tests is an essential skill for a software developer and something that we have valued highly in the pre-assignment reviews and interviews. We are still not seeing as many tests in the pre-assignments as we would like to. We understand that writing tests can seem intimidating if you have never written any tests, and knowing how to write good and useful tests is even more so. We encourage you to see the pre-assignment as a chance to practise writing tests. Having at least a few good tests will make your pre-assignment stand out more than having all the suggested extra features implemented.

To get started with software testing you can check the [testing primer for Dev Academy applicants blog post](https://dev.solita.fi/2022/11/01/testing-primer-dev-academy.html). You can also check the [Let’s Test -series on YouTube](https://www.youtube.com/watch?v=ByWnpZo4u1M&list=PL0JMxkVljrHps5inT2YjG1uqKCwZBNzQn). Moreover, the [Fullstack Open course](https://fullstackopen.com/en/) has some good material for testing React and Express applications. If you are using some other technologies, you can find a plethora of material online.

## Lots of features is not a silver bullet 
While it is nice that many pre-assignments have several nice-to-have features implemented, the additional features do not necessarily make the project stand out if it is lacking in other aspects. Instead, we would like you to prioritise the other aspects of the project over implementing lots of features. You could focus on, for example (not in any specific order):
- good quality code
    - Does your project have a clear file structure? Can your code be understood without comments or is it spaghetti? Do you have unused imports or variables in your code? Remember to use a linter and code formatter!
- different types of tests
    - See above about testing. You can test, for example, the database, backend logic, API routes and UI components. You can also test the whole application with E2E tests.
    - If you have tests in your application, remember to include instructions on how to run the tests in your README.
- error handling
    - What happens if you navigate to a non-existing URL (e.g. my_app/stations/\<id-that-does-not-exist>), or if you send invalid data to the backend?
- input validation
    - Do you have forms or search fields, how do they handle invalid input (e.g. a string where there should be a number)? Do they give the user feedback about what kind of input is expected?
- good UI
    - Is it accessible? Is it responsive? Is it intuitive to use? Is it nice looking?
- good documentation
    - See above about documentation. In addition to that you could tell us about what features you implemented, what challenges you faced while doing the assignment and how you might improve it in the future.

![A game board with black and red pieces](/img/pre-assignments-2/Solita-Tampere-office-game.jpg)

We recognise that implementing features is easy compared to the other stuff mentioned above. Maybe you don’t know that much about error handling or are not familiar with good coding practices. Again, take this as a learning opportunity and your chance to get started with those things. You will need them as a software developer! 

Of course, you are welcome to implement as many features as you like, just remember that lots of features are not required for a good result and an interview. We assume that you have a limited time to spend on the pre-assignment and if you want to maximise the return of time invested in this project, lots of features is not the way to go. It is better to have a couple of features completed and working well than many features that are so-so. Moreover, we are more likely to ask you about testing or code quality in the interview than how to implement a sorting feature.

## To conclude: What to expect in the interview
Did you make it to the interview? Congratulations, it’s already a great achievement and you should be proud of yourself! Usually, around 30 applicants are interviewed. To conclude we want to share with you some tips about the interview.

The interview for Dev Academy will have two parts: a general discussion about, among others, your experience and your expectations about working at Solita, and a technical part where you will present us your pre-assignment, after which we will discuss, among other things, your implementation, what you liked about doing it and what kind of challenges you faced while doing it. So, be prepared to demo your application to us. We will also talk about your technical skills in general.

![Solitans chilling out at Helsinki office terrace](/img/pre-assignments-2/Solitans-at-Helsinki-office-terrace.jpg)

At Solita, our core values are [caring, easy-going, courage and passion](https://www.solita.fi/en/blogs/how-our-values-impact-on-the-employee-experience-at-solita/). These values are really important to us and what we are looking for in candidates is that they fit with our culture and values and also what they might add to our culture. In the interview, we would like to hear why you want to work at Solita. We understand that as a junior developer, the most important thing is to get that first job in the field. However, our tip for the interview is that you take a look at Solita’s web pages, read about our work, values and culture, and think about how that resonates with you and why you would like to work specifically at Solita.

Obviously, we also look at your technical competence and potential, but we would rather hire someone who we really want to work with and who we see having the potential to grow into a software professional than someone who already has a stellar CV but who does not share our values.
