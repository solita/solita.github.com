---
layout: post
title: Refactoring Primitive Obsession
author: orfjackal
excerpt: Enriching the domain model by fixing Primitive Obsession code smells requires careful refactoring in small steps. Here I'm presenting some tips for doing that almost fully with automated refactorings, making it much faster and safer to do.
---

[Primitive Obsession](http://www.jamesshore.com/Blog/PrimitiveObsession.html) means using a programming language's generic type instead of an application-specific domain object. Some examples are using an integer for an ID, a string for an address, a list for an address book etc.

You can see an example of refactoring Primitive Obsession in James Shore's [Let's Play TDD](http://www.jamesshore.com/Blog/Lets-Play) episodes 13-18. For a quick overview, you may watch [episode #14](http://www.jamesshore.com/Blog/Lets-Play/Episode-14.html) at 10-12 min and [episode #15](http://www.jamesshore.com/Blog/Lets-Play/Episode-15.html) at 0-3 min, to see him plugging in the TaxRate class.

The sooner the Primitive Obsession is fixed, the easier it is. In the above videos it takes just a couple of minutes to plug in the TaxRate class, but the Dollars class takes over half an hour. James does the code changes manually, without automated refactorings. For a big project with rampant Primitive Obsession it will easily take many hours, even days, to fix the problem of a missing core domain type.

Here I'm presenting some tips of using fully automated refactorings to solve Primitive Obsession. I'm using IntelliJ IDEA's Java refactorings, but the ideas should, to some extent, be applicable also to IDEs with inferior refactoring support.


## The Example

Let's assume that we have a project that uses lots of thingies which are saved in a database. The thingies each have an ID that at the moment is just an integer. To avoid the thingy IDs getting mixed with other kinds of IDs, we create the following value object:

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

This kinds of refactorings are quite mechanical, but because they require cascading changes, it's very easy to mess things up. So it's best to start small and proceed in small steps.

It makes sense to start from a central place from where the change can be propagated to the whole application. For example by starting to use ThingyId inside this one class, without changing its public interface:

![Animation](/img/refactoring-primitive-obsession/start.gif)


## Pushing Arguments Out

When there is a method which wraps one of its arguments into ThingyId, we can propagate it by pushing that argument wrapping outside the method. In IntelliJ IDEA this can be done with the *Extract Parameter* (Ctrl+Alt+P) refactoring:

![Animation](/img/refactoring-primitive-obsession/push-args-out.gif)


## Pushing Return Values

When there is a method which unwraps its return value from ThingyId to int, we can propagate the unwrapping outside the method. There is no pre-made refactoring that, but fortunately we can use a combination of *Extract Method* (Ctrl+Alt+M) and *Inline* (Ctrl+Alt+N) for doing that.

First extract a method that does the same as the old method, but does not unwrap ThingyId. Then inline the original method and rename the new method to be the same as the original method.

![Animation](/img/refactoring-primitive-obsession/push-retval.gif)


## Pushing Return Values of Interface Methods

A variation of the previous refactoring is required when the method is part of an interface. IntelliJ IDEA 12 doesn't support inlining abstract methods (I would like it to ask that which of the implementations to inline), but since IDEA can refactor code that doesn't compile, we can copy and paste the implementation into the interface and then inline it:

![Animation](/img/refactoring-primitive-obsession/push-retval-interface.gif)


## Pushing Arguments In

- push from inside the class to change, remove reduncancy afterwards


## Removing Redundancy

- replace structurally: new Foo(foo.toInt())


## Updating Test Constants

- extract new constant, reorder definitions, inline old constant


## Finding the Loose Ends

- usages of constructor
- usages of toInt()
