---
layout: post
title: Virusscanner as a REST service
author: lokori
excerpt: How to setup a open source virusscanner as a REST service. 
---

Every time we deal with user supplied content, such as file attachments, we must take precautions
to make sure they are free of virii and trojans. The traditional solution in our projects has been
a commercial file system based scanner, but it turns out we can do better. Here's a recipe for
setting up the virus scanner as a REST service, free of charge.

## Handling file attachments

Malicious users can supply compromised files on purpose or the users can upload them unintentionally. Whatever
the system is, it's usually a good idea to set certain limits for attachments. As an example I might recommend
these sort of limitations:

1. Limit the maximum file size to something sane.
2. Whitelist allowed content types. Block everything else.
3. Don't rely on the file extension for content type.

Even so, the file may contain something nasty and should be scanned for problems.

## Traditional scanner deployment

File system based scanners are good for workstations. They scan for new files in the system
and report the results. This can be done on a web server by saving the files to some 
temporary directory and calling ```System.exec``` before they are accepted.

This is a bit complicated to test and deploy, files must be saved on disk needlessly and it's not
real time. It scales poorly.

## Scanner as a service

Here's how we deployed a virus scanner and made it available as a REST service. You could
deploy one scanner server for dozens of applications this way.

![Deployment](/img/rest-virusscan/virusscanner-deployment.png)

In this case the virus scanner is [ClamAV](http://www.clamav.net/index.html), which is a open source
virus scanner. Installing ClamAV on Linux is [a few simple commands](https://github.com/solita/clamav-java/blob/master/env/clamd.sh). 

The diagram may look complicated as there are separate servers for the application, scanner and logging. You could run everything with just
one server, but then you wouldn't need a REST service. The REST service makes sense when you deploy one scanner service used from multiple
applications. The log server is optional, ClamAV doesn't require it.


## Setting up the REST service

As such, ClamAV runs as a Linux daemon and has it's own command protocol. We open sourced [ClamAV Java client](https://github.com/solita/clamav-java) 
which implements the absolute minimal Java client for the ClamAV protocol. You don't need to compile the project yourself as we made it available as 
a Maven artifact from Sonatype repository.

In order to set it up as a REST service we need a web server application. A mimimal web application [clamav-rest](https://github.com/solita/clamav-rest) does just that.
With [Spring Boot](http://projects.spring.io/spring-boot/) the code is pretty straightforward and short. It is possible to use it as it is, but it was intended
as an example. 

## A word about Clojure

As the code is Java, it's not difficult to use it from Clojure. For reference, [ClamAV Clojure](https://github.com/Opetushallitus/aitu/blob/master/ttk/src/clj/aitu/integraatio/clamav.clj) should
provide some reference. The REST server of course doesn't care if the client is Java, Clojure or something else.

## Is it any good?

According to [Shadow server statistics](https://www.shadowserver.org/wiki/pmwiki.php/Stats/Viruses) ClamAV has one of the 
best detection rates and beats many commercially available scanners in this regard.

We have deployed the solution we present here for few of our clients last year and everything has been running smoothly,
no problems.

So yeah, this is good in my book.

To test yourself, you can use our [Vagrant configuration](https://github.com/solita/clamav-java/blob/master/vagrant/Vagrantfile) on Github to set up a virtual server. Of course you need [Vagrant](https://www.vagrantup.com/) and [Virtualbox](https://www.virtualbox.org/) to take it for a spin.

