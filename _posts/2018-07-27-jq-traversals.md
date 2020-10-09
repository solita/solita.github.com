---
layout: post
title: Practical JSON handling and Haskell traversals
author: pkalliok
excerpt: >
 jq expressions are, by nature, the same as Haskell's lens library's
 Traversals.  A traversal is a focal object that specifies a place, or
 several, within a bigger data structure.  Traversals are composable and
 you can do both inspection and updates through them.
tags:
 - functional programming
 - composability
 - traversal
 - JSON
 - command line
 - Linux
 - lens
 - Haskell
---

Ever wonder how ``jq``'s language even *works*?  ``jq`` is a great tool
meant for manipulating JSON documents (or data structures, if you want
to see it that way).  It's probably easy enough to see how this works:

```
$ echo '{"foo":{"bar":1},"baz":2}' | jq .foo.bar
1
```

It's basically a simple composition of two projection functions, the
first takes the "foo" key of a map, and the second takes the "bar" key.
``jq`` documentation is generous enough to tell us that ``.foo.bar`` is
actually an abbreviation for ``.foo|.bar``, where pipe ("|") is the
``jq`` notation of function composition.

But how about this?

```
$ echo '[{"foo":3},{"foo":4},{"bar":5}]' | jq .[].foo
3
4
null
```

Now there are three distinct results, which means that ``jq`` functions
don't return just one value but 0..n.  And the ``.foo`` function gets
called for each result of ``.[]``, which means that evaluating the
composition of two ``jq`` functions is quite like the monadic bind in
the indeterminism (ie. list) monad.  We can readily verify this by
writing "flatten" in ``jq``:

```
$ echo '[[1,2],[3],[4,5,6]]' | jq '.[]|.[]'
1
2
3
4
5
6
```

So far, what we have seen is roughly the equivalent of XPath
expressions, like other expression oriented languages that select parts
of a data structure (like a document tree).  ``jq`` has equivalents for
XPath selectors etc:

```
$ echo '[[1,2],[3],[4,5,6]]' | jq '.[]|select(length > 1)|.[]'
1
2
4
5
6
$ echo '[[1,2],[3],[4,5,6]]' | jq '.[]|.[]|select(.%2==0)'
2
4
6
```

(The dot (".") is the ``jq`` name of the identity function, i.e. the
accessor for whatever input an expression gets.)

``jq`` is a function-oriented language in the same way that
concatenative languages are.  Every expression is actually a function
from one input to 0..*n* outputs, even ``2``, which takes an input and
produces exactly one 2.  This principle also means that operators (like
``+``) produce functions, not direct values, and are *distributive* in
the way that whatever input ``+`` gets, it gives to both of its argument
expressions (which are, of course, also functions).

```
$ echo '[[1,2],[3],[4,5,6]]' | jq '.[]|.[]|2'
2
2
2
2
2
2
$ echo '[[1,2],[3],[4,5,6]]' | jq '.[]|length + .[0]'
3
4
7
```

Of course, the argument functions of ``+`` (or other operators) can also
produce multiple results, and in these cases, ``+`` forms its results
(sums) from a cross product of the results of its arguments, much like
the ordinary ``+`` function when it is lifted into the indeterminism
monad:

```
$ echo '[[1,2],[3],[4,5,6]]' | jq -c '.[]|[.[]+.[]]'
[2,3,3,4]
[6]
[8,9,10,9,10,11,10,11,12]
```

But it gets weirder.  It turns out that whatever result (be it singular
or a list of results) can be used as a context for making updates.  For
instance, to delete the second item of every sublist, we can do:

```
$ echo '[[1,2],[3],[4,5,6]]' | jq -c '.[]|del(.[1])'
[1]
[3]
[4,6]
```

If we want to get the original list as a result (but with updates), we
can do it this way:

```
$ echo '[[1,2],[3],[4,5,6]]' | jq -c 'del(.[]|.[1])'
[[1],[3],[4,6]]
```

