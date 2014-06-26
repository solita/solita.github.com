---
layout: post
title: Writing Compact Java: working with functions and data
author: pvto
excerpt: Rethinking stylistic issues could help us in dealing with complex problems, while computation, after all, is not all about ownership.
---


In this post I reiterate some well-known things to shorten [Java](http://www.oracle.com/technetwork/java/index.html) source code and to make it more readable.

Motivation for this is an observation that style is fun.  Rethinking stylistic issues could also help in dealing with complex problems.  This is to provide for the future.  And computation, after all, is not all about ownership.


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
    for(int i = 0; i &lt; template.length(); ) {
        list.add(new MyThing((int)templ[i++], (String)templ[i++], (int)templ[i++]));
    }
{% endhighlight %}


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

        List list = new LinkedList();

        {
            list.add(1);            list.add(2);
        }
        public InIn() { list = immutableList(list); }
    }
{% endhighlight %}

Those two list.add() statements within a { } block are executed while an InIn is constructed, after the instantiation of the preceding list and before any constructor-methods.

Such a block does look a bit lonely, but then it could alleviate us from extensive [constructor overloading](http://docs.oracle.com/javase/specs/jls/se8/html/jls-8.html#jls-8.8.8) or other contagious aesthetic maladies.  This I'll cover with another example later on.

![Scissors](/img/scissors.png)
##Remove unnecessary getters

Getters may be required by frameworks like EJB and Spring, but otherwise they are seldom necessary.  Especially getter-less data classes are more conscise and more beautiful than getter-ified ones.

##Template data classing

{% highlight java %}
    class Node {
        int how = 1, why = 2;
        List&lt;Node&gt; children;
    }
    static class Node0 extends Node {{how = 0;}}
{% endhighlight %}

In the above example we have a class that is used, say, in a traversable tree structure.  The *Node0* subclass then is static and therefore there is no extra [performance penalty]() in its construction.

The field *how*, however, would be set twice, first to *1* and then to *0*.  Implicit superclass constructor always gets the first take.  So we could omit variable initialisation in the super class.


##... with a dynamic subclass (double brace initialization)

If your object is construed infrequently, you could use a dynamic subclass, along with a [double brace initialization pattern](http://www.ayp-sd.blogspot.fi/2012/12/double-brace-initialization-in-java.html) which is somewhat infamous.  Beware of any implicit references that would prevent garbage collection of such an object – mix this with builders or other inner classes only if you understand everything.

{% highlight java %}
    final int myValue = 1;
    Node dyn = new Node(){{how = myValue;}}
    // . . .  
{% endhighlight %}


##Methods away
![do](/img/do.png)

If you operate on data types that are not overtly specialized, it is extremely fast to accumulate common behaviors into helper methods, and using them will be a whiz.  This is a philosophy behind [Python](https://www.python.org/), [R](http://www.r-project.org/), [Matlab](http://www.mathworks.se/products/matlab/) and other environments that were designed for scientific use:  they offer easy access to computation, and undermine the notion and value of class structure per se.  One interesting asset is that the simpler structures you use, the more portable your computations become.  (Consider the [Rootbeer project](https://github.com/pcpratts/rootbeer1).)

Here are two examples in Java (a bad and a good one).

{% highlight java %}
    class NaughtyComputer {
        int age;
        static int sumAge(List&lt;NaughtyComputer&gt; list) {
            int sum = 0;            for { . . . }            return sum;
        }
    }
{% endhighlight %}

{% highlight java %}
    class DeNaughtifiedComputer {
        int age;
    }
    static List&lt;Integer&gt; extractAge(List&lt;DeNaughtifiedComputer&gt; list) { 
        List&lt;Integer&gt; list = new ArrayList&lt;&gt;(list.size());
        for { . . . }
        return list;
    }
    static int sum(List&lt;Integer&gt; list) { . . . }

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

If you *absolutely* need to implement complex stateful behaviour that references an object, you should synchronize over the object itself in all client code, like this.

{% highlight java %}
    class ComplexNode {
        int unsafe1, unsafe2;
    }
    // . . .
    new Thread(new Runnable() {  public void run() {
        ComplexNode node;
        synchronized(node) {
            if (node.unsafe1 == 1) {
                node.unsafe1 = 2;            node.unsafe2 = 3;
            }
        }
    }});
{% endhighlight %}

If we are uncertain of over what to synchronize, our program is likely to break, so it is good to keep to simple and thoroughly understood behaviours while we process data.

![note](/img/note.png)

In finis, to summarize: it may pay to avoid any interfering idioms.  This post provided assorted ideas for that end.  Resulting compact patterning will render Java an ok language.  And while correctness and readability are necessary aspects of good code, fit and skinny structuring will assist us to get there.

As a bonus, here are some excellent background reads on Java: [Josh Bloch's Effective Java](http://www.amazon.com/Effective-Java-Edition-Joshua-Bloch/dp/0321356683/ref=sr_1_1?ie=UTF8&qid=1403521178&sr=8-1&keywords=josh+bloch) and [Java puzzlers](http://www.amazon.com/Java%C2%BF-Puzzlers-Traps-Pitfalls-Corner/dp/032133678X/ref=sr_1_2?ie=UTF8&qid=1403521213&sr=8-2&keywords=josh+bloch); Brian Goetz' [Java Concurrency in Practice](http://www.amazon.com/Java-Concurrency-Practice-Brian-Goetz/dp/0321349601/ref=sr_1_1?s=books&ie=UTF8&qid=1403521289&sr=1-1&keywords=java+concurrency+in+practice).
