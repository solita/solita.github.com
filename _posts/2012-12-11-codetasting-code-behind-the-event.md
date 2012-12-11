---
layout: post
title: "Solita Code Tasting 2012: Code Behind the Event"
author: orfjackal
excerpt: Explaining the platform for the programming competition in Solita Code Tasting 2012. It was implemented with Clojure and was designed to encourage good software development practices among the participants. Not surprisingly, those who wrote tests won.
---

For the [Solita Code Tasting 2012](/2012/12/10/codetasting.html) programming competition I implemented the [rpi-challenger](https://github.com/solita/rpi-challenger) platform, which bombards the participants' machines with challenges and checks for right answers. The participants had to implement a HTTP server and deploy it on their production environment: a [Raspberry Pi](http://www.raspberrypi.org/). The challenges were sent in the body of a POST request as newline-separated plain text and the answers were also in plain text.

For example, one of the challenges was:

    +
    23
    94

and if the participant's server responded with `117`, the challenger accepted the answer and started sending more difficult challenges. All the arguments of challenges were randomized to prevent hard-coding. The way how points were given from passing the challenges was designed to encourage good development practices such as writing tests, releasing early and high availability.

In this article I'll first describe how the competition was devised to reach these goals. Afterward I'll tell about my experiences of writing rpi-challenger in Clojure.


## Punishing for Bad Practices

Due to the challenges being the way they were, there was barely any need for good design – a long if-else chain that switched based on the challenge's keyword was enough. But the way of *scoring* the challenges was *brutal* against bad software development practices.

The participants in Solita Code Tasting were university students, and apparently they don't teach good software development practices in university – [SNAFU](http://en.wikipedia.org/wiki/List_of_military_slang_terms). Most of the participants had a [developmestruction environment](http://thedailywtf.com/Articles/The_Developmestuction_Environment.aspx) – they were developing and testing in the production environment. In the first Code Tasting there was only one team who wrote tests for their software and deployed it only after the code was working. Thanks to the challenger's scoring function, they won with 2 times more points than the team which came second.


### Developmestruction vs. The Scoring Function

The challenger's scoring function was as follows:

The tournament consists of multiple rounds, each one minute long, and the points for each round are based on the challenge responses during that round. Challenges are sent to each participant every 10&nbsp;ms and if *even one* request fails due to a network problem (e.g. the participant's HTTP server is down), that's automatically zero points for that round.

We had about ten challenges, each worth 1-35 points. If all responses to all challenges worth 5 or less points are correct, then the maximum points for that round is 5 points. The actual points slowly increase towards the maximum points, using an acceleration of 1 points per round. In other words, `Points[RoundN] = min(MaximumPoints[RoundN], Points[RoundN-1] + 1)`, or as it is implemented:

{% highlight clojure %}
(def acceleration 1)

(defn points-based-on-acceleration [round previous-round]
  (let [max-points (:points round)
        previous-points (or (:points previous-round) 0)]
    (-> round
      (assoc :max-points max-points)
      (assoc :points (min max-points (+ acceleration previous-points))))))

(defn apply-point-acceleration [rounds]
  (reduce (fn [previous-rounds round] (conj previous-rounds (points-based-on-acceleration round (last previous-rounds)))) [] rounds))
{% endhighlight %}

The point of this scoring function is to encourage the participants to avoid regressions and service outages. This should drive the participants to write tests for the software, avoid doing any testing and development in the production environment, and make suitable technology choices or use load balancing which lets them upgrade their software without interrupting the service.

From the results it's obvious that who had developmestruction and who didn't:

![Score History for Top 4 Teams](/img/codetasting/2012-12-04-hki-score-history.png)

The purple area in the diagrams signifies the maximum points and the orange area signifies the actual points per round. For the latest round it's shown numerically in the velocity column.

The first team wrote tests and deployed (by restarting the server) when a feature was ready. This can be seen from the low number of service outages. The second team did all their development in the production environment and restarted their server often to see how it would respond to challenger's requests. Even though towards the end they managed to implement more challenges than anyone else, it was too late because their service had had so little uptime.


### Abandon Buggy Technologies

There was one more difference between the top 2 teams. Both of them started with the [Bottle](http://bottlepy.org/) web framework for Python, and both of them were able to crash the challenger so that it would not send requests anymore to their server – it was necessary to restart challenger, but it would happen again soon. Probably there was some incompatibility between Bottle's HTTP server and the HTTP client used by challenger ([http.async.client](https://github.com/neotyk/http.async.client) which is based on [Async Http Client](https://github.com/AsyncHttpClient/async-http-client)). The problem did not happen with the other teams who were using different HTTP servers.

The team which came first quickly decided to drop Bottle and switch to some other HTTP server. The team which came second persistently kept on using Bottle, even though they had to many times come tell the organizers to restart the challenger, so that they would again start receiving points.

This kinda reminds me of many projects where Oracle DB, Liferay or some other technology is used (typically because the customers demanded it) even though it produces more problems than it solves...


### Challenges with a Catch

There were a couple of challenges which were designed to produce regressions. This was to see who wrote tests for their software. The challenger keeps on sending also already completed challenges, in order to reveal any regressions.

For example one of the first challenges had to do with summing two integers. Then, much later, we introduced another challenge requiring summing 0 to N integers. Since the operator (the first line of the challenge) was the same for both, there was a good chance that without tests somebody would break the old implementation.

Another sadistic challenge was calculating Fibonacci numbers. Normally it would ask for one of the first 30 Fibonacci numbers, but there is a less than 1% probability that it will ask for a Fibonacci number that is over 9000 – that's a [big number](http://www.bigprimes.net/archive/fibonacci/9000/). So that challenge required an efficient solution and also the use of big integers, or else there would be an occasional regression.


### High Availability

The abovementioned scoring function punished severely for service outages. The idea was to encourage creating services which can be updated without taking the service down. Nobody appeared to have implemented such a thing, but if somebody had, they would probably have won the competition easily.

One easy solution would have been to use a technology that supports reloading the code without restarting the server (a one-liner in Clojure), but nobody appeared to have a setup like that. The participants used Python or Node.js – I don't know about their code reloading capabilities.

Another solution, which will work with any technology and is more reliable and flexible, is to have a proxy server that routes the challenges to backend servers. That could even enable running multiple versions of backend servers simultaneously. Implementing that would have been only a dozen lines of code. Even a generic load balancer might have fared well.


## Building the Challenger

Before this project I had barely used Clojure – just done some small exercises and implemented Conway's Game of Life – so I was quite clueless as to Clojure's idioms and how to structure the code. Getting started required learning a bunch of technologies for creating web applications ([Leiningen](https://github.com/technomancy/leiningen), [Ring](https://github.com/ring-clojure/ring), [Compojure](https://github.com/weavejester/compojure), [Moustache](https://github.com/cgrand/moustache), [Enlive](https://github.com/cgrand/enlive) etc.) which took about one or two hours per technology of reading tutorials and documentation. When implementing the challenger, I had much more trial and error than if I had used a familiar platform. Here are some things that I learned.


### Code Reloading

Clojure has rather good metaprogramming facilities. I wrote only one macro, so let's not go there, but the reflection and code loading capabilities are worth mentioning.

The challenges that challenger uses are stored in another source code repository to keep the challenges secret. I used `find-clojure-sources-in-dir` (from [clojure.tools.namespace](https://github.com/clojure/tools.namespace)) and `load-file` to load all challenges dynamically from an external directory. Challenger does that loading repeatedly every minute, so that it will also get new and updated challenges without having to be restarted. AFAIK, that doesn't remove functions that were removed from source code, but [clojure.tools.namespace](https://github.com/clojure/tools.namespace) should have some tools also for doing that without having to restart the JVM.

The challenger itself also supports upgrading on-the-fly through [Ring](https://github.com/ring-clojure/ring)'s `wrap-reload`. When we had our first internal coding dojo, where we were beta testing rpi-challenger and this whole Code Tasting concept, I implemented continuous deployment with the following command line one-liner:

    while true; do git fetch origin; git reset --hard origin/master; sleep 60; done

That upgraded the application on every commit without restarting the server. Also the challenges, which were in a separate Git repository, were similarly upgraded on-the-fly using a similar command. In that dojo it was then possible for some people to create more challenges (and make bug fixes to challenger) while others were as participants trying to make those challenges pass.


### Dynamic Bindings Won't Scale

Coming from an object-oriented background, I used test doubles to test some components in isolation. I'm not familiar with all the [seams](http://www.informit.com/articles/article.aspx?p=359417&seqNum=2) enabled by the Clojure language, so I went ahead with [dynamic vars](http://clojure.org/vars) and the `binding` function. That approach proved to be unsustainable.

I had up to 4 rebindings in some tests, so that I could write tests for higher level components without having to care about lower level details. For example in this tests I simplified the low-level "strike" rules, so that I can easier write tests for the "round" layer above it:

{% highlight clojure %}
; dummy strikes
(defn- hit [price]   {:hit true,  :error false, :price price})
(defn- miss [price]  {:hit false, :error false, :price price})
(defn- error [price] {:hit false, :error true,  :price price})

(deftest round-test
  (binding [strike/hit? :hit
            strike/error? :error
            strike/price :price]
     ...))
{% endhighlight %}

The problem here is that from the external interface of the system under test (the `round` namespace) it's not obvious that what are its dependencies. Instead you must know its implementation and that it calls those methods in the `strike` namespace, and that `strike/miss?` is implemented as `(defn miss? [strike] (not (hit? strike)))` so rebinding `strike/hit?` is enough, and that nothing else needs to be rebound – and if the implementation changes in the future, whoever does that change will remember to update these tests and all other places which depend on that implementation.

That's quite many assumptions for a test. It has almost all the negative sides of the [service locator pattern](http://martinfowler.com/articles/injection.html). In future Clojure projects I'll try to avoid binding. Instead I'll make the dependencies explicit with dependency injection and try making the interfaces explicit using [protocols](http://clojure.org/protocols) (as suggested in [SOLID Clojure](http://www.infoq.com/presentations/SOLID-Clojure)). I will also need to look more into how to best do mocking in Clojure, in order to support [GOOS](http://www.growing-object-oriented-software.com/)-style TDD/OO.


### Beware of Global Variables

You might think that since Clojure is a functional programming language, it would save you from global variables. Not automatically. Quite on the contrary, Clojure's web frameworks seem to encourage global variables. I used [Compojure](https://github.com/weavejester/compojure) and its `defroutes` macro relies on global state ([Noir](http://www.webnoir.org/)'s `defpage` appears the have the same problem). Any useful application has some mutable state, but since `defroutes` takes no user-specified parameters, it relies on that mutable state being accessible globally – for example as a `(def app (ref {}))`, or a global database connection or configuration.

Though there are workarounds, the tutorials of those frameworks don't teach any good practices for managing state. The only place where I found good practices being encouraged was the documentation of [clojure.tools.namespace](https://github.com/clojure/tools.namespace), where there is a section [No Global State](https://github.com/clojure/tools.namespace#no-global-state) which tells you to avoid this anti-pattern (though it only glances over *how* to avoid it). The solution is to use [dependency injection](http://misko.hevery.com/2008/11/11/clean-code-talks-dependency-injection/), for example like this:

{% highlight clojure %}
(defn make-routes [app]
  (routes
    (GET "/" [] (the-handler-for-index-page app))
    ...))
{% endhighlight %}

This is almost the same as what the `defroutes` macro would produce, except that instead of the route being a global, we define it as a factory function that takes the application state as parameter and adapts it into a web application. Now we can unit test the routing by creating a new instance of the application (possibly a test double) for each test.


## Future Plans

We will probably run some internal coding dojos with rpi-challenger and do some incremental improvements to it. First of all we'll need to improve the reliability, so that a buggy HTTP server can't make challenger's HTTP client fail, and solve some performance problems when saving the application state with `clojure.pprint` (it takes tens of seconds to write a file under 500&nbsp;KB). Holding the application state in a database might also be a good idea.

In the long run, some new kind of programming competition may be desirable. Maybe something that would require more design from the competitors, for example an AI programming game (one of my first programs was a robot for the MikroBotti programming game back in 2000). A multiplayer AI remake of [Battle City](http://www.mobygames.com/game/nes/battle-city) or Bomberman might be fun, though it remains to be seen how hard it will be to implement an AI for such a complex game in one evening.
