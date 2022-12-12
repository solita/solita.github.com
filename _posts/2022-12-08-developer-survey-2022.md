---
layout: post
title: Solita Developer Survey 2022 - summary of results
author: aleksi.sitomaniemi

excerpt: >
 The bi-annual Solita Developer Survey was conducted again in 2022. Read more here to learn about the findings.
tags:
 - Software Development, Developer Survey

---

The bi-annual Solita Developer Survey was conducted in 2022 again, now with a participation of almost 300 people. Since 2020, the company headcount has grown with over _nnn_. The early 2022 acquisitions of Intellishore and Commentor from Denmark brought in a good one hundred people on board, the rest of the sum is new hires. The survey is targeted to all Solitans who are participating in development work regardless of their domain of expertise and title.

See the links section at the end of the post for result summaries from the previous survey years.

## Responder facts

This year, we extended the with separate sections for DevOps, testing & monitoring, and security. We also added some new questions to get more insights in the regular survey content about project setup, language preferences and stacks. In total, this year the survey had 52 questions in 8 sections.

Total respondent count was 286 persons. The geographical distribution covers all Solita office locations in Finland, Sweden, Denmark, Estonia, Germany and Belgium. Roughly 2/3 of the respondents are from Finland.

In the responder facts section, we also asked about team size and co-location. It's worth mentioning that Solita developers very rarely work in solo mode. The most common Solita team size in a project is 2-5 persons, but we also do a lot of projects where teams be up to 10 and more people. Many teams are co-located sharing the same office, some teams who work from multiple offices. As a repercussion from the epidemic, about third of the respondents report that they're mostly working remotely from home.

Most of the survey respondents identify themselves as full-stack developers, followed by the roles of Backend developer, Software architect, Frontend developer and DevOps specialist. The rest of the lot splits into different more specific domains of data, cloud, integrations, and mobile & low-code development.

## CompDev + Open Source

In the competence development section we asked how Solita developers update and maintain their skillsets. We also had a set of questions regarding contribution to open source projects.

In the question about learning platforms, one thing was clear: video is king; YouTube was the most used platform when learning new stuff. We are also widely making use of the O'Reilly online catalog which is available for all Solitans. We also have a healthy budget for attending developer conferences and events to hook up with the dev communities and learn. Action on the events front has been a bit low key in the past due to the obvious reasons, but the scene is getting more lively all the time.

35 respondents had been working in a customer project that is either completely or partially open sourced during the past year. In addition to that, about two thirds of the respondents reported that they use varying number of hours in open source projects of their own choice in their free time. 

We also encourage the participation in Open Source projects with an OSS Contribution program available for developers in Finland. 10% of respondents had participated in the OSS contribution program where you can get a small compensation for your outside working hours contributions to projects publicly available in e.g. GitHub or GitLab.

## Developer preferences

The project teams at Solita have a lot of freedom in setting up the development environment and tooling, including the choice of languages, but the feasibility in the customer's context also needs to be considered to get the best results. The following graph illustrates which languages we have liked most working with in the past two years.

[![Liked languages](/img/developer-survey-2022/keyboard.png)](/img/developer-survey-2022/keyboard.png)

Obviously, there is the other side of the coin here, and some languages have a significant downvoting as well. Out of the languages we have been using frequently in projects, JavaScript, Java and SQL received the most dislikes in the survey.

In the next illustration, you can see what we indicated as languages that we would like to use in the customer work in the near future. All of these languages are in use in at least one project at Solita, but there is a lot of interest towards e.g. Go, Rust and F# which are not yet widely utilized. 

Reflecting upon the previous survey, in 2020 Kotlin was the number 1 most wanted in this question, with a fraction of a percentage of use in customer projects. In this survey, while it is still on the wantlist, Kotlin has already made it to top 10 most used languages in projects, and it is regularly applied in backend, frontend and other (e.g. scripting) contexts. Likewise, it is likely that in the next survey, Go and Rust will have a noticeable presence in the project languages response.

Individual votes were also cast for Elixir, Haskell, Smalltalk, Elm, Lisp in the wanted section.

[![Top wanted](/img/developer-survey-2022/chalkboard.png)](/img/developer-survey-2022/chalkboard.png)

In the development environments, Visual Studio Code has bumped the IntelliJ Idea from the top position, and the vim/emacs derby is still turning for vim. Note that the illustration shows the percentage of votes per editor in a multiple choice question. A lot of our developers use multiple IDEs in their work with different projects, or within one for different contexts.

[![IDE](/img/developer-survey-2022/screen.png)](/img/developer-survey-2022/screen.png)

For their work computer OS, 52% choose Windows, 40% go for MacOS and 8% prefer Linux. The most popular Linux distribution used in Solita linux workstations is Ubuntu. Arch Linux and Debian get a handful of votes. 

## Stacks

Let's have a closer look to what did we do in the past two years then. In the following illustration you can see what were the most used languages in our projects. 

[![Used languages](/img/developer-survey-2022/pen.png)](/img/developer-survey-2022/pen.png)

Despite the rise of nosql solutions, oldschool relational databases are still in the majority, hence SQL in the lead. Among the databases we use most are PostgreSQL, Microsoft SQL Server, Azure SQL, Oracle, SQLite and MySQL. 

