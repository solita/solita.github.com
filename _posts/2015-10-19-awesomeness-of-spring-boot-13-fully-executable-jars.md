---
layout: post
title: Awesomeness of Spring Boot 1.3 Fully Executable Jars
author: ruoat
excerpt: Spring boot 1.3 provides easy way to run Java programs as unix service
---

Awesomeness of Spring Boot 1.3 Fully Executable Jars
----------------------------------------------------

Since [Spring Boot](https://github.com/spring-projects/spring-boot) and Java 8 the world has been a better place for a Java developer. Java 8 Streams and Spring Boot's conventions 
have simplified the code and made programming more enjoyable.

I have loved the Spring Boot's convention of packaging your application as an executable jar, which can be easily started with `java -jar myapplication.jar`.
If the application was a web application an embedded Tomcat or Jetty would be started and no existing container would be needed. By using conventions you could customize application
parameters by providing environment specific properties or yaml configuration. The same jar could be used in different environments and configurations could be taken easily from different
version control repository leaving the application's source repository empty from sensitive data like production passwords.

This concept has worked well. It is easy to build deployment automation with executable jars. But running those executable jars as unix service has not been easy enough. You have had to create
`init.d` or `systemd` scripts, which would launch suitable java with suitable user and suitable profile with suitable JVM options etc. One could google init.d script template for java and modify it until you
had a decent version or maybe grab it from someone of your colleague. I think it has been too tedious task and init.d scripts could have contained bugs.

But the great minds of Spring Boot [contributors](https://github.com/spring-projects/spring-boot/graphs/contributors) have also thought this problem and provided a solid
solution - The [Fully Executable Jar](http://docs.spring.io/spring-boot/docs/1.3.0.M5/reference/htmlsingle/#deployment-install).
The trick is in Boot's Maven or Gradle plugin, which will generate an executable jar (or war) and put
bash [script](https://github.com/spring-projects/spring-boot/blob/master/spring-boot-tools/spring-boot-loader-tools/src/main/resources/org/springframework/boot/loader/tools/launch.script) in the front of the jar file.
The script will load the configuration and bootstrap the jar launching.

Look at this coolness:

`head -n 10 myapplication.jar`
 
```bash
#!/bin/bash
#
#    .   ____          _            __ _ _
#   /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
#  ( ( )\___ | '_ | '_| | '_ \/ _`` | \ \ \ \
#   \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
#    '  |____| .__|_| |_|_| |_\__, | / / / /
#   =========|_|==============|___/=/_/_/_/
#   :: Spring Boot Startup Script ::
#
```

The jar still is working normally. It can be opened with zip programs although some compression programs may throw some warnings.

For example `unzip -t myapplication.jar | head -5` informs:

```bash
warning [myapplication.jar]:  5251 extra bytes at beginning or within zipfile
  (attempting to process anyway)
Archive:  myapplication.jar
warning [myapplication.jar]:  5251 extra bytes at beginning or within zipfile
  (attempting to process anyway)
    testing: META-INF/                OK
    testing: META-INF/MANIFEST.MF     OK

```

The startup script does some clever things. It reads `myapplication.conf` where you can specify things like JAVA_HOME and JAVA_OPTS. It also runs the jar with
the same user as the owner of the file. Just link the init script `sudo ln -s /var/myapplication/myapplication.jar /etc/init.d/myapplication`
and you are able to start the application as service with `service myapplication start`. Awesome!

I think Spring Boot is a great platform to build modern Java applications. It provides lots of solid, well engineered stuff, so you are no longer forced to keep reinventing the wheel.
The final version of Spring Boot 1.3.0 has not been published yet but you can grab the [milestone version](http://docs.spring.io/spring-boot/docs/1.3.0.M5/reference/htmlsingle/).

