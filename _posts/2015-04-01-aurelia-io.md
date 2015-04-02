---
layout: post
title: Aurelia.io
author: arto
excerpt: Coding with Aurelia JavaScript framework and ECMAScript 6 - right now
---
I've always been fond of keeping my eyes at the horizon, constantly watching what new technologies will emerge, what useful tools will we have in the years to come. With this mindset I recently started a quest to learn Angular 2 - before it will be mainstream. I had studied it a bit earlier, too, but then it felt way too ugly and early to have anything to do with project work. Working in [Solita](http://www.solita.fi) - there is no excuse to let your skills or knowledge go stagnant - or letting your toolbox to be outdated. So I went looking for Angular 2 - but ended up finding something else.

### What is Aurelia? ###

Aurelia is a framework that is relatively new and not many have heard of it - or used it. It's not stable for production use yet - but it is looking pretty good already. It's also looking a lot like Angular 2, just much better. This is of course no big surprise, since one of the key developers is Rob Eisenberg, previously a member of Angular 2 team.

### What's cool about Aurelia? ###

What fascinates me about Aurelia? Many things. One core thing is that it's based on using ECMAScript 6 - and 7. This means you are able to code with future languages - right now. But it still works in todays browsers - thanks to Babel 6to5 transpiler, that forms a core part of this framework. This means support for all current Evergreen browsers, and there's even some work being done for IE10 and IE9 support. It's beautiful, and applicable today.

Don't believe me? Take a look at this:

{% highlight javascript %}
import {HttpClient} from 'aurelia-http-client';
import _ from 'underscore';

export class App {

  static inject() { return [HttpClient]; }

  constructor(http){
        this.title = 'Whatever';
        this.items = [];
        this.http = http;
  }

  // ... more good stuff
}
{% endhighlight %}

What is happening here? A lot. Aurelia uses ES6 module system so import becomes much simpler than with Angular+RequireJS combination. We see dependency injection in action, we provide some metadata and HttpClient becomes injected in our constructor. And no more $scope! Our scope is now the viewmodel, and we simply store any interesting variables in this (that now works better, too)

### How's the view? ###

Aurelia uses view-viewmodel architecture, and what we see here is viewmodel named App. The view for this viewmodel would be named app.html, and it looks like this:

{% highlight html %}
<template>
    <section>
        <h2>${title}</h2>

        <input value.bind="query">

        <div repeat.for="item of items">
                    ${item.name} ${item.created_at}
        </div>
    </section>
</template>
</code>
{% endhighlight %}

Here we can see example of another powerful Aurelia feature - binding. There's a whole binding engine at work to figure out what's the best way to implement the binding based on your code. There are several options. Any html attribute may be bound, in this case you can see repeat.for, but similarly you can bind with value.bind="somevalue", or href.bind="somehref" - you can also use one-way binds or two-way binds by replacing '.bind' part with '.one-way', or '.two-way', to be more precise.

To me it seems like Aurelia is very clean and pure code, compared to the mess that Angular 1 and 2 very easily tend to become. Using strong points of ES6 is definitely a plus, since ECMAScript 6 will come, one day. Being able to already start making transition and learning to apply it will be valuable.

### What else is there? ###

So, other impressive things about aurelia are:
- It's backed by Durandal Inc - not just a one guy project
- It's highly modular - you can pick which modules you like and drop the rest
- While you can use ECMAScript 5, CoffeeScript, or TypeScript, you probably like to use ES6
- While you can use bower and grunt, you probably want to use jspm and gulp instead
- There are conventions over configuration - for example, to create a new view, you just create view.js and view.html file - and you don't need to configure anywhere how they work together - it's just magic. I like magic (well, good kind of).
- You can use existing libraries easily with your solution, I used Bootstrap and Underscore in this little tech demo of mine.
- Routing - yeah, there's much improved routing capabilities, much effected by work done for Angular 2
- Custom elements and templates
- This framework didn't appear from scratch - it's based on Durandal, as well as earlier 6to5 transpiler system, and of course Angular 2 work. That means certain level of maturity even though it's very new.

### Time to wrap it ###

Aurelia still has a long way to go - it's not even claimed to be production-ready yet, and there are other cool and emerging JavaScript frameworks so only time will tell if this framework will be the One. But having tried it a little bit I have to say I love the simplicity, and would consider using it for real work - mostly for the ES6 future-proofing and support. Can't wait to see what becomes of it.

### Links (check them out!) ###

[Aurelia.io](http://aurelia.io/)

[Aurelia vs AngularJS](http://ilikekillnerds.com/2015/01/aurelia-vs-angularjs-round-one-fight/)

[Aurelia vs Angular 2](http://blog.durandal.io/2015/03/16/aurelia-and-angular-2-code-side-by-side/)

[ECMAScript 6 Browser Compatibility](https://kangax.github.io/compat-table/es6/)
