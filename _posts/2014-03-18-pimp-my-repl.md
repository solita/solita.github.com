---
layout: post
title: Pimp My REPL
author: noidi
excerpt: Everyone knows Lisp programmers live in the REPL, and Clojurians are no exception. This is a tour of Clojure libraries and practices that make life in the REPL even more comfortable.
---

Everyone knows Lisp programmers live in the [REPL](http://en.wikipedia.org/wiki/REPL), and Clojurians are no exception. This is a tour of Clojure libraries and practices that make life in the REPL even more comfortable.

## Project-specific REPL utilities with user.clj and the :dev profile

To get the most out of REPL-based development, you have to design your application to be testable, inspectable, and controllable from the REPL. Typically this means you'll have several utility functions that are only needed for interacting with the application from the REPL. So, what's a good place for these development-time utilities that are not really part of your application?

![Tools](/img/pimp-my-repl/tools.jpg)
*Image by [OZinOH](http://www.flickr.com/photos/75905404@N00/)*

Ideally you'd want to:

1. Have your utilities immediately available when you start a REPL
2. Keep them separate from your application code
3. Exclude them from your build artifacts

When you start a Clojure REPL, it starts in a namespace called `user`. Wouldn't it be great if there was a way to stick all your utilities in there? It would, and there is! Hooray!

Upon startup, Clojure looks for a file called `user.clj` in the root of the classpath and loads it automatically. Just create the file `src/user.clj` with your utilities and we're done! Right? Sadly, no. `src/user.clj` fulfills our requirements #1 and #2, but it still gets packaged into our build artifacts, so technically we're only two-thirds done.

How can we add things to the classpath during development and still keep them out of our build artifacts? With [Leiningen's profiles](https://github.com/technomancy/leiningen/blob/master/doc/PROFILES.md). Profiles allow us to have different Leiningen configurations for different tasks. The `:dev` profile is meant for development-time settings, and it's *not* active during the `jar` and `uberjar` tasks. If we add a new source directory in the `:dev` profile, its contents will be added to the classpath when we start a REPL, but when we're packaging our project, it's as if the directory didn't exist.

Let's change our `project.clj` to add a development-time source directory called `dev`.

    (defproject myproject "0.5.0-SNAPSHOT"
      :description "A project for doing things."
      :dependencies [[org.clojure/clojure "1.5.1"]]
      :profiles {:dev {:source-paths ["dev"]}})

Now we can create `dev/user.clj`.

    (ns user
      (:require [myproject.core :refer :all]))

    (defn my-repl-util []
      ...)

With that, we're done!

## Resetting REPL state with tools.namespace

Here's a snag I'm sure you've hit if you've spent any time in the Clojure REPL. Say we have two functions with one calling the other.

    (defn foo []
      (println "foo"))

    (defn bar []
      (foo))

Let's rename `foo` to `xyzzy`.

    (defn xyzzy []
      (println "the artist formerly known as foo"))

    (defn bar []
      (foo))

When we evaluate the namespace, it compiles without errors. All our tests pass when we run them from the REPL.

Now let's restart the REPL and try to evaluate the namespace again.

    CompilerException java.lang.RuntimeException:
    Unable to resolve symbol: foo in this context

It took us a restart to notice we'd made a mistake because the state of our REPL had diverged from the source code: we removed `foo`'s *definition* from the source, but `foo` itself continued its existence in our REPL.

The easiest and surest way to reset the REPL's state to match the source is to restart it. Unfortunately it's a relatively slow and cumbersome operation that, depending on your development environment, may involve some manual steps and can take over ten seconds. That might not sound like much if you're used to waiting for the compiler, but compared to the instant feedback you typically get in the REPL, ten seconds feels like ages. It's enough of a nuisance that people tend to put it off, which means that many errors are detected much later than they should be.

![Tools](/img/pimp-my-repl/reset.jpg)
*Image by [Greg McMullin ](http://www.flickr.com/photos/gergtreble/)*

To solve this problem, [Stuart Sierra](https://twitter.com/stuartsierra) wrote [`tools.namespace`](https://github.com/clojure/tools.namespace), which detects changes to source files and reloads the changed files and their dependents in the correct order, removing all trace of the old definitions. With `tools.namespace` you can get your REPL to a clean state almost instantly!

Stuart has written [an excellent description of his workflow][sierra] with `tools.namespace`, and you should absolutely read it, but here's the gist of it. First you need to add `tools.namespace` to your `project.clj` as a development-time dependency.

    (defproject myproject "0.5.0-SNAPSHOT"
      :description "A project for doing things."
      :dependencies [[org.clojure/clojure "1.5.1"]]
      :profiles {:dev {:source-paths ["dev"]
                       :dependencies [[org.clojure/tools.namespace "0.2.4"]]}})

Then you can call `clojure.tools.namespace.repl/refresh` to reset your REPL. Note that this ensures that all your namespaces match their source, but your application itself may be in a state that's impossible with the new code! To make sure this never happens, you'll typically want to combine the call to `refresh` with a complete restart of your application.

    (ns user
      (:require [clojure.tools.namespace.repl :refer [refresh]]))

    (defn start
      "Start the application"
      []
      ...)

    (defn stop
      "Stop the application"
      []
      ...)

    (defn reset []
      (stop)
      (refresh :after 'user/start))

This is all explained in much more detail in [Stuart's article][sierra], so go read it!

[sierra]: http://thinkrelevance.com/blog/2013/06/04/clojure-workflow-reloaded "Stuart Sierra: My Clojure Workflow, Reloaded"

## Global REPL utilities with profiles.clj and the :user profile

Above, we needed to add `tools.namespace` as a dependency in the `:dev` profile, because our `user.clj` depended on it. However, for most other tools and libraries showcased in this article, adding them as dependencies in each project's `project.clj` is a bad idea for several reasons.

1. Every time your set of go-to tools changes (even if it's just a version upgrade), you'd have to make the same change to each project you work on.
2. Not everyone uses the same set of tools. Each project's `project.clj` would have to contain every tool that any of its developers want to use.
3. You might not have control over the `project.clj`. It would be nice to have your utilities available when you're contributing to an open source project even if its maintainers don't want to add them to their `project.clj`.

![Tools](/img/pimp-my-repl/tools2.jpg)
*Image by [OZinOH](http://www.flickr.com/photos/75905404@N00/)*

Lucky for us, the Leiningen developers have thought of *everything*. In addition to *project-wide* profiles (defined in `project.clj`), Leiningen has *user-wide* profiles, which it loads from `~/.lein/profiles.clj` and merges into the `:profiles` map of any project you happen to work on.

In case of name collisions, the project-wide profiles take precedence over user-wide profiles. To avoid such collisions, Leiningen has two different profiles for development-time settings: the project-wide `:dev` profile (defined in `project.clj`) and the user-wide `:user` profile (defined in `~/.lein/profiles.clj`).

Say you want to make `debug-repl` available in all your projects. (We'll take a closer look at `debug-repl` in a bit.) Just create the file `~/.lein/profiles.clj` and add the dependency into the `:user` profile.

    {:user {:dependencies [[org.clojars.gjahad/debug-repl "0.3.3"]]}}

Now, no matter which project you're working on, `debug-repl` is on the classpath, just a `require` away!

## Keeping utilities at hand with Vinyasa

I tend to switch my REPL to the namespace I'm currently editing. This way I can refer to its vars without prefixes, I have all its `require`d namespaces available under the same aliases I see in the source, and I can access the namespace's private vars.

This is all very handy, but there's a catch: the namespace I'm switching to typically doesn't have mappings for all the utility functions I use, such as `clojure.repl/doc` or `clojure.pprint/pprint`, so I have to call them by their full names or `require` them over and over again.

[Vinyasa](https://github.com/zcaudate/vinyasa) solves this problem with a clever trick it calls [*injection*](https://github.com/zcaudate/vinyasa#inject): it copies your utilities to the `clojure.core` namespace (optionally prefixing them to avoid name collisions). Since all namespaces contain mappings to all the names in `clojure.core` (unless they're explicitly excluded), this means your utilities remain available anywhere you go.

![Swiss Army Knife](/img/pimp-my-repl/swiss-army-knife.jpg)
*Image by [AJC1](http://www.flickr.com/photos/ajc1/)*

To enable Vinyasa's injection feature, we need to modify the `:user` profile in `~/.lein/profiles.clj`. First we add Vinyasa as a dependency. Then we use a Leiningen feature that's, confusingly enough, called *injections* (no relation to Vinyasa's injection):  forms that are evaluated once whenever Leiningen needs to evaluate some code within your project's context, e.g. when running your tests with `lein test` or starting a new REPL with `lein repl`. Using Leiningen's injections we `require` `vinyasa.inject` and use it to inject our utilities into `clojure.core`, prefixed with ">".

    {:user {:dependencies [[im.chit/vinyasa "0.1.8"]]
            :injections [(require 'vinyasa.inject)
                         (vinyasa.inject/inject 'clojure.core '>
                           '[[clojure.repl doc source]
                             [clojure.pprint pprint pp]])]}}

Now, no matter which namespace we're in, we can look up docstrings and sources with `(>doc ...)` and `(>source ...)` or pretty-print forms with `(>pprint ...)` and `(>pp)`!

You can use the same process to add any utility functions to your REPL:

1. Add the required libraries as dependencies.
2. Add a `require` form for the namespace containing the utilities.
3. Add a `vinyasa.inject/inject` form that injects the utilities into `clojure.core`.

In the rest of this article, when you see a form prefixed with `>`, you can assume that it's been injected into `clojure.core` with Vinyasa.

## More Vinyasa goodness

If that was all Vinyasa did, it would already be worth the price tag, but it has yet more tricks up its sleeves.

One of the annoyances of using the stock Clojure REPL is that you have to restart it every time you add a new library to your dependencies. Vinyasa provides [`vinyasa.pull/pull`](https://github.com/zcaudate/vinyasa#pull), a simple interface to [`pomegranate`](https://github.com/cemerick/pomegranate), which you can use to add new dependencies on the fly. You can even leave out the version number to download the latest release. `pull` returns the Leiningen coordinates of the version it downloaded so you can add them to your `project.clj`'s `:dependencies`.

    (>pull 'robert/hooke)
    ;= {[robert/hooke "1.3.0"] nil}

Vinyasa also has a couple of features which I haven't needed myself, but which you might find useful. [`vinyasa.reimport/reimport`](https://github.com/zcaudate/vinyasa#reimport) allows you to recompile and reimport all your Java classes without restarting the REPL. With [`vinyasa.lein/lein`](https://github.com/zcaudate/vinyasa#lein) you can call Leiningen from your REPL without opening a new terminal. Note that both of these functions expect to find the correct version of Leiningen on the classpath, as described in [Vinyasa's installation instructions](https://github.com/zcaudate/vinyasa#installation).

## Quick and dirty debugging with Spyscope

Often a couple of well placed `println` (or even better, `pprint`) calls are all it takes to debug a problem. Sometimes, though, the form whose value you want to print is nested inside a more complex form. [Spyscope](https://github.com/dgrnbrg/spyscope) defines some new [reader tags](http://clojure.org/reader#The%20Reader--Tagged%20Literals) that you can use to pretty-print a form without factoring it out of the containing form.

![Microscope](/img/pimp-my-repl/microscope.jpg)
*Image by [Canada Science and Technology Museum](http://www.flickr.com/photos/cstmweb/)*

To install Spyscope, add the following lines to your `~/.lein/profiles.clj`.

    {:user {:dependencies [[spyscope "0.1.4"]]
            :injections [(require 'spyscope.core)]}}

Let's say we want to inspect the result of the `range` call in this piece of code.

    (apply + (range 11 20 2))

We can do this by prefixing it with the tag `#spy/p`.

    (apply + #spy/p (range 11 20 2))

This causes Spyscope to rewrite the form into the following.

    ;; Prints (11 13 15 17 19)
    (apply + (doto (range 11 20 2) clojure.pprint/pprint))

The fancier tag [`#spy/d`](https://github.com/dgrnbrg/spyscope#spyd) gives you more context and allows you to customize the debugging output. Let's ask Spyscope to add a timestamp to the output.

    (apply + #spy/d ^{:time true} (range 11 20 2))

If the above form is placed in the function `asdf.core/foo`, calling the function produces the following output.

    asdf.core$foo.invoke(core.clj:4) 2014-03-14T10:16:47 (range 11 20 2) => (11 13 15 17 19)

As you can see, in addition to the result, `#spy/d` shows us the top of the call stack, the form being inspected, the source line it came from and the timestamp we requested.

For even more features, check out [Spyscope's documentation](https://github.com/dgrnbrg/spyscope#spyscope).

## Exploratory debugging with debug-repl

If you find yourself changing a piece of code and re-running it just to see how its debugging output changes, what you probably really want is a REPL at the time and place you wish to explore. That's exactly what [debug-repl](https://github.com/georgejahad/debug-repl) gives you.

![Yo dawg...](/img/pimp-my-repl/yo-dawg.jpg)

To install debug-repl, add the following lines to your `~/.lein/profiles.clj`.

    {:user {:dependencies [[org.clojars.gjahad/debug-repl "0.3.3"]]
            :injections [(require 'alex-and-georges.debug-repl)
                         (vinyasa.inject/inject 'clojure.core '>
                           '[[alex-and-georges.debug-repl debug-repl]])]}}

Now insert `(>debug-repl)` anywhere in your code. When the execution hits that point, it's given over to the REPL. Once you're done, enter `()`, and the regular execution is resumed.

    (defn foo [a b]
      (>debug-repl)
      (+ a b))

    user=> (foo 1 2)
    dr-1-1001 => a
    1
    dr-1-1001 => b
    2
    dr-1-1001 => (+ a b)
    3
    dr-1-1001 => (- a b)
    -1
    dr-1-1001 => ()
    3
    user=>

## Comparing forms with difform

I recently broke a function I was refactoring, but luckily the unit tests caught the breakage. The problem was, the data structure that the function produced was quite large, and to my eyes the expected and actual results looked the same. Instead of laboriously poring over them, I gave the task over to [`difform`](https://github.com/GeorgeJahad/difform) – a diff for Clojure data structures.

Difform couldn't be simpler to use. First, add it to your `~/.lein/profiles.clj`.

    {:user {:dependencies [[difform "1.1.2"]]
            :injections [(require 'com.georgejahad.difform)
                         (vinyasa.inject/inject 'clojure.core '>
                           '[[com.georgejahad.difform difform]])]}}

Then just call `>difform` with the two values to compare!

    user=> (>difform {:first-name "John", :last-name "Doe"}
                     {:first-name "Jane", :last-name "Doe"})
       {:first-name "J
     - oh
     + a
       n
     + e
       ", :last-name "Doe"}

    user=> (>difform {:foo {:value [13 3 54 5 323 44]}
                      :bar {:value [13 3 54 5 323 44]}}
                     {:foo {:value [13 35 4 5 323 44]}
                      :bar {:value [13 3 54 5 323 44]}})
       {:bar {:value [13 3 54 5 323 44]}, :foo {:value [13 3
     + 5

     - 5
       4 5 323 44]}}

Remember that the Clojure REPL remembers the last three printed values as `*1`, `*2` and `*3`, so when you're [golfing](http://en.wikipedia.org/wiki/Code_golf) a form in the REPL, you don't have to eyeball the printouts to see if and how the result changed: difform can do that for you with `(>difform *2 *1)`.

## Exploring the REPL state with clj-ns-browser

[clj-ns-browser](https://github.com/franks42/clj-ns-browser) is a GUI tool for browsing the REPL state. It shows you searchable lists of the namespaces that have been loaded and the vars they contain. For each var it shows you its docstring, source code, metadata, and even usage examples from [clojuredocs.org](http://clojuredocs.org/). It can even list the unloaded namespaces that are available on the classpath!

![clj-ns-browser](/img/pimp-my-repl/clj-ns-browser.png)

It's especially useful for exploring an unfamiliar library. No more do you have to dig through the (often unsearchable) documentation or, in its absence, the source code looking for the function you need. Just fire up clj-ns-browser with `(>sdoc)`, see what namespaces the library made available, require the one that sounds relevant with a click of a button, and browse its functions.

To install clj-ns-browser, add the following to your `~/.lein/profiles.clj`.

    {:user {:dependencies [[clj-ns-browser "1.3.1"]]
            :injections [(require 'clj-ns-browser.sdoc)
                         (vinyasa.inject/inject 'clojure.core '>
                           '[[clj-ns-browser.sdoc sdoc]])]}}
