---
layout: post
title: Case aloitepalvelut - Moving closer to Continuous Delivery while updating infrastructure
author: bafe
excerpt: Time to update your infrastructure is also a time to update your deployment pipeline! 
categories: 
- Continuous Delivery
- Automation
tags: 
- Java
- OpenSource 
- Continuous Delivery
- Automation
- Deployment Pipeline
- Ansible
- Jenkins
---

Just like software needs to be constantly refactored and its dependencies updated to keep it working and running, needs the infrastructure some love from time to time as well. Our well known services [kansalaisaloite.fi](https://www.kansalaisaloite.fi) ([github](https://github.com/solita/kansalaisaloite)) and [kuntalaisaloite.fi](https://www.kuntalaisaloite.fi) have been sitting on same machines for a few years now and it was time to make some changes to keep everything under control, up to date and running. Apache/httpd will be switched to nginx, java7 to java8, centos will be upgraded to version 7 and so on. But it's also time to update all the processes according to configurations and deployments.

## Automate all the things!

We have always been using Jenkins for releasing software and deploying it to dev and test environments, and our test-coverage and QA are in a reasonable state. But in the old world we did not have required control over the server configurations or production deployments. Even though deployments were mostly scripted, there were always some manual phases were you must remember to execute all the scripts in right machines, users and orders.

I'm a huge fan of Continuous Delivery, QA and automation. I wrote my masters thesis about Continuous Delivery (readable in finnish @ [www.bafe.fi/dippa.pdf](http://www.bafe.fi/dippa.pdf) and decided to implement some of the best practices of CD to these services during this infrastructure updating.

In Continuous Delivery, you should always keep your software deployable into production. Everything that is related to deployment should be automated and auditable: Server configurations for frontend and backend, database migrations, deployments and of course unit and end to end testing.

In Solita, we mostly use Ansible for automating server configurations and setup. All configurations for 3 different applications together with 9 environments and 20 servers are now kept in one git-repository in a single branch. It's easy with Ansible to split the setup in different tasks, roles and environments. At the same time you get the synergy of unified settings but are also able to configure environment- and application-specific setups.

## Configuration pipeline

Although Jenkins is messy and complex, the plugin tool offers many reasonable tools for job pipelines and archiving the artifacts. All changes to configurations should be deployed to dev and test before production, so it was obvious to make a pipeline for server configurations. I wanted to separate the server configuration and deployment to own pipelines because changes to them mostly don't depend on each other in this case.

![Tools](/img/kansalaisaloite-cd/ansible.png)

Every change to configuration repository creates a new pipeline. With Build Pipeline plugin in Jenkins, we can deploy the changes through dev and test environments all the way into production with just a simple mouse-clicks. All applications have their own configuration pipeline. Every change leaves its mark in VCS and the deployments to every environment are automated and trackable with Jenkins. 

## Deployment-related changes to applications

Even though automating the server configurations is a huge step when it comes to controlling the whole system, needed the applications and deployments some leveling up too. First thing was to throw away the separate jetty-server and war-crap and build the application as a simple jar with embedded jetty included ([commit](https://github.com/solita/kansalaisaloite/commit/b7404c181328a8c2118f44ca6e2f5406c7780837)). I did not have the time and interest into switching to spring boot so I ended up just including jetty as a library. Anyway, this had a positive impact on the server startup time: It decreased from about a minute to a few seconds.

Another obvious change was to automate the database migration. I usually prefer separated migration phase in the deployment process rather than letting the application migrate itself, but now I decided to go with the easy way: Include Flyway as a library, package also the sql-increments and make the application responsible of migrating the database on startup if necessary ([commit](https://github.com/solita/kansalaisaloite/commit/b62cf3680cce84086e51bfb54f967d48a3cc4c2d)).

## Deployment pipeline

Now, lets talk about the deployment pipeline. Continuous Delivery relies on a deployment pipeline, where every change in the VCS triggers the automated building, testing and deploying process. It's very important that you build the binaries only once and deploy the same binary into production that you have tested in previous phases and other environments. In our solution, the CI job stores the jar, which is the Release Candidate, and triggers dev-deployment automatically after unit-, integration- and end-to-end-test executions have succeeded. After dev-deployment, the same artifact can be promoted to test-environment and after that, into production. The deploy-job is an ansible-task and also responsible for updating application-specific settings (application.properties) during the deployment.

![Tools](/img/kansalaisaloite-cd/pipeline.png)

The deploy-job also runs smoke tests against the application to verify that it's really running. It also tails some of the application log during the server restart, so while the deployment is running, you can have a look at the log from Jenkins instead of having to go to the server yourself.

Now that the configuration process, deployment process and binaries are the same into every environment, it's very unlikely for the deployment to fail or any problems to occure in production. We always now when we have installed what and reverting the old version or server configurations is as easy as deploying the new one (if the database schema just is compatible).

## Stress-testing the new setup

During this change I was able to also improve many other things, for example caching in nginx. I wanted to run some efficiency tests to be sure we can still serve people with at least the same capability than before. We survived the massive [Tahdon 2013](http://www.tahdon2013.fi/)-campaign pretty well and want to be prepared for other popular initiatives in the future. Gatling is a very simple and powerfull tool for stress testing your application and it gives you many nice diagrams about the results.

![Tools](/img/kansalaisaloite-cd/gatling.png)

## Conclusion

The practices of Continuous Delivery make a massive improvement to the quality of the product, stability of the deployments and readiness to act when we need to make any changes to the application or the server configurations. Automation, reasonable testing and full control of everything are the key factors when it comes to quality and effectivity.