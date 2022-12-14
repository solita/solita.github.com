---
layout: post
title: Solita Developer Survey 2022 - summary of results
author: aleksi.sitomaniemi

excerpt: >
 The biennial Solita Developer Survey was conducted again in 2022. This time we had almost 300 respondents from all six countries where Solita has offices in. This summary of the survey results provides a view to how we do software development at Solita, what are our preferred stacks & languages and what might getting more traction in the next projects. 
tags:
 - Software Development, Developer Survey, DevOps, Testing, OSS, Competence Development

---

The biennial Solita Developer Survey was conducted in 2022 again, now with a participation of almost 300 people. Since the previous survey in 2020, the company has grown significantly (roughly 500 new Solitans since end of 2020 in all the operation domains together). The early 2022 acquisitions of [**Intellishore**](https://intellishore.dk/) and [**Commentor**](https://commentor.dk/) from Denmark brought in a good one hundred people on board, the rest of the sum is new hires. The survey is targeted to all Solitans who are participating in software development work regardless of their domain of expertise and title. 

See the links section at the end of the post for result summaries from the previous survey years.

## Responder facts

This year, we extended the with separate sections for DevOps, testing & monitoring, and security. We also added some new questions to get more insights in the regular survey content about project setup, language preferences and stacks. In total, this year the survey had 52 questions in 8 sections.

Total respondent count was 286 persons (+109 increase from 2020 survey). The geographical distribution covers all Solita office locations in Finland, Sweden, Denmark, Estonia, Germany and Belgium. Roughly 2/3 of the respondents are from Finland.

In the responder facts section, we also asked about team size and co-location. It's worth mentioning that Solita developers very rarely work in solo mode. The most common Solita team size in a project is 2-5 persons, but we also do a lot of projects where teams be up to 10 and more people. Many teams are co-located sharing the same office, some teams work from multiple offices. As a repercussion from the epidemic, about third of the respondents report that they're mostly working remotely from home.

Most of the survey respondents identify themselves as Full-Stack developers, followed by the roles of Backend developer, Software architect, Frontend developer and DevOps specialist. The rest of the lot splits into different more specific domains of data, cloud, integrations, and mobile & low-code development.

## Competence Development + OSS Contributions

In the competence development section we asked how Solita developers update and maintain their skillsets. We also had a set of questions regarding contribution to open source projects.

In the question about learning platforms, one thing was clear: video is king; [**YouTube**](https://www.youtube.com) was the most used platform when learning new stuff. We are also widely making use of the [**O'Reilly Online Learning**](https://www.oreilly.com/online-learning/) catalog which is available for all Solitans. We also have a healthy budget for attending developer conferences and events to hook up with the dev communities and learn. Action on the events front has been a bit low key in the past due to the obvious reasons, but the scene is getting more lively all the time.

35 respondents had been working in a customer project that is either completely or partially open sourced during the past year. In addition to that, about two thirds of the respondents reported that they use varying number of hours in open source projects of their own choice in their free time. 

We also encourage the participation in Open Source projects with an OSS Contribution program available for developers in Finland. 10% of respondents had participated in the OSS contribution program where you can get a small compensation for your outside working hours contributions to projects publicly available in e.g. [**GitHub**](https://github.com) or [**GitLab**](https://about.gitlab.com).

## Developer preferences

The project teams at Solita have a lot of freedom in setting up the development environment and tooling, including the choice of languages, but the feasibility in the customer's context also needs to be considered to get the best results. The following graph illustrates which languages we have liked most working with in the past two years. [**C#**]() has the lead, and [**Clojure**](https://clojure.org/), [**Kotlin**](https://kotlinlang.org/), [**Java**](https://en.wikipedia.org/wiki/Java_%28programming_language%29) & [**TypeScript**](https://www.typescriptlang.org/) come with a solid following each.

[![Liked languages](/img/developer-survey-2022/keyboard.png)](/img/developer-survey-2022/keyboard.png)

The coin has two sides here, and some languages have a significant downvoting as well. Out of the languages we have been using frequently in projects, [**JavaScript**](https://en.wikipedia.org/wiki/JavaScript), **Java** and [**SQL**](https://en.wikipedia.org/wiki/SQL) received the most _dislikes_ in the survey.

In the next illustration, you can see what we indicated as languages that we would like to use in the customer work in the near future. All of these languages are in use in at least one project at Solita, but there is a lot of interest towards e.g. [**Go**](https://golang.org/), [**Rust**](https://www.rust-lang.org/) and [**F#**](https://fsharp.org/) which are not yet widely utilized. 

Reflecting upon the previous survey, in 2020 Kotlin was the number 1 most wanted in this question, with a fraction of a percentage of use in customer projects. In this survey, while it is still on the wantlist, Kotlin has already made it to top 10 most used languages in projects, and it is regularly applied in backend, frontend and other (e.g. scripting) contexts. Likewise, it is likely that in the next survey, **Go** and **Rust** will have a noticeable presence in the project languages response. 

Individual votes were also cast for [**Elixir**](https://elixir-lang.org/), [**Haskell**](https://www.haskell.org/), [**Smalltalk**](https://en.wikipedia.org/wiki/Smalltalk), [**Elm**](https://elm-lang.org/), [**Lisp**](https://en.wikipedia.org/wiki/Lisp_%28programming_language%29) in the wanted section.

[![Top wanted](/img/developer-survey-2022/chalkboard.png)](/img/developer-survey-2022/chalkboard.png)

In the development environments, [**Visual Studio Code**](https://code.visualstudio.com/) has bumped the [**IntelliJ Idea**](https://www.jetbrains.com/idea/) from the top position, and the [**Vim**](https://www.vim.org/)/[**Emacs**](https://www.gnu.org/software/emacs/) derby is still turning for Vim. Note that the illustration shows the percentage of votes per editor in a multiple choice question. A lot of our developers use multiple IDEs in their work with different projects, or within one for different contexts.

[![IDE](/img/developer-survey-2022/screen.png)](/img/developer-survey-2022/screen.png)

For their work computer OS, 52% choose **Windows**, 40% go for **MacOS** and 8% prefer **Linux**. The most popular Linux distribution used in Solita linux workstations is **Ubuntu**. **Arch Linux** and **Debian** also got a handful of votes.

## Development Stacks

Let's have a closer look to what did we do in the past two years then. In the following illustration you can see what were the most used languages in our projects. 

[![Used languages](/img/developer-survey-2022/pen.png)](/img/developer-survey-2022/pen.png)

Despite the rise of nosql solutions, oldschool relational databases are still in the majority, hence SQL in the lead. Among the databases we use most are [**PostgreSQL**](https://www.postgresql.org/), [**Microsoft SQL Server**](https://www.microsoft.com/en-us/sql-server/), [**Azure SQL**](https://azure.microsoft.com/en-us/products/azure-sql), [**Oracle**](https://www.oracle.com/database/), [**SQLite**](https://www.sqlite.org/index.html) and [**MySQL**](https://www.mysql.com/). 

We do a lot of frontend development for our customers, so it is natural to see a lot of JavaScript used. Compared to 2020, TypeScript has jumped up a couple of positions, and is almost neck to neck with JavaScript now. In the backend section, C# and plain old Java are holding the fort, but Python and Kotlin are catching up. Solita has always been known for Clojure expertise, and it is expected to stay high on the list also in the future. Clojure is used in both backend and frontend work at Solita.

In the frameworks compartment, for backend we are using Microsoft [**.NET**](https://dotnet.microsoft.com/en-us/) and [**ASP.NET**](https://dotnet.microsoft.com/en-us/apps/aspnet) with the .NET runtime, [**Spring Boot**](https://spring.io/projects/spring-boot) and [**Spring Framework**](https://spring.io/) with JVM, [**Express**](https://expressjs.com/) with **node.js**  and [**Flask**](https://palletsprojects.com/p/flask/) with **Python**.

For frontend development, the framework ruling the landscape at Solita is [**React**](https://reactjs.org/) with almost half of the votes (45%). The runner-ups are [**vue.js**](https://vuejs.org/) (14%) and [**Angular**](https://angular.io/) (13%). From the **Clojure** context, [**Reagent**](https://reagent-project.github.io/) and [**re-frame**](https://day8.github.io/re-frame/) are also getting around 10% of votes each.

The variety of stacks used in projects is visible also in the most used libraries, frameworks and tools below where you can spot **Java**/**Clojure**/**Python** flavors, and also hints from the integrations and data engineering projects.

[![Libraries](/img/developer-survey-2022/books.png)](/img/developer-survey-2022/books.png)

In the Low-Code section, Solita does a number of projects in both [**Microsoft PowerApps**](https://powerapps.microsoft.com/) and [**Outsystems**](https://www.outsystems.com/). In addition to those, there are various one-off projects with platforms like **AppSheet**, **Dell Boomi**, **MuleSoft** or **SalesForce Lightning**.

Mobile development is done mostly with modern native declarative UI frameworks ([**SwiftUI**](https://developer.apple.com/xcode/swiftui/), [**Jetpack Compose**](https://developer.android.com/jetpack/compose)), and with [**React Native**](https://reactnative.dev/) and [**Flutter**](https://flutter.dev/) where cross-platform stacks are needed. Some desktop cross-platform work is also done with [**Electron**](https://www.electronjs.org/) and [**Qt**](https://www.qt.io/) frameworks.

## Platforms and Deployment targets

When our cloud projects get live, we deploy them most often in [**Microsoft Azure**](https://azure.microsoft.com/) and [**Amazon AWS**](https://aws.amazon.com/) (roughly 33% for each) and [**Google GCP**](https://cloud.google.com/) (12%). Some 10% are deployed in private cloud setups and 10% in [**Windows Server**](https://www.microsoft.com/en-us/windows-server). A number of developers are also indicating interest towards deploying in [**IBM Cloud**](https://www.ibm.com/cloud), which is currently not used in the projects.

For deployment setup and configuration, we use [**Docker**](https://www.docker.com/) (65%), [**Kubernetes**](https://kubernetes.io/) (15%), [**VirtualBox**](https://www.virtualbox.org/) (8%), [**Podman**](https://podman.io/) (5%) and [**Vagrant**](https://www.vagrantup.com/) (5%).

During past two years, Solita developers have done desktop applications for **Windows**, **Linux** and **MacOS**, even though the volumes are much lower than in more common browser based solutions. 

In the mobile context, we have done **iOS**/**Android** apps, some wearable OS and assistant solutions, plus a handful of [**Raspberry Pi**](https://www.raspberrypi.org/) / [**Arduino**](https://www.arduino.cc/) projects. There is also a good amount of interest among the personnel to get more work in the mobile/embedded projects.

## DevOps

For version control, Git has swept the floor - in the survey we did not have a single vote for any other version control system. In the VCS service selection, there was more variation. **GitHub** was the most used (Solita is a GitHub corporate customer). Where the customer has other preferences, we have used [**Azure DevOps Services**](https://azure.microsoft.com/en-us/products/devops/), GitLab and [**BitBucket**](https://bitbucket.org).

In the DevOps section we had an open question about the use of Git hooks in the daily work. Hooks are quite widely used in Solita projects for various purposes, most often for pre-commit or pre-push code formatting, tests or style checks, but also build pipelines, deployments and posting [**Slack**](https://slack.com/) messages!

The build and deployment pipelines are most often built with either [**Azure Pipelines**](https://azure.microsoft.com/en-us/products/devops/pipelines/) (35%), [**Jenkins**](https://www.jenkins.io/) (28%), or [**GitHub Actions**](https://github.com/features/actions) (20%). Some projects use [**GitLab CI**](https://docs.gitlab.com/ee/ci/) (7%), or do deployments with custom scripting (5%). The rest consists of 4-5 votes per platform in the list of [**CircleCI**](https://circleci.com/), [**BitRise**](https://www.bitrise.io/), [**Octopus Deploy**](https://octopus.com/) and [**TeamCity**](https://www.jetbrains.com/teamcity/).

For infrastructure management, the top votes spread over various **shell**/**makefile**/**yaml**/**powershell** solutions, [**Terraform**](https://www.terraform.io/), [**Ansible**](https://www.ansible.com/) and [**AWS CDK**](https://aws.amazon.com/cdk/)/[**CloudFormation**](https://docs.aws.amazon.com/cloudformation/index.html). A bit smaller percentage of projects make use of [**Azure CLI**](https://learn.microsoft.com/en-us/cli/azure/), [**Azure Resource manager**](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/overview) or [**Google Cloud Deployment Manager**](https://cloud.google.com/deployment-manager/docs).

Majority of the projects have automated deployment of the software to test environments. For production environments, it is more common to have automated deployment with a manual trigger, but 25% of respondents indicate that in their projects also the production deployment is fully automatic.

## Testing & Monitoring

While in the title catalog in the Solita developer community we do not have many people with dedicated testing roles, we do have proper focus in the maturity and quality of the code that we produce. Our teams contribute in all testing activities from smoke testing to regression/acceptance tests and we also conduct penetration testing and A/B testing for some of our customers.

In the past two years the most used test frameworks are [**Cypress**](https://www.cypress.io/) for end-to-end (E2E) testing (31%), [**JUnit**](https://junit.org/junit5/) (30%) and [**Jest**](https://jestjs.io/) (21%) for unit testing. Besides these, testing is also done with e.g. [**Robot Framework**](https://robotframework.org/), [**Puppeteer**](https://pptr.dev/) and [**Cucumber**](https://cucumber.io/) frameworks.

Automation is heavily used in the testing. 79% have automated unit tests, 63% integration tests, 48% E2E tests. Around 10% of the respondents indicate that in their projects the automation extends to performance and security testing.

## Trends & Insights

During the past two years, Solita Developer community has grown significantly both through organic new hires and acquisitions. Particularly **Commentor** from Denmark joining Solita brought in a merry lot of Microsoft/Azure stack users (and about 70 respondents in the survey). This has an impact on multiple levels, and it shows also in this survey in the response spread for many questions, starting from the most common workstation OS, which tipped towards Windows by a clear margin. Solita's Mobile development has been traditionally Finland-originating endeavour, but with Commentor, we now also have several people working with mobile stacks in Denmark.

Low-code platforms are something that the 2020 survey did not acknowledge at all. In the past two years, we have seen an increasing demand for low-code solutions in our customer base, and we have started to invest in utilising various low-code platforms in our projects.

The rise of Kotlin that was already visible in the 2020 survey has become more and more evident, and a lot of our backend projects that would have been done in java a couple of years ago have now been started with Kotlin instead. With Kotlin Multiplatform, it can be anticipated that use of the language spreads further into different areas.

## Links to previous surveys

* [**Solita Developer Survey 2020**](https://dev.solita.fi/2020/12/10/developer-survey-2020.html)
* [**Solita Developer Survey 2018**](https://www.solita.fi/blogit/development-teknologiakartoitus/) _In Finnish only_
* [**Solita Developer Survey 2016**](https://dev.solita.fi/java/2016/05/13/Developers-love-spaces.html)
