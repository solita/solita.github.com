---
layout: post
title: Microservices FTW
author: arto
excerpt: How to boot up and get some feedback fast
---

My name is Arto Santala. I've worked in many roles, including software developer, engineer, project manager, scrum master, and architect, as well as a trainer/coach. I've worked for companies such as Tieturi, ICL, Finnair, and many others. While I've been involved in producing software since the mid-90's, and even before that, I joined Solita as a new employee early this year, so it's an exciting new step for me.

A new software designer in Solita will first get to do an exercise in coding, no matter what they will end up doing here. The idea is to pass on knowledge and ideas both ways, on tools, technologies and architecture, and I think it's a great idea. Equally important is to get to know people, habits, and ways of working together - these also go both ways, since everybody brings along unique set of skills and experiences. So I wanted to write a little blog post on my experiences.

I am pretty experienced in all things Java, and recently also in Angular, so I wanted a mix of something familiar - but also something new, to raise the bar a bit and learn something new. For the familiar base I chose Spring Boot and AngularJS - I'm pretty experienced with Spring after training it for major companies in Finland, and also using in various production systems along the way. I chose to base everything on Spring Boot because that part still has something new for me to learn. Maven was the solid basis for my builds, while Grunt handled whatever automation JavaScript side required.

Spring Boot will get you a nice EE environment and services in an embedded container with just a little bit of Maven/Gradle build script. It can be deployed as a .jar file, and the only requirement then is to have Java installed.

![Microservices container is up and running in 5 seconds](/img/microservices/springbootrun.png)

I chose to mix things up by not using Bootstrap as my UI library, but instead to go for more mobile-like and puristic approach with Google Material Design philosophy and libraries. I also chose to use Java EE standards and generic APIs as much as possible, instead of coding against specific third party implementations.

To make things more difficult/fun I chose a Macbook Pro as my laptop - being a veteran Windows/Linux user, this is a new experience and actually much fun. On the other hand I find myself often in the ever so familiar terminal window when things get hairy.

I also made transition from NetBeans to IntelliJ Idea - now I love NetBeans, but IntelliJ is more common here, and I've heard a lot of great things about it, too. So Idea it is.

Topic of the exercise was to build a simple application with a few key domain objects and requirements listed. In my case, they are employees, departments, and municipalities, with nearly CRUD-like services - but with some more specific points like which fields are mandatory, and where specific validation rules are needed.

I wanted to have great test coverage, and for me that typically means unit tests as specifications, and API/integration/system/e2e tests to prove the features and service API. I ended up doing unit tests for Java, unit tests for JavaScript, RestAssured tests to prove the REST API, and Protractor tests to prove the requirements/features that were in the initial specification.

## Good stuff

So, what went well? Due to having familiar basis and especially knowing what can be done, work was fast in the beginning. I started writing tests early, and included tests with every bit of progress I made, making their cost cheaper. On the other hand, tests helped me polish places where there were conditional statements or loop structures faster and earlier, with more feedback. Java EE standards like JAX-RS, and JPA work suprisingly well with Spring Boot - and I'm able to use an embedded lightweight server instead of packaging to .war and deploying to more heavyweight application server. Spring lets met still maintain valuable services like automatic transaction management.

![Material design is bold and simplistic, and scales well to and from mobile devices](/img/microservices/employeesapp.png)

Actually, the microcontainer approach worked so well that a devil went into me and I decided to see if I can run the app inside Raspberry Pi v2 that I recently purchased. And it was lovely! ;) Just install Java into Pi, and run the packaged .jar - and Spring Boot takes care of everything. Gotta love the simplicity and elegance. It's just somewhat  different an experience to deploying a J2EE .ear into Websphere Application Server....

I also love good test coverage, it gives the instant feedback I want when I make changes.

![Karma+Jasmine will do the basic specifications nicely](/img/microservices/testcoverage.png)

## Bad stuff

Disappointments? While I love Material Design philosophy - I've always been into minimizing buttons and stages in the UI, trying to make it read users mind instead of forcing to go through endless chores - I have to say that Angular Material library is not there yet, not by far. It's missing a lot of essentials like selection/combo boxes, calendar pickers, etc, and there are a lot of bugs with existing functionality, too.

But still... It's beautiful, and what I was missing from Material I implemented with Bootstrap. They do work together, but I hope at some point I would not have to do that anymore.

## Some fun unexpected findings:

- It's possible to use LocalDate with JPA - just have to write a @Converter class. It's not always working so well on REST services side, but it can be made to work with a little effort.
- Java 8 is mature enough for use, even with coverage. Spring Boot does have some issues with live reloading of code while you change it, but that's not a big dealbreaker for me. I love streams and Lambdas, even though I've seen languages where they feel more natural.
- Angular can be beautiful and clear, I've seen it written a lot more messy in my past, but with a bit of design it can be made something that's easier to understand. There's a lot of power in directives - that power can be used for great things or for utter darkness.
- Material design themes and palettes can be created programmatically, making it easy to tailor them or swap them to get exactly that right shade..
- JHipster could have been used to boost initial setup. However grails-like fast start setups may often slow down a lot when tailoring begins - so for me they are not typically faster - provided that I know the technologies I'm working on. And if I don't, it's a recipe for disaster anyway.
- Best setup is to have unit tests being either run as part of build process, or even better, whenever something changes. Especially on JavaScript side this is very useful feedback
- Mental note to dive deeper also into Clojure, React, and Node.js server-side solutions.
- I'm sold on topic of Microservices. I used to be a fan of good open source application servers like Glassfish and Wildfly - because they come equipped with pretty much any services you might need. But having an embedded container has its uses, too, and there are many places where it's a superior solution. Simple is good, fast journey from vision to product is good, too. That gets early feedback cycle going. Using Spring means there's more configuration that can be done programmatically, and less unique environment-specific configuration work to set up a server. Hello, Chaos Monkey!

So, what do you think is a hot stack right now? What's coming and what's going?

### Some links to resources mentioned here:

[Spring Boot](http://projects.spring.io/spring-boot/)

[AngularJS](https://angularjs.org/)

[Material Design](http://www.google.com/design/spec/material-design/introduction.html)

[Angular Material](https://material.angularjs.org/)

[Bootiful Java EE Support in Spring Boot 1.2](http://spring.io/blog/2014/11/23/bootiful-java-ee-support-in-spring-boot-1-2)

[Definition of Microservices by Victor Klang](http://klangism.tumblr.com/post/80087171446/microservices)
