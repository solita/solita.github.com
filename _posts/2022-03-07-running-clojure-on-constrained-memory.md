---
layout: post
title: Running Clojure programs on constrained memory
author: joonas.sarajarvi
excerpt: >
  How much main memory is required to run a web service written
  in Clojure? Does choosing a dynamic JVM-based language
  for side projects require a hefty personal IT budget?
  How to find out if your Clojure program is close to running
  out of memory?

tags:
 - Clojure
 - Performance
---

Java and JVM (Java Virtual Machine) have a reputation for being a
platform on which memory-intensive programs are born. This may be
simply attributed to the JVM being a popular runtime environment for
programs that are big in some sense. However, there are some aspects
in common JVM implementations that inherently require some memory. For
example, JIT (just-in-time) compilation requires memory for the
various machine language variants of program parts, and GC (garbage
collection) in general requires space for the garbage, before it is
removed in the next GC run. Perhaps the reputation is not entirely
undeserved.

[Clojure](https://clojure.org/) in turn is a dynamic programming
language, which I have using for back-end programming on the JVM for
the last year or so. I think it is a fun and productive language, but a
dynamic language on top of JVM has potential to exacerbate the memory
intensiveness of the JVM platform. This is not necessarily a problem
for production workloads where it would be common to use a gigabyte or
four of main memory for a compute node. On the other hand, high memory
requirements can be inconvenient for side projects or prototypes that
get deployed on public cloud. In these, it would be common that the
budget for computational resources is either small or non-existent.

My original motivation for exploring this topic comes from the desire
to run a small side project without wasting too much money. At the
moment, even free compute nodes are convenienty available from
[fly.io](https://fly.io/docs/about/pricing/), but only for programs
that can fit into a compute instance equipped with 256 megabytes of
main memory. I wanted to try Clojure for the project, but my initial
impression was that a Clojure program would not easily scale down to
fit these constraints. My colleagues at Solita seemed more confident
that it is at least feasible to run a trivial program, for some value
of *trivial*.

When I tried this out in practice, it kind of turns out that there is
apparently no problem at all in fitting a Clojure program into a 256
megabyte instance, at least for a small service. So in short - if you
are interested in doing that for something non-critical, you might
just go and deploy and not worry about it too much. If the workload is
more essential or if you just wish to dig deeper, the remainder of
this blog entry discusses the metrics I used when making the
conclusion above. It may be worth revisiting the topic any time there
is a change in the workload, to avoid blindly running into trouble.

# Workload and metrics collection

In order to have something simple to experiment with, I wrote a small program
called [sysinfo](https://github.com/muep/clj-sysinfo). It is intended
to be a pretty trivial HTTP service that finds out memory-related
metrics from itself and the surrounding environment. These are available
in JSON form over a simple HTTP interface.
In the end, it grew to be a bit complicated and
messy. I kept adding stuff to check some one more thing, and maybe it
should not all be in the same namespace any more. It should be just fine
for the requirements of this post, even though it is not exactly a
shining example of software architecture.

In addition to the basics of getting and returning metrics, there are
some gratuoitous database parts and a logging framework as well, just
to include a few things that tend to exist in almost every HTTP
service in some form. So in addition to the application code and the
data that is processed, all of these and their dependencies need to be
loaded into the JVM:

- Clojure
- [http-kit](http://http-kit.github.io/) for HTTP service
- [reitit](https://github.com/metosin/reitit) to define endpoints
- [muuntaja](https://github.com/metosin/muuntaja) to coerce responses
- [clojure.java.jdbc](https://github.com/clojure/java.jdbc),
  Postgresql [jdbc driver](https://jdbc.postgresql.org/),
  [hikari-cp](https://github.com/brettwooldridge/HikariCP) for
  database connectivity.
- [logback](https://logback.qos.ch/) to format logs

Using the same tool as the test workload as well as the thing that
collects and reports metrics is not always ideal, but it is quite
convenient to use the same mechanism on the development system
and the cloud system where the tooling otherwise is more constrained.

To demonstrate what `sysinfo` does, here is how the program can be executed:

    $ clojure -M -m sysinfo
    21:00:01.547 [main] INFO  sysinfo - (org.httpkit.server/run-server (app db nil ) {:port 8080} )

There is not much to see in the terminal. When trying out various
settings, that one print about entering `run-server` was useful.
Otherwise it was not always clear if the server managed to load itself
up or if JVM is just stuck running the garbage collector.

The metrics are available on a simple HTTP GET endpoint, that can be
fetched with the venerable [curl](https://curl.se/) tool. for example:

    $ curl -s localhost:8080/sys-summary | jq
    {
      "process-id": 1216441,
      "jvm-nonheap-kib": 41966,
      "jvm-heap": {
        "size-kib": 8134656,
        "used-kib": 57344,
        "utilization": 1
      },
      "cpu-seconds": 5.9,
      "linux-mem-available": "17461600 kB",
      "process-rss-kib": 235752
    }
    $


To make JSON from curl results easier to read, I like piping them
through the [jq](https://stedolan.github.io/jq/) tool. Some examples
may also use it to filter down the result set to make the excerpts
more concise.

The program is not exactly portable. Even if it starts, I would expect the
metrics collection to fail to work on any operating system not based
on Linux. The discussion on virtual memory is also more or less based
on my understanding of Linux.

# Effects of small memory

Limiting the amount of main memory on a system that runs the JVM
has two important consequences that I wish to point out. First, a direct
effect that happens regardless of if our program runs on the JVM or some other
runtime, is that the operating system must provide its services with
less memory. This affects especially the page cache, but it also may result
in swapping-out of memory content. Even in absence swap, heavy filesystem
read load can result from having to reclaim cached-in filesystem content
too soon. Finally, if the memory reclamation mechanisms fail to
otherwise find memory needed for the operating system to operate, it
will be necessary to terminate some memory-intensive process or even
restart the whole system. Both actions are disruptive, but normally we really
want to be way below the level of memory use where the memory
reclamation mechanism becomes inefficient.

The second important effect from a small main memory is the JVM heap
size. To avoid driving the operating system into a memory-starved
state, at least OpenJDK defaults to only using half of the main
memory for its heap. This is a quite sensible default, but it is not
always the best value. The JVM process needs memory for quite a few
things other than just the application heap, so the remaining half may
be insufficient. The operating system might also be running some other
programs that require memory. On the other hand, if the workload of
the operating system is lean
enough, it may be advantageous to use more than half of the main memory
for the JVM heap.

I suppose that most people using JVM-based programming languages are
familiar with the heap size of JVM being manually tunable. On the
other hand, at least I previously had only vague ideas on what exactly I
should pick on a small-memory system. Selecting a small heap will make
it less likely that things apart from the JVM run out of memory, but
it at the very least increases the frequency of GC runs. More
severely, it may also happen that the GC finds nothing to free, not
unlike how the operating system might find itself unable to reclaim
memory. In this case, a new memory allocation inside the JVM likely
throws an
[OutOfMemoryError](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/lang/OutOfMemoryError.html).
This error can in theory be caught and handled, but it difficult to do it
reliably or even figure out a sensible course of action. Doing almost
anything is likely to require further allocations from the heap.

To summarize, it seems that the range of reasonable values for the
heap size is quite large. The low end low end of the range is
constrained at least by the risk of having the program terminate on an
unhandled OutOfMemoryError. On the high end, the constraining factor
is the increasing risk of starving the operating system of available
memory, which also tends to result in some kind of termination of the
program.

# Memory capacity of the operating system

To make it likely that the operating system can provide physical
memory to programs that need it, we need to make sure that either
unused memory or at least easily reclaimable memory is available. For
this, it seems that the `MemAvailable` line in the `/proc/meminfo`
file is a pretty good metric.
[Documentation](https://man7.org/linux/man-pages/man5/proc.5.html)
on the `proc` pseudo-filesystem states that it gives an estimate for
memory that can be used to start new applications. It seems safe to
assume that it is convenient for growing existing ones as well. In addition,
this seems to be exactly what the popular `free` tool from the
[procps](https://gitlab.com/procps-ng/procps) suite uses to produce
its `available` column.

To make it easy to track `MemAvailable`, `sysinfo` collects it and a few other
items from `/proc/meminfo`. In the example above, `MemAvailable` is
produced in the `linux-mem-available` attribute of the response. In
this example, my development system expects to be able to provide 17
gigabytes to some new use.

In this context, the
[RSS](https://en.wikipedia.org/wiki/Resident_set_size) of the JVM
process is also interesting. It is obtained by `sysinfo` from
`/proc/self/stat` and indicates the amount of main memory that the
program is utilizing at present. One reason for my low expectations on
fitting the 256 megabyte target was that the service might utilize 230
megabytes before even performing much useful work. Regardless, it
makes sense to try how it looks in a more constrained environment
where there exists pressure on Linux to reclaim some of this memory
for other purposes.

# JVM heap utilization
One of the things that quite surprised me when digging into this topic
is that Clojure, a multi-threaded HTTP server and a PostgreSQL
connection pool and all that other stuff actually has quite modest
requirements for heap space.

In the example invocation, 57 megabytes of heap space was utilized.
However, most of that memory is simply data that would be cleared out on the
next CG cycle. Because the heap is unnecessarily large by
default on my development system, it takes a long time to reach an
utilization level that would trigger a GC run. This
can be confirmed from the `/sys-stat` endpoint of `sysinfo`, which
compared to `/sys-summary`, provides a larger collection of
metrics.

    $ curl -s localhost:8080/sys-stat|jq .heap.gc
    {
      "g1-young-generation": {
        "count": 2,
        "time": 21
      },
      "g1-old-generation": {
        "count": 0,
        "time": 0
      }
    }
    $

At the moment of checking, the young generation has been collected
just twice, and old generation has not had a single collcetion. One
option in this case would be to programmatically trigger GC runs to
force a minimal heap size. I went for making the heap smaller instead,
because it kind of has the same effect without requiring code
changes.

To get a smaller heap with the `clojure` entry point of Clojure, the
`-Xmx` option to `java` must be passed through the `-J` flag. It looks
a bit funny, but this is one way to start `sysinfo` with a 50 megabyte
heap:

    $ clojure -J-Xmx50m -M -m sysinfo
    22:45:50.614 [main] INFO  sysinfo - (org.httpkit.server/run-server (app db nil ) {:port 8080} )

Let's check the metrics from `sys-summary`:

    $ curl -s localhost:8080/sys-summary | jq
    {
      "process-id": 1237685,
      "jvm-nonheap-kib": 52369,
      "jvm-heap": {
        "size-kib": 51200,
        "used-kib": 18137,
        "utilization": 36
      },
      "cpu-seconds": 7.58,
      "linux-mem-available": "17174460 kB",
      "process-rss-kib": 193084
    }
    $

Compared to the earlier state with a very large heap limit, the heap
is now forced to be actually smaller than what the heap utilization
used to be. Now utilization sits around 18 megabytes, and there is a
bit less than twice that sitting unused. Now just to check if the memory
utilization has a tendency to grow from this and also to get some
performance numbers, let's run the
[drill](https://github.com/fcsonline/drill/) tool with this
configuration:

    concurrency: 40
    base: 'http://localhost:8080'
    iterations: 40000
    rampup: 1

    plan:
      - name: Fetch the current system stat
        request:
          url: '/sys-stat'
      - name: Fetch a historic system stat
        request:
          url: '/sys-stat/1'

This will do 80000 requests in total, in 40 concurrent tasks. Output
from a run after a few warm-up runs looks like this:

    $ drill -b /tmp/benchmark-local.yml -s -q
    Concurrency 40
    Iterations 40000
    Rampup 1
    Base URL http://localhost:8080


    Fetch the current system stat Total requests            40000
    Fetch the current system stat Successful requests       40000
    Fetch the current system stat Failed requests           0
    Fetch the current system stat Median time per request   3ms
    Fetch the current system stat Average time per request  3ms
    Fetch the current system stat Sample standard deviation 1ms

    Fetch a historic system stat Total requests            40000
    Fetch a historic system stat Successful requests       40000
    Fetch a historic system stat Failed requests           0
    Fetch a historic system stat Median time per request   3ms
    Fetch a historic system stat Average time per request  3ms
    Fetch a historic system stat Sample standard deviation 1ms

    Time taken for tests      6.4 seconds
    Total requests            80000
    Successful requests       80000
    Failed requests           0
    Requests per second       12466.48 [#/sec]
    Median time per request   3ms
    Average time per request  3ms
    Sample standard deviation 1ms
    $

At least the application seems to be responding nicely, doing over
10000 requests per second. Also after this, the heap utilization seems
quite similar to the starting state:

    $ curl -s localhost:8080/sys-summary|jq
    {
      "process-id": 1237685,
      "jvm-nonheap-kib": 64656,
      "jvm-heap": {
        "size-kib": 51200,
        "used-kib": 19158,
        "utilization": 38
      },
      "cpu-seconds": 97.32,
      "linux-mem-available": "17140112 kB",
      "process-rss-kib": 255420
    }
    $

Trying out various settings, I was quite surprised that even a pesky
20 megabyte heap would run the program through the same stress test
with drill. After handling 80000 requests, heap utilization sits
around 80 %:

    $ curl -s localhost:8080/sys-summary|jq
    {
      "process-id": 1231485,
      "jvm-nonheap-kib": 64419,
      "jvm-heap": {
        "size-kib": 20480,
        "used-kib": 16409,
        "utilization": 81
      },
      "cpu-seconds": 471.87,
      "linux-mem-available": "17157344 kB",
      "process-rss-kib": 205816
    }
    $

With this quite borderline working heap limit, the heap usage always
seemed to end up around 16 megabytes. It seems safe to assume that the
hard minimum heap size is roughly there, but a practical minimum is
somewhere higher. Even with this 20 megabyte setting, the service only manages to
process roughly 350 requests per second. Compared to the 50 megabyte heap,
the reduction in throughput is about 30-fold. This together with the
high risk of `OutOfMemoryError` sounds like a high price for 30 megabytes
of extra memory.

I kind of like that the likely symptom from a under-sized heap is slow
service, instead of outright interruption of service. The results here
seem especially nice with regards to the defaults on the target
environment, because the program would be getting a heap limit of
around 100 megabytes. There would need to be at least tens of
megabytes of unanticipated demand for heap space, before any issues
should arise.

# Testing on fly.io

As was mentioned in the start of this post, the defaults of OpenJDK
seem sensible and `sysinfo` should be just fine with a 100-ish
megabyte heap. It is not immediately clear if the remaining half of
main memory will be sufficient for needs of the rest of the JVM and
also the Linux-based operating system, but I think it was simplest to
just try this out directly on fly.io.

While fly.io uses a full virtualization mechanism called
[Firecracker](https://firecracker-microvm.github.io/), the deployment
is still based on OCI container images. This means that there is quite
a lot of freedom on what to use for the Java runtime or other aspects
of the environment. The setup tested here is what I would expect to be
a typical way to deploy a Clojure program. Both `sysinfo` and its
dependencies are packed into a single 18 megabyte jar file with the
[uberdeps](https://github.com/tonsky/uberdeps) tool, and this jar file
is then stacked on top of a standard OpenJDK 11 base image:

    FROM openjdk:11
    COPY clj-sysinfo.jar /
    CMD ["java", "-jar", "clj-sysinfo.jar"]

After the resulting image is built and deployed on fly.io, it is a bit
tricky to fully pre-warm the JVM.  Again I used `drill` for this, but
it takes a somewhat long time due to the larger latency and my
unwillingess to place hundreds of concurrent requests between myself
and the compute instance in Frankfurt. Regardless, eventually the
instance has processed a few tens of thousands of requests, and it
should be safe to assume that at least most of the JIT compilation and
other warming-up has happened. In this state, the response
from the `sys-summary` endpoint looks like this:


    {
      "process-id": 515,
      "jvm-nonheap-kib": 56137,
      "jvm-heap": {
        "size-kib": 110912,
        "used-kib": 19282,
        "utilization": 18
      },
      "cpu-seconds": 181.55,
      "linux-mem-available": "76104 kB",
      "process-rss-kib": 151896
    }

The numbers that interest me here are the ones in `process-rss-kib`
and `linux-mem-available`. Based on the RSS reading of 151896
kibibytes, it seems that the JVM process is utilizing quite a sizeable
share of the 226472 kibibytes of memory that the kernel reports as the
total memory size on a 256 MB fly.io instance. Roughly 76 megabytes is
still reported as *available*, which sounds like plenty of space for
any newly introduced demand for physical memory. It is also nice to
see that the program that took 230 megabytes on my large system, will
utilize quite a bit less on a small one.

Without studying further, it seems a bit risky that
`linux-mem-available` is a quantity smaller than the amount of unused
heap space. With a smaller heap utilization level, a lot of it is
likely not mapped into physical memory. Then if the program happens to
need most of the space at some, it might end up starving the operating
system. As the amount of unused heap capacity is quite a bit larger
than I expect to need, it would seem more robust to perhaps limit the
heap size to 50 megabytes, so it is easier to predict what happens if
the program in some circumstances exceeds the expected level memory of
memory utilization. For my side projects, I think I will just stick
with the defaults and see if I actually ever hit a problem with the OS
running out available memory.

It seems that compared to the generic performance metrics that cloud
providers offer, one gets much better visibility if one queries the
kernel and the JVM directly for their memory utilization. The stock
monitoring tools on cloud do not typically see inside the JVM at all,
and fly.io for example would usually simply display that almost all
of the main memory is utilized.

# Interpreted mode

I did try tweaking many JVM tunables to see how small an RSS `sysinfo`
could have. I got early versions with fewer features running at below
64 megabytes, but there was little reason to artificially limit the
size below what it easily available. Limiting the number of threads or
really minimizing the heap size have quite lousy returns in memory
capacity, compared to the hit on performance and reliability that they
have.

The one thing of these attempts that I feel like recommending is to
turn off the JIT compiler infrastructure and run the JVM in
interpreter-only mode. The `-Xint` option does just that. This will
also naturally come with a pretty performance penalty, but at least it
is simple and the effect on memory use is measured in tens of
megabytes. Let's just try this in the `Dockerfile`:

    FROM openjdk:11
    COPY clj-sysinfo.jar /
    CMD ["java", "-Xint", "-jar", "clj-sysinfo.jar"]

With this deployed on fly.io, the `sys-summary` looks like this:

    {
      "process-id": 515,
      "jvm-nonheap-kib": 34863,
      "jvm-heap": {
        "size-kib": 110912,
        "used-kib": 21509,
        "utilization": 20
      },
      "cpu-seconds": 114.8,
      "linux-mem-available": "128648 kB",
      "process-rss-kib": 101308
    }

Heap use is again quite similar to the previous case. I did not do
thorough testing on it, but in my testing this seems to reduce the
throughput by a factor somewhere between 5 and 10. The memory headroom
certainly does not come free, but this might be a useful option for
some low-traffic thing that otherwise would not fit.

# Conclusion

Based on this anecdotal case, I think that a 256 megabyte
compute node should be able to run small Clojure service quite acceptably.
If in doubt, set up the service and then monitor the utilization of
the JVM heap and the memory stats from the operating system.

The defaults in the OpenJDK JVM are reasonably good. With my particular
workload, it might be slightly more ideal to reduce the heap limit.
Finding out a more optimized size would require more studying. Maybe the
program could be altered so that some endpoint would allow the caller
to effect how memory intensive it is to serve the request. Then various
tunables could be changed to find settings that maximize the "size" of the
request that can be handled.

From this exercise, I got a good refresh on my assumptions on memory
requirements of Clojure. Hopefully this encourages others to check
their assumptions as well. Especially for non-critical workloads
running on pay-as-you-go cloud infrastructure, use of smaller
computational resources can save some money every month. On top of
this, it seems safe to assume that small instances in general have
small environmental footprints as well.
