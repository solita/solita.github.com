---
layout: post
title: Solita Developer Survey 2020 - what technologies do we use and like?
author: juholei
excerpt: >
  We conducted a developer survey to find out what technologies we use in the year 2020 and what may lie in the future.
tags:
 - Software Development

---

The Developer survey has become a tradition here at Solita. Every two years, we survey our developer-minded folks regarding technologies and practices we use in our every-day work. The first survey was conducted in 2016 and you can find those results in [our previous blog post](https://dev.solita.fi/java/2016/05/13/Developers-love-spaces.html). The results for the following 2018 survey can be found [here (blog post in Finnish)](https://www.solita.fi/blogit/development-teknologiakartoitus/). This year we once again conducted our survey, with a total of 27 questions. These 27 questions should give us deeper insight into what we use, what we enjoy and what could remain relevant into the foreseeable future. Comparing these results to the previous ones can also give us some information on trends, such as what new technologies we are adopting and what we are moving away from.

A total of 177 of our developers took the survey. The majority of the people who answered the survey considered themselves full-stack developers. Other common roles were backend developers, frontend developers, software architects, data engineers, integration specialists and mobile developers.

## Languages we use

[![All languages](/img/developer-survey-2020/all_languages.png)](/img/developer-survey-2020/all_languages.png)

The first question in the survey regarding programming languages asked to list all the languages you have worked with in the previous year. [**JavaScript**](https://en.wikipedia.org/wiki/JavaScript) and [**SQL**](https://en.wikipedia.org/wiki/SQL) were the dominant ones: SQL is present in some form in most projects we do and JavaScript is ubiquitous in frontend and hard to miss even if you primarily use different languages for frontend. Next up were [**Java**](https://en.wikipedia.org/wiki/Java_%28programming_language%29) and [**Python**](https://www.python.org/).

Apart from languages that are used for the actual systems, scripting languages like [**Sh/Bash**](https://www.gnu.org/software/bash/) (fourth most used overall), [**PowerShell**](https://docs.microsoft.com/fi-fi/powershell/) and [**Groovy**](http://www.groovy-lang.org/) were widely used.

The following questions were about main backend and frontend languages. These questions were added this year to get better information on how the languages are used. As such, these results can't be compared directly to previous years. The following usage comparisons are based on the previous question about all languages used.

[![Backend languages](/img/developer-survey-2020/backend_languages.png)](/img/developer-survey-2020/backend_languages.png)

Java proved to be the most popular language for backend development. Around 45% reported Java being one of the primary backend languages in ther projects. Rest of the top 3 are then [**Clojure**](https://clojure.org/) with about 19% usage and [**Kotlin**](https://kotlinlang.org/) with 18%. Compared to results from 2018, percentage of Kotlin users rose from 15% to 24%. Java and Clojure usage were both a little bit down when comparing 2020 to 2018, which could be explained by Kotlin. Neither seem to be going away though, as shown by being top 1 and 2 used languages for backend and both are well liked (more on that later).

As backend programming languages, we can safely assume that JavaScript, [**TypeScript**](https://www.typescriptlang.org/) and [**ClojureScript**](https://clojurescript.org/) are run atop [**Node.js**](https://nodejs.org/en/). TypeScript was the most used language with Node.js, with only a slight margin over JavaScript.

[![Frontend languages](/img/developer-survey-2020/frontend_languages.png)](/img/developer-survey-2020/frontend_languages.png)

For frontend languages, the clear winner was JavaScript with 68% usage. The other languages that were widely used are Typescript (37%) and ClojureScript (19%). ClojureScript is an obvious choice for projects that are powered by Clojure in the backend, thus they often go hand in hand. [**CoffeeScript**](https://coffeescript.org/) had a handful of users - it seems that the number has been stable compared to 2018 figures (4% overall usage in 2020 compared to 5% in 2018). Most likely it's not used for any new projects but it is still in use in some long-time projects. New to the list was [**PureScript**](https://www.purescript.org/), with a handful of developers here.

## Languages we like
[![Liked languages](/img/developer-survey-2020/liked_languages.png)](/img/developer-survey-2020/liked_languages.png)

For the next question, we wanted to get personal: what language do you like the most? The most used backend language was also the most liked one, as 17% of respondents said that Java was their favorite language. Clojure came second with 15%. This is an impressive achievement considering that even though Clojure is used quite much, in terms of raw numbers Java developers outnumber Clojure developers by a mile. Clojure developers then really know what they like. Kotlin was the third most liked language. The top-3 most liked languages mirrored the top-3 most used backend languages.

Compared to results from 2018, JavaScript fell from number #2 spot to number #4. This could be explained by TypeScript, which gained almost as many percentages now as JavaScript lost. All in all, most top languages were in decline compared to the previous survey. The exception to this rule was Kotlin, which received much more love this year compared to 2018. This time there also seemed to be a lot more niche languages getting a few votes than before, which also explains why the top languages were in decline.

## Languages we would like to use
[![Languages we would like to use](/img/developer-survey-2020/would_like_to_use_languages.png)](/img/developer-survey-2020/would_like_to_use_languages.png)

The answers to this question could tell us several things. First, they tell us that for already widely used languages, there is still interest in keeping them around. Second,they identify growing interest in some languages, so their usage  has the potential to grow in the future. Lastly, for languages that are not yet widely used, they tell us what programming languages we could potentially be using in the future.

Kotlin was the most wanted language here, with 29% of the respondents saying they would like to use Kotlin in the future. People currently using Kotlin want to continue using it, spiking interest on others. As such, Kotlin seems like a good choice for future projects.

Clojure came second, with 22% wanting to use it in the future. TypeScript came third with 18%. With TypeScript usage having increased a lot in two years, the interest in it is still growing.

For languages not currently in use, [**Rust**](https://www.rust-lang.org/) was a clear winner, with 8% of respondents wanting to use it. With appropriate projects, we could very well have Rust in use by the next survey. [**Go**](https://golang.org/) was at similar numbers with Rust: the difference between the languages is that Go is already used here and there.

## Frontend libraries and frameworks
[![Frontend frameworks](/img/developer-survey-2020/frontend_frameworks_and_libraries.png)](/img/developer-survey-2020/frontend_frameworks_and_libraries.png)

[**React**](https://reactjs.org/) rules the frontend at the moment. 66% of respondents who answered to the question about frontend libraries or frameworks in use reported having used React in the last year. All the competition ([**Angular.JS**](https://angularjs.org/), [**Angular**](https://angular.io/), [**Aurelia**](http://aurelia.io/), [**Vue.JS**](https://vuejs.org/)) combined just barely reached React's numbers. Over half of the React users also used [**Redux**](https://redux.js.org/) with it and a half also used [**React Router**](https://reactrouter.com/). ClojureScript developers rely on [**Reagent**](https://reagent-project.github.io/) as their React library and then most of them also use [**re-frame**](https://github.com/Day8/re-frame) for state-management.

For CSS frameworks or React components, about a fifth of the respondents reported using [Bootstrap](https://getbootstrap.com/) or [Material-UI](https://material-ui.com/).

## Backend libraries, frameworks and tools

The sheer amount of potential answers for backend libraries frameworks and tools used was overwhelming. Nonetheless, the most used frameworks and libraries were:

1. [Spring Boot](https://spring.io/projects/spring-boot)
2. [Spring Framework](https://spring.io/projects/spring-framework)
3. [Log4J](https://logging.apache.org/log4j/)

Unquestionably, the most frequently used tool was [**Docker**](https://www.docker.com/), which in the context of this question means that it is used at least for setting up one's development environment. Integration frameworks in use were [**Camel**](https://camel.apache.org/), [**Mule ESB**](https://www.mulesoft.com/platform/soa/mule-esb-open-source-esb) and [**Dell Boomi**](https://boomi.com/).

Other common answers were Node.js, [**Hibernate**](https://hibernate.org/orm/), [**.NET Core**](https://dotnet.microsoft.com/), [**ASP.NET**](https://dotnet.microsoft.com/apps/aspnet), and parts of Clojure web stack such as [**Compojure**](https://github.com/weavejester/compojure), [**Reitit**](https://github.com/metosin/reitit) and [**Ring**](https://github.com/ring-clojure/ring).

## Platforms and deployment targets

Where do we deploy our software? 50% reported that their software runs on **Linux**. That Linux can of course then be running in traditional servers or on some kind of cloud service. The most used cloud platform was **AWS**, followed by **Azure** which had a bit over half the users as AWS. 23% of respondents reported also using a serverless computing platform of their cloud service provider. All the cloud services had their usage increase compared to 2018 survey.

When asked what platforms we would like to use in the future, the top 3 consisted of the three big cloud services. The most wanted was AWS, followed by Azure and then **Google Cloud Platform**, a perfect reflection of the current usage.

## IDEs

[![Editors](/img/developer-survey-2020/editors.png)](/img/developer-survey-2020/editors.png)

A new question this year was regarding which IDEs or editors we use. Most people use several, perhaps based on what languages they are working with currently. Of course then there are also those who only use one and for example Emacs people wouldn't probably want to leave it for any task they need to do.

Most popular one was [**IntelliJ Idea**](https://www.jetbrains.com/idea/) and other IDEs based on it. Idea is definitely very popular for Java work. [**Cursive**](https://cursive-ide.com/) for Clojure and [**Android Studio**](https://developer.android.com/studio) for Android app development were much used too. [**Visual Studio Code**](https://code.visualstudio.com/) has gathered a huge following in a relatively short time. It's no surprise seeing our developers use it a lot too, considering that [StackOverflow survey in 2019 ](https://insights.stackoverflow.com/survey/2019#development-environments-and-tools) had VS Code as the most popular editor in 2019.

[The eternal war](https://en.wikipedia.org/wiki/Editor_war) between [**Vim**](https://www.vim.org/) and [**Emacs**](https://www.gnu.org/savannah-checkouts/gnu/emacs/emacs.html) users ended this time in favor of Vim, as Vim was used by 9% and Emacs was used by 7%.

## Operating Systems

[![Operating systems](/img/developer-survey-2020/operating_systems.png)](/img/developer-survey-2020/operating_systems.png)

Over half of the respondents reported using **macOS** as their primary operating system. About a third reported using **Windows** and 11% used **Linux**. A few people reported using multiple operating systems and mostly working in virtual machines. Virtual machine usage for different use cases is probably more common than that, as this question was only about the primary operating system in use.

## Trends

Usage of cloud platforms is on the rise and that has an impact on lots of things, like solutions used for infrastructure-as-code or CI/CD. For example, [**Jenkins**](https://www.jenkins.io/) was still the most used CI/CD solution, but its usage had dropped sharply. The usage of solutions provided by the cloud platforms, such as **Code** tools in AWS were up. In infrastructure-as-code tools [**Ansible**](https://www.ansible.com/) was still the most used, but its usage had dropped significantly and [**AWS CDK**](https://aws.amazon.com/cdk/), [**Terraform**](https://www.terraform.io/) etc. had a lot more usage now than two years ago.

TypeScript usage has increased significantly in two years. When asking for generally used programming languages, TypeScript was reported by 35% of the respondents. In 2018 it was only used by 19%. This change also meant that JavaScript, even though still the most widely used language in general, dropped from 84% to 69% of usage.

## Conclusion

What does our technology usage then tell about us as a company and a community of developers? We are passionate to learn and tinker with shiny new toys. There's a time and place for that, but for unproven and bleeding edge technologies that place is often not in actual projects but in other contexts. To be a professional means to use things that get the job done the best possible way, not to use all the shiny things. This can be seen in how many hyped-up technologies of the past years are nowhere to be seen here. Elm might have been cool a few years ago, but what would be the situation in five years on, when the system we built is still in use and developed further?

On the other hand, when something has proven itself, we are quick to embrace it. This happened all those years ago with Clojure and it has long since been a household technology for us instead of a niche language. The same kind of thing is now happening with TypeScript and Kotlin: their usage is rising as they have proven their worth and at some point they could become the default choice for their use cases. Similarly for example React has become _de facto_ front end library: we can count on it doing its job well for the foreseeable future. In five years time, there may have been a handful of newer and shinier things that have come and gone. Maybe something else has become the best option for new projects. But those things we chose to use are probably still there and get the job done well.

*Visualizations by Heini Kekki*