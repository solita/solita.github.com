---
layout: post
title: What is a list anyway?
author: tatut
excerpt: >
  Programmers work with lists every day, but what are they?
  Take a look at some wisdom of the ancients on how to work
  with lists properly.
tags:
 - Prolog
 - LISP
---

As programmers, we work with lists all day every day... any time you have more than one of something,
you will most likely make a list. Having nothing or having one of something can be considered
special cases... and the common case is to have `N` somethings.

Because lists are so ubiquitous, all higher-level programming languages provide types or classes to
work with lists, this usually includes creating lists, selecting items from lists, processing the
items of a list and so on.

*But what is a list in its essence?*

If we go back to 1958 when John McCarthy discovered the LISP (short for LISt Processor), we can see
that a list boils down to simply a pair of values: an element and a pointer to the next pair.
In LISP this is called the *cons cell* and its slots are called [CAR and CDR](https://en.wikipedia.org/wiki/CAR_and_CDR)
respectively.

So we can see that "a list" is not a thing in and of itself, but rather an amalgamation of
cons cells. Many Object Oriented programming languages, like Java, provide a [List class](https://docs.oracle.com/javase%2F8%2Fdocs%2Fapi%2F%2F/java/util/List.html)
which differs from the original lispy view of things and models the whole instead of the part.

In this post, we will take a look at what programming in lists means, but we won't be using LISP (or
any of its many successors), but the declarative logic language [Prolog](https://en.wikipedia.org/wiki/Prolog).
All examples work with the free [SWI-Prolog](https://www.swi-prolog.org) implementation.


## List basics

Prolog, like LISP and many other languages, has a built-in syntax for lists. Prolog uses square brackets
and commas:

```prolog
?- Languages = [lisp, c, assembly].
Languages = [lisp, c, assembly].
```

We can also destructure a list into its *head* (the first element) and *tail* (the rest of the list)
using the `|` character.

```prolog
?- [One|Rest] = [1,2,3,4].
One = 1,
Rest = [2, 3, 4].
```

The last element is the empty list:
```prolog
?- [First|NothingMore] = [1].
First = 1,
NothingMore = [].
```

We can also check the members of a list:
```prolog
?- member(X, [1,2,3]).
X = 1;
X = 2;
X = 3.

?- member(3, [1,2,3]).
true

?- member(42, [1,2,3]).
false
```

## Basic utilities

What do we usually do with a list? Well, we need to go through its items, for example, to do something
for each item. We must be able to create new lists and take apart lists.

To map a goal to each element we can use `maplist`:

```prolog
?- maplist(succ, [1,2,3,4], PlusOnes).
PlusOnes = [2, 3, 4, 5].
```

Here we can see the difference of Prolog to "regular" programming as `maplist` isn't a procedure that
"returns" a new list. What we are declaring is a relation from one list to another and we can do it
the other way as well or use it to check if the relation holds for the given parameters:

```prolog
?- maplist(succ, MinusOnes, [1,2,3,4]).
MinusOnes = [0, 1, 2, 3].

?- maplist(succ, [1,2], [2,3]).
true.
```

Next, let's define relational versions of the usual list functions: drop (remove N items from front)
and take (take only the N first items of the list).

```prolog
drop(0, Lst, Lst).
drop(N, [_|Rest], Out) :-
  N > 0,
  N1 is N - 1,
  drop(N1, Rest, Out).
```

Above you can see we define two clauses. The first states that when dropping 0 elements
from a list, the output list is the list itself. The second states that for a positive
number N, the first element of the input list is discarded, and then a recursive clause
is added for N-1.

Similarly, we can define take as:
```prolog
take(0, _, []).
take(N, [I|Items], [I|Taken]) :-
  N > 0,
  N1 is N - 1,
  take(N1, Items, Taken).
```

Again we have a recursive definition with a base case of taking zero items, but here
the output of taking zero items from anything is the empty list.

We can now use both of these definitions:
```prolog
?- drop(2, [1,2,3,4], Dropped).
Dropped = [3, 4].

?- take(3, [42, 1, 2, 3, 4], Taken).
Taken = [42, 1, 2].
```

As these are relations, can we run them the other way? Yes, somewhat.

```prolog
?- between(1,3,N), drop(N, Input, [1,2,3]).
N = 1,
Input = [_, 1, 2, 3];

N = 2,
Input = [_, _, 1, 2, 3];

N = 3,
Input = [_, _, _, 1, 2, 3].
```

We can state that the result of dropping N items is the list `[1,2,3]` and Prolog
will give us the possible input lists, but all the items before will be
placeholders that can refer to anything.

But we can further constrain the list and state that all numbers are between 1 and 3 to
get all possible permutations:

```prolog
?- between(1,3,N), drop(N, Input, [1,2,3]), maplist(between(1,3), Input).
N = 1,
Input = [1, 1, 2, 3];

N = 1,
Input = [2, 1, 2, 3];

N = 1,
Input = [3, 1, 2, 3];

N = 2,
Input = [1, 1, 1, 2, 3];

N = 2,
Input = [1, 2, 1, 2, 3];

% ...many results omitted...

N = 3,
Input = [3, 3, 3, 1, 2, 3].
```

## Enter append

Of course, a language must also have a way to concatenate lists. For this, we have `append` which comes
in two forms: append two lists to get a third one and append a list of lists to get all of them concatenated.

```prolog
?- append([h,e], [l,l,o], Out).
Out = [h, e, l, l, o].

?- append([[1,2], [3,4], [5,6]], All).
All = [1, 2, 3, 4, 5, 6].
```

Pretty simple... a utility found in most languages.
What if I told you that the above utilities of `drop` and `take` aren't needed
because we have `append`? How can appending lists be used to split them apart, I hear you ask.
Remember that we are describing a relation between the parameters, so can do drop and take like:

```prolog
?- length(Dropped, 3), append(_, Dropped, [1,2,3,4,5,6]).
Dropped = [4, 5, 6]

?- length(Taken, 3), append(Taken, _, [1,2,3,4,5,6]).
Taken = [1, 2, 3]
```

We can even use the second list of lists form to split a list at
given element and extract it:
```prolog
?- length(Before, 3), append([Before, [Fourth], After], [1,2,3,4,5,6]).
Before = [1, 2, 3],
Fourth = 4,
After = [5, 6]
```

If we don't specify the length of the `Before` list, Prolog will give us
results for all different possible lengths of `Before` and `After` including empty,
allowing us to effectively iterate the items with lookback and lookahead. Neat!

## Where we're going, you won't need objects

Many programming languages, like JavaScript and Clojure, also have direct syntax for creating
key/value mappings that can be accessed by key. Hashtables are obviously good for performance
when you have big mappings, but many LISP and Prolog programs traditionally use association
lists. You can model the same information as a list of key/value pairs.

For many cases with small mappings, like arguments to some call or the fields of an object,
the cost of hashing means the difference between a list vs a hashtable is negligible.

For example, SWI-Prolog JSON library represents an object as a compound term `json([Key=Value, ...])`
by default. This makes the list of fields easily accessible with Prolog list processing. We can easily
access the value of a specific key with the standard list membership (`member`) predicate.

```prolog
?- Attrs = [firstname="John",lastname="Doe",email="john.doe@example.com"], member(firstname=F, Attrs).
Attrs = [firstname="John", lastname="Doe", email="john.doe@example.com"],
F = "John"
```

Another common example is an environment bindings mapping (like in an interpreter). You can easily
overwrite a key by appending a new mapping to the front of the list. Because lists are just cons cells,
we can create a new cell that contains the new mapping and points to the old list. Very efficient.
We also don't need to remove anything when we exit, just keep using the old unchanged list.

## Closing thoughts

Lists are more than just a type of object. I hope you can see why Lisp and Prolog (and many other functional
programming languages) use lists heavily. They become very handy if the language includes direct syntax
for creating and destructuring lists. Many pattern-matching languages also allow easy destructuring into
the head and tail of a list.
