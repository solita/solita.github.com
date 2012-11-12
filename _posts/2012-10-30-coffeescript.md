---
layout: post
title: On CoffeeScript
author: massimo
excerpt: CoffeeScript - if you aren't yet familiar with it - is a nice little language that compiles to readable, "safe" JavaScript (everything wrapped in an anonymous function, variables are lexically scoped). It swaps curly braces for indentation, arrows for function definitions and adds a few features such as classes and array comprehensions.
---

### A sip ###
[CoffeeScript](http://coffeescript.org) - if you aren't yet familiar with it - is a nice little language that compiles to readable, "safe" JavaScript (everything wrapped in an anonymous function, variables are lexically scoped).
It swaps curly braces for indentation, arrows for function definitions and adds a few features such as classes and array comprehensions.

Basically, it looks like this. Note how there's no explicit return statement and how the conditional is an expression.
{% highlight coffeescript %}
isFoo: (x) -> if x is 'foo' then true else false
getFoos: (xs) -> (x for x in xs when isFoo x)
{% endhighlight %}

Another example. Compared to JS prototypes, the syntax is really nice.
{% highlight coffeescript %}
class Cat
  constructor: (@name) ->
  meow: -> console.log "I'm #{@name}! Hear me roar!"
class NyanCat extends Cat
  constructor: (name) -> super name
  meow: ->
    super()
    console.log 'Nyan!'
{% endhighlight %}

### Aroma ###
Not being a JS ninja, using CS seemed like a great chance to leverage the full power of JS in a UI-heavy project.
Having written a few lines of Python and Haskell in the past, the clean, parenthesis-free syntax was enticing and the concept of classes was familiar to a Java developer.

After a few weeks I was in evangelization mode.

### Bitterness ###
Soon, however, everyone's code started to look a little different. Some used parentheses in function invocations while others didn't. Classes were used when a simple object literal would have sufficed.

The team found that the CS compiler doesn't always follow the [principle of least astonishment](http://en.wikipedia.org/wiki/Principle_of_least_astonishment), even if the behavior is documented.

{% highlight coffeescript %}
arr = (n for n in [1, 2, 3]) # arr contains 1, 2, 3
arr = n for n in [1, 2, 3]   # arr contains just 3
{% endhighlight %}

{% highlight coffeescript %}
doSomething() -> 'hello'
# above calls the result of doSomething() with an anonymous function
doSomething () -> 'hello'
# above calls doSomething with an anonymous function
{% endhighlight %}

I also noticed that writing new code was accompanied by a feeling of undecidedness, not knowing whether my approach is *the* idiomatic way to solve a problem. Later I found an article that summarized my feelings about CS, [Less typing, bad readability](http://ceronman.com/2012/09/17/coffeescript-less-typing-bad-readability/) by Manuel Cerón.

As our codebase grew, our makeshift [Rhino](https://developer.mozilla.org/en-US/docs/Rhino) compiler started to stagger and build times grew to half a minute (with just a few files and a total of < 1000 LOC).

### Sweetener ###
A clever developer on our team wired up [Node.js](http://nodejs.org) to an Eclipse builder resulting in compilation times of less than a second. [Sublime Text 2](http://www.sublimetext.com/) emerged as a great CS editor.

Diversity in the codebase was addressed by employing [this style guide](https://github.com/polarmobile/coffeescript-style-guide) with some minor modifications. We started ditching classes in favor of simple object literals and revealing modules. In general we were using CS as it should be used: a simpler way to write JS.

### An empty cup ###
Using CS has been a rocky road but a fun one. It's fun to write and easy to debug. It gives its wielder a terse, expressive syntax with exceedingly many ways to do things. Unfortunately it's also easy to shoot yourself and other developers in the feet.