We do a lot of frontend development for our customers, so it is natural to see a lot of JavaScript used. Compared to 2020, TypeScript has jumped up a couple of positions, and is almost neck to neck with JavaScript now. In the backend section, C# and plain old Java are holding the fort, but Python and Kotlin are running up. Solita has always been known for Clojure knowhow, and it is expected to stay high on the list also in the future. Clojure is used in both backend and frontend work at Solita.

In the frameworks compartment, for backend we are using .NET Core and ASP.NET with the .NET runtime, Spring Boot and Spring Framework with JVM, Express/node.js and Flask/Python.

For frontend development, the framework ruling the set at Solita is react with almost half of the votes (45%). The runner-ups are vue.js (14%) and Angular (13%). From the clojure context, Reagent and re-frame are also getting around 10% of votes each.

The variety of stacks used in projects is visible also in the most used libraries, frameworks and tools below where you can spot Java/Clojure/Python flavors, and also hints from the integrations and data engineering projects.

[![Libraries](/img/developer-survey-2022/books.png)](/img/developer-survey-2022/books.png)

In the Low-Code section, Solita does a number of projects in both Microsoft PowerApps and Outsystems. In addition to those, there are various one-off projects with platforms like AppSheet, Dell Boomi, MuleSoft or SalesForce Lightning.

Mobile development is done mostly with modern native declarative UI frameworks (SwiftUI, Jetpack Compose), and with React Native and Flutter where cross-platform stacks are needed. Some desktop cross-platform work is also done with Electron and Qt frameworks.

## Platforms and Deployment targets

When our cloud projects get live, we deploy them most often in Microsoft Azure and Amazon AWS (roughly 33% for each) and Google GCP (12%). Some 10% are deployed in private cloud setups and 10% in Windows Server. A number of developers are also indicating interest towards deploying in IBM Cloud, which is currently not used in the projects.

For deployment setup and configuration, we use Docker (65%), Kubernetes (15%), VirtualBox (8%), Podman (5%) and Vagrant (5%).

During past two years, Solita developers have done desktop applications for Windows, Linux and MacOS, even though the volumes are much lower than in more common browser based solutions. 

In the mobile context, we have done iOS/Android apps, some wearable OS and assistant solutions, plus a handful of Raspberry Pi / Arduino projects. There is also a good amount of interest among the personnel to get more work in the mobile/embedded projects.

## DevOps

For version control, git has swept the floor - in the survey we did not have a single vote for any other version control system. In the VCS service selection, there was more variation. GitHub was the most used (Solita is a GH corporate customer). Where the customer has other preferences, we have used Azure DevOps Services, GitLab and BitBucket.

In the devops section we had an open question about the use of git hooks in the daily work.

The build and deployment pipelines are most often built with either Azure Pipelines (35%), Jenkins (28%), or GitHub Actions (20%). Some projects use GitLab CI (7%), or do deployments with custom scripting (5%). The rest consists of 4-5 votes per platform in the list of CircleCI, BitRise, Octopus Deploy and TeamCity.

For infrastructure management, the top votes spread over various shell/makefile/yaml/powershell solutions, Terraform, Ansible and AWS CDK. Some projects make use of other Azure products like CloudFormation and Resource manager or Google Cloud Deployment Manager.

Majority of the projects have automated deployment of the software to test environments. For production environments, it is more common to have automated deployment with a manual trigger, but 25% of respondents indicate that in their projects also the production deployment is fully automatic.

## Testing & Monitoring

While in the title catalog in the Solita developer community we do not have many people dedicated testing roles, we do have proper focus in the maturity and quality of the code that we produce. Our teams contribute in all testing activities from smoke testing to regression/acceptance tests and we also conduct penetration testing and A/B testing for some of our customers.

In the past two years the most used test frameworks are Cypress (31%), JUnit (30%) and Jest (21%). Besides unit testing, UI testing and E2E testing are done with e.g. Robot Framework, Puppeteer and Cucumber frameworks.

Automation is heavily used in the testing. 79% have automated unit tests, 63% integration tests, 48% E2E tests. Around 10% of the respondents indicate that in their projects the automation extends to performance and security testing.

## Trends & Insights

During the past two years, Solita Developer community has grown significantly both through organic new hires and acquisitions. Particularly Commentor AS from DK joining Solita brought in a merry lot of MicroSoft/Azure stack users (and about 70 respondents in the survey). This has an impact on multiple levels, and it shows also in this survey in the response spread for many questions, starting from the most common workstation OS, which tipped towards Windows. Solita's Mobile development has been traditionally Finland-originating endeavour, but with Commentor, we now also have several people working with mobile stacks in Denmark.

Low-code platforms are something that the 2020 survey did not acknowledge at all. In the past two years, we have seen an increasing demand for low-code solutions in our customer base, and we have started to invest in utilising  

The rise of Kotlin that was already visible in the 2020 survey has become more and more evident, and a lot of our backend projects that would have been done in java a couple of years ago have now been started with Kotlin instead. With Kotlin Multiplatform, it can be anticipated that use of the language spreads further into different areas.

# Links

Solita Developer Survey 2020
Solita Developer Survey 2018
Solita Developer Survey 2016