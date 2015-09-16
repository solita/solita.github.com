---
layout: post
title: Goodbye classpath - or how about a cup of steaming Java 9?
author: arto
excerpt: Java 9 is coming - are you ready?
---

Java 9 is on schedule to be published late 2016 - and feature complete by end of this year. There are still around 10 million Java developers around, who will sooner or later be interested in what's coming up next, so I decided to sit down and write about some things that interest me there.

I like to get a view of what's to be expected in the future so in addition to reading about Java 9 I installed prerelease in my machine to have a spin. It's also useful to test-compile your legacy software with upcoming JDK just to see what might break.

## Managing multiple JVMs with Jenv

A recommendation first: Having multiple virtual machines in your computer can be a mess. I used to run Windows, and there you can play with environment variables, but registry still messes things up now and then. With OSX, I've been quite happy with tool called jenv, which allows me to set up multiple installations of Java, and swap between them. It will also change JAVA_HOME, so many command line tools work properly. Highly recommended! (As is also nvm tools for Node development - that immediately also supports Node 4.0). Anyways, I digress. But jenv makes it very easy to experiment with the latest and greatest, then go back to warm and fuzzy, safe old Java 8.

## What puzzles me about classpath

So what's coming up next year when Java 9 is released? Well, a major thing is going to be Jigsaw - yes the modularity system that was supposed to be released already with Java 7. It's taken so long (8 years) for a few reasons. One is certain corporate buyout and changes in the way things are done. Second is because Jigsaw has ambitious goal of modularizing core of JRE - and the dependency map between different parts is crazy!

So what's coming up? Well, essentially there's a new concept, module. One way to explain the structure is this: class <- package <- module. Module is a collection of code that can refer to other modules or be referred to. Module is described by a module descriptor, and with this descriptor file, you are able to export a module, or require any number of modules. Yes, this is reminiscent of OSGI - and not by accident :)

There's a new class java.lang.reflect.Module that you can access run-time to get information on that new dimension. Typically modules are named, but there's also concept of unnamed modules for backwards compatibility with code that does not export any module definitions. There's also a new package java.lang.module, that contains more definitions for the module system. The API gives pretty good idea of what you can do in Java 9.

## Examples of module-info.java

Simplest declaration of module could be to create a file named module-info.java at your source path root with this kind of content:

```java
module fi.solita.blogster { }
```

This declares a module with a name, and after compilation, it becomes module-info.class. Like package names, module names must not conflict, so same best practices for naming modules apply. You can simply package this compilation result as you would normally do, and it becomes a modular jar file. For JDK itself, there's a plan for new format called JMOD, but that's entirely different thing.

To use more of the keywords we could do:

```java
module fi.solita.blogster {
    requires fi.solita.iotdriver;
    requires java.sql;
    exports fi.solita.blogster.alpha;
    exports fi.solita.blogster.beta;
}
```

Dependency to other modules with requires-keyword implies both compile and run-time dependencies. It will magically build the right classpath. Dependencies are transitive, meaning that by declaring dependency to java.sql module, you get also whatever modules it depends on and so forth. And when we export a package, it means we make all public types available for use by other modules. If you declare a module with no exports, it's not going to be very re-usable.

Versions can be declared and required, for example:

```java
module fi.solita.crawlingturtle @ 0.1 {
    requires fi.solita.noisebox @ 1.2;
}
```

So, as you can see, new keywords being added: module, requires, exports. I hope you haven't used them as variable names ;) Unfortunately, it seems current build of JDK 9 does not yet process the module keyword, so we have to wait a bit further to really play with it.

## What else is there?

Obviously it's not just about Jigsaw - there's dozens of other updates to APIs all over. Some that interest me are:

- **G1 garbage collector** becomes the new default for server virtual machines - finally. This mainly means improved support for large heap memories, and more toggles for tuning gc pauses etc. This has of course been available for long time, but going to default setting implies certain level of maturity.
- **HTTP 2.0 client** offers improved/simplified API with asynchronous calls and websocket support. Byebye HttpURLConnection! ;)
- Some project coin refinements, one of them means underscore is not just frowned upon in idenfitifer names, it's now an error
- **JShell** and **REPL** (Read-Eval-Print-Loop) enable you to play with and test code earlier and easier 
- Better access to OS level details such as process level

Some of the changes are pretty big, and will break some existing code. So if you intend to keep up to date and not use trusty old Java 1.6 (or later ones) forever, it's time to start planning and testing for the future. See you there!

## Some links on these topics:

[OpenJDK 9](http://openjdk.java.net/projects/jdk9/)

[JEnv](http://www.jenv.be/)

[java.lang.reflect.Module API](http://cr.openjdk.java.net/~mr/jigsaw/spec/api/java/lang/reflect/Module.html)

[java.lang.module package](http://cr.openjdk.java.net/~mr/jigsaw/spec/api/java/lang/module/package-summary.html)

[The State of the Module System](http://openjdk.java.net/projects/jigsaw/spec/sotms/)

[JEP 222 JShell](http://openjdk.java.net/jeps/222)

[OpenJDK Quickstart](http://openjdk.java.net/projects/jigsaw/doc/quickstart.html)

[Module declaration grammar](http://openjdk.java.net/projects/jigsaw/doc/lang-vm.html#jigsaw-1)


