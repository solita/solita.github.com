---
layout: post
title: "Need for Speed, or: What Is (Probably) Coming to the Java VM in a Few Years"
author: orfjackal
excerpt: There are a bunch of improvements that are currently being investigated for the Java VM and language. Most of them won't make it into Java 9, but maybe a couple of years later we can enjoy them.
---

Though people are still migrating to Java 8, there are already many new developments for future Java versions. Especially keep an eye out for the vikings in [Project Valhalla](http://mail.openjdk.java.net/pipermail/valhalla-dev/2014-July/000000.html) who are experimenting with a bunch of interesting improvements to both the Java VM and language, such as Value Types and Generics Specialization.

This article lists some features that you can expect to be added into Java in a few years. Let's start with some smaller updates that will probably make it into Java 9, and then move on to the bigger changes which may come later.


![](/img/what-is-coming-to-java-vm/memory.jpg =300x)


## Java Memory Model Update ([JEP 188](http://openjdk.java.net/jeps/188))

There are plans under way for [improving the Java Memory Model](http://shipilev.net/blog/2014/jmm-pragmatics/) (JMM), which was last revised in Java 5. The improved JMM is currently being targeted for Java 9.

The goal of this JEP is to improve the JMM specification and cover concurrency primitives that have been added since Java 5. It may also pave the way for tools to automatically check for race conditions, though creating such tools is outside the scope of this JEP.

But more interesting for developers are some other JMM related changes that are currently being investigated:


### All Accesses Are Atomic

In the current JMM, writing a `long` or `double` field may happen in two steps, so that other threads may observe transient values where only 32 of the 64 bits have changed (depending on the CPU). The current solution is to mark the field `volatile`, but that imposes memory barriers on the field, which makes it slower.

The article [All Accesses Are Atomic](http://shipilev.net/blog/2014/all-accesses-are-atomic/) tells about the investigation of giving atomicity guarantees also to non-volatile fields. If it doesn't incur too much overhead, that change will probably be included in the new JMM.


### All Fields Are Final

The current JMM provides some additional guarantees for final fields - after constructing an object, other threads are guaranteed to see it fully initialized (unless a reference to `this` is leaked inside the constructor). This is enforced (on CPUs that need it) by having a memory barrier at the end of the constructor.

The article [All Fields Are Final](http://shipilev.net/blog/2014/all-fields-are-final/) tells about the investigation of giving the same visibility guarantee to all objects. This way an object that doesn't have final fields, but is not modified after constructing it, will behave from the JMM's point of view in the same way as a similar object where all fields are final. Early benchmarks show the overhead to be bearable, so this may also be included in the new JMM.

P.S. If you read the previous articles or [other articles](http://shipilev.net/) on the same site, you might have noticed some handy new tools for benchmarking and analyzing performance: [JMH](http://openjdk.java.net/projects/code-tools/jmh/) and [JOL](http://openjdk.java.net/projects/code-tools/jol/).


![](/img/what-is-coming-to-java-vm/vikings.jpg =300x)


## Enhanced Volatiles ([JEP 193](http://openjdk.java.net/jeps/193))

Related to the JMM, though part of Project Valhalla, this proposal aims to give `volatile` fields the same operations as `AtomicInteger` et al. by adding some new syntax to the Java language. This will help to avoid the overhead of the atomic wrapper classes, while being safer and easier than using the `Unsafe` class for those operations.


## Value Types ([JEP 169](http://openjdk.java.net/jeps/169))

This might be the biggest addition to the Java VM *ever*. Currently Java has a predefined set of primitive types which are passed by value, and everything else is objects which are passed by reference.

The goal of the [Value Types proposal](http://cr.openjdk.java.net/~jrose/values/values-0.html) to support small immutable, identityless *value types* which will "code like a class, work like an int." This is primarily a performance improvement: the value types have no object header and they avoid the indirection of object references, thus improving memory use and cache locality. Arrays of value types will be supported. To understand why this is a big deal for performance, read [What Every Programmer Should Know About Memory](http://www.akkadia.org/drepper/cpumemory.pdf). It may also let Java programs take advantage of modern CPUs' native data types and e.g. vector instructions.

This will let developers to write small classes (e.g. a complex number) which will have the same performance as primitives, but can be used like objects (i.e. they have methods and encapsulation). The existing primitive types may be retrofitted to be value types, in which case it might be possible to call methods on them (many of the methods in their [wrapper classes](http://docs.oracle.com/javase/8/docs/api/java/lang/Integer.html) are good candidates).


## Generics Specialization ([JEP draft](http://openjdk.java.net/jeps/8046267))

Java's generics don't currently work with primitives - all primitives must be wrapped into objects before they can be e.g. added into a `java.util.List`. Some other languages, such as Scala and C#, support [specialization of generic classes](http://www.scala-notes.org/2011/04/specializing-for-primitive-types/).

The goal of the [Specialization proposal](http://cr.openjdk.java.net/~briangoetz/valhalla/specialization.html) is to extend generics to support primitive type arguments. This will make it possible to create a `List<int>` where no boxing and unboxing of primitives will be required, because the class will contain an `int[]` instead of an `Object[]` and the methods will also take the primitive as a parameter.

This will nicely complement the value types proposal.


## Arrays 2.0

Currently Java's arrays are limited to the size of `int`, multi-dimensional arrays are implemented as nested one-dimensional arrays (which harms cache locality), they cannot be resized, their elements cannot be `volatile` etc.

There is a [proposal for improved Java arrays](http://cr.openjdk.java.net/~jrose/pres/201207-Arrays-2.pdf) that would allow developers to create custom array types. For example it would be possible to customize the width and number of indexes (e.g. `array[i,j,k]`), even the *type* of index (making it more like a `Map`). Basically the proposal suggests that custom collections can be used with the same syntax as arrays. Even at the bytecode level, array specific instructions (`arraylength`, `aaload`, `iastore` etc.) will be interpreted as normal `invokevirtual` calls.


![](/img/what-is-coming-to-java-vm/panama.jpg =400x)  
[<small>Panama Canal by Roger Wollstadt</small>](http://www.flickr.com/photos/24736216@N07/3166075815/)


## Foreign Function Interface ([JEP 191](http://openjdk.java.net/jeps/191))

JNI has been the only way to interface between Java and native code libraries, but JNI is painful to use and has poor performance.

The goal of [Project Panama](https://blogs.oracle.com/jrose/entry/the_isthmus_in_the_vm) is to provide a built-in FFI API at the JDK level, which would be easier and safer for Java developers to write. It will likely be based on the [Java Native Runtime (JNR)](http://www.oracle.com/technetwork/java/jvmls2013nutter-2013526.pdf), but with better JVM support to avoid the JNI overhead.
