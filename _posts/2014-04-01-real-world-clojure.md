---
layout: post
title: Real World Clojure
author: lokori
excerpt: You may have heard already that Clojure is great and going to dominate the world this year. But will it? In this article I will dig deep into one of our Clojure projects so that you can see what a real world Clojure project looks like and decide for yourself.
---


You may have heard already that Clojure is great and going to dominate the world this year.
But will it? In this article I will dig deeply into one of our Clojure projects so that you can 
see what a real world Clojure project looks like and decide for yourself. I will try to offer as objective a view on the matter as I can.  

This is not a huge project, but not a trivial example either. Our software, Aitu, is a 
practical and pretty straightforward web project. You can view the full source code 
as [Aitu lives in Github](https://github.com/Opetushallitus/aitu). In addition to 
actual web software there are database configurations etc. so you can set it up in a matter of minutes with
the help of [Vagrant](http://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/) should you want
to play with it.


## Clojure programmers are happier 

There are a number of things that are different with Clojure that don't directly affect
the code, but greatly improve the efficiency of a seasoned programmer's workflow. 
Programming feels good because there are benefits such as:

  * [REPL](http://en.wikipedia.org/wiki/REPL) workflow has been [covered already](http://dev.solita.fi/2014/03/18/pimp-my-repl.html). 
  * [Leiningen](http://leiningen.org/) is doing it right while [Maven is doing it wrong](http://nealford.com/memeagora/2013/01/22/why_everyone_eventually_hates_maven.html). 
  * [Clojars](https://clojars.org/) is great.
  * Clojure is [homoiconic](http://en.wikipedia.org/wiki/Homoiconicity). You'll learn to appreciate this.
  * [edn](https://github.com/edn-format/edn) + REPL + immutability lead to very efficient handling of test data
  
In general I consider the Clojure community as one of the finest programming language communities. 
The libraries are of high quality and the attitude is to do things properly. Libraries and 
frameworks are focused and modular. This is no small feat. Being able to trust and understand
third party libraries makes programming in Clojure feel good.

## Clojure takes on PostgreSQL

Currently there is no established de facto library for relational database access. There is the
[clj-jdbc](http://niwibe.github.io/clj.jdbc/) wrapper for low level needs, but higher level abstractions are still under construction. In September 
we chose to use [SQL Korma](http://sqlkorma.com/) for our project.

It has turned out to be somewhat frustrating. We are still using Korma, but there are some issues:

 * [Multiple foreign keys are not supported](https://github.com/korma/Korma/pull/182) at the moment.
 * Jodatime wrappers are missing. Everyone reinvents the wheel as [we did](https://github.com/Opetushallitus/aitu/blob/master/ttk/src/clj/aitu/integraatio/sql/korma.clj).
 * Korma's preferred connection pool, C3P0 has some bugs. Like, [infinite recursion](http://sourceforge.net/p/c3p0/bugs/100/).
 * Korma's default settings for C3P0 are not suitable for real work. Infinite timeout on connection checkout is not nice.
 * At the moment, [Korma uses a deprecated version of clj-jdbc](https://github.com/korma/Korma/issues/207).

Still, Korma is better than nothing and the source code is reasonable. We have read it through a couple of times.

## Testing with Clojure

A lot could be said about testing in Clojure, but I'll skip the obvious and cover some things which I consider to be particularly interesting. 
Clojure tests don't really need additional "testing frameworks" as the language ships with enough power to take on any
other programming language. 

### Still doing assertions?  

There is proper support for [design by contract](http://en.wikipedia.org/wiki/Design_by_contract) with preconditions and postconditions. 
As an abstraction postconditions and preconditions are an order of magnitude more powerful than old school assertions. You certainly can still 
write on occasional assertion, but there is no state which you would check with assert in OOP and imperative programming.

### Dissect your source code, I dare you

However, if you make a small mistake in your syntax with preconditions, there will not be any compiler warning. This is unfortunate and may change in some future
version of Clojure. For the meantime, we wrote a separate test to ensure that
our postconditions and preconditions are actually used as the programmer has intended. 
Full [source_test.clj](https://github.com/Opetushallitus/aitu/blob/master/ttk/test/clj/aitu/source_test.clj) contains util functions
omitted here. The code here has been translated to english.

	(defn pre-post [form]
		(when (= 'defn (nth form 0))
			(some #(and (map? %)
				(or (contains? % :pre)
                    (contains? % :post))
                %)
          form)))

	(defn pre-post-in-wrong-place? [form]
		(when-let [pp (pre-post form)]
      		(not (or (and (symbol? (nth form 1))
            	      (vector? (nth form 2))
            	      (= pp (nth form 3)))
            	 (and (symbol? (nth form 1))
                	  (string? (nth form 2))
                 	 (vector? (nth form 3))
                 	 (= pp (nth form 4)))))))

	(defn pre-post-not-vector? [form]
    	(when-let [pp (pre-post form)]
      		(not (every? vector? (vals pp)))))
 

	(deftest pre-post-at-right-place-test
    	(is (empty? (matching-forms "src/clj" pre-post-in-wrong-place?))))

	(deftest pre-post-vector-test
    	(is (empty? (matching-forms "src/clj" pre-post-not-vector?))))

This code takes advantage of homoiconocity and [Clojure's reader](http://clojure.org/reader). The source code is parsed by
the reader, and our test examines it. We are using basic data structures and standard algorithm predicates like `when`, 
`some` and `map`. On the other hand, we are searching for the Clojure code structure `defn` which is used to define a function. **This
sort of test would be extremely difficult to do in almost any other language**. 

## Static checking with steroids

This approach can be applied to many other static checks. Clojure is intentionally built with dynamic typing, but
writing your own static checks is quite easy when you need them. You need custom static checks in any case because
type systems in general are limited. Even Haskell will not tell you if you accidentally messed up the encoding
of a properties file. But it's not difficult to check:

	(deftest properties-encoding-test
  		"Find characters which are not 'printable characters'. There shouldn't be any."
  		(is (empty? (matching-lines "resources/i18n"
    	                   			#".*\.properties"
                          			[#"[^\p{Print}\p{Space}]+"]))))

We rely on a generic function which recursively iterates over the files matching the directory and name pattern (here, i18n properties files) and matches each line in each file 
with some regular expression. In this case we search for unprintable characters. One could argue that it's easy to write this in Java. Having done that, I consider
Clojure a much more efficient tool in this respect.

In our project we have not written pre-emptive checks for all imaginable scenarios, but rather followed the Lean path of [poka-yoke](http://en.wikipedia.org/wiki/Poka-yoke). After one of us messed up the encoding, I
wrote that test to make sure it doesn't happen again. The temptation to cut corners is smaller when **the language empowers the programmer** and **enables doing the right thing**.


## Isolating for maximum gain

Due to it's functional nature, Clojure is great at isolating things. Since there is no state, almost anything
can be tested with a unit test. This doesn't mean that every single function should have a unit test,
but rather that any important function can always be isolated for testing.

Even functions with side effects can be tested relatively easily. Consider this [auditlog test](https://github.com/Opetushallitus/aitu/blob/master/ttk/test/clj/aitu/auditlog_test.clj).

The actual test looks pretty straightforward (code translated to english):

	(deftest test-contract-update
    	(testing "logs properly an update to a contract"
      	(log-validate
       		 #(auditlog/contract-update! 123 "12/12")
       	 	[[:info "uid: T-X oper: update target: contract meta: ({:contractid 123, :diaryidentifier \"12/12\"})"]])))

With a few lines of code I set up a mock to capture the logging output in a non-intrusive manner, mock
the authentication framework and test that the piece of code responsible for formatting the audit log messages works.
The test checks these things:

1. The audit log formatter calls the logging framework with properly formatted messages.
2. It properly attaches the "current user" id to the log messages. 

No need to start up and configure services and [figure out a way to create a test application context](http://stackoverflow.com/questions/10104372/testing-with-spring-and-maven-applicationcontext). Just write the test for
whatever piece of code you wish to test.

## Play it again, Sam?

To put it bluntly, yes. I would still prefer to write this application in Clojure if I could go back in time with the information I
have now. I do believe this would be in the best interest of our client as well.  

To summarize, here's my current advice for crafting a "professional" Clojure application:

  * Use [component](https://github.com/stuartsierra/component) or something like that to manage application life cycle.
  * Use [schema](https://github.com/prismatic/schema) or something similar to define important interfaces through the data structures
  * Use Korma or something else, but be wary when combining Clojure and relational databases.
  * Take full advantage of Clojure's special strengths. Otherwise, what's the point? 
  * Avoid macro wankery. Macros offer [Turing complete power](http://en.wikipedia.org/wiki/Turing_completeness) and should be used sparingly.
  * [Apply dynamic binding thoughtfully](http://cemerick.com/2009/11/03/be-mindful-of-clojures-binding/). Dynamic variables scattered around the code are antithesis of Clojure's principles. 
  * Be critical about book examples. They leave out "details" which turn out to be important.
  * Be prepared to add functionality to libraries. We had to write [HTTP logging middleware](https://github.com/Opetushallitus/aitu/blob/master/ttk/src/clj/aitu/infra/print_wrapper.clj) though it's a pretty obvious feature.
  * Java interop is great, but keep it simple. Generating Java classes with [gen-class](http://clojuredocs.org/clojure_core/clojure.core/gen-class) was painful. [reify](http://clojuredocs.org/clojure_core/clojure.core/reify) was easy.

### The final verdict

Clojure is still an infant taking it's first steps in the world of Real Applications. This is evident as some popular libraries are lacking
essential functionality. But as a language it is mature and stable. The language has deep roots and powerful ideas backing it up. A fine 
community is growing daily. The [world domination](http://dev.solita.fi/2013/09/04/about-languages.html) is commencing.
