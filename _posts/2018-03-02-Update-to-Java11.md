---
layout: post
author: arto
title: Update to Java 11 now!
excerpt: What's coming up in the world of JVM
tags:
- Java
- Java 11
- Software development
---

I recently wrote an article on updating your environment to Java 9 for better modularity and reduced memory and disk use. Turns out that was not cutting edge enough since many are already using Java 9 to run production systems. Also, after my article, there was some news coverage on how Java 9 and 10 will end up having a very short support period, and many people potentially jumping straight to Java 11. Let's do that!

![Java 11 - come out and play!](/img/java11/Java_11_image.png)

A Java 11 early access release is already out. If you want to take a look at what's coming up, you can download it and start hacking. The safest way to try it out is to whip out Docker, as we did last time.

## Whip out Docker

To try out the early access build of Java 11 you need a nice Linux base image and some JDK installation magic on top of that. Here's an example Dockerfile:

```
FROM centos

ENV LANG C.UTF-8
ENV JAVA_PACKAGE_URL https://download.java.net/java/early_access/jdk11/2/GPL/openjdk-11-ea+2_linux-x64_bin.tar.gz

# Upgrading system
RUN yum -y upgrade
RUN yum -y install wget

WORKDIR /opt

RUN wget --no-cookies --no-check-certificate \
  $JAVA_PACKAGE_URL -O /opt/jdk11.tar.gz \
  && tar -zxvf jdk11.tar.gz \
  && rm jdk11.tar.gz

ENV JAVA_HOME /opt/jdk-11
ENV PATH "$PATH:$JAVA_HOME/bin"

RUN useradd -ms /bin/bash javauser
USER javauser
WORKDIR /home/javauser

CMD jshell
```

It's very crude but gets the thing done for now. If you are impatient, you can also use our this image directly from Docker hub. I do not guarantee long support though, I'm sure better images will start emergin anytime now.

```
docker run -it solita/jdk11-ea
```

Got it? Go play!

## What's new?

Not so much is new. Java 10 and 11 are still moving targets, and lots will change as well. But some things that we know are already out there.

Java 10 is to be released any moment now. Java 9 public updates are also destined to end soon, so you should update to Java 10 soon if you like those updates. Java 10 is going to be another short term support update, with Java 11 being a long term support update, like Java 8.

![Some of the JDK 10/11 goodies](/img/java11/jshell_inference.png)

Java 10 will have type inference for local variable type (YAY!), so your code will look like this:

```Java
// Upcoming Java 10 code
var productList = new ArrayList<String>();
productList.add("Macbook Pro");
var productStream = productList.stream();
productStream.forEach(System.out::println);
```

Note a few things. This requires you to define the generic typing on the right side, so it can be inferred. No diamond operator for you. Secondly, there's no 'val', only var. Meaning, it's just a normal mutable variable declaration, with a bit syntactic sugar. Still nice. You can test it immediately with Java 10/11 early access build, and soon with Java 10 GA build.

It will not work for method/constructor parameters or return types, member variables/fields, or catch formals. Only for logic within methods, including loop indexes.

Of course, we still have all Java 9 goodies such as new Stream functions:

```
jshell> IntStream.range(0,10).takeWhile(x -> x < 5).forEach(System.out::println)
0
1
2
3
4
```

If you update to any of these Java versions, 9, 10, 11, you get access to JShell and goodies like that. JShell that was introduced in Java 9, starts up now significantly faster, making it much better REPL experience for those who value it.

There is some Docker love coming up in Java 10 - improved container detection and resource configuration usage. So Java becomes more aware of its environment, especially running in containers.

As always, better performance, improved garbage collection, experimental Jit compiler, open sourced root certificates, yada yada yada. Expect the major releases to happen much faster, even twice a year. Long term support releases will come every 3 years - but to get that three years support updates you will probably need to pay for it, too. See the blog link at end of article on free, secure, stable.

JDK 11 will continue the modularity work and more aggressively remove modules from core Java, making it lighter and easier to update. Next on list are CORBA and Java EE modules. You can still get them, on top of core Java, when you need them. But they're not bundled with every micro-service, freeing up 22 megabytes and 9 modules from it. It goes leaner and meaner.

Project Panama and Valhalla are still coming up, value types, generic specialization, native function calling from JVM, etc. Amber project started with local variable type inference, but enums will be having much more love in future versions, too. At this early stage, not much concrete to show yet.

But it's probably safe to say - this is not your grandfather's Java anymore.

## Disclaimer and closing thoughts

You might have noticed that I'm an incurable jester. Half of what I say is not so serious: the trick is detecting which half. I do not endorse always using the latest available platform for running production systems, unless you know what you are doing. I certainly do not encourage you to run outdated ones, either. But you should be relatively fine with Java 8 for a while longer. So please do not install JDK 11 on your production system yet.
 
I do have a great passion for technology and believe firmly in always having an eye for future, and playing with things before using them for production. Java 11 is now in play-phase, and this article is about understanding that you can already start learning it and playing with it, to be prepared. 

Moving from Java 8 to any of the upcoming releases is not going to be minor update - it's going to be a huge, risky and painful update, mostly due to the module system. It's also going to bring marvelous new features and capabilities, with the potential to keep the Java platform alive for years to come. 

The interesting thing is that other JVM languages such as Kotlin, Scala, Clojure and Groovy will need to be updated too, and so will numerous libraries that are not compatible or aren't using the new features available. Since this is a lot of work, it's quite likely that many add-ons on top of Java will simply choke on migration to version 9 and die out. It will be interesting to see which ones have a vibrant community behind them to survive.

Some view this new Java release model as 'update stress' - I view it as attempt to have a slow and outdated platform attempt to reinvent itself, get more flexible, lightweight, and perhaps find new ways to be useful, too. 10 million Java developers around the world are curious to see how it turns out.

Also, keep an eye on the artist formerly known as Java EE - now known as Jakarta EE. Enterprise Java is reshaping itself, and the future seems fuzzy - especially with Microprofile Java competing/supplementing it somewhat. There's a lot of useful stuff in it still, so let's hope that open sourcing and freeing it is not a death stroke, but gives it a new more flexible life  on the platform.


## Links
- [JDK 11 EA Docker image](https://hub.docker.com/r/solita/jdk11-ea/)
- [JDK 10 Early Access builds](http://jdk.java.net/10/)
- [JDK 10 Early Access release notes](http://jdk.java.net/10/release-notes)
- [JDK 11 Early Access builds](http://jdk.java.net/11/)
- [JDK 11 Early Access release notes](http://jdk.java.net/11/release-notes)
- [Oracle Java SE support roadmap](http://www.oracle.com/technetwork/java/eol-135779.html)
- [Blog post on Java support models and versions](https://www.azul.com/java-stable-secure-free-choose-two-three/)
