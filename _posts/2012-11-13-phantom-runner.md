---
layout: post
title: Interactive Javascript testing
author: empperi
---

**tldr;** PhantomRunner is a Java based testing library which provides
integration between JUnit and Jasmine via PhantomJS headless browser
and it is hosted at
[https://github.com/solita/phantom-runner](https://github.com/solita/phantom-runner)

# The pain of Javascript #

Most of us who are in the business of writing software to the Web are
more or less familiar with Javascript - the "assembly" of the web.
Although writing Javascript isn't nearly as painful as writing raw
assembly it can get quite tedious due to several unexpected properties
it has.

However most of the problems of Javascript can be bypassed and they
don't cause too big a problem when you are aware of them. But there is
still one huge workflow issue considering Javascript: testing.
Currently the way we test Javascript code is either by not doing it at
all (the most common case) or via system level testing by using
something like [Selenium](http://seleniumhq.org/). System level
testing is fine and very much needed but due to the rise of Single
Page Applications we have real need for unit testing the business
logic of Javascript code too. For this we should use one of the
available unit testing libraries for Javascript.

Obviously both system level and unit level testing is required these
days where Javascript code bases get bigger and bigger. In fact, with
Javascript it is **even more important** due to the language's quirky
behavior. There is no real type mechanism, there are no imports and so
on. Good unit tests can remove a lot of pain from developing
Javascript code.

But those who like to develop their program code test-first are facing
a dilemma: all of the testing libraries available expect you to run
your tests in a browser. This is a reasonable requirement since
browsers have the most up to date Javascript interpreters and if you
are writing code with Javascript you are more than likely to run it in
browser too where you have stuff like DOM available. But really, who
wants to continuously switch between your programming environment and
a browser when you are developing software test-first? You want to be
able to run tests **all** the time without context switches.

## jsTestDriver ##

Fortunately there is a solution (or two actually) available to bypass
this problem. [JsTestDriver](http://code.google.com/p/js-test-driver/)
is a test execution framework which allows you to keep your browser in
a background while executing tests from command line or from your IDE.
It does this by starting a HTTP server which provides a special page
for the browsers which binds them to jsTestDriver and readies them to
receive tests to be executed.

The instant benefit of this is that your tests can be executed
blindingly fast - so fast in fact that the default in jsTestDriver's
Eclipse plugin is to run your tests all the time after each save. Even
largish test sets can be ran in milliseconds (yes, milliseconds, not
seconds). Another benefit is that you can bind multiple browsers at
the same time and jsTestDriver can send the tests to each of these
concurrently thus allowing one to ensure that all browsers execute
your code properly.

There are problems though. First of these is that the jsTestDriver IDE
plugins are really buggy. Even if the command line software works fine
the IDE integration does not. It isn't really a much better to switch
between your IDE and command line than to switch between your IDE and
a browser to execute your tests. Sure, with jsTestDriver you can
execute your tests with multiple browsers at once which is indeed a
big bonus. But still with a lacking support for IDEs the jsTestDriver
just doesn't quite get there.

Another problem with jsTestDriver is that it forces you to write your
tests in jsTestDriver's own format. It does not provide any kind of
abstraction over existing testing libraries and thus if you've already
written a huge amount of tests with for example
[Jasmine](http://code.google.com/p/js-test-driver/) then you're out of
luck.

A third problem is the fact that since it is it's own test runner
executable the integration with continuous integration systems can get
a bit tedious. It can be done, sure, but expect quite a bit of work
until you get there.

Despite it's problems jsTestDriver is a really good idea and if it is
developed further it might be the ultimate tool for interactive
Javascript testing. But right now it's just a nice concept.

## PhantomRunner ##

After trying to integrate jsTestDriver into a Javascript intensive
project I got really frustrated. Such a great tool but not quite
there. This gave me an idea to create my own version of jsTestDriver
which would bypass the main problems it has.

First of all, I decided that I want my test runner to be tightly
integrated with [JUnit](http://www.junit.org/). This causes a
dependency to Java but it also removes a whole bunch of problems. Due
to the JUnit integration I can run my tests anywhere which can run
JUnit based tests. This means a **huge** amount of different tools:
continuous integration servers, build tools, IDEs and so on. I don't
have to worry about writing IDE specific plugins - just let the
existing JUnit integrations to do the work for me.

Second, I realized that I will not be able to create a perfect testing
framework which would be better in any way compared to the existing
frameworks. Thus I wanted the architecture to be flexible enough to
support any testing framework provided that a support is written for
it.

Third, I wanted the architecture to allow different server
implementations. This would allow me to run my tests just once without
pre-starting the server which would be great for CI environments or I
could start a server once and keep on pounding tests at it thus
providing me with a good test execution speed.

And last, I wanted to do all of this by using the
[PhantomJS](http://phantomjs.org/) headless browser.

### Where are we currently? ###

The very first implementation of PhantomRunner is located at
[Github](https://github.com/solita/phantom-runner). It is currently
usable and can execute
[Jasmine](http://code.google.com/p/js-test-driver/) based tests. It
requires the latest PhantomJs browser to function and it does not
support the prestarting of a server. But it does provide two different
server implementations for different use case scenarios as a proof of
concept that it can be done.

Already in it's current form PhantomRunner is ready to be used. Right
now it requires you to compile it yourself (it's built with
[Maven](http://maven.apache.org/)) and you need to write a single
JUnit test class to bind it to JUnit. Below is an example of how this
is done (it's actually the test class used in developing the PhantomJS
and can be found from Github):

{% highlight java %}
@RunWith(PhantomRunner.class)
@PhantomConfiguration(
		phantomPath="phantomjs", 
		tests="**/*-test.js",
		injectLibs="classpath:require.js",
		interpreter=@JavascriptTestInterpreterConfiguration(
				interpreterClass=JasmineTestInterpreter.class,
				libraryFilePaths="classpath:jasmine/jasmine.js"
		))
public class PhantomRunnerTest {

}
{% endhighlight %}

PhantomRunner supports adding arbitrary libraries which will be loaded
before the tests are ran which allows you to write tests which rely on
the existence of those libraries. For example you might want to use
[RequireJs](http://requirejs.org/) to handle your module loading. This
allows you to test code reliably in such a way that all of it's
dependencies are loaded too:

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

In addition to easy integration to other testing frameworks
PhantomRunner supports multiple server implementations to be used for
communication between PhantomRunner and PhantomJs browser.

### What should still be done? ###

Current implementation of PhantomRunner is built purely for writing
unit tests for your Javascript code. That does not mean however that
it couldn't be expanded to support the more conventional integration
testing needs. This would require a new server implementation which
allows the PhantomJS to fetch the "test" HTML page from an actual
server running your software and executing tests against it. This is
the most requested feature for PhantomRunner inside Solita so it will
be the first big new feature to appear into PhantomRunner.

Also currently PhantomRunner supports only Javascript based tests. It
should be pretty easy to add support for CoffeeScript too which is
used more and more everywhere these days. And finally the third big
new feature would be to add a server implementation which would allow
binding any browser (not just PhantomJS) to PhantomRunner, although
this is still being evaluated if PhantomRunner should even try to do
something like this.
