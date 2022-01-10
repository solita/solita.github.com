---
layout: post
title: Spice up your JavaScript with curry
author: vesala
excerpt: Functional programming comes with a plethora of jargon. Let us delve deeper into the technique called currying.
tags:
  - JavaScript
  - functional programming
  - currying
  - functional composition
---

# Spice... what? (What are curried functions and how to implement them in JavaScript?)

Most of us know curry as a delicious food item or a spice blend. While this is true, [_currying_](https://en.wikipedia.org/wiki/Currying) is also a term used in the field of computer science. The Second big thing named after the mathematician/logician [Haskell Curry](https://en.wikipedia.org/wiki/Haskell_Curry).

Currying is an extremely powerful technique and it should be essential for every developer to have basic understanding about it in their toolbox. It truly enables us to write functional code with heavy emphasis on reuse, testing and robustness on the solutions we implement.

Currying refers to a technique of turning a function that accepts _multiple parameters_ (`variadic`) to a function that accepts a single parameter (`unary`) at a time. It turns a function into a function that sums two numbers, most of us would write it as a function that accepts numbers `a` and `b` and returns the sum.

```javascript
// using arrow function expression style
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions
const add = (a, b) => a + b;

// using function expression style
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/function
function add(a, b) {
  return a + b;
}
```

Manually currying this function would look like this:

```javascript
// using fat arrow
const add = (a) => (b) => a + b;

// using function keyword
function add(a) {
  return function (b) {
    return a + b;
  };
}
```

In addition to currying there are also [_partially applied_](https://en.wikipedia.org/wiki/Partial_application) functions. The significant difference between a curried and partially applied function is that curried functions always take parameters one at a time (unary) while partially applied functions can be called multiple parameters at a time (variadic).

```javascript
// function for summing 3 numbers
const add = (a, b, c) => a + b + c;

// curried function
const curriedAdd = (a) => (b) => (c) => add(a, b, c);
const curriedAdd2 = curriedAdd(2);
const curriedAdd5Add2 = curriedAdd2(5);
curriedAdd5Add2(10) === 17; // true

//partially applied function
const partialAdd2 = add.bind(null, 2);
partialAdd2(5, 10) === 17; // true
isNaN(partialAdd2(5)); // true
```

However, in this form, both currying and partial application comes with caveats. You cannot call a curried function written in this form with multiple parameters at a time, since a normal function that is curried always returns a _unary_ function. This is a function that has an _arity_ of 1 meaning it only takes one argument.

Partial application, however, does not protect you from calling the function with incomplete arguments before evaluating the function, which is what happened on the last row of the previous example. With currying the function is invoked lazily and it runs only after getting all the parameters.

Currying with a language that does not natively understand currying is a chore. In ML-type languages (f.ex. F#) all functions are automatically curried, and the syntax supports that with proper developer ergonomics.

```fsharp
// F# example of curried function
let add a b c = a + b + c

let add2 = add 2
let add5add2 = add2 5
(add5add2 10) = 17 // true

// However with F# we can skip phases here
let add5add2 = add 2 5
(add5add2 10) = 17 // true

// Or with more brevity
(add 2 5 10) = 17 // true
```

As you can see, in ML-style languages, developer ergonomics are present and you can pass any number of arguments at once into a curried function. This style can be achieved in JavaScript using a helper function.

```javascript
const curry = (fn) =>
  function _curry(...args) {
    return args.length >= fn.length
      ? fn(...args)
      : (...args2) => _curry(...args, ...args2);
  };

// As an aside, this is the last part where I use the function keyword.

const add = curry((a, b, c) => a + b + c);

// now these all should be equivalent
add(2, 5, 10) === 6; // true
add(2)(5, 10) === 6; // true
add(2, 5)(10) === 6; // true
add(2)(5)(10) === 6; // true
```

The curry-function is a wrapper for any variadic function. It either invokes the function when enough parameters have been passed to it or returns a function that awaits more parameters.

# Spice... why? (What does curried functions enable?)

Now this is a good question. With examples like adding a few numbers the value proposition is not clear. However the above techniques have unlocked the potential to turn any function into a _higher order function_.

Higher order functions are functions that can accept and return functions. This elevates our functions into [first class citizens](https://en.wikipedia.org/wiki/First-class_function) and they should be considered as just variables. With higher order functions we can achieve `functional composition`.

Functional composition in simple terms is taking 2 functions and combining them into one function where internally one function's output is provided as an input to the other function. If you have ever used pipe operations in unix, this is similar.

Let us create a function that composes multiple functions into a single function.

```javascript
const compose =
  (...fns) =>
  (arg) =>
    fns.reduceRight((arg, fn) => fn(arg), arg);

// note: I like reading compositional definitions in reverse.
// Arguments come last so the reading direction naturally starts there.
// This choice is purely stylistic and it will vary by language ecosystem and project.
```

Functional composition allows us to build new more abstract functions from primitive functions. This way we can assemble our software from highly reusable primitive functions by just building more abstract layers on top of them with composition.

# Spice... must flow? (How to utilize curried functions?)

We just supercharged our ability to write JavaScript. This duo is much like an assembly line for creating new functions based on existing functions. I know just proclaiming that does not make it true. We need examples from real life:

```typescript
// Using TypeScript here since defining types in native JavaScript is a path to insanity
type Employee = {
  firstName: string;
  middleNames: string[];
  lastName: string;
  gender: string;
  salary: number;
};
```

## Problem 1: Write a function that returns median salary from a list of employees.

```javascript
// We need a function that returns a salary from an Employee object
const salary = (employee) => employee.salary;

// We need a function that sorts given list in ascending order
const sortAscending = (list) => list.sort((a, b) => a - b);

// We need a function that returns the middle item
const medianOdd = (list) => list[Math.floor(list.length / 2)];

// And a function that returns average of summed middle items even numbered lists
const medianEven = (list) => {
  const middleIndex = Math.floor(list.length / 2);
  return (list[middleIndex] + list[middleIndex + 1]) / 2;
};

// We need a function that returns the item in the center of list or average of
// 2 middle items in lists that contain even number of items
const median = (list) =>
  list.length % 2 === 0 ? medianEven(list) : medianOdd(list);

// We need a mapping function that takes a list of employees and returns their salaries
const salaries = (list) => list.map(salary);

const medianSalaries = compose(median, sortAscending, salaries);
```

This is a naive solution for the given problem. However functional composition enables us to reuse code in our codebase. The solution above does allow that but in a limited quality. Let's rewrite it with future reuse in mind by generalizing the solution.

```javascript
// Function that returns a salary, could be generalized as a function that returns
// a property of an object
const prop = curry((key, obj) => obj[key]);

// Sorting function should take in the sorting function
const sort = curry((sortFn, list) => list.sort(sortFn));

// With this we can create a function for ascending order
const subtract = curry((a, b) => a - b);
const ascending = sort(subtract);

// note: we could implement a flip function for descending order,
// flip is a function that takes 2 arguments and flips their order in the invoked function.
const flip = (fn) => curry((arg1, arg2) => fn(arg2, arg1));
const descending = sort(flip(subtract));

// The length itself is a property on an array object
const length = prop("length");

// The median function is a little tricky, since it requires the given list for 2 things.
// First sorting in ascending order and then accessing the element from the center.
// For this we implement some combinatory magic and auxiliary functions. Nothing too fancy.

// First we need a function that returns nth item from a list
const nth = curry((n, list) => list[n]);

// Then we need a way to somehow run in "parallel" the calculation for the middle index and
// sorting in ascending order, then we need to converge these values into the nth-function.

const applyTo = curry((value, fn) => fn(value));
const apply = curry((fn, args) => fn(...args));
const map = curry((fn, list) => list.map(fn));

const converge = curry((convergingFunction, branches, value) =>
  compose(apply(convergingFunction), map(applyTo(value)))(branches)
);

// Confused? No worries, this is a lot simpler than it looks. We just created a function that
// runs the given value against every branch that we supply it with. Then it just applies the
// branching functions return values to the converging function. It should clear up when we
// implement median with this. However, we still need a few functions to implement it.

const add = curry((a, b) => a + b);
const divide = curry((a, b) => a / b);
const floor = (n) => Math.floor(n);
const middleIndex = compose(floor, flip(divide)(2), length);
const slice = curry((index, amount, list) => list.slice(index, index + amount));

// Now the 2 cases of median
const medianOdd = converge(nth, [middleIndex, ascending]);
const medianEven = (employees) =>
  compose(
    flip(divide)(2),
    apply(add),
    slice(middleIndex(employees), 2),
    ascending
  )(employees);

// Just for the fun of it, let's wrap ifElse branching into a function.
const ifElse = curry((pred, ifT, ifF, value) => pred(value) ? ifT(value) : ifF(value));

// Generic isEven-function
const equals = curry((expected, value) => expected === value);
const mod = curry((a,b) => a % b);

const isEven = compose(
  equals(0),
  flip(mod)(2)
);

const median = ifElse(compose(isEven, length), medianEven, medianOdd),

// Voilà. Median implemented with combining very primitive functions. Now to generalize this
// for lists.

const pluck = curry((property, list) => map(prop(property), list));

const medianSalary = compose(median, pluck("salary"));
```

## Problem 2: Write a function that returns average salary from a list of employees.

Considering we implemented a bunch of generalized functions in the previous solution, we can reuse them:

```javascript
// We need a function that sums up a list of numbers
const reduce = curry((fn, initialValue, list) => list.reduce(fn, initialValue));
const sum = reduce(add, 0);

// Now combining with the previous example, we have all we need.
const average = converge(divide, [sum, length]);

const averageSalary = compose(average, pluck("salary"));
```

## Problem 3: Write functions for gender based average salaries

Still reusing the same functions:

```javascript
// This is just filtering based by gender and then running the average function
const filter = curry((fn, list) => list.filter(fn));
const propEq = curry((expectedProp, expectedValue, obj) =>
  compose(equals(expectedValue), prop(expectedProp))(obj)
);

const averageGenderSalary = curry((gender, employees) =>
  compose(averageSalary, filter(propEq("gender", gender)))(employees)
);

const averageMenSalary = averageGenderSalary("male");
const averageFemaleSalary = averageGenderSalary("female");
const averageOtherSalary = averageGenderSalary("other");
```

## Problem 4: Write a function that formats an employees name in the form of {firstName} {middleName initials separated by .} {lastName}:

```javascript
const join = curry((separator, list) => list.join(separator));
const toUpper = (str) => str.toUpperCase();
const head = (list) => list[0];

const fullName = compose(
  join(" "),
  converge(Array.of, [
    prop("firstName"),
    compose(join("."), map(head), prop("middleNames")),
    prop("lastName"),
  ])
);
```

At this point it is hopefully clear how easy combining functions with composition is.

This type of composition is achieved by having a set of curried functions that can be partially applied as a basic building block.

# Spice... controls the universe? (Pros and cons of curry functions?)

No. This is not the end of all techniques. As with everything there are upsides and downsides, a perfect balance of pros and cons.

There is no silver bullet. This style of _tacit programming_ or _pointfree programming_ requires some time to get used to and in some places, it can get incredibly obscure to read. For people not versed in functional programming these lines of code might seem like some dark invocations. Also, with this style at least from my point of view TypeScript is completely out of the question.

And then there is the worst of them all; debugger support stepping over this kind of code in JavaScript is futile. You are restricted to debugging single functions at a time. However logging as a debugging strategy has existed for a long time and with a simple helper function we can add logging to our composes trivially.

```javascript
const tap = curry((fn, value) => {
  fn(value);
  return value;
});

const log = tap(console.log);

compose(
  log, // 5
  add(1),
  log, // 4
  subtract(9)
)(5);
```

# Spice... conclusion

I personally am very enthusiastic about this style of programming. All functions I created in previous examples are pure functions and have single responsibilities. Pure functions mean they have no side-effects. They do not depend on some global state that tends to change during the lifetime of an application. They are referentially transparent, so they always return the same output with the same input. This should make f.ex. [memoization](https://en.wikipedia.org/wiki/Memoization#:~:text=In%20computing%2C%20memoization%20or%20memoisation,the%20same%20inputs%20occur%20again.) a breeze.

As for testing, pure functions with a single responsibility make unit testing the functions completely trivial. Just remember to reuse things built in the past, you should not implement these foundational functions by yourself as there are plenty of tested and supported libraries such as [lodash/fp](https://github.com/lodash/lodash/wiki/FP-Guide) and [Ramda](https://ramdajs.com/).

The big idea is that, when the foundational pieces are built out of simple reusable Lego blocks that have no side effects, I can rest assured that when I compose these foundational parts with side effects eventually, I will have built the system on solid foundations.

I left out a hefty amount of pure theory that I myself might not even understand correctly. However there is a place and a time for chewing pure theory and the perfect one might be in a hot tub preferably during [Solita DevDay](https://dev.solita.fi/2021/12/13/devday-of-solita.html). So if you feel that I left out some essential parts or am purely wrong in some places, you know where and when to find me.
