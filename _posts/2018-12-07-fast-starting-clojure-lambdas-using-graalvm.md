---
layout: post
title: Fast starting Clojure AWS Lambdas using GraalVM and a Lambda custom runtime  
author: hjhamala, markkuko
excerpt: Clojure suffers of a slow start-up time which makes using it problematic for APIs running in AWS Lambdas. Compiling Clojure to a native binary using GraalVM and running it in a Lambda custom runtime solves the start-up problem. 
tags:
- AWS
- Clojure
- Serverless 
- Lambda
- GraalVM
---

[**Clojure**](https://clojure.org/) is a dynamic Lisp language which is compiled to JVM bytecode for running as a normal JVM application. Starting a Clojure program is pretty slow compared to many other languages. The start-up takes at least one second but depending on program size this could be almost ten seconds.

**JVM** itself starts [fast](http://clojure-goes-fast.com/blog/clojures-slow-start/) in 50 ms. The slow start-up time is mostly caused by JVM class loading. Unfortunately Clojure generates a lot of classes because every Clojure variable definition and function are compiled to classes. This applies also to anonymous functions which are quite common in Clojure applications. For example a Clojure REST API with 2800 lines of code is compiled to over 200 JVM classes. The start-up time of the program is almost eight seconds when running in MacBook Pro 2017 model. The minimum start-up time of one second or more makes Clojure also a bad choice for command-line tools which are expected to run very fast.

**Lambda** is an AWS serverless technology which lets users to run code without managing servers. Lambdas are paid only for the consumed compute time, which makes them very attractive option for rarely used web applications. Lambdas itself have a start-up time which depends on whether the Lambda instance is _cold_ or _warm_. When a Lambda is used first time or there has been about 15 to 30 minutes between the last Lambda usage it takes about 600 ms to start the Lambda. After that Lambda is _warm_, and subsequent invocations are quite similar compared to applications running in normal virtual machines or containers. Performance of a Lambda depends on the memory allocated for it on creation. More memory gives also more computation time.

The start-up time is not a problem for Lambdas which are run as cron-like tasks, SQS queue pollers or otherwise where there is no need for quick synchronous responses. 

## Clojure running in JVM AWS Lambdas 

Due to the nature of Clojure start-up time, using Lambdas have their penalties. In the next table are statistics for different Hello World applications. Clojure applications are tested with 1000 MB and 3000 MB memory for evaluating its effect on Clojure start-up.  Other runtimes are tested with 1000 MB memory. Tests were made using a consumer broadband located in Finland against the AWS Ireland region (eu-west 2). The latencies could be better with better network and closer distance to the region. Running tests inside AWS region in EC2 virtual machine would give lower network latencies.

| Memory (MB)| Runtime              | N    | Average    | Standard deviation |
| ---------- | -------------------- | ---- | ---------- | ------------------ |          
| 1000       | JVM Java (cold)      | 1000 | 0.585      | 0.108              |
| 1000       | JVM Java (warm)      | 5000 | 0.205      | 0.063              |
| 1000       | JVM Clojure (cold)   | 922  | 2.942      | 0.391              |
| 1000       | JVM Clojure (warm)   | 4600 | 0.237      | 0.133              |
| 3000       | JVM Clojure (cold)   | 1000 | 2.348      | 0.325              |
| 3000       | JVM Clojure (warm)   | 5000 | 0.228      | 0.134              |
| 1000       | Python (cold)        | 1000 | 0.594      | 0.210              |
| 1000       | Python (warm)        | 5000 | 0.358      | 0.074              |                                                                    
                                  
The results are quite problematic for Clojure. Using fastest available Lambda gives a start-up time of 2.34 seconds. A start-up time using 1000 MB Lambda is nearly three seconds. The long start-up time makes Clojure unusable for example outgoing Slack commands which have a timeout of three seconds. Slow start-up is recognized in the Clojure community. Solving it may be partially accomplished with changes to Clojure itself. Fortunately, a new VM has been created with good results for Clojure.  

## A new hope emerges - GraalVM and Lambda custom runtime

This year has given two new releases which make the situation better. First, Oracle released a new [GraalVM universal virtual machine](https://www.graalvm.org/) for running applications written in JavaScript, Python, Ruby, R, JVM-based languages like Java, Scala, Kotlin, Clojure, and LLVM-based languages such as C and C++. GraalVM can ahead-of-time (AOT) compile JVM applications to native binaries which start very fast compared to just-in-time (JIT) compiled programs running in the regular JVM. The memory footprint is also smaller in native images.

Second important release was [custom AWS Lambda Runtimes](https://docs.aws.amazon.com/lambda/latest/dg/runtimes-custom.html) which were introduced in AWS re:Invent 2018. The custom runtimes makes possible to make Lambdas with any technology which can be run on Linux - a support is now available for example Ruby, PHP and Cobol! Before that, supported were JVM, Python, Node.JS, C#, GO and PowerShell. With the custom runtime it is possible to compile Clojure as a native GraalVM binary and run it in AWS Lambda.

A custom runtime API exposes API location via  environment variables. API itself contains three different REST methods for fectching invocations, posting responses and reportin errors. AWS documentation contains a useful tutorial for creating a custom runtime.

## Results using GraalVM

I made a simple custom runtime for running a Clojure program in a custom runtime. Compiling it was quite simple but required using a Docker container because binary must be compiled in Linux environment. Compilation times are  long compared to JVM compilation which must be made before compiling as a native image. The results are described in the next table. 

| Memory | Runtime                     | N    | Average | Standard deviation |
| ------ | --------------------------- | ---- | ------- | ------------------ |          
| 1000   | GraalVM Clojure (cold)      | 1000 | 0.624   | 0.202              |
| 1000   | GraalVM Clojure (warm)      | 5000 | 0.202   | 0.068              |
| 1000   | JVM  Java (cold)            | 1000 | 0.585   | 0.108              |
| 1000   | JVM  Java (warm)            | 5000 | 0.205   | 0.063              |
| 1000   | JVM  Clojure (cold)         | 922  | 2.942   | 0.391              |
| 1000   | JVM  Clojure (warm)         | 4600 | 0.237   | 0.133              |

GraalVM makes Clojure run excellently in the Lambda environment. The cold start time is comparable to regular JVM. A quite interesting result is the warmed performance which is better in GraalVM than in the regular JVM.  

## Limitations of GraalVM

GraalVM have currently some problems compiling native images. For example no instances are allowed in the image heap for a class that is initialized or reinitialized at image runtime. These classes must be given as parameters which is cumbersome. The test program contained SSL libraries which caused compilation problems. Also certain libraries cannot be currently compiled. The Apache HTTP client which is used for example by Clojure Clj-http library is one of them. The compilation problem seems not to be Clojure specific so this should be fixed in the future versions of GraalVM. GraalVM added HTTPS protocol support to native-image in version 1.0.0-rc7, but it still has limitations. First, the provided certificate store has only limited set of CA certificates and second, you must configure path to libsunec.so (Sun Elliptic Curve crypto library). GraalVM tries to load the library from the current directory or from **java.library.path* when its first used. You can workaround these limitations by:

1. Copy or make a symbolic link to the certificate store from, e.g., your distribution's OpenJDK to your GraalVM-installation. The certificate store is usually located in the file *$JDK_HOME/jre/lib/security/cacerts*.
2. Configure path *java.library.path* to include the library *libsunec.so* (in Linux this is in directory *$GRAALVM_HOME/jre/lib/amd64/*) or copy the library file to the working directory).

The runtime performance of the native images is [slightly worse](https://www.graalvm.org/docs/reference-manual/aot-compilation/) than regular JVM HotSpot compiler. This may of course change in the future. GraalVM is still in a release candidate phase for 1.0 version so the situation may change in the future. 

Java HotSpot VM is a battle tested technology compared to GraalVM which is a relatively young invention. What is the stability of GraalVM compared to Java HotSpot VM is not known yet. Also HotSpot is able to aggressively compile most used code paths during runtime compared to GraalVM. Of course this is not a very big advantage for Lambdas which may have relatively young time of life.

## What about ClojureScript?
Instead of using Clojure, we could use ClojureScript which is compiled to JavaScript. This makes possible to run it in the Node.JS runtime. Start up time is quite same than native JavaScript but tooling is currently poorer because traditionally ClojureScript has been targeting the browser environment. If Clojure becomes unviable in AWS perhaps ClojureScript will be Lisp family's choice for cloud native compilation in the future?

## Conclusion 
Lambda and the other serverless technologies are most likely to be very important parts of any software product running in a cloud in the future. To be competitive in an enterprise environment, we must fix Clojure's slow start-up time when running Lambdas. GraalVM seems to fix this by allowing Clojure programs to be compiled to native binaries. The future looks good for Lisp users in the AWS cloud.

Source for tests:
[https://github.com/hjhamala/graalvm-clojure-lambda-tests](https://github.com/hjhamala/graalvm-clojure-lambda-tests)
