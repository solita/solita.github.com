---
layout: post
title: Solita Developer Survey 2020 - what technologies do we use and like?
author: juholei
excerpt: >
  We conducted a developer survey to find out what technologies we use in the year 2020 and what may lie in the future
tags:
 - Software Development

---

Developer survey has become a tradition here at Solita. Every two years we survey our developer-minded people regarding technologies and practices we use in our every-day work. The first survey was conducted in 2016 and you can find a blog post about those results in [our previous blog post](https://dev.solita.fi/java/2016/05/13/Developers-love-spaces.html) and then in 2018 [(blog post in Finnish)](https://www.solita.fi/blogit/development-teknologiakartoitus/). This year we once again took a look at the survey and came up with a total of 27 questions that would give us interesting insight into what we use, what we like and what could be big in the future. Comparing these results to the previous ones can also give us some information on trends - what technologies are increasing in use and what are in decline?

## Languages we use

![All languages](/img/developer-survey-2020/all_languages.png)

The first question in the survey regarding programming languages asked to list all the languages you have worked with in the previous year. JavaScript and SQL were the dominant ones: SQL is present in some form in most projects we do and JavaScript is ubiquitous in frontend and hard to miss even if you primarily use different languages for frontend. Following them were Java and Python.

Apart from languages that are used for the actual system, scripting languages like Sh/Bash (third most used overall), PowerShell and Groovy were widely used.

The following questions about main backend and frontend languages were new this year and were added to get better information on how the languages are used. As such, these can't be compared as such to previous years. Usage comparisons are then based on the question about all languages used.

![Backend languages](/img/developer-survey-2020/backend_languages.png)

Moving on to more focused questions, Java proved to be the most used language for backend development. 45% reported Java being one of the primary backend languages in ther projects. Rounding out top 3, are then Clojure with about 19% usage and Kotlin with 18%. Compared to results from 2018, percentage of Kotlin users rose from 15% to 24% (comparison based on the question of all languages used). Java and Clojure usage were both a little bit down when comparing 2020 to 2018, which could be explained by the increased usage of Kotlin. Neither seem to be going away though, as shown by being top 1 and 2 used languages for backend and both are well liked (more on that later).

As this question was about backend languages, we can assume that JavaScript, TypeScript and ClojureScript here mean that they are run on NodeJS. TypeScript was then the most used language with only a slight margin over JavaScript (11% vs. 10%)

![Frontend languages](/img/developer-survey-2020/frontend_languages.png)

For frontend languages the clear number one was JavaScript with 68% usage. The other languages that have wide usage are Typescript (37%) and ClojureScript (19%). ClojureScript is an obvious choice for projects that use Clojure in the backend, so it seems those two go hand in hand quite much. CoffeeScript has a handful of users - it seems that the number has been stable compared to 2018 figures (4% overall usage in 2020 compared to 5% in 2018). Most likely it's not used for any new projects but it is still in use in some long-time project. PureScript also had a handful users here, which is new compared to 2018.

## Languages we like
![Liked languages](/img/developer-survey-2020/liked_languages.png)

Next, we asked for opinions: what language do you like the most? The most used backend language was also the most liked one, as 17% of respondents said that Java was their favorite language. Clojure came second with 15%, which is impressive considering that even though it is used quite much, in terms of raw numbers Java developers outnumber Clojure developers by a mile. Clojure developers then really know what they want. Kotlin was the third most liked language, meaning that the top 3 of liked languages mirrors the top 3 of backend languages by usage.

Compared to results from 2018, JavaScript fell down from number #2 spot to number #4. This could be explained by TypeScript, which gained almost as many percents now than JavaScript lost. All in all, most top languages were in decline compared to the previous survey, except Kotlin, which received much more love this year compared to 2018. This time there also seemed to be a lot more niche languages getting a few votes than before, which also explains why the top languages were a bit in decline.

## Languages we would like to use
![Languages we would like to use](/img/developer-survey-2020/would_like_to_use_languages.png)

The answers to this question tells us several things. First, it tells us that for widely already used languages there is still interest in continuing to use them. Second, the answers can tell us that there's even more interest in some languages, so their usage could still grow in the future. Third, for languages that are not yet widely used, the answers tell us what languages we could be potentially be using in the future.

Kotlin was the most wanted language here, with 29% of the respondents saying they would like to use Kotlin in the future. As such, people using Kotlin currently seem to want to continue using it and others would like to start using it. As such, Kotlin seems like a good choice for future projects.

Clojure came second, with 22% wanting to work with it in future. TypeScript came third with 18%. With TypeScript usage having increased a lot in two years, the interest is still growing.

For languages not currently in wide use, Rust was a clear winner, with 8% of respondents wanting to use it. With appropriate projects, we could very well see Rust move to the used languages category for the next survey.

## Frontend libraries and frameworks
![Frontend frameworks](/img/developer-survey-2020/frontend_frameworks_and_libraries.png)

React rules the frontend at the moment. 66% who answered to the question about used frontend libraries or frameworks reported having used React in the last year. All the competition (Angular, Aurelia, Vue) combined actually only just barely reached React's numbers. Over half of the React users also used Redux with it and a half also used React Router. ClojureScript developers rely on Reagent as their React library and then most of them also use re-frame for state-management.

For CSS frameworks or React components, about a fifth of the answerers reported using Bootstrap or Material-UI.

## Backend libraries, frameworks and tools

For backend libraries frameworks and tools the amount of things that could be included here made it a hard question to answer. Interpreting the results, the most used frameworks and libraries were:

1. Spring Boot
2. Spring Framework
3. Log4J

The most used tool was Docker, which in the context of this question means that it is used at least for setting up development environments. Integration frameworks in use were Camel, Mule ESB and Dell Boomi.

Other common answers were Node.js, Hibernate, .NET Core, ASP.NET, and parts of Clojure web stack such as Compojure, Reitit and Ring.

## Platforms

Where do we deploy our software? 50% reported that their software runs on Linux. That Linux can of course then be running in traditional servers or in some kind of cloud service. The most used cloud platform was AWS, followed by Azure which had a bit over half the users as AWS. 23% of respondents reported also using a serverless computing platform of their cloud service provider.

When asked what platforms we would like to use in the future, the top 3 consisted of the three big cloud services. The most wanted was AWS, followed by Azure and then Google Cloud Platform. This mirrored the current usage.

## IDEs

![Editors](/img/developer-survey-2020/editors.png)

A new question this year asked what IDEs or editors we use. Most people use several, perhaps based on what languages they are working with currently. Of course then there are also those who only use one (Emacs people wouldn't probably want to leave it for any task they need to do). All the cloud services had their usage increase compared to 2018 survey.

Most popular one was IntelliJ Idea and other IDEs based on it. Idea is definitely very liked for Java work and Cursive for Clojure and Android Studio for Android app development are much used too. Visual Studio Code has gathered a huge following in a relatively short time and it's no surprise being used a lot among our developers too, considering that [StackOverflow survey in 2019 ](https://insights.stackoverflow.com/survey/2019#development-environments-and-tools) had it as the most popular editor.

The eternal war between VIM and Emacs users ended this time in favor of Vim, as Vim was used by 9% and Emacs was used by 7%.

## Operating Systems

![Operating systems](/img/developer-survey-2020/operating_systems.png)

Over half of the respondents reported using macOS as their primary operating system. About a third reported using Windows and a bit over 10% used Linux. A few people reported using multiple operating systems and mostly working in virtual machines. Virtual machine usage for different use cases is probably more common than that, as the question was about the primary operating system in use and not about every operating system people use in some capacity.

## Trends

Usage of cloud platforms is on the rise and that has an impact on lots of things, like solutions used for infrastructure-as-code or CI/CD. For example, Jenkins was still the most used CI/CD solution, but its usage had dropped a quite significantly in percentage and the usage of the solutions provided by the cloud platforms, such as Code* tools in AWS were up. In infrastructure-as-code tools Ansible was still the most used, but its usage had dropped a lot and AWS CDK, Terraform etc. had a lot more usage now than two years ago (TARKISTA!!!).

TypeScript usage has increased significantly in two years. When asking for generally used programming languages, TypeScript was reported by 35% of the respondents, where in 2018 it was only used by 19%. This change also meant that JavaScript, even though still the most widely used language in general, dropped from 84% to 69% of usage.

## Conclusion
