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

You will need to move on to Java 9 at some point. The earlier you can start flirting with it the easier it will be for you. I like to work at cutting edge myself, to embrace challenges at early date, and to evaluate new advances a bit early. Then new things become tools in my toolkit, so I can apply them when they make the most sense. In some situations, yes, it makes sense to run older versions, which are stable, and have had many bugfixes and updates already. You might even feel it's impossible to move on to new versions. Perhaps so, but today's technologies like Docker make it easier, and if you think you cannot update your platforms now and then, cannot find a way to do so, you might be the worst obstacle for updating yourself. There is often a way, if there's a will. With todays technologies, almost anything is possible.

I played a lot with JDK 9 prereleases, betas, early access, to get hold of new things like the module system, jshell, new stream API tricks, etc. But now it's out of beta, general availability, with some updates in already. Ready to go.

But it's not going to be easy. Java 9 is going to be a huge step due to its module systems and new deprecations. It will simply not run many of your existing software stacks and libraries. For example, Spring Boot 1.x is not going to work at all, and it's not going to be working at any future point either. If you wish to run Spring Boot, like many do, you need to first update Spring Boot to version 2.0. Many other libraries will break. Some have been updated, some will be updated at some point, some never will. What will help you a lot with experimentation, is Docker.

## Docker

It's no big secret that I love Docker. I've written a lot about it, used it extensively, and encouraged many to take it in their toolkit. It warms my heart to see that it's getting used more and more extensively these days. The reason why I love Docker for development work is because it makes experimentation much easier. If you wish to experiment with Java 9, for example, you can of course install it in your machine. But your typical installer might overwrite it as default Java, making your life much harder when you still need Java 8..7...6... for your daily work. So Docker to the rescue.

This part is purely optional here, if you don't want to install Docker, or feel it's synonymous to some ugly STD, feel free to skip to next chapters. But there are many Docker images already with JDK 9 in them. And once you start one, you can run any JDK 9 tools from it. If you map your local folder to your workdir in Docker container, you can easily compile code, run maven, run your code, examine your code, test your code, etc. And of course, you can even package your .jar with JDK 9 container, and deploy that, taking full control of your OS and environment for production. You can naturally run your CI pipeline in Docker, things like Jenkins/Travis, SonarQube, run your API and E2E tests there, etc. If you're cloud fanatic like me, you can run your Docker containers easily in AWS, today also with Kubernetes support and AWS Fargate. But for your daily development needs, main thing about Docker is that you can easily try something with it, without needing to permanently install anything locally on your machine, without messing any other installations. Once you're done, you can also easily reset your Docker container.

There are several good images for JDK 9 already. For example, there's openjdk/9-jdk, which surprisingly comes with beta JDK, but still stable enough for my needs. There's Alpine Linux distributions, that come with minimal Linux tooling, but have the benefit of minimal memory footprint (only 5 megabytes), as well. They make great containers for production. But of course, you can also create your own, if you like. For now, let's use the openjdk version. 9-jdk-slim is trimmed down version of JDK, that runs --headless, perfect for tooling without GUI. Right now non-slim version also has a bug, so best to use the slim one (I did mention cutting edge didn't I ;). 

