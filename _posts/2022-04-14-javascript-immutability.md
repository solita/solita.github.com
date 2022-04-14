---
layout: post
title: Writing Immutable JavaScript in 2022
author: jarzka
excerpt: >
  JavaScript was not built for immutability, yet the concept has become more popular in recent years. How can we do it without cooking spaghetti?

tags:
 - JavaScript
 - Immutability
 - Immer
 - ImmutableJS
 - seamless-immutable
 - lodash/fp
 - Rambda
---

One of my colleagues once said that programming is just moving data from one place to another. From a database to a server, from the server to a client, from an application state to pixels on the screen. This data is rarely presented in one form: it needs to be modified, transformed, merged and split in order to be useful in different layers of an application.

Once the data has been baked into a form that is ready to be used, you wouldn't like anyone to change it in the middle of the process, would you? Unfortunately, it is quite possible if your data is mutable. If you are using JavaScript, like many frontend developers, your data is mostly mutable by default - unprotected from an external change.

I have been programming web frontend professionally for more than seven years now. What makes things interesting is that for most of my career I haven't touched JavaScript very much. I'm familiar with the language, but frontend apps that me and my teammates have built have been mainly written in [ClojureScript](https://clojurescript.org) - a Lisp dialect that compiles into JavaScript. Clojure has built-in support for functional programming and immutability, to which I am now highly addicted.

I think this concept of immutability would be useful in the JavaScript world too. Unfortunately, JavaScript, by nature, is highly focused on object-oriented programming and mutable data. Luckily for us, it's still versatile enough for doing functional programming and modifying data immutably. Let's see how.

## Brief Concept of Immutability

Immutability is a simple concept: **an immutable value is some data that cannot be changed**. If you _do_ want to change it, you create a completely **new version of it with the updated data**.

In JavaScript, primitive types like numbers, strings and booleans are **immutable.** Modifications create new values:

```js
let oldString = 'Hello';
// Let's try to modify oldString by transforming the text to uppercase
let newString = oldString.toUpperCase();
```

After this, `newString` contains the modified text `'HELLO'`, but `oldString` still contains the original text `'Hello'`. This means that `toUpperCase` method did not mutate the original string, instead it returned a **new modified copy**.

The same thing happens if you assign a string into a new variable:

```js
let oldString = 'Hello';
let newString = oldString; // This creates a copy of 'Hello'
newString = 'World';
```

After this, `newString` contains the text `'World'`, but `oldString` still contains the original text `'Hello'`. We did not modify it, because `newString` got a **copy of it**! 

_Hold on, can't I just modify 'Hello' to something else by assigning a new value into its variable?_

```js
let oldString = 'Hello';
oldString = 'Hello world!';
```

This doesn't actually change the string `'Hello'` _itself_. Instead, we create a **new string**, which is a modified version of the original text, and assign it to `oldString`. See, when working with immutable data, we never change the data itself, we just create new versions.

## Mutability

In contrast to immutable primitive types, objects and arrays in JavaScript are **mutable**. Modifications truly modify the original data _inside_ them:

```js
let oldPerson = {name: 'Ismo'};
let newPerson = oldPerson; // I assume I'm creating a copy... right?
newPerson.name = 'Seppo';
console.log(oldPerson.name); // Oops, both persons now have 'Seppo' as their name.
```

The same thing happens with arrays:

```js
let oldArray = [];
let newArray = oldArray; // Copy or not?
newArray.push('Hello world');
console.log(oldArray); // Oops, both arrays now have the string 'Hello world'.
```

Objects and arrays in JavaScript are so called _reference types_. We cannot make copies of them as easily as with primitive types, we simple create a **new reference** to the original data. If we make modifications to our "copies", we actually mutate both values.

_So... why is this a problem?_

I don't think mutability is a problem in itself, but it can _cause_ problems if you are not careful. A typical problem is that when a data is mutable, modifications are not easy to predict and track down. This is especially true in large applications.

Consider a simple example in which you have your application `state` stored as a mutable object. You and your teammates have agreed that `setNumbers` is the only way you are allowed to change the numbers in the `state`. This should make changes to the `state` predictable:

```js
let state = {numbers: [1, 2, 3], names: ['Ismo', 'Seppo']};
let setNumbers = (newNumbers) => {
  console.log('I\'m changing numbers to: ', newNumbers);
  // Replace numbers in the state by creating a new state with the new numbers
  state = {...state, numbers: newNumbers}; // We will cover this syntax later in the article
};
```

Later, you mean to read the state and modify it as a copy:

```js
let temporaryNumbers = state.numbers;
let temporaryNumbersPlusOne = numbers.push(1);
// Oops, you have mutated the application state outside of setNumbers!
```

See, it is very easy to _accidentally_ modify mutable state. If the `state` object had been immutable, we could not have made such a mistake. Thus, I believe having immutable values and making modifications only by creating new versions of the old data helps us to write code that is more predictable, safer and also easier to test.

_I sure did a mistake! I want to learn how to work with objects and arrays immutably!_

## Immutability Using Vanilla JavaScript

If a single human being has faced a problem in JavaScript and solved it, they have probably packed the solution into a JavaScript library. Things are no different with the concept of immutability: there are many possible libraries that can help you with that. The good news is that you don't necessarily need anyone of those to encourage immutability. Immutable code can be written in vanilla JavaScript. Let's take a look! 

### The const Keyword

In 2015, when EcmaScript 6 was released, a new keyword was added to JavaScript: `const`. That sounds good! Const... constant... something that cannot be changed.

_That's immutable! Right?_

Not quite. `const` only means that a variable cannot be _reassigned_. It works quite well for primitive types like numbers and strings:

```js
const oldNumber = 1;
oldNumber = 2; // Error
```

But it does not actually prevent making changes to objects and arrays, since these are _reference types_. The variable holding the data can be seen as a pointer to the real data. While the pointer itself cannot be changed, the data itself can:

```js
const myPerson = {name: 'Ismo'};
myPerson.name = 'I can still modify you!';

const myArray = [1, 2, 3];
myArray.push('And you too!');

// Reassignment:
myPerson = {name: 'Seppo'}; // Well, at least this throws an error
```

Even if `const` does not make objects and arrays immutable, it is still a good habit to use it since it can prevent accidental variable reassignments. But if `const` doesn't make things deeply constant, or immutable, what does? There is something in JavaScript that makes things even more constant than the `const` keyword, and that is freezing objects.

### Object, Freeze!

We can make JavaScript objects immutable by calling `Object.freeze(object)`:

```js
const person = Object.freeze({name: 'Ismo'});
person.name = 'Seppo';
console.log(person.name); // person still has the name 'Ismo' after this. Great!
```

_Have we finally made it? We have created an immutable object and proven that we cannot modify it!_

Except, we can still modify it.

_What!?_

Yes. When we freeze an object with `Object.freeze`, it is so called _shallow freeze_. See, objects in JavaScript can contain other objects, and `Object.freeze` only freezes the top level object properties. 

Let's have an example in which our person has an address, which is another object. While we cannot modify the `streetAddress` property itself, we can still mutate the actual `streetAddress` object:

```js
const oldPerson = Object.freeze({name: 'Ismo', streetAddress: {name: 'Pihlajakatu 23 B'}});
const newPerson = oldPerson;
newPerson.streetAddress.name = 'Pihlajakatu 23 C';
console.log(oldPerson.streetAddress.name); // Oops, the address of oldPerson has been mistakenly updated!
```

How do we freeze the street address, and all the other inner objects we are going to add in the future? We need to manually check all the properties of the object we want to freeze, and if they are objects, recursively freeze them too:

```js
const deepFreeze = (thing) => {
    Object.keys(thing).forEach(key => {
        if (typeof thing[key] === 'object') {
            deepFreeze(thing[key]);
        }
    });
    return Object.freeze(thing);
};

const oldPerson = deepFreeze({name: 'Ismo', streetAddress: {name: 'Pihlajakatu 23 B'}});
const newPerson = oldPerson;
newPerson.streetAddress.name = 'Pihlajakatu 23 C';
console.log(oldPerson.streetAddress.name); // Finally, nothing changed in oldPerson!
```

An alternative way to freeze objects, kind of, is making it's individual properties virtually impossible to modify. One could use something like `Object.defineProperty` to achieve this:

```js
function makeImmutable(thing, key, value) {
  Object.defineProperty(thing, key, {
    get() {
      return value;
    },
    set() {
      throw new Error("Nope!");
    },
  });
}

const person = {};
makeImmutable(person, 'name', 'Ismo');
console.log(person.name); // 'Ismo'
person.name = 'Seppo'; // Error: Nope!
```

_Doesn't all of this feel a bit... inconvenient?_

It does. One could wrap some of these into helper functions, but we would need to use those helper functions for _every_ single new object to make it immutable. Not to mention that freezing objects also eats up some performance.

It turns out that vanilla JavaScript hardly gives us any easy way to make things deeply immutable. I wish we could have something like [TypeScript const assertions](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-3-4.html#const-assertions) which makes introducing new immutable things quite handy:

```typescript
let a = {
  b: 'Hello world',
  c: 123,
  d: {e: 456}
} as const /* This makes every field readonly (in compile time) and prevents modifications */;

a.d.e = 666; // Error: Cannot assign to 'e' because it is a read-only property
```

Things may still be better in the future. There is a proposal of introducing new types for JavaScript: [Record and Tuple](https://github.com/tc39/proposal-record-tuple). These are deeply immutable structures built-in to JavaScript. They are also primitive types, which means that we can use the `===` operator to _structurally_ compare the equality of them, something we cannot easily do with vanilla JavaScript objects and arrays. Using these new types seems easy since the new types can be introuced using a preceding `#` modifier:

```js
const myRecord = #{ a: 1, b: 2 } // Object-like data strcuture
const myTuple = #[1, 2] // Array-like data strcuture

// Built-in operations always return a new copy

console.log(myTuple.pushed(3)) // #[1, 2, 3]
console.log(myTuple) // #[1, 2]
```

Naturally, these are not yet ready for production as I'm writing this. Still, I'm very excited to see more options for immutability in upcoming JavaScript versions.

### Making Immutable Modifications

Now that we have learned making things truly, _deeply_, constant in JavaScript, let's learn how to manipulate our data immutably.

In 2015, EcmaScript 6 introduced a new `...` operator (dotdotdot or spread operator), which "spreads" values from another object or array. We can take advantage of it. Let's begin with arrays.

#### Arrays

Common data modification operations in arrays are inserting, removing and sorting items. JavaScript has all of these easily covered, though the operations mutate the original array.

```js
const things = ['B'];
// Add 'A' at the end
things.push('A'); // ['B', 'A']
// Add 'C' at the beginning
things.unshift('C'); // ['C', 'B', 'A']
// Remove the last item
things.pop(); // ['C', 'B']
// Sort the end result
things.sort(); // ['B', 'C']
```

We can do similar operations immutably. In the following example, we always create a new array, make use of the previous state and do the needed modifications.

```js
const things = ['B'];
// Add 'A' at the end
const thingsPushed = [...things, 'A']; // ['B', 'A']
// Add 'C' at the beginning
const thingsUnshifted = ['C', ...thingsPushed]; // ['C', 'B', 'A']
// Remove the last item
const thingsPopped = thingsUnshifted.slice(0, thingsUnshifted.length - 1); // ['C', 'B']
// Sort the end result
const thingsSorted = [...thingsPopped].sort(); // ['B', 'C']

console.log(things); // ['B']
```

By creating a new array with every modification, we make sure that we do not mutate the original array. As a bonus, we have a snapshot of the state of the array after every single modification. We could make use of it if we wanted to program some _undo_ functionality.

_But... I think the previous version, in which we mutated the original array, looked much simpler..._

You are quite right. That's basically because JavaScript is a mutable language by its nature, and simple array methods like `push`, `unshift`, `pop` and `sort` are designed to modify the original array. If you do these data mutations in a _complete isolation_, for example in a single function in which the outside world cannot modify your data, you are probably good to go with the standard mutating methods. Otherwise, immutable modifications are your friend, even if they require a bit more work.

Luckily for us, not all array methods in JavaScript are actually mutable! The `slice` method we used returns a new array and does not modify the original. Also, if you are familiar with functional programming, methods like `map` and `filter` are available in plain JavaScript arrays and are supported in old browsers too. These too create new arrays instead of modifying the original.

```js
// Removing a single letter from an array using filter method
// without modifying the original array
const result = things.filter(character => character !== 'A');
```

In any case, if you use the well-known JavaScript array methods, remember to be sure if the method mutates the original array or returns a new copy. It's a big difference between mutability and immutability.

#### Objects

How about objects then? Perhaps the most common thing you want to do with objects is that you want to change a value of some property:

```js
const person = {name: 'Ismo', age: 50};
person.name = 'Seppo';
// person: {name: 'Seppo', age: 50}
```

But modifications like this are highly illegal if you want to encourage immutability. Immutable version requires to create a new object, "spread" all the old values from the old object, and make necessary changes:

```js
const oldPerson = {name: 'Ismo', age: 50};
const newPerson = {...oldPerson, name: 'Seppo'};
// newPerson: {name: 'Seppo', age: 50};
```

_That looks quite simple!_

And it is. But let me disappoint you once again. If we have a deeply nested object, and we want to mutate a single property inside of it, things are going to get messy:

```js
const oldPerson = {name: 'Ismo',
                   age: 50,
                   location: {name: 'Finland',
                              place: {city: {name: 'Helsinki'},
                                      street: {area: 6,
                                               name: 'Pihlajakatu 23 B9'}}}};

// Let's change the street address without modifying the original object:                           

const newPerson = {...oldPerson,
                   name: 'Seppo',
                   location: {...oldPerson.location,
                              place: {...oldPerson.location.place,
                                      street: {...oldPerson.location.place.street,
                                               name: 'Pihlajakatu 23 B3'}}}};
```

_Ouch! That's ugly!_

And that's not all. Remember when we froze objects and learned that freezing was shallow, i.e. inner objects were not frozen? The `...` operator is also shallow, which means that it does not make _deep copies_ of objects. Properties copied with the `...` operator that are objects or arrays do still reference to the original item. If we mutate it, we also mutate our new object:

```js
oldPerson.location.place.city.name = 'Turku';
console.log(newPerson.location.place.city.name)
// Prints: 'Turku'. Oops, we have once again mutated things we did not meant to.
```

Because the city is an object, and we made a shallow copy of it, the city object is shared between the two person objects. Making modifications to one city modifies both persons' cities. 

_But does it matter if we encourage immutability and never mutate object properties?_

In that case, it doesn't. Like we have learned, it is possible to modify JavaScript objects by creating new ones, without making changes to the original. Even if shallow copies are not protected from accidental mutations, they are much faster to create than making deep copies of big objects.

Sometimes you still want to make a truly deep copy of an object. In that case, you can always use a good old JSON-based hack: `JSON.parse(JSON.stringify(object))`. Modern browsers also support a new global [structuredClone](https://developer.mozilla.org/en-US/docs/Web/API/structuredClone) function. It should be more robust and often faster than the classic hack.

We have learned that vanilla JavaScript offers tools we can use to encourage immutability. Unfortunately, most of these do not fully prevent meaningless data mutations. Let's see if 3rd party tools can make our lives easier.

## 3rd Party Tools

If you are building a web frontend application, you are probably using a state management library, such as [Redux](https://redux.js.org) or [Vuex](https://vuex.vuejs.org). These kind of libraries definitely make our lives easier by wrapping the state of the entire application into a _single source of truth_ and ensuring modifications to the state occur only through the services provided by the library - usually immutably.

These libraries do not, however, completely solve the mutability problem for us. Even if you keep your application state encapsuled in these libraries (and trust that they prevent harmful data mutations), you probably still work with a lot of data that is never stored or touched by these libraries. This kind of data can come from an external source, such as from the web server, or you might introduce it by yourself while doing some calculations. We need another solution for working with this type of data.

### Solution 1: Immutable 3rd Party Data Structures

One possible solution to encourage immutability in JavaScript is to partially replace the plain object and array types with new types that are immutable by nature. Libraries such as [ImmutableJS](https://immutable-js.com) offer this kind of solution. They offer 3rd party data structures that are promised to prevent data mutations and offer methods for making modifications immutably.

With these tools, array methods such as `push`, `pop` and `sort` can be used in the same way as with standard JavaScript arrays, except that their immutable counterparts do not make modifications, but instead they return a new array. Similarly, modifications to objects return new objects:

```js
// Modifying a Map in ImmutableJS
const oldPerson = Map({ name: 'Ismo', age: 50 });
const newPerson = oldPerson.set('name', 'Seppo');

console.log(oldPerson) // ImmutableJS map containing { name: 'Ismo', age: 50 }
console.log(newPerson) // ImmutableJS map containing  { name: 'Seppo', age: 50 }
```

_Great! I'm going to replace all objects and arrays with ImmutableJS data structures!_

If it only was that simple. The main issue with these kind of libraries is typically that data structures are not backwards-compatible with plain JavaScript. These types can only be handled by the library's own API, and for everything else, you need to convert data back to plain JavaScript types and then back to ImmutableJS format. Depending on the context, this can be either a frustrating repetitive process or not a problem at all.

There is also another library that promises to tackle this problem: [seamless-immutable](https://github.com/rtfeldman/seamless-immutable). Internally it uses JavaScript features like `Object.freeze` and `Object.defineProperty` to create data structures that are immutable, but also backwards-compatible with normal arrays and objects. Creating immutable things should be as easy as wrapping them with `Immutable`. A bit like wrapping things with `deepFreeze` like we did earlier.

```js
const numbers = Immutable([1, 2, 3])
numbers.sort() // This will throw an ImmutableError, because sort() is a mutating method.
```

Solution like this can prevent mutations done by a mistake, but it requires to wrap new arrays and objects with `Immutable`. This library is not as popular as ImmutableJS (based on GitHub stars and npm downloads) and I'm also a bit worried that, as I'm writing this, the library has not been actively updated for years.

### Solution 2: Modifying Native Types By Returning New Versions

If we don't want to replace native JavaScript objects and arrays with 3rd party data structures, we could use tools that modify plain JavaScript types immutably. Libraries such as [lodash/fp](https://github.com/lodash/lodash/wiki/FP-Guide) and [Ramda](https://ramdajs.com/) can help us do just that.

From these libraries, Lodash might be a familiar name to many JavaScript developers. It has been around since 2012, but it now has additional module called **lodash/fp**. It's the functional counterpart of Lodash that encourages immutability.

For instance, one could use the `set` function in **lodash/fp** to return a new version of an object instead of modifying it, like the original Lodash `set` function does.

```js
import { fp } from 'lodash/fp';

const person = {name: 'Ismo'};
const newPerson = fp.set('name', 'Seppo', person); // Returns a new person with 'Seppo' as its name
```

The property name argument passed to `set` can even be a path:

```js
import { fp } from 'lodash/fp';

const person = {name: 'Ismo', streetAddress: {name: 'Pihlajakatu 23 B'}};
const newPerson = fp.set('streetAddress.name', 'Pihlajakatu 23 C', person);

console.log(person); // {name: 'Ismo', streetAddress: {name: 'Pihlajakatu 23 B'}}
console.log(newPerson); // {name: 'Ismo', streetAddress: {name: 'Pihlajakatu 23 C'}}
```

_This is way more convenient than using the ... operator everywhere!_

Indeed! A single function call is a simple solution. TypeScript developers might not like it, however, since it cannot check that the path truly exists. Nevertheless, it encourages immutability, just like other Lodash functions that have their functional / immutable counterparts in the [lodash/fp](https://github.com/lodash/lodash/wiki/FP-Guide) module.

### Solution 3: Making Mutations Without Actually Making Any Mutations

We still have one solution left, which is perhaps the most interesting one. It's called [ImmerJS](https://immerjs.github.io/immer/).

It does not introduce its own immutable data types nor does it introduce new immutable counterparts for standard JavaScript methods. What Immer does is that it makes it possible to take an existing data as a draft, modify it with well-known mutable JavaScript methods, and promises that it still returns a new version without making changes to the original data.

```js
import produce from "immer";

const persons = [
    {
        name: 'Ismo',
        age: 53
    },
    {
        name: 'Seppo',
        age: 56
    }
];

const nextState = produce(persons, draft => {
    draft[1].age = 54
    draft.push({name: 'Jukka', age: 45})
});
```

How immer achieves this? It's `produce` function takes the base state as an argument, and a `recipe` function that is passed a `draft` to which we can safely mutate. Once all mutations are completed, Immer will produce a new state, without modifying the original. Immer will also freeze the data, preventing accidental modifications in the future.

Immer offers multiple benefits. In addition to be able to use standard JavaScript types with well-known methods, it's API is simple to use with built-in object freezing and deep updates. However, we need to wrap our operations with 3rd party function in order to be able to modify it immutably.

## Conclusion

So, which solution should we use to encourage immutability and avoid accidental data mutations? Vanilla JavaScript or one of the introduced 3rd party tools? The answer depends on the application you want to build and also comes down to personal preferences.

[ImmutableJS](https://immutable-js.com) appeared somewhere around 2013 and is well know by many who want to work with immutable data. The main issue with it is that it's data structures are not backwards-compatible with plain JavaScript. You probably need to often convert data back to plain JavaScript objects and then back to ImmutableJS format. [seamless-immutable](https://github.com/rtfeldman/seamless-immutable) promises to tackle this problem, but as I'm writing this, the GitHub repository has not been updated in many years.

For me, it sounds like a good idea to stick with plain old JavaScript types (objects and arrays) for compatibility, possibly deep freezing them in critical places, and simply avoid mutating them as much as possible. The vanilla `...` operator and the new global `structuredClone` function help with this, but one can also use libraries such as [lodash/fp](https://github.com/lodash/lodash/wiki/FP-Guide) and [Ramda](https://ramdajs.com/) to make immutable data modifications easier. [ImmerJS](https://immerjs.github.io/immer/) is also good if you want to use the standard data modification methods JavaScript already offers and you possibly don't care about functional programming that much. In the future, I hope that new JavaScript types [Record and Tuple](https://github.com/tc39/proposal-record-tuple) will provide us a built-in standard for working with immutable data. 

And, of course, you can always do yourself a favor a learn a bit of [ClojureScript](https://clojurescript.org), which has immutability already built-in. ;)
