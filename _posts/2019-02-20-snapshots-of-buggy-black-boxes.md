---
layout: post
title: Snapshots of Buggy Black Boxes
author: mpajunen
excerpt: Snapshot testing has been gaining popularity in frontend development. Could it be useful for testing legacy code as well?
tags:
- Legacy code
- Testing
---

Snapshot tests have recently become popular in testing UI components. We tried snapshots in testing legacy code.

## A Black Box of Code

A while ago we were faced with a typical situation when working with legacy code: a largely unknown and practically untested Black Box. This Black Box had been lifted from an older system and rewritten for the new platform already. Unfortunately, much of the old cruft remained.

We already had a list of new features and improvements to implement. Looking at the code this seemed like a tall order: Data fetches, business logic and output marshalling were all gloriously mixed up. It didn't take long to realize that significant refactoring was needed before we could start working on the new features.

### Testing Black Boxes

Faced with the refactoring task, we wanted to make sure not to break too many things that were already working. This meant we'd need to write at least some tests first.

A major problem with untested code is that it's often untestable as well. If the code blocks are long and deeply nested and functions are even longer or common state is modified without care, writing meaningful tests can be impossible.

Writing unit tests for the existing code was quickly ruled out except for a few isolated sections. Integration tests proved more reasonable. Simply initializing the relevant state with known values and matching the output increased our confidence to make changes quite a bit. Some bugs were also discovered right away.

Handling these bugs turned out to be the next challenge. Unit tests had proved nearly impossible and integration tests looked like a lot of work: the lengthy messages in the assertions would have to be updated after any intentional changes or fixes.

Fortunately, we had already thought of a solution. We had recently started using snapshot testing for frontend components. The Black Box seemed like a similar if slightly more complex problem: set some initial values, get a result, check that it matches a known value.

## Snapshot Testing

Snapshot testing has been mainly used to test UI components. The idea is simple: Instead of writing assertions for the test output manually, a snapshot test automatically stores the output of the first test run. On successive runs the output is compared to the earlier, stored version. If there are changes, the test fails. Storing the snapshot files in version control makes sure no unintentional changes occur.

Not having to write assertions makes snapshot tests quick to add. Usually the test library also provides an easy way to update the snapshots, making snapshot tests even quicker to maintain and update. This can be ideal for UI components than can change quite often. Or any code that is potentially buggy --- as in our case.

### A Basic Snapshot Test

Writing a snapshot test is simple with library support. The following examples use [Jest](https://jestjs.io/). If needed, adding the requisite functionality to a test framework or library is usually straightforward as well.

A simple (if contrived) example of a snapshot test looks like this. First the function being tested, then the test and finally the snapshot:

```javascript
// Product.js
export const createProduct = (name, category) => ({
  name,
  category,
  enabled: true,
})

// Product.test.js
it('Creates products', () => {
  const product = createProduct('Foo', 1234)

  expect(product).toMatchSnapshot()
})

// Product.test.js.snap
exports[`Creates products 1`] = `
Object {
  "category": 1234,
  "enabled": true,
  "name": "Foo",
}
`;
```

Now assume we later want to add a tag field to our product, like this:

```javascript
// Product.js
export const createProduct = (name, category, tags = []) => ({
  name,
  category,
  tags,
  enabled: true,
})
```

Running the test will now fail:

```
Received value does not match stored snapshot "Creates products 1".

- Snapshot
+ Received

  Object {
    "category": 1234,
    "enabled": true,
    "name": "Foo",
+   "tags": Array [],
  }

   6 |   const product = createProduct('Foo', 1234)
   7 |
>  8 |   expect(product).toMatchSnapshot()
     |                   ^
   9 | })
  10 |

> 1 snapshot failed from 1 test suite. Inspect your code changes or press `u` to update them.
```

Since this was an intentional change, we can simply update the snapshot in version control.

## Deconstructing the Black Box

Snapshot tests proved to be an excellent tool for working with the Black Box. Splitting changes to two different kinds of commits was crucial to keep the history understandable:

1. Minimal change commits to fix bugs without significant refactoring. The code changes should be only a few lines, but the snapshot changes can be extensive.
2. Pure refactoring commits, sometimes with extensive changes. These should not change the snapshots at all.

Gradually the Box started to change and eventually only a few dark corners remained. These we decided could wait for later: they were still covered by the snapshot tests and didn't necessarily need changes soon.

## Lessons Learned

Snapshot tests turned out to be a great tool for working with legacy code. Since the tests are lightweight, getting solid coverage is quick. You're also not mired with continuously making extensive changes to the tests when the eventual fixes and new features arrive.

Like any tool, snapshot tests are not without problems:

* Good tests can often serve as technical documentation. Snapshot tests don't usually directly describe what the code being tested is *intended* to do.
* Unintentional changes can sometimes slip through if you're not careful. Using smaller snapshots helps.
* Sometimes there can be a lot of churn from formatting changes and the like. Adding a small preprocess step can help.

Snapshot tests are also limited in what can be tested. You can't easily test typical user interactions or intentional side effects with snapshots for example.

Even so, snapshot testing is an excellent tool to have in your toolbox. It's easy to try out by testing UI components for example. And it was helpful in testing legacy code in our case. Using it for other kinds of integration tests can make sense as well.
