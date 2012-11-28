---
layout: post
title: Solita Code Camp 2012
author: n1ko
excerpt: Code Camps are a great way to learn new things and socialize with your mates. Solita hosted its first internal Code Camp november 2012 and it was a great success!
---

### In the beginning ###

Solita has been hosting internal (and semi-internal)
[Coding Dojos](http://codingdojo.org/cgi-bin/wiki.pl?WhatIsCodingDojo)
for many years now. It has been great fun and and an awesome way to
learn new things together.

If you aren't familiar with the concept of a Coding Dojo, it basically
goes like this:

{% highlight java %}
Set<Programmer> coders = gatherPeople();
while (beerLasts && eyesStayOpen) {
    tryToSolveChallengeBrilliantly(coders);
}
presentSolutions(coders);
{% endhighlight %}

### So what is this Code Camp you are talking about? ###

A simple explanation of a
[Code Camp](http://en.wikipedia.org/wiki/Code_Camp) is that it's an
extended Coding Dojo. The main principles are the same: a programming
challenge, a bunch of programmers having fun, beer, food, relaxing.
But where a Coding Dojo is a fun way to spend an evening, a Code Camp
is a great way to spend a day.

What do you need for your own Code Camp? First of all, some kind of an
idea for a challenge. It could be related to a subject
([Justin Bieber](http://www.justinbiebermusic.com),
[Ponies](http://www.hasbro.com/mylittlepony)) or maybe a technology
([Brainfuck](http://esolangs.org/wiki/brainfuck),
[Fortran](http://www.fortran.com/),
[COBOL](http://www.webopedia.com/TERM/C/COBOL.html)). Just make sure
the idea is something that will be exciting for all the people taking
part in the Code Camp.

So you got a brilliant idea and people wanting to participate? Next,
you need to able to host the event. I suggest you pick a venue that is
not affliatiated with your organisation. For example, we rented a
cabin in the woods. It helps separate the happening from work (or
studies) and makes it easier for the participants to relax.

The next thing you need is the basic infrastracture for the challenge.
You will probably need at least the following:

* Workstations
  * Chairs
  * Tables
  * Remember that team work is golden, so plan the workstations accordingly!

* Networking
  * Internet (meaning some kind of uplink)
  * DHCP/DNS services
  * Switches, WLAN APs etc.

* A revision control system ([Git](http://git-scm.com/) etc.)

You'll most likely need these as well:

* A projector (for showing the awesome software the attendees built)
* Post-Its, Pens, Drawing boards
* Spare machines, mice etc.

Remember to test the IT stuff beforehand, especially if you took my
advice and are planning to host the event in a cabin or an otherwise
unfamiliar place. Our network setup looked like this :

[![network_stuffzzz](/img/codecamp/small/codecamp_interweb.jpg)](/img/codecamp/codecamp_interweb.jpg)

Also make sure you have enough food and [drinks](http://xkcd.com/323/)
so that everyone can focus 100% on the task on hand. While energy
drinks and snacks are nice, don't forget about real food either.

### Solita Code Camp 2012: Success delivered. ###

[![tirila](/img/codecamp/small/ascii_tirila.jpg)](/img/codecamp/ascii_tirila.jpg)

The patron saint of Solita Code Camp, with the teams listed next to him.

Solita had an internal Solita Camp 16th November 2012 @ the middle of
nowhere. It was a huge success (in my mind, but also judging by the
feedback we got). Our idea for the Code Camp was to learn more about
the dozens of Javascript libraries out there.

We arrived at the Code Camp HQ at 10 am and started setting up chairs,
network etc. To our disappoiment the network service in the area was
awful for DNA and Sonera. And of course all of our dongles and load
balancers were dependant on those service providers. Luckily some
people had personal phones equipped with Saunalahti/Elisa and we could
use them as hotspots.

Other than the idea of using Javascript based/related technologies we
made no restrictions on what to use or what to do. Some of us made
games, some of us made simulators, and some visualized data in a nice
graphical form. We randomly picked the subject for the projects by
looking through the day's Twitter trends and voting for the best
topic. You can actually see the the candidates in the previous
picture. The winning topic was "Global warming".

[![planning](/img/codecamp/small/concept.jpg)](/img/codecamp/concept.jpg)

After setting up the necessities we divided into groups of three or
four people. We quickly started planning our projects. Ideas flowed,
and like I said, the projects were all quite different in their
nature.

[![developers](/img/codecamp/small/developersdevelopersdevelopers.jpg)](/img/codecamp/developersdevelopersdevelopers.jpg)

We kept working on our projects until 7 pm and, oddly enough, took
almost no breaks. Apart from a quick lunch in the middle of the day,
it was non-stop coding till the evening. Everybody was really into the
projects and was trying their best. The level of communication even
between teams was awesome, probably thanks to our Internet problems.

We used a revision control system, of course. Our original plan was to
use a private Gitlab installation because we suspected that we
couldn't rely on having an Internet connection. Some of us lucky
enough to have Elisa as their operator used Github, but most of the
projects used the onsite Gitlab installation. After the Code Camp all
of the projects were transferred (naturally) to Github.

Some of the technologies used :

* [ClojureScript](https://github.com/clojure/clojurescript)
* [Three.js](https://github.com/mrdoob/three.js/)
* [RequireJS](http://requirejs.org/)
* [Backbone.js](http://backbonejs.org/)
* [Underscore.js](http://underscorejs.org/)
* [Sass](http://sass-lang.com/)
* [D3.js](http://d3js.org/)
* ... and others

[![funny](/img/codecamp/small/very_funny.jpg)](/img/codecamp/very_funny.jpg)

After we were semi-happy with our little lovechildren we started to
review them on the screen. It was awesome too see what the teams had
come up with, and also to have some laughs at our not-so-serious
background stories for the projects.

We decided to give out awards in two categories: technological
awesomeness and artful presentation. The award for the technological
category was [Raspberry Pis](http://www.raspberrypi.org/) for the
whole team. The awards for the other category can be seen in the next
picture.

[![jallua](/img/codecamp/small/timo_juo_jallua.jpg)](/img/codecamp/timo_juo_jallua.jpg)

Timo didn't even win the category but the artists were kind enough to
share!

After reviewing the end results, it was time for some sauna and booze.

### Sum it up ###

All in all the event was a great success in terms of learning and
working together. Although we all work for the same company, most of
us don't work together on the same project in "real life". Getting to
know each other's skills in a practical setting like this is really
helpful because you get to know what the other guys are good at and
who to ask for help at work.

You can check out what we managed to achieve during those productive
~8 hours on our [Github account](https://github.com/solita) (the
projects marked with codecamp2012).
