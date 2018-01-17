---
layout: post
author: arto
title: Put your Java on a diet with Java 9 Modules - Spring Boot 2 - Docker - Oh my!
excerpt: New year, new technologies. Java 9 modules, Spring Boot 2 and Docker work extremely well together, and I'll show you how.
tags:
- Java
- Java 9
- Spring
- Spring Boot
- Microservices
- Docker
---

It's year 2018, and it's time to update your knowledge to date. Many people are running Java 8 or older, yet Java 8 will go EOL by September (and anything older is already extinct). This means no security updates for you, well at least if you don't pay for them. Furthermore, Java 8 was released in 2014, based on work done before that, so if you are working on Java 8 or older platforms, you are using technology that is very old by todays pace, and limiting your options severely.

You will need to move on to Java 9 at some point. The earlier you can start flirting with it the easier it will be for you. I like to work at cutting edge myself, to embrace challenges at early date, and to evaluate new advances a bit early. Then new things become tools in my toolkit, so I can apply them when they do make the most sense. In some places, yes, it makes sense to run older versions, that are stable and have had many bugfixes and updates already. You might even feel it's impossible to move on to new versions. Perhaps so, but todays technologies like Docker make it easier, and if you think you cannot update your platforms now and then, cannot find a way to do so, you might be the worst obstacle for updating yourself. There is often a way, if there's a will. With todays technologies, almost anything is possible.

I played a lot with JDK 9 prereleases, betas, early access, to get hold of new things like the module system, jshell, new stream API tricks, etc. But now it's out of beta, general availability, with some updates in already. Ready to go.

But it's not going to be easy. Java 9 is going to be a huge step due to it's module systems and new deprecations. It will simply not run many of your existing software stacks and libraries. For example, Spring Boot 1.x is not going to work at all, and it's not going to be working at any future point either. If you wish to run Spring Boot, like many do, you need to first update Spring Boot to version 2.0. Many other libraries will break. Some have been updated, some will be updated at some point, some never will. What will help you a lot with experimentation, is Docker.

## Docker

It's no big secret that I love Docker. I've written a lot about it, used it extensively, and encouraged many to take it in their toolkit. It warms my heart to see that it's getting used more and more extensively these days. The reason why I love Docker for development work is because it makes experimentation much easier. For production it has much more different qualities, but they are not the topic today. If you wish to experiment with Java 9, for example, you can of course install it in your machine. But your typical installer might overwrite it as default Java, making your life much harder when you still need Java 8..7...6... for your daily work. So Docker to the rescue.

This part is purely optional here, if you don't want to install Docker, or feel it's synonymous to some ugly STD, feel free to skip to next chapters. But there are many Docker images already with JDK 9 in them. And once you start one, you can run any JDK 9 tools from it. If you map your local folder to your workdir in Docker container, you can easily compile code, run maven, run your code, examine your code, test your code, etc. And of course, you can even package your .jar with JDK 9 container, and deploy that, taking full control of your OS and environment for production. You can naturally run your CI pipeline in Docker, things like Jenkins/Travis, SonarQube, run your API and E2E tests there, etc. Do not that if you're cloud fanatic like me, you can run your Docker containers easily in AWS, today also with Kubernetes support. But for your faily development needs, main thing about Docker is that you can easily try something with it, without needing to permanently install anything locally on your machine, without messing any other installations. Once you're done, you can also easily reset your Docker container.

There are several good images for JDK 9 already. For example, there's openjdk/9-jdk, which suprisingly comes with beta JDK, but still stable for my needs. There's Alpine Linux distributions, that come with minimal Linux tooling, but have the benefit of minimal memory footprint (5 megabytes), as well. They make great containers for production. But of course, you can also create your own, if you like. For now, let's use the openjdk version. 9-jdk-slim is trimmed down version of JDK, that runs --headless, perfect for tooling without GUI. Right now non-slim version also has a bug, so best to use the slim one (I did mention cutting edge didn't I ;). 

```
docker run -it openjdk:9-jdk-slim /bin/bash

root@aabf371985b2:/# java -version
	openjdk version "9.0.1"
	OpenJDK Runtime Environment (build 9.0.1+11-Debian-1)
	OpenJDK 64-Bit Server VM (build 9.0.1+11-Debian-1, mixed mode)
root@aabf371985b2:/# javac -version
	javac 9.0.1
root@aabf371985b2:/# jshell
	Jan 17, 2018 6:57:03 AM java.util.prefs.FileSystemPreferences$1 run
	INFO: Created user preferences directory.
	|  Welcome to JShell -- Version 9.0.1
	|  For an introduction type: /help intro
jshell> System.out.println("Konban-wa!")
	Konban-wa!
jshell> /exit
	|  Goodbye
root@aabf371985b2:/# exit

```


Yes, I love the new JShell. Finally Java has REPL environment for rapid experimentation and prototyping. But again, not the main point of this article. Now that you have JDK 9 capability, you can also map your local folder to your workfolder, and run any builds, link things, etc, within the container, without polluting your local environment. Here's how to start container with mapping:

```
docker run -it -v $PWD:/root openjdk:9-jdk-slim /bin/bash
cd
ls
exit
``` 

Yes, you can see now your current folder files from within the container. Granted, it would be great idea to use some other account than root but for that you would need to extend the image somewhat. But this article is not just about Docker, so let's move onwards..

## Spring Boot 2 

This is a very short topic. Spring Boot 1 does not work with Java 9, and it will never do so. It's time to move to Spring Boot 2. As of writing this blog, it's not yet GA release, so we are working with milestones. However, in todays world, if you always wait for GA release, it might have already become legacy. So embrace the uncomfort zone!

Fast way to get started with Spring is initializr (link at the end of blog). Right now you can already choose 2.0 snapshots and milestones, so let's do so. You can set up group and artifact to your likings, like I did, and include any dependencies you prefer. When people play with Spring Boot, they often pick up things like Web, Security, Actuator, Devtools, and some even choose to use JPA. You can do all that, and download a .zip containing all you need. I did that, and extracted the contents to a folder. So far this doesn't really require Java 9, so any Java will do. To run your new Spring Boot app you can do:

```
./mvnw clean package
```

And yes, it will compile. To run it you can do:

```
java -jar target/*.jar
```

And yes it will run. You can test this simple app immediately at http://localhost:8080.

Note, Spring Boot version 1.x would not run with Java 9 virtual machine, but version 2 will. You might get some warnings - there's still work to do with 3rd party libraries such as CGLIB and ASM. But it will at least start.

Spring Boot 2 is amazing. It contains a lot of new things like support for reactive programming model, Java 9 (d'oh!), and improvements to many areas, like security and devtools. It does require JDK 8 at minimum, versions 7 and below are no longer supported at all.

Right now, sadly, it does not support JDK 9 module model, or much modularity at all. Since Spring is kind of a heavyweight beast, that would be delightful, if done right. But we'll see how that progresses.

## Java 9 jlink



## Links

http://www.oracle.com/technetwork/java/javase/overview/index.html

https://hub.docker.com/_/openjdk/

https://hub.docker.com/r/cantara/alpine-zulu-jdk9/

https://start.spring.io/