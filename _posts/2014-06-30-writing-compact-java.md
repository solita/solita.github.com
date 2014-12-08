---
layout: post
title: Writing Compact Java with functions and data
author: pvto
excerpt: Rethinking stylistic issues could help us in dealing with complex problems. Computation is not all about ownership.
---


In this post I reiterate some well-known ways to shorten [Java](http://www.oracle.com/technetwork/java/index.html) source code and to make it more readable.

Motivation for this is an observation that style is fun.  Rethinking stylistic issues could help in dealing with complex problems.  This is to provide for the future, while computation, after all, is not all about ownership.


##Index is structure
![Index is structure](/img/index-is-structure.png)

Creating complex structures, maps, or lists of objects, may be verbose or semi-fluent in Java.  To forestall needless new code, big constructors, [builders](http://en.wikipedia.org/wiki/Builder_pattern) and whatnots, code should use built in data structures cleverly.  One such pattern is a plain array and a loop over it, allowing the data itself be laid out pleasantly.

{% highlight java %}
    Object[] templ = new Object[] {
        // id   name  next
        1, "x", 2
        2, "y", 4
        3, "z", 5
    };
    for(int i = 0; i < templ.length(); ) {
        list.add(new MyThing((int)templ[i++], 
            new NameEntity((String)templ[i++]), (int)templ[i++])));
    }
{% endhighlight %}

I have restricted the hard-to-read part of code to minimum, giving reader possibility to focus on the data and its internal relations.  This will be useful especially when the amount of structural data within the program increases.

##Instance initialisers

A [block](http://docs.oracle.com/javase/specs/jls/se8/html/jls-14.html#jls-14.2), in a simple sense, means some lines of Java statements surrounded by { }.

{% highlight java %}
    {
        int precious = 1;
        // . . .
    }
{% endhighlight %}

[An instance initialiser](http://docs.oracle.com/javase/specs/jls/se8/html/jls-8.html#jls-8.6) then is a block that is executed once per the lifetime of a java object.

{% highlight java %}
    class InIn {

        MyThing myt = new MyThing();

        {
            myt.id = 1;
            myt.name = "example";
        }
    }
{% endhighlight %}

Statements within the { } block are executed while an InIn is constructed, after the instantiation of the preceding list and before any constructor-methods.  Notice how from reading this piece of code it is obvious what MyThing is parameterised with. The reader/maintainer does not have to remember a constructor signature to intuitively understand what happens, and we avoided creating two non-default constructors, those of InIn and MyThing.

Such an instance initialiser block does look a bit lonely, but then it could alleviate us from extensive [constructor overloading](http://docs.oracle.com/javase/specs/jls/se8/html/jls-8.html#jls-8.8.8) or other contagious aesthetic maladies.  This I'll cover with another example later on.

However this pattern may lead to code deterioration in certain cases; keep in mind as always that a stylistic choice should lead to improved code clarity.

![Scissors](/img/scissors.png)
##Remove unnecessary getters

Getters may be required by frameworks like EJB and Spring, but otherwise they are seldom necessary.  Especially getter-less data classes are more concise and more beautiful than getter-ified ones.

##Template data classing

{% highlight java %}
    class Node {
        int how = 1, why = 2;
        List<Node> children;
    }
    static class Node0 extends Node { {how = 0; } }
{% endhighlight %}

In the above example we have a class that is used, say, in a traversable tree structure.  The *Node0* subclass then is static and therefore there is no extra complexity in its construction or garbage collection.

The field *how*, however, would be set twice, first to *1* and then to *0*.  Implicit superclass constructor always gets the first take.  So we could omit variable initialisation in the super class.  Depending on your JVM, your [JIT](http://www.javaworld.com/article/2078635/enterprise-middleware/jvm-performance-optimization--part-2--compilers.html) could do this optimisation for you.


##... with a dynamic subclass (double brace initialisation)

If our object is constructed infrequently, we could use a dynamic subclass, along with a [double brace initialisation pattern](http://www.ayp-sd.blogspot.fi/2012/12/double-brace-initialization-in-java.html) which is somewhat infamous.  Beware of any implicit references that would prevent garbage collection of such an object, so mix this with builders or other inner classes only if you understand everything.

{% highlight java %}
    final int myValue = 1;
    Node dyn = new Node(){ {how = myValue;} }
{% endhighlight %}


##Methods away
![do](/img/do.png)

If we operate on data types that are not overtly specialised, it is extremely fast to accumulate common behaviors into helper methods, and using them will be a whiz.  This is a philosophy behind [Python](https://www.python.org/), [R](http://www.r-project.org/), [Matlab](http://www.mathworks.se/products/matlab/) and other environments that were designed for scientific use:  they offer easy access to computation, and undermine the notion and value of class structure per se.  One interesting asset is that the simpler structures you use, the more portable your computations become.  (Consider the [Rootbeer project](https://github.com/pcpratts/rootbeer1).)

Here are two examples in Java (a bad and a good one).

{% highlight java %}
    class NaughtyComputer {
        int age;
        static int sumAge(List<NaughtyComputer> list) {
            int sum = 0;            
            for { . . . }            
            return sum;
        }
    }
{% endhighlight %}

{% highlight java %}
    class DeNaughtifiedComputer {
        int age;
    }
    static Iterable<Integer> extractAge(Iterable<DeNaughtifiedComputer> list) { 
        . . .
    }
    static int sum(Iterable<Integer> list) { . . . }

{% endhighlight %}

In Java 8, we could do without extractAge(), with a little lambda syntax and Java's built in map/reduce facilities.

{% highlight java %}
    int summedAge = list
        .stream()
        .map(DeNaughtifiedComputer::age)
        .sum();
{% endhighlight %}

##Wielding asynchronous data classes

If you need to manipulate data from multiple threads, (a pattern that should be built on very sparingly), consider these options.

* [AtomicReference](http://docs.oracle.com/javase/8/docs/api/java/util/concurrent/atomic/AtomicReference.html) and primitive datatype atomics [there](http://docs.oracle.com/javase/8/docs/api/java/util/concurrent/atomic/package-frame.html).  These are classes for which [atomicity of operations](http://en.wikipedia.org/wiki/Atomicity_(programming)) is guaranteed.
* on Java8, [StampedLock](http://docs.oracle.com/javase/8/docs/api/java/util/concurrent/locks/StampedLock.html) for fast, advanced locking behaviors

The easiest way to prevent stale reads from memory, while these preceding options may or may not yield some performance benefits over it, is

* [volatile](http://docs.oracle.com/javase/specs/jls/se8/html/jls-8.html#jls-8.3.1.4). 

{% highlight java %}
    class SyncedNode {
        volatile SyncedNode nextNode;   
        Object content;
    }
{% endhighlight %}

*Volatile* dictates that your JVM will enforce the order of access to marked fields.  In other words it is a bit like *synchronized* for fields in Java and ensures you will not read a stale value.

If you *absolutely* need to implement complex stateful behaviour that references an object, you should synchronise over the object itself in all client code, like this.

{% highlight java %}
    class ComplexNode {
        int unsafe1, unsafe2;
    }
    // . . .
    new Thread(new Runnable() {  public void run() {
        ComplexNode node = ...;
        synchronized(node) {
            if (node.unsafe1 == 1) {
                node.unsafe1 = 2;            
                node.unsafe2 = 3;
            }
        }
    }});
{% endhighlight %}
If we are uncertain of over what to synchronise, our program is likely to break, so it is good to keep to simple and thoroughly understood behaviours while we process data.

![note](/img/note.png)

In finis, to summarise: it may pay to avoid any interfering idioms that boldly stand between a need and a clear solution.  This post provided assorted ideas for that end.  Resulting compact patterning will render Java an ok language.  And while correctness and readability are necessary aspects of good code, fit and skinny structuring will assist us to get there.

As a bonus, here are some excellent background reads on Java: [Josh Bloch's Effective Java](http://www.amazon.com/Effective-Java-Edition-Joshua-Bloch/dp/0321356683/ref=sr_1_1?ie=UTF8&qid=1403521178&sr=8-1&keywords=josh+bloch) and [Java puzzlers](http://www.amazon.com/Java%C2%BF-Puzzlers-Traps-Pitfalls-Corner/dp/032133678X/ref=sr_1_2?ie=UTF8&qid=1403521213&sr=8-2&keywords=josh+bloch); Brian Goetz' [Java Concurrency in Practice](http://www.amazon.com/Java-Concurrency-Practice-Brian-Goetz/dp/0321349601/ref=sr_1_1?s=books&ie=UTF8&qid=1403521289&sr=1-1&keywords=java+concurrency+in+practice).
