---
layout: post
title: Playwright for the rest of us
author: tatut
excerpt: >
    Playwright is a great tool but unluckily it doesn't include bindings for every language... until now.
tags:
 - Smalltalk
 - Playwright
 - Testing
---

[Playwright](https://playwright.dev) is a great tool for browser based testing. We use it in many of
our projects and I personally like it a lot. Unluckily it only supports some *niche* programming
languages like Java, Python, JavaScript and C#... but does not have support for the OG of OO: Smalltalk.

To rectify this glaring omission, I decided to create my own bindings.

## The plan

Obviously it is easiest to start with one of the existing languages and add a layer on top of that.
I wanted to make this as general as possible, so I decided to create a host program that wraps the
existing API and exposes the functionality to clients.

JSON is pretty ubiquituous these days and most languages will have either a builtin or easily available
libraries to handle the format. I considered building an [OpenAPI](https://www.openapis.org) but the
stateless nature didn't seem like a good idea for such a chatty use case... there will be lots of
messages going through and a constant connection seemed more appropriate. I still wanted to stay
within HTTP tooling so WebSockets seemed like a good fit.

## Playwright over WebSocket

After I had the approach selected, the program came about pretty easily and got the name [pows](https://github.com/tatut/pows)
for Playwright over WebSocket. It is implemented in Clojure using the [Playwright Java](https://playwright.dev/java/)
bindings. It implements many of the Playwright Locator action commands (like click, fill, check and so on)
as well as the LocatorAssertions (like hasCount, hasClass, hasText etc) as simple commands that can
be invoked with a JSON object.

The protocol is command & response, the client sends a command and waits for the response to it.
Commands are processed one at a time.

```json
{"locator": "button.save", "click": 1}
{"success": true}
```

[![asciicast](https://asciinema.org/a/630656.svg)](https://asciinema.org/a/630656)
See a screencast of using Playwright with the [websocat](https://github.com/vi/websocat)
command line WebSocket tool.

## Bridging the gap

Once the host program was ready, all that was needed was to create a Smalltalk library that uses it.
This library is named [pharo-Pows](https://github.com/tatut/pharo-Pows) and support
[Pharo](https://pharo.org) Smalltalk.

The basic idea of the library is to model a Playwright connection that allows navigating to a URL
and a Playwright Locator that represents some element location on the page.
The Locator has methods that can be used to manipulate an element or check
assertions about it.

![playground](/img/2024-01-pows/pharo-Pows-playground.png)
Screenshot of a playground session using the library.

Now that we have the library we need some finishing touches, mainly creating a [SUnit](https://sunit.sourceforge.net)
`PowsTestCase` class that can be used as the superclass of any tests that need Playwright. The class
will handle automatic setup and teardown of a pows connection for each test method.
With that in place our test methods look like:

```smalltalk
testCounter
  self
  go: 'http://localhost:8080/examples/counter';
  locate: 'div.counter' assert: [ :l | l hasText: '0' ];
  locate: 'button.inc' do: #click;
  locate: 'div.counter' assert: [ :l | l hasText: '1' ];
  locate: 'button.dec' do: [ :b | b click; click ];
  locate: 'div.counter' assert: [ :l | l hasText: '-1' ]
```

## Conclusion

Smalltalk is a very nice and concise OO language and Pharo is a modern integrated environment
for it.
Playwright is one of the best tools for programmatic browser testing these days and with pows
it can be made to work with any technology that has support for JSON and WebSockets.

I made these libraries to scratch my own itch as side projects.
Hopefully someone else can also benefit from them.
