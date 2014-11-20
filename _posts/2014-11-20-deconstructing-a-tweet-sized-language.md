---
layout: post
title: Deconstructing a tweet-sized language
author: noidi
excerpt: 140 characters might not seem like much, but it's enough to implement an interpreter for a simple programming language. This post explains how.
---

Some time ago, [Brandon Bloom](https://twitter.com/BrandonBloom) [tweeted](https://twitter.com/BrandonBloom/status/528262785642545153) this snippet of Clojure code:

<blockquote class="twitter-tweet" lang="en"><p>(let [dict {&#39;dup (fn [[x &amp; s] _] (conj s x x)) &#39;* (fn [[x y &amp; s] _] (conj s (* x y)))}] (reduce #((dict %2 conj) %1 %2) () &#39;(5 dup *)))</p>&mdash; Brandon Bloom (@BrandonBloom) <a href="https://twitter.com/BrandonBloom/status/528262785642545153">October 31, 2014</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

Spend a couple of minutes and see if you can figure out what it does.

If you gave it a try and still have no idea of what you just read, I hope that this post will help you see what makes this such an exciting piece of code.

## Going Forth

The key to understanding the tweet is right at the end:

{% highlight clojure %}
5 dup *
{% endhighlight %}

This looks exactly like a [Forth](http://en.wikipedia.org/wiki/Forth_%28programming_language%29) program for taking the number 5 and multiplying it by itself. And indeed, the tweeted code implements an interpreter for an extremely limited Forth-like language and uses it to run this little program!

Like Forth, the implemented language is [concatenative](http://www.drdobbs.com/architecture-and-design/what-is-a-concatenative-language/228701299). A program in a concatenative language is a function from a type (typically a [stack](http://en.wikipedia.org/wiki/Stack_%28abstract_data_type%29)) to the same type. Each term (word) in the language is also such a function, which means that any term by itself is also a complete program.

To [compose](http://en.wikipedia.org/wiki/Function_composition) two programs (functions), we write them one after the other:

{% highlight clojure %}
a b
{% endhighlight %}

This would translate to Clojure as

{% highlight clojure %}
(comp b a)
{% endhighlight %}

Function composition is [associative](http://en.wikipedia.org/wiki/Associative_property), so we can compose programs of any length like this. To apply the program

{% highlight clojure %}
c d e
{% endhighlight %}

to the result of the program

{% highlight clojure %}
a b
{% endhighlight %}

we *concatenate* them into

{% highlight clojure %}
a b c d e
{% endhighlight %}

## Everything is a function

Looking at the program `5 dup *`, you might be wondering what that `5` is doing there. Shouldn't all terms be functions? Yes, and it is! In a concatenative language, `5` is a function that takes a stack and returns a stack with the number 5 pushed on top. Similarly, `dup` is a function that duplicates the topmost item on the stack, and `*` pops two items off the stack, multiplies them together, and pushes the result onto the stack.

The program is a function from a stack to a stack made by composing these three functions together, so we could translate it into Clojure as

{% highlight clojure %}
(comp * dup 5)
{% endhighlight %}

if we could call our functions `5` and `*` in Clojure.

## Step by step

Let's see what happens when we apply the program to an empty stack, represented by an empty Clojure list `()`.

1.  The function `5` is applied to the empty stack `()`, yielding the stack `(5)`, which is passed on to `dup`.

2.  `dup` duplicates the topmost item on the stack `(5)`, yielding the stack `(5 5)`, which is passed on to `*`.

3.  `*` pops two items off the stack `(5 5)`, multiplies them together, and pushes the result onto the stack, yielding the stack `(25)`, which is the result of the program.

## Defining the terms

OK, now we know how to read and write programs in this little language. Let's move on to interpreting them!

The first thing we need is the functions that correspond to the three terms used in the program. Let's start with `5`:

{% highlight clojure %}
(fn [s]
  (conj s 5))
{% endhighlight %}

Like all functions in this language, `5` takes a stack `s` as a parameter. The stack is a Clojure list, so we can use the [`conj`](http://clojuredocs.org/clojure.core/conj) function to add the number 5 to the beginning of the list.

`dup` is just a bit more complicated:

{% highlight clojure %}
(fn [[x & s]]
  (conj s x x))
{% endhighlight %}

We use [destructuring](http://blog.jayfields.com/2010/07/clojure-destructuring.html) to name the first item of the list (i.e. the topmost item of the stack) `x` and the rest of the list `s`. Then we add the item twice to the beginning of the list using `conj`.

`*` follows the same pattern as `dup`:

{% highlight clojure %}
(fn [[x y & s]]
  (conj s (* x y)))
{% endhighlight %}

This time we pop two items off the stack, multiply them, and push the product on top of the stack.

We collect these functions into a dictionary, which is a map from terms to the functions they represent:

{% highlight clojure %}
(let [dict {5 (fn [s]
                (conj s 5))
            'dup (fn [[x & s]]
                   (conj s x x))
            '* (fn [[x y & s]]
                 (conj s (* x y)))}])
{% endhighlight %}

Note that we have to quote the symbols to prevent Clojure from trying to look them up in the current namespace.

## A literal interpretation

According to the semantics of this little language, the program `5 dup *` is a function from a stack to a stack formed by composing three such functions together. The most literal way to implement it would be something like this:

{% highlight clojure %}
(let [dict {5 (fn [s]
                (conj s 5))
            'dup (fn [[x & s]]
                   (conj s x x))
            '* (fn [[x y & s]]
                 (conj s (* x y)))}
      program '(5 dup *)
      f (apply comp (reverse (map dict program)))]
  (f ()))
{% endhighlight %}

In Clojure, map data structures can be used as functions from keys to values. This means we can apply `dict` to a term to get the function that the term represents:

{% highlight clojure %}
(dict 5)
;= #<function>

(dict 'dup)
;= #<function>
{% endhighlight %}

The function [`map`](http://clojuredocs.org/clojure.core/map) (not to be confused with the map data structure) takes a function and a sequence of values, applies the function to each value, and returns the results as a sequence. To convert a sequence of terms to a sequence of functions that they represent, we `map` over the terms using `dict`.

{% highlight clojure %}
(map dict program)
;= (#<function> #<function> #<function>)
{% endhighlight %}

Once we have looked up the functions corresponding to each term, we compose them into the function `f`. Clojure's `comp` expects functions in the opposite order than the language we're implementing, so we have to `reverse` the function sequence before applying `comp` to it.

{% highlight clojure %}
(apply comp (reverse (map dict program)))
;= #<function>
{% endhighlight %}

Finally, we apply `f` to an empty stack (the state in which the program starts), yielding a new stack, which is the program's result.

{% highlight clojure %}
(f ())
;= (25)
{% endhighlight %}

## DIY function composition

If you look at the tweet, there's no mention of `map` or `comp` in it. That's because it does not compose the whole program into the function `f` like we did above, but instead walks the sequence of terms using [`reduce`](http://clojuredocs.org/clojure.core/reduce), looking up and applying each function as it goes.

{% highlight clojure %}
(let [dict {5 (fn [s]
                (conj s 5))
            'dup (fn [[x & s]]
                   (conj s x x))
            '* (fn [[x y & s]]
                 (conj s (* x y)))}
      program '(5 dup *)]
  (reduce (fn [s t]
            ((dict t) s))
          ()
          program))
{% endhighlight %}

The function that we pass to `reduce` takes as its parameters a stack and a term. It looks up the function corresponding to the term from `dict` and applies it to the stack, returning a new stack.

{% highlight clojure %}
(fn [s t]
  ((dict t) s))
{% endhighlight %}

First `reduce` applies the function to its second argument (the empty stack `()`) and the first term of the program (`5`), yielding a new stack (`(5)`). Then the reduction function is called with the returned stack (`(5)`) and the next term (`dup`), and so on, until we get to the end of the program.

This version of the interpreter is equivalent to the one above. The same term functions get applied to the same stack values in the same order. The difference is that we've combined term function lookup and application into a single operation, and we pass values from one function to the next with `reduce` instead of leaving it to `comp`.

## Push all the things!

There's a huge flaw in our interpreter: it only supports the number five. Trying to interpret a valid program like `2 3 *` would result in a `NullPointerException`, as the term lookup would return `nil` for the terms `2` and `3` instead of functions.

If we added functions `2` and `3` to `dict`, our interpreter would still fail with programs containing `4`, so it's clear that our current approach (listing each number in the dictionary) does not scale. And it's not just natural numbers that we have to worry about. In the tweeted language, any term without an entry in the dictionary is pushed on the stack.

Let's make a little change to the function we pass to `reduce`. First we check if there's an entry for the term in the dictionary. If there is, we proceed as before. Otherwise, we push the term on the stack. This way we no longer need a special function for the term `5` in the dictionary.

{% highlight clojure %}
(let [dict {'dup (fn [[x & s]]
                   (conj s x x))
            '* (fn [[x y & s]]
                 (conj s (* x y)))}
      program '(5 dup *)]
  (reduce (fn [s t]
            (if (contains? dict t)
              ((dict t) s)
              (conj s t)))
          ()
          program))
{% endhighlight %}

## Unconditional lookups

Clojure maps can be used as functions from keys to values, but we can also pass them a second parameter, a "not found" value to return when the key is not found in the map:

{% highlight clojure %}
({:a 1, :b 2} :b)
;= 2

({:a 1, :b 2} :c)
;= nil

({:a 1, :b 2} :c 0)
;= 0

({:a 1, :b 2} :b 0)
;= 2
{% endhighlight %}

We can use this "not found" parameter to get rid of the `if`. When a function matching the term is not found in the dictionary, we return a function that pushes the term onto the stack.

{% highlight clojure %}
(let [dict {'dup (fn [[x & s]]
                   (conj s x x))
            '* (fn [[x y & s]]
                 (conj s (* x y)))}
      program '(5 dup *)]
  (reduce (fn [s t]
            (let [f (dict t (fn [s] (conj s t)))]
              (f s)))
          ()
          program))
{% endhighlight %}

## Making conj fit in

Note that `conj`, as we use it in the "not found" function, has almost the same signature as `dup` and `*`. It takes a stack and returns a stack. The only difference is that in addition to the stack, we pass `conj` the current term. Let's add a term parameter to our functions so that they match our use of `conj` in the "not found" function.

{% highlight clojure %}
(let [dict {'dup (fn [[x & s] _]
                   (conj s x x))
            '* (fn [[x y & s] _]
                 (conj s (* x y)))}
      program '(5 dup *)]
  (reduce (fn [s t]
            (let [f (dict t (fn [s t] (conj s t)))]
              (f s t)))
          ()
          program))
{% endhighlight %}

Following the Clojure convention, the new parameter is named `_` to indicate that it's not used in the function body.

Note that all the "not found" function does now is pass its parameters to `conj`, so we might as well just use `conj` directly.

{% highlight clojure %}
(let [dict {'dup (fn [[x & s] _]
                   (conj s x x))
            '* (fn [[x y & s] _]
                 (conj s (* x y)))}
      program '(5 dup *)]
  (reduce (fn [s t]
            (let [f (dict t conj)]
              (f s t)))
          ()
          program))
{% endhighlight %}

## Packing it up

The term function lookup is now so simple that we can remove the `let`.

{% highlight clojure %}
(let [dict {'dup (fn [[x & s] _]
                   (conj s x x))
            '* (fn [[x y & s] _]
                 (conj s (* x y)))}
      program '(5 dup *)]
  (reduce (fn [s t]
            ((dict t conj) s t))
          ()
          program))
{% endhighlight %}

We can shorten the code a little further by using Clojure's [special syntax for anonymous functions](https://coderwall.com/p/panlza/function-syntax-in-clojure).

{% highlight clojure %}
(let [dict {'dup (fn [[x & s] _]
                   (conj s x x))
            '* (fn [[x y & s] _]
                 (conj s (* x y)))}
      program '(5 dup *)]
  (reduce #((dict %2 conj) %1 %2)
          ()
          program))
{% endhighlight %}

Moving the program directly into the `reduce` call saves a couple more characters.

{% highlight clojure %}
(let [dict {'dup (fn [[x & s] _]
                   (conj s x x))
            '* (fn [[x y & s] _]
                 (conj s (* x y)))}]
  (reduce #((dict %2 conj) %1 %2)
          ()
          '(5 dup *)))
{% endhighlight %}


Now all we have to do is remove the linebreaks and extra whitespace, and here we have it, the code from Brandon's tweet!

{% highlight clojure %}
(let [dict {'dup (fn [[x & s] _] (conj s x x)) '* (fn [[x y & s] _] (conj s (* x y)))}] (reduce #((dict %2 conj) %1 %2) () '(5 dup *)))
{% endhighlight %}
