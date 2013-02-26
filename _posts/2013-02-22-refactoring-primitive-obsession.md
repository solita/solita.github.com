---
layout: post
title: Refactoring Primitive Obsession
author: orfjackal
excerpt: Enriching the domain model by fixing Primitive Obsession code smells requires careful refactoring in small steps. Here I'm presenting some tips for doing that almost fully with automated refactorings, making it much faster and safer to do.
---

[Primitive Obsession](http://www.jamesshore.com/Blog/PrimitiveObsession.html) means using a programming language's generic type instead of an application-specific domain object. Some examples are using an integer for an ID, a string for an address, a list for an address book etc.

You can see an example of refactoring Primitive Obsession in James Shore's [Let's Play TDD](http://www.jamesshore.com/Blog/Lets-Play) episodes 13-18. For a quick overview, you may watch [episode #14](http://www.jamesshore.com/Blog/Lets-Play/Episode-14.html) at 10-12 min and [episode #15](http://www.jamesshore.com/Blog/Lets-Play/Episode-15.html) at 0-3 min, to see him plugging in the `TaxRate` class.

The sooner the Primitive Obsession is fixed, the easier it is. In the above videos it takes just a couple of minutes to plug in the `TaxRate` class, but the `Dollars` class takes over half an hour. James does the code changes manually, without automated refactorings. For a big project with rampant Primitive Obsession it will easily take many hours, even days, to fix the problem of a missing core domain type.

Here I'm presenting some tips of using fully automated refactorings to solve Primitive Obsession. I'm using IntelliJ IDEA's Java refactorings, but the ideas should, to some extent, be applicable also to IDEs with inferior refactoring support.


## The Example

Let's assume that we have a project that uses lots of "thingies" which are saved in a database. The thingies each have an ID that at the moment is just an integer. To avoid the thingy IDs getting mixed with other kinds of IDs, we create the following value object:

{% highlight java %}
public final class ThingyId {

    private final int id;

    public ThingyId(int id) {
        this.id = id;
    }

    public int toInt() {
        return id;
    }

    @Override
    public boolean equals(Object obj) {
        if (!(obj instanceof ThingyId)) {
            return false;
        }
        ThingyId that = (ThingyId) obj;
        return this.id == that.id;
    }

    @Override
    public int hashCode() {
        return id;
    }

    @Override
    public String toString() {
        return getClass().getSimpleName() + "(" + id + ")";
    }
}
{% endhighlight %}

Creating such a class is easy, but putting it to use is not so when the primitive ID is used in a couple of hundred places...


## Starting Small

Refactoring Primitive Obsession is quite mechanical, but because it requires cascading changes, it's very easy to mess things up. So it's best to start small and proceed in small steps.

It makes sense to start from a central place from where the change can be propagated to the whole application. For example by starting to use `ThingyId` inside this one class, without changing its public interface:

![Animation](/img/refactoring-primitive-obsession/start.gif)


## Pushing Arguments Out

When there is a method which wraps one of its arguments into `ThingyId`, we can propagate it by pushing the act of wrapping outside the method. In IntelliJ IDEA this can be done with the *Extract Parameter* (Ctrl+Alt+P) refactoring:

![Animation](/img/refactoring-primitive-obsession/push-args-out.gif)


## Pushing Return Values

When there is a method which unwraps its return value from `ThingyId` to `int`, we can propagate the unwrapping outside the method. There is no built-in refactoring for that, but it can be accomplished by combining *Extract Method* (Ctrl+Alt+M) and *Inline* (Ctrl+Alt+N).

First extract a method that does the same as the old method, but does not unwrap `ThingyId`. Then inline the original method and rename the new method to be the same as the original method.

![Animation](/img/refactoring-primitive-obsession/push-retval.gif)


## Pushing Return Values of Interface Methods

A variation of the previous refactoring is required when the method is part of an interface. IntelliJ IDEA 12 does not support inlining abstract methods (I would like it to ask that which of the implementations to inline), but since IDEA can refactor code that doesn't compile, we can copy and paste the implementation into the interface and then inline it:

![Animation](/img/refactoring-primitive-obsession/push-retval-interface.gif)


## Pushing Arguments In

Instead of trying to refactor a method's arguments from the method caller's side, it's better to go inside the method and use *Extract Parameter* (Ctrl+Alt+P) as described earlier. This leaves us with some redundant code, as can be seen in this example. We'll handle that next.

![Animation](/img/refactoring-primitive-obsession/push-args-in.gif)


## Removing Redundancy

By following the above tips you will probably end up with some redundant wrapping and unwrapping such as `new ThingyId(thingyId.toInt())` which is the same as `thingyId`. Changing one such thing manually would be easy, but the problem is that there are potentially tens or hundreds of places to change. In IntelliJ IDEA those can be fixed with one command: *Replace Structurally* (Ctrl+Shift+M).

In the following example we use the search template "`new ThingyId($x$.toInt())`" and replacement template "`$x$`". For extra type safety, the `$x$` variable can be defined (under the *Edit Variables* menu) to be an expression of type `ThingyId`.

![Animation](/img/refactoring-primitive-obsession/redundancy.gif)


## Updating Constants

When there are constants of the old type, as is common in tests, those can be updated by extracting a new constant of the new `ThingyId` type, redefining the old constant to be an unwrapping of the new constant, and finally inlining the old constant:

![Animation](/img/refactoring-primitive-obsession/constants.gif)


## Finding the Loose Ends

The aforementioned refactorings must be repeated many times until the whole codebase has been migrated. To find out what refactoring to do next, search for the usages of the new type's constructor and its unwrapping method (e.g. `ThingyId.toInt()`). Use an appropriate refactoring to push that usage one step further. Repeat until all the usages are at the edges of the application (e.g. saving `ThingyId` to database) and cannot be pushed any further.

And as always, run all your tests after every step. If the tests fail and you cannot fix them within one minute, you're about to enter [Refactoring Hell](http://c2.com/cgi/wiki?RefactoringHell) and it's the fastest that you revert your changes to the last time when all tests passed. Reverting is the easiest with IntelliJ IDEA's [Local History](http://www.jetbrains.com/idea/features/local_history.html) which shows every time that you ran your tests and whether they passed or failed, letting you revert all your files to that time. The other option is to commit frequently, after every successful change (preferably [rebased before pushing](http://gitready.com/advanced/2009/02/10/squashing-commits-with-rebase.html)), and revert using `git reset --hard`.