There's a whole lot of "destructive" operations, only they are *not*
destructive; they return the original data structure with modifications.
But somehow magically, they know from a functional (and compositional)
specification exactly which place(s) in the data structure they should
modify:

```
$ echo '[[1,2],[3],[4,5,6]]' | jq -c '(.[]|.[1]) += 3'
[[1,5],[3,3],[4,8,6]]
```

So, how does it all work?

``jq`` expressions are, by nature, the same as Haskell's lens library's
[Traversals](http://hackage.haskell.org/package/lens-4.15.3/docs/Control-Lens-Traversal.html).
A traversal is a focal object that specifies a place (or several) within
a bigger data structure.  Traversals are composable (meaning, you can
combine two traversals if one of them produces what the other consumes)
and you can do both inspection (viewing) and updates through them.

You can also make combinators for traversals, such as a concatenation
operator that gives the same input to two traversals and produces the
output of both (this combinator is called "," in ``jq``).  ``jq``'s
``.[]`` is Haskell's "traverse", a traversal taking a single value and
focusing on each of its parts.  In Haskell, it works for every
traversable data structure; in JSON, there are only two (list and map).

``jq`` combines this functional framework with a weird, terse syntax,
and a function-oriented language that skips explicit parameters and
where every expression is a traversal.  This makes composite expressions
(such as ``del(...)``) functions from traversals to traversals; and
simple binary operators (such as ``>``), functions (traversal,
traversal) -> traversal.

This means that it's *really* hard to understand the true nature of an
update-oriented, binary operator such as ``+=``.  It takes two
parameters, the first of which it treats as a traversal to update over,
the second specifying a traversal that produces values that are added in
the update (but as there might be several, it also produces as many
results as the second input).

```
$ echo '[[1,2],[3],[4,5,6]]' | jq -c '(.[]|.[1]) += ([.[0][0],5]|.[])'
[[1,3],[3,1],[4,6,6]]
[[1,7],[3,5],[4,10,6]]
```

An interesting source of confusion is that when a traversal is updated
over, it produces one result (the whole data structure the traversal is
played on) irrespectible of how many places the traversal focuses on,
but when a traversal is viewed, it produces more results for each focus
point.  That's why you see two results above (because ``+=`` is a view
as it comes to its right-hand argument), but not three or six (because
``+=`` is an update as it comes to its left-hand argument).  But if I
feed many inputs to the traversal formed by ``+=``, I get results for
each of them:

```
$ echo '[[1,2],[3],[4,5,6]]' | jq -c '.[]|((.[0],.[2]) += (length,1))'
[3,2,2]
[2,2,1]
[4,null,1]
[4,null,1]
[7,5,9]
[5,5,7]
```

I think ``jq``, and its effective use, is a great way to come to understand
the point of Haskell's traversals (and lenses, prisms and iso's in
general).  It's a very modern example of what an expression-oriented
data structure language is like.  

I haven't touched much the practical aspects of ``jq`` or its vocabulary
here; my examples are more to demostrate the compositionality of ``jq``
expressions.  ``jq`` is a great tool to everyone's toolpack; so much so
that nowadays I think that command-line XML handling is better done by
cross-tripping to JSON, and also some traditional uses of AWK (or
similar data-handling) are better handled with ``jq``.

However, I also recommend delving into traversals, because they provide
a very good option to expression-oriented updates; somewhat better, in
my opinion, to traditional BCPL-language family lvalues, or Common
Lisp's ``(setf)``.  However, their current implementation in Haskell is
kind of "over-nifty" in the way that they play games with the language's
type system to get function composition (.) work as traversal
composition, and get the built-in "traverse" to work as a traversal.  As
a result, the types of traversals are unintelligible, and error messages
abysmal.  These problems are also discussed in the [Lens tutorial](http://hackage.haskell.org/package/lens-tutorial/docs/Control-Lens-Tutorial.html#g:7).