```bash
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

```bash
docker run -it -v $PWD:/root openjdk:9-jdk-slim /bin/bash
cd
ls
exit
``` 

Yes, you can see now your current folder files from within the container. Granted, it would be great idea to use some other account than root but for that you would need to extend the image somewhat. But this article is not just about Docker, so let's move onwards..

## Spring Boot 2 

This is a very short topic. Spring Boot 1 does not work with Java 9, and it will never do so. It's time to move to Spring Boot 2. As of writing this blog, it's not yet GA release, so we are working with milestones. However, in todays world, if you always wait for GA release, it might have already become legacy. So embrace the uncomfort zone!

Fast way to get started with Spring is initializr (link at the end of blog). Right now you can already choose 2.0 snapshots and milestones, so let's do so. You can set up group and artifact to your likings, like I did, and include any dependencies you prefer. When people play with Spring Boot, they often pick up things like Web, Security, Actuator, Devtools, and some even choose to use JPA. Note that right not Milestone 7 is stable, and snapshot is whatever it is at current time. Also note that if you add JPA, Spring requires you to configure the database before you can run the app.

You can do all that, and download a .zip containing all you need. I did that, and extracted the contents to a folder. So far this doesn't really require Java 9, so any Java will do. To run your new Spring Boot app you can do:

```bash
./mvnw clean package
```

And yes, it will compile. To run it you can do:

```bash
java -jar target/*.jar
```

And yes it will run. You can test this simple app immediately at http://localhost:8080.

If you wish to do these with Docker, you can do:

```bash
# Just make sure java tools are in path
docker run -it -p 8080:8080 openjdk:9-jdk-slim java -version
docker run -it -p 8080:8080 openjdk:9-jdk-slim javac -version

# Compile with JDK 9
docker run -it -p 8080:8080 -v `pwd`:/opt/app openjdk:9-jdk-slim /bin/bash -c "cd /opt/app;./mvnw clean package"

# Run with JDK 9
docker run -it -p 8080:8080 -v `pwd`/target:/opt/app openjdk:9-jdk-slim /bin/bash -c "cd /opt/app; java -jar *.jar"
```

![Spring Boot with Java 9 started](/img/java9modules/jdk_9_spring_boot.png)

The above examples for compile and run also map your local folder to Docker container, so it's expected that you would be in your Spring Boot app folder. Sadly, this version will load a lot of stuff from Maven repositories, so compilation will take a while. You would probably want to have a mechanism that would let you reuse those downloads once done, such as team repository, cache, local folder mapping, ready-made layer with most typical libraries, etc. But I digress. Naturally, you can get a better result by packaging your app in a Docker image with Dockerfile like this:


```bash
FROM openjdk:9-jdk-slim
COPY target/*.jar /opt/

EXPOSE 8080
CMD java -jar /opt/*.jar
```

You can build this, and run it with port 8080 mapping, to get the app running.

Note, Spring Boot version 1.x would not run with Java 9 virtual machine, but version 2 will. You might get some warnings - there's still work to do with 3rd party libraries such as CGLIB and ASM. But it will at least start. Here is a typical warning at startup, that actually gives you some hints on what to do:

```code
WARNING: An illegal reflective access operation has occurred
WARNING: Illegal reflective access by org.springframework.cglib.core.ReflectUtils$1 (jar:file:/opt/app/bootdemo-0.0.1-SNAPSHOT.jar!/BOOT-INF/lib/spring-core-5.0.2.RELEASE.jar!/) to method java.lang.ClassLoader.defineClass(java.lang.String,byte[],int,int,java.security.ProtectionDomain)
WARNING: Please consider reporting this to the maintainers of org.springframework.cglib.core.ReflectUtils$1
WARNING: Use --illegal-access=warn to enable warnings of further illegal reflective access operations
WARNING: All illegal access operations will be denied in a future release
```

This is actually an interesting thing, unlike the instruction says, you can and should use --illegal-access=deny, to stop cglib from attempting an operation that's illegal in JDK 9. It will attempt it once, then fall back, but if you set illegal access to deny, it will just silently fail and not even give this warning. Eventually you will get much more warnings or even error like this though, especially if you choose to activate modules with module-info.java file at later point.

Spring Boot 2 is amazing. It contains a lot of new things like support for reactive programming model, Java 9 (d'oh!), and improvements to many areas, like security and devtools. It does require JDK 8 at minimum, versions 7 and below are no longer supported at all.

## Java 9 jlink

Java was released around 1995, as tiny runtime for smart home devices and applets. Since then, with each release new things have been added, but rarely anything has been removed. This has caused Java Runtime bloat: Currently JDK is around 300 megabytes, and you need all of that to even run a hello world program.

With Java 9 there's a new concept of modular runtime, which means, you have more power to tailor your runtime, choose just the modules you actually need. It's not perfect yet, it's a very new thing and there are still some rough edges. But it's possible to create your own JDK/JRE, and put it on a strict diet. No more dragging along ancient Midi instruments, or Corba IIOP support!

So, how do you do that trick? You can run Java jlink tool to do this. Furthermore, you can even run it within a container. You can even generate your runtime to different platform than where you currently are. I recently used this option to generate a modular Windows runtime, on MacOS, within Dockerized Linux container. You do need to have the original full distribution for the platforms of your choosing. Here's the incantation to just trim down the jdk with minimal set of modules:

```bash
jlink --module-path $JAVA_HOME/jmods --verbose --add-modules java.base,java.logging,java.xml,jdk.unsupported,java.sql,java.naming,java.desktop,java.management,java.security.jgss,java.instrument --compress 2 --no-header-files --output jdk-9-minimal-osx --no-man-pages
```

To generate for other platform, just point the --module-path to that platforms native folder. Difference is pretty huge on this level: Where full-blown JDK takes up 298,4MB of space - this minimal version takes up just 45-50MB. That's one sixth of a full release. This set of modules is currently just enough to get Spring Boot app started, the one that we built earlier.

![Modular runtime](/img/java9modules/jdk9_runtime_sizes.png)

And since we did talk about Docker, here's a Dockerfile that will first generate a minimal Alpine image of JDK 9, then use that newly created image to package your .jar:

```
FROM dekstroza/openjdk9-alpine as packager

# First stage: JDK 9 with modules required for Spring Boot
RUN /opt/jdk-9/bin/jlink \
    --module-path /opt/jdk-9/jmods \
    --verbose \
    --add-modules java.base,java.logging,java.xml,jdk.unsupported,java.sql,java.naming,java.desktop,java.management,java.security.jgss,java.instrument \
    --compress 2 \
    --no-header-files \
    --output /opt/jdk-9-minimal

# Second stage, add only our custom jdk9 distro and our app
FROM alpine:3.6
COPY --from=packager /opt/jdk-9-minimal /opt/jdk-9-minimal
COPY target/*.jar /opt/

ENV JAVA_HOME=/opt/jdk-9-minimal
ENV PATH="$PATH:$JAVA_HOME/bin"

EXPOSE 8080
CMD java -jar /opt/*.jar
```

Nice, isn't it? There are still leaner technologies to use for micro-services, but why not grab the benefits of Java platform technological advances?

You can get a full listing of modules by running:

```bash
➜  my-crazy-machine git:(master) ✗ java --list-modules
java.activation@9
java.base@9
java.compiler@9
java.corba@9
java.datatransfer@9
java.desktop@9
java.instrument@9
java.jnlp@9
java.logging@9
java.management@9
java.management.rmi@9
java.naming@9
java.prefs@9
java.rmi@9
java.scripting@9
java.se@9
java.se.ee@9
java.security.jgss@9
java.security.sasl@9
java.smartcardio@9
java.sql@9
java.sql.rowset@9
java.transaction@9
java.xml@9
java.xml.bind@9
java.xml.crypto@9
java.xml.ws@9
java.xml.ws.annotation@9
javafx.base@9
javafx.controls@9
javafx.deploy@9
javafx.fxml@9
javafx.graphics@9
javafx.media@9
javafx.swing@9
javafx.web@9
jdk.accessibility@9
jdk.attach@9
jdk.charsets@9
jdk.compiler@9
jdk.crypto.cryptoki@9
jdk.crypto.ec@9
jdk.deploy@9
jdk.deploy.controlpanel@9
jdk.dynalink@9
jdk.editpad@9
jdk.hotspot.agent@9
jdk.httpserver@9
jdk.incubator.httpclient@9
jdk.internal.ed@9
jdk.internal.jvmstat@9
jdk.internal.le@9
jdk.internal.opt@9
jdk.internal.vm.ci@9
jdk.jartool@9
jdk.javadoc@9
jdk.javaws@9
jdk.jcmd@9
jdk.jconsole@9
jdk.jdeps@9
jdk.jdi@9
jdk.jdwp.agent@9
jdk.jfr@9
jdk.jlink@9
jdk.jshell@9
jdk.jsobject@9
jdk.jstatd@9
jdk.localedata@9
jdk.management@9
jdk.management.agent@9
jdk.management.cmm@9
jdk.management.jfr@9
jdk.management.resource@9
jdk.naming.dns@9
jdk.naming.rmi@9
jdk.net@9
jdk.pack@9
jdk.packager@9
jdk.packager.services@9
jdk.plugin@9
jdk.plugin.dom@9
jdk.plugin.server@9
jdk.policytool@9
jdk.rmic@9
jdk.scripting.nashorn@9
jdk.scripting.nashorn.shell@9
jdk.sctp@9
jdk.security.auth@9
jdk.security.jgss@9
jdk.snmp@9
jdk.unsupported@9
jdk.xml.bind@9
jdk.xml.dom@9
jdk.xml.ws@9
jdk.zipfs@9
oracle.desktop@9
oracle.net@9
```

So with full-blown non-trimmed JDK, that's what you have on the disk, and that's pretty much what you load in memory every time you run a hello-world. In the future we will all be tailoring our Java, pretty much.

Unfortunately, as of right now, Spring Boot is not particularly modular in the sense of Java 9 modules. It's still much jar-based, and comes with a metric drek ton of dependencies. When running Spring, whatever you save in JDK/JRE memory footprint, will have less of an effect on full service. But I expect this to change, in the future, when more people start using later versions of technology. There are also more lightweight runtimes around, with less core features, such as Java Microprofile, and Spark. If you're looking to really put Java on a diet, you might want to take a look at these, too. Both are very interesting and attractive choices.

On the other hand, using Docker, and making clever layers, it's probably also possible to squeeze thinner and more lightweight versions of your Java software. Most people start a new year with some promises and new healthy habits that last at least a month. How about doing that with Java 9, Docker, and Spring now? :)


## Links

- [Java SE 9 overview and downloads](http://www.oracle.com/technetwork/java/javase/overview/index.html)

- [Java 9 modules explanation](https://www.oracle.com/corporate/features/understanding-java-9-modules.html)

- [Docker openjdk images](https://hub.docker.com/_/openjdk/)

- [Issues with Openjdk image](https://github.com/docker-library/openjdk/issues/145)

- [Docker Alpine JDK 9 image](https://hub.docker.com/r/cantara/alpine-zulu-jdk9/)

- [Spring initializr](https://start.spring.io/)

- [Spark framework](http://sparkjava.com/)

- [Microprofile](http://microprofile.io/)



