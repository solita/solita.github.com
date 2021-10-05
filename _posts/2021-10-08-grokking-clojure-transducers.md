---
layout: post
title: Grokking Clojure transducers
author: eerohe
excerpt: >
  Transducers are great and if you're not already using them, you're a terrible person and you should feel bad.
tags:
 - clojure
 - transducers
 - programming
---

So you're a Clojure programmer and you need to apply many transformation steps to a collection of items. Like, for example, you have a big list of things, and you need to remove some of them, transform others, then remove duplicates. What do you do?

The stock approach is to reach for the thread-last macro (`->>`). It's a fine implement for skinning this particular cat, but, well... what if I told you there's another way? In Clojure, we have this thing called [transducers](https://clojure.org/reference/transducers). They were made for precisely this sort of thing.

In this article, it is my noble aim to instill in you an intuition for transducers. We'll start by examining the building blocks of transducers to see how they work. We'll then make a couple of transducers of our own. Finally, we'll look at how you can apply your newfound knowledge of transducers in the real world.

You're in the target audience of this article if:

* you're a Clojure programmer who hasn't paid much attention to transducers up until now, or,
* you're not a Clojure programmer, but you understand what the `reduce` function does, and you're curious about transducers.

If you already know how `reduce` works, you probably also know what a reducing function is. If you don't, though, you're in luck, because that's where we'll set forth on our exciting adventure into the wonderful world of transducers.

## First steps

To understand transducers, you must first understand reducing functions. So what's a reducing function?

A **reducing function** is a function you can use as the first argument of  `reduce`. A reducing function takes an **accumulated result** and an **input** and returns a **new result**.

`conj` is an example of a reducing function. It takes a collection (the result we've accumulated so far) and an item (the input) and adds the item into the collection (the new result).

Here's an example of using `conj`:

```clojure
(conj [1 2] 3)
;;          ^ input
;;    ^^^^^ accumulated result
;;=> [1 2 3]
;;   ^^^^^^^ new result
```

Since `conj` is a reducing function, let's try using it with `reduce`. Here, we use `conj` to add every number in the given Clojure vector (`[1 2 2 3 1]`) into an empty hash set (`#{}`):

```clojure
(reduce conj #{} [1 2 2 3 1])
;;=> #{1 3 2}
```

Cool! We got what we expected: a set that contains each distinct number in the input collection.

Now that we know what reducing functions are, let's discuss how they relate to transducers.

<!-- ## Making our first transducer -->

In essence, a **transducer** is *a function that takes a reducing function* (like `conj`) and *turns it into a new, more awesome reducing function*. Let's give it a try. Let's make a transducer called `inc-transducer`:

```clojure
(defn inc-transducer
  "Given a reducing function rf, return a new reducing function that increments
  every input it receives, then calls rf with the result and the incremented
  input."
  ;; rf stands for "reducing function"
  [rf]
  ;; this here's a new reducing function
  (fn [result input]
    ;; here we call the original reducing function
    (rf result (inc input))))

;; If you already know transducers, you'll notice that inc-transducer doesn't
;; actually have everything a real, production-grade transducer needs to have.
;; Don't worry, we'll get there.
```

We've made our first transducer! `inc-transducer` takes a reducing function like `conj` and returns a modified version of it. Let's give it a try:

```clojure
(def inc-then-conj (inc-transducer conj))
;;=> #'user/inc-then-conj
(inc-then-conj [1 2] 3)
;;=> [1 2 4]
```

What is `inc-then-conj` supposed to do again? Let's recap. It should:

1. Increment the input `3` by one to get `4`.
2. Add the incremented input `4` into the result to get `[1 2 4]`.

Looks like it works! Can we use it with `reduce`, like we did with `conj`?

```clojure
(reduce inc-then-conj [] [1 2 3 4 5])
;;=> [2 3 4 5 6]
```

Boom! When used with `reduce`, `inc-then-conj` incremented every input, then added each incremented input into the result vector (`[]`).

Of course, we can give `inc-transducer` *any* reducing function, not just `conj`. Let's try to use it to transform some other reducing function. Let's pick `+`, which, happily, is also a reducing function:

```clojure
(reduce (inc-transducer +) 0 [1 2 3 4 5])
;;=> 20
```

It worked! When we used `inc-transducer` with `+`, for each number in the input collection, it incremented the number, then added it into the accumulated sum.

However... what if there comes a day when we want to do something else than increment a number? That's all `inc-transducer` lets us do, increment numbers! What to do?

I think it was Benjamin Franklin who used to say, "Functions are like violence: if it's not working, you're not using enough of it. Or them. Or whatever, you know." Stimulated by this enlightening adage, let us beat this problem into submission by employing an additional function. Instead of baking in `inc` as the function that transforms the input, let's make a new function. This new function takes any function and uses it to transform the input. Here's the new function:

```clojure
(defn mapping
  "Given function f, return a transducer that calls f on every input it
  receives."
  [f]
  (fn [rf]
    (fn [result input]
      (rf result (f input)))))
```

Our brand new function bears the inspired name of `mapping`. `mapping` is not a transducer. It is a function that **takes a function** and **returns a transducer**. Let this illuminating example shed light on this mystical conundrum of a function:

```clojure
(def inc-mapper
  "Given a reducing function rf, return a reducing function that increments its
  input before calling rf."
  (mapping inc))

(def inc-rf
  "A reducing function that increments its input, then adds it into the
  accumulated result."
  (inc-mapper conj))

(reduce inc-rf [] [1 2 3 4 5])
;;=> [2 3 4 5 6]
```

Right on! We've reimplemented `inc-transducer` without baking in `inc` into the reducing function.

Although... haven't we just reimplemented `map`, kinda?

```clojure
(map inc [1 2 3 4 5])
;;=> (2 3 4 5 6)
```

It might indeed appear so at first, but there are crucial differences that set the transducer version apart from plain old mapping. That's what we'll focus on next.

## What's so special about transducers?

The first difference between using `map` and using a transducer is this: with `map`, the reducing function "at the bottom" is always `conj`. `conj` is baked into `map` -- there's no way to pull it out of there.

With transducers (like the one `mapping` returns), on the other hand, we can decide which reducing function to use. For example, we can use `+`, like earlier:

```clojure
;; This is otherwise equivalent to the previous example, but we're just
;; forgoing the intermediate vars `inc-mapper` and `inc-rf`, and passing in `+`
;; instead of `conj`.
(reduce
  ((mapping inc) +)
  0
  [1 2 3 4 5])
;;=> 20
```

Secondly, notice how the transformation (incrementing numbers) is distinct from how the final output is built. In other words, `(mapping inc)` does not say anything about how to make the final value. This is a crucial feature of transducers: they allow you to define transformations that do not know or care what happens once the transformation is complete. Put another way, `(mapping inc)` only says "increment numbers", while `(map inc [1 2 3 4 5])` says "increment numbers and then add them into a new list".

This decoupling of the transformation from its inputs and outputs has important repercussions. For one, it means we can also use transducers with things like `clojure.core.async` channels (which, if you don't know, are these things that look a bit like queues, if you squint). Before transducers, `core.async` used to have its own `map`, `filter`, etc. implementations. Transducers, because they're so awesome, have made them unnecessary, so they have since been deprecated. Now, you can just sort of stick a transducer to a channel and the transducer transforms whatever you put in the channel.

Here's another very important distinction between transducers and traditional methods of transforming collections. Let's say we want to transform the input collection in more ways than one. For example, let's say that we only want to increment every **even** number in the input collection. Faced with a case like this, most Clojure programmers reach for the thread-last macro (`->>`):

```clojure
(->>
  [1 2 3 4 5]
  (filter even?)
  (map inc))
;;=> (3 5)
```

The thread-last macro is eminently readable, but using it comes at a cost. When we use the thread-last macro, after every step of the transformation process, we create an intermediate collection, only to immediately throw it away. Let's spell that out:

```clojure
(->>
  [1 2 3 4 5]
  (filter even?) ;; intermediate collection (2 4), discarded immediately
  (map inc) ;; final result (3 5)
  )
```

Here, we throw away the result of the filtering step (`(2 4)`) immediately after making it. What a waste! With transducers, we can make the same transformation without making a single unnecessary intermediate collection. Before we can do that, though, we have to make a function that's like `mapping`, but it's, uh... `filtering`.

```clojure
(defn filtering
  "Given a predicate function pred, return a transducer that only retains items
  for which pred returns true."
  [pred]
  (fn [rf]
    (fn [result input]
      (if (pred input)
        (rf result input)
        result))))
```

Like `mapping`, `filtering` is a function that takes a function and returns a transducer. However, `filtering` is different from `mapping` in that it only calls its reducing function if the input matches the predicate function you give it.

Now that we have `filtering`, we can compose a multi-step transformation powered by transducers. Watch this:

```clojure
(def rf
  "A reducing function that filters even numbers, increments every remaining
  number, then conjoins them into the result."
  ((comp (filtering even?) (mapping inc)) conj))

(reduce rf [] [1 2 3 4 5])
;;=> [3 5]
```

Blammo! Filtering and mapping in one fell swoop, with zero intermediate collections. Of course, in this example, the transformation has few steps and its input is small, so there's probably no perceptible performance difference compared to the thread-last version. The larger your input is and the more steps your transformation has, [the more significant the performance gains will be](https://www.grammarly.com/blog/engineering/building-etl-pipelines-with-clojure-and-transducers/).

You might be wondering about the `comp` there. `comp` (short for "compose") is the most common way to make multi-steps transformations with transducers -- or *compose* transducers, if you will. Notice how the order of operations is the same with `comp` as with `->>`:

```clojure
(,,,
 (comp
   (filtering even?)
   (mapping inc))
 ,,,)

(->>
  [1 2 3 4 5]
  (filter even?)
  (map inc))
```

Here's another way to think about the difference between the thread-last macro and transducers:

The thread-last macro *transforms collections*. Transducers, in turn, *transform reducing functions*. You can then use those reducing functions to transform things, without caring where those things come from and where they go, without generating any waste in the process.

With all that out of the way, let's move onto discussing how you'd actually use transducers in your code.

## Using transducers in the real world

So far, to illustrate how transducers work, we've been creating our own transducers and using them with `reduce`. In the real world, you rarely need to do the former, and the latter probably never.

Now, uh... there's something I must confess. We did not actually need to define `mapping` and `filtering` ourselves. Giving only the first argument to the `map` or `filter` core functions actually returns a transducer. That means we can simply replace `filtering` and `mapping` in our previous example with `filter` and `map`, like so:

```clojure
(reduce
  ((comp (filter even?) (map inc)) conj) ;; <- reducing fn (awesome conj)
  [] ;; <- initial value
  [1 2 3 4 5] ;; <- input collection
  )
;;=> [3 5]
```

Besides `map` and `filter`, there's [a whole bunch of functions](https://clojure.org/reference/transducers#_defining_transformations_with_transducers) in the Clojure core that return a transducer when you give them all the arguments you usually do, *except* for the input collection (the last argument).

Also... I've got another confession to make. `mapping` and `filtering` are not "real" transducers. Each transducer is a function that can take either one, two, or three arguments. Since that is something you only really need to know when you're creating your own transducers (which is not likely to be all that often), we won't discuss that detail here. If you want to know more about the different arities of proper transducers, check out [the official documentation](https://clojure.org/reference/transducers#_creating_transducers).

So if we shouldn't use `reduce` with transducers, what should we use? There are four functions in the Clojure core that take transducers as arguments:

* `transduce`
* `into`
* `sequence`
* `eduction`

Next, we'll take a brief look at what each function is good for. We won't go too deep here, so after you're done reading this article, make sure you read the docstring for each function and [the official reference](https://clojure.org/reference/transducers#_using_transducers) to get a better understanding of how each function works.

### `transduce`

`transduce` is like `reduce`, but specifically for transducers. To show how `transduce` works, let's rewrite our previous example using `transduce` instead of `reduce`.

```clojure
(transduce
  (comp (filter even?) (map inc))
  conj
  []
  [1 2 3 4 5])
;;=> [3 5]
```

The result is the same. So what's the difference to the `reduce` version? For one, the `transduce` version avoids the slightly awkward `((comp (filter even?) (map inc)) conj)` construction. Also, `reduce` doesn't work perfectly with every kind of transducer, for reasons we won't go into here. The upshot? Don't use transducers with `reduce`. Use `transduce` or one of the other functions we discuss here instead.

Besides that, an important property of `transduce` is that unless you tell it to stop using `halt-when`, `take`, or the like, `transduce`consumes the entire input collection. If you want to be able to consume only a part of the input, consider using `sequence` or `eduction` instead. For a more comprehensive discussion of how `transduce`, `sequence`, and `eduction` consume their inputs, see the section titled "Laziness" in [Renzo Borgatti's article *Clojure transducers from the ground up: the practice*](https://reborg.net/post/621473763865821184/clojure-transducers-from-the-ground-up-the).

### `into`

Use `into` if you want to transform the input collection into a certain type of output collection as fast as possible.

For example, here's an example where we generate an infinite sequence of random numbers, take the first million, remove all odd numbers, multiply each number by ten and finally stick the result into a hash set:

```clojure
(into #{}
  (comp
    (take 1000000)
    (remove odd?)
    (map #(* % 10)))
  (repeatedly #(rand-int 100)))
;;=> #{0 920 580 240 620 20 980 60 360 300 940 260 540 740 460 420 ...}
```

Personally, I tend to use `into` whenever I know I need a particular type of output collection.

Note that `into` doesn't let you choose which reducing function to transform. With `into`, it's always `conj`.

### `sequence`

Use `sequence` whenever you need your transformation to produce a [lazy sequence](https://www.braveclojure.com/core-functions-in-depth/#Lazy_Seqs). There are many situations where you want a lazy sequence. One is when you need to use the transformation result more than once. Check out this example:

```clojure
(def xs
  (sequence
    (comp (filter even?) (map inc))
    (range 100)))

;; in one case, we might need to take the first ten things from `xs`
(take 10 xs)
;;=> (1 3 5 7 9 11 13 15 17 19)

;; later, in another context, we might need to take just the first five numbers
(take 5 xs)
;;=> (1 3 5 7 9)
```

In this example, when we call `take` the second time, the lazy sequence that `sequence` returns has already transformed and cached the first ten values (actually more because performance, but again, let's not go into that) for us and has them handy when we need them. We do not need to transform the input again to get at the values.

Since most transformations that use the thread-last macro yield a lazy sequence, `sequence` might be the most straightforward option for refactoring a transformation that uses the thread-last macro into a transducer-powered one.

### `eduction`

Out of these four functions, I found `eduction` the most difficult to understand when I was first learning about transducers. In a nutshell, if `sequence` is for when you want caching (to reuse the transformation result), `eduction` is for when you don't. One case where you might use `eduction` is [when you want to transform data that you're reading from an external resource, such as a file](https://www.grammarly.com/blog/engineering/building-etl-pipelines-with-clojure-and-transducers/#enter-transducers).

You might also want to choose `eduction` over `sequence` if you know you're going to consume **all** of the final result, and you're only going to do it **once**. There is some overhead to making a lazy sequence, and `eduction` allows you to avoid it when you need to. Don't take this to mean that you should avoid using `sequence`. In most cases, the cost of lazy sequences is negligible.

Here's an example that might clarify the difference between `sequence` and `eduction`:

```clojure
(def xs1
  (sequence
    (map #(do (prn "sequencing!") (inc %)))
    (range 32))) ;; prints "sequencing!"

(prn xs1) ;; prints "sequencing!"
(prn xs1) ;; doesn't print "sequencing!"

(def xs2
  (eduction
    (map #(do (prn "educing!") (inc %)))
    (range 32))) ;; doesn't print "educing!"

(prn xs2) ;; prints "educing!"
(prn xs2) ;; prints "educing!"
```

`sequence` consumes a part of the input sequence when we define `xs1`. When we reference `xs1`, it returns the values it cached when it consumed the input sequence for the first time. Conversely, `eduction` consumes the input sequence only when we reference `xs2`, and does so every time we do it.

Here's another way to think about `eduction`: it lets you bundle just the input collection and the transformation and defer the decision on which reducing function you want to modify and which initial value (accumulated result) you want to use. Here's an example:

```clojure
;; Create a transformation that filters the even numbers between 0 and 99 and
;; increments the remaining numbers.
;;
;; Don't transform anything just yet, though.
(def xf
  (eduction
    (comp (filter even?) (map inc))
    (range 100)))

;; Apply the eduction to sum the transformed numbers.
(reduce + 0 xf)
;;=> 2500

;; Apply the eduction to multiply each number by ten, then add them into a hash
;; set.
(reduce (fn [s n] (conj s (* n 10))) #{} xf)
;;=> #{950 530 410 970 70 430 370 110 ...}
```

Calling `reduce` on an eduction grabs the transducer (the first argument to `eduction`) from the eduction and uses it to transform the reducing function we give to `reduce`. Only then does it carry out the transformation on the input collection that lives inside the eduction.

All right! That's it for the four core functions that take transducers as arguments. All that's left is to wrap things up.

## Final words

In a side note of his fantastic book *Elements of Clojure*, Zach Tellman writes:

> The real value of transducers is not performance, but rather that non-standard data representations like `core.async` channels can use `clojure.core` directly rather than having to define their own `map`, `filter`, and so on.

While that is no doubt the *raison d'être* of transducers, we should not think of them as just this thing that let Cognitect get away with writing less code when implementing `core.async`. For a long time, that was more or less the way I thought about transducers: something that Clojure takes care of for me that I don't really need to think that much about.

I was wrong. After all, much of what we do as Clojure programmers is convert data from one shape into another. For that, transducers are a tremendously useful tool. They let us compose powerful transformations from simple parts, apply those transformations to pretty much anything we want, then, separately, decide how to build the final result of those transformations.

With that, we end this tour of transducers. Naturally, there's much more to transducers than what we've discussed here. If you want to learn more about them, see [the official reference for transducers](https://clojure.org/reference/transducers#_creating_transducers). Hopefully, reading this article has made it a bit easier to understand.

Note that you might be able to use transducers even if you don't use Clojure. There are implementations for [Java](https://github.com/cognitect-labs/transducers-java), [JavaScript](https://github.com/cognitect-labs/transducers-js), [Python](https://github.com/cognitect-labs/transducers-python), [Ruby](https://github.com/cognitect-labs/transducers-ruby) and probably other languages as well.

## Acknowledgements

Thanks to Pedro Girardi for his valuable feedback on an earlier version of this article.
