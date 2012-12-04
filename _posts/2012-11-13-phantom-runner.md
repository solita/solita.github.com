---
layout: post
title: Interactive JavaScript testing with PhantomRunner
author: empperi
excerpt: "Introducing PhantomRunner: a Java based, open source testing library that provides integration between JUnit and Jasmine via the PhantomJS headless browser."
---

**tl;dr:** PhantomRunner is a Java based, open source testing library
that provides integration between JUnit and Jasmine via the PhantomJS
headless browser. You can find it
[on GitHub](https://github.com/solita/phantom-runner).

### The pain of JavaScript ###

Most of us in the business of writing software for the web are more or
less familiar with JavaScript -- "the assembly language for the web".
Although writing JavaScript isn't nearly as painful as writing raw
assembly, it can get quite tedious due to several unexpected properties
it has.

Most of JavaScript's problems can be bypassed and they don't cause too
much trouble when you are aware of them. But there is still one huge
workflow issue with JavaScript: testing. Currently the way we test
JavaScript code is either by not doing it at all (the most common
case) or via system level testing with something like
[Selenium](http://seleniumhq.org/). System level testing is fine and
very much needed, but due to the rise of Single Page Applications we
have a real need for unit testing the business logic of the JavaScript
code. For this we should use one of the available JavaScript unit
testing libraries.

Obviously both system level and unit level testing is required these
days, as JavaScript code bases are getting bigger and bigger. In fact,
with JavaScript it is *even more important* due to the language's
quirky behavior. There is no real type mechanism, there are no imports
and so on. Good unit tests can remove a lot of pain from JavaScript
programming.

But those who like to develop their program code test-first are faced
with a dilemma: all the available testing libraries expect you to run
your tests in a browser. This is a reasonable requirement since
browsers have the most up to date JavaScript interpreters, and if you
are writing JavaScript code, you are more than likely to run it in
a browser, where you have stuff like DOM available. But really, who
wants to continuously switch between their programming environment and
a browser when they are developing software test-first? You want to be
able to run your tests *all the time* without context switches.

#### jsTestDriver ####

Fortunately there is a solution (or actually two) available to this
problem. [JsTestDriver](http://code.google.com/p/js-test-driver/) is a
test execution framework that allows you to keep your browser open in
the background while executing tests from a command line or an IDE. It
does this by starting an HTTP server providing browsers with a special
page, which binds them to jsTestDriver and prepares them to receive
tests to be executed.

The immediate benefit is that your tests can be executed blindingly
fast -- so fast, in fact, that by default jsTestDriver's Eclipse
plugin runs your tests each time you save a file. Even largish test
suites can be run in milliseconds (yes, milliseconds, not seconds).
Another benefit is that you can bind multiple browsers at the same
time and jsTestDriver can send the tests to each of them concurrently,
thus ensuring that your code works in all the browsers.

There are some problems, though. The first of these is that the
jsTestDriver IDE plugins are really buggy. Even if the command line
software works fine, the IDE integration does not. It isn't much
better to switch between your IDE and a command line than to switch
between your IDE and a browser to execute your tests. Sure, with
jsTestDriver you can execute your tests with multiple browsers at
once, which is indeed a big bonus. But still, with a lacking support
for IDEs, the jsTestDriver just isn't quite there yet.

Another problem with jsTestDriver is that it forces forces you to
write your tests in jsTestDriver's own format. It does not provide any
kind of abstraction over existing testing libraries, so if you've
already written a huge amount of tests with, for example,
[Jasmine](http://pivotal.github.com/jasmine/), then you're out of
luck.

A third problem is that since jsTestDriver is its own test runner
executable, the integration with continuous integration systems can
get a bit tedious. It can be done, sure, but expect quite a bit of
work until you get there.

Despite its problems jsTestDriver is a really good idea, and if it is
developed further it might become the ultimate tool for interactive
JavaScript testing. But right now it's just a nice concept.

### PhantomRunner ###

After trying to integrate jsTestDriver into a JavaScript intensive
project I got really frustrated. Such a great tool but not quite
there. This gave me the idea to create my own version of jsTestDriver
that would overcome its main problems.

First of all, I decided that I want my test runner to be tightly
integrated with [JUnit](http://www.junit.org/). This adds a dependency
to Java but also removes a whole bunch of problems. Due to the JUnit
integration I can run my tests anywhere I can run JUnit based tests.
This means a *huge* amount of different tools: continuous
integration servers, build tools, IDEs and so on. I don't have to
worry about writing IDE specific plugins -- just let the existing
JUnit integrations to do the work for me.

Second, I realized that I will not be able to create a testing
framework that is in any way better than the existing frameworks. Thus
I wanted the architecture to be flexible enough to allow adding
support for any testing framework.

Third, I wanted the architecture to allow different server
implementations. This would allow me to run my tests just once without
pre-starting the server, which would be great for CI environments, or
I could start a server once and keep pounding on it with tests, thus
providing me with a good test execution speed.

And last, I wanted to do all of this by using the
[PhantomJS](http://phantomjs.org/) headless browser.

#### Where are we currently? ####

The very first implementation of PhantomRunner can be found on
[Github](https://github.com/solita/phantom-runner). It is currently
usable and can execute [Jasmine](http://pivotal.github.com/jasmine/)
based tests. It requires the latest PhantomJs browser to function and
it does not support pre-starting the server. But it does provide two
different server implementations for different use case scenarios as a
proof of concept.

Already in its current form PhantomRunner is ready to be used. Right
now it requires you to compile it yourself (it's built with
[Maven](http://maven.apache.org/)) and you need to write a single
JUnit test class to bind it to JUnit. Below is an example of how this
is done (it's actually PhantomJS's own test class and can be found
on Github):

{% highlight java %}
@RunWith(PhantomRunner.class)
@PhantomConfiguration(
        phantomPath="phantomjs",
        tests="**/*-test.js",
        injectLibs="classpath:require.js",
        interpreter=@JavaScriptTestInterpreterConfiguration(
                interpreterClass=JasmineTestInterpreter.class,
                libraryFilePaths="classpath:jasmine/jasmine.js"
        ))
public class PhantomRunnerTest {
}
{% endhighlight %}

PhantomRunner supports adding arbitrary libraries to be loaded before
the tests are run, which allows you to write tests that rely on those
libraries. For example you might want to use
[RequireJs](http://requirejs.org/) to handle your module loading. This
allows you to test code reliably with all its dependencies loaded:

{% highlight javascript %}
// This is a completely valid way to do things with PhantomRunner
// and Require.js
require(["some/module"], function(module) {
    describe("Some module suite", function() {
        it("tests stuff", function() {
            expect(module.someMethod()).toBe("foo");
        });
    });
});
{% endhighlight %}

#### What should still be done? ####

The current implementation of PhantomRunner is built only for unit
testing JavaScript code. That does not mean, however, that it couldn't
be expanded to support the more conventional integration testing
needs. This would require a new server implementation that allows
PhantomJS to fetch the test HTML page from an actual server running
your software and executing the tests against it. This is the most
requested feature for PhantomRunner at [Solita](http://www.solita.fi)
so it will be the first big new feature to be added to PhantomRunner.

Also currently PhantomRunner only supports JavaScript based tests. It
should be pretty easy to add support for CoffeeScript, which is used
more and more everywhere these days. And finally, the third big new
feature would be to add a server implementation that allows binding
any browser (not just PhantomJS) to PhantomRunner, although I'm still
evaluating whether that's something PhantomRunner should even try to
do.
