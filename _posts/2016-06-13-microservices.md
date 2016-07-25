---
layout: post
title: He started using microservices and you won't believe what happened....
author: arto
excerpt: Easy introduction to microservices
categories: 
- Microservices
tags: 
- JavaScript
- Microservices
- NodeJS
---

Okay, that was a total clickbait, and a sad one at that. But this article is about microservices, so listen up. Microservices can be a wonderful thing to have, especially in agile projects, but it can also be an extremely dangerous tool to use in your architectures. I'm going to try and explain some points here.

To start up, here's simple structure of very simple and typical monolithic application:

![Basic monolithic app architecture](/img/microservices-simple/monolithic.jpg)

When application is simple and has only few responsibilities, this is an okay solution. It's easy enough to maintain with not so many moving parts. The module doesn't get too big and it makes sense to have a few database tables in the same spot. Troubles occur, however, when this module grows larger. Build times go up, LOC indicators go crazy with hundreds of thousands or millions of lines of code mixed up in the same container. If anything goes wrong, all the functionality is offline. Reusability is pretty much zero - of course clever architects may still use libraries here to get a little bit of reusability.

Microservice is a suitable-sized and independent processing unit, that provides a value increment all by itself. Meaning, it does something useful, and only communicates via APIs, doesn't expose, for example, its database directly or go to other databases except through APIs. Well, anyways, that's what a good microservice is, isolated and useful.

Here's a microservice in node.js.

```javascript
var express = require("express");
var bodyParser = require("body-parser");
var app = express();
 
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
 
app.get("/", function(req, res) {
    res.send(new Date());
});
 
var server = app.listen(3000, function () {
    console.log("Listening on port %s...", server.address().port);
});
```

Not what you expected? Disappointed? Well, it's still a microservice. It provides a service, and it is isolated and independent. More importantly, it's perfect for sake of explaining some things, since it's simple enough to easily understand. You can compose something bigger with it, and other services like it, a bit like we did in good old days of SOA. 

## Interconnected Microservices

Here's another microservice. This one is a counter.

```javascript
var express = require("express");
var bodyParser = require("body-parser");
var app = express();
 
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

var counter = 0;
 
app.get("/", function(req, res) {
	counter++;
    res.send(""+counter);
});
 
var server = app.listen(4000, function () {
    console.log("Listening on port %s...", server.address().port);
});
```


So, for sake of conversation, let's say that our first microservice wants to use the second one, naturally through the APIs. Let's do that modification:

```javascript
var express = require("express");
var app = express();
var Client = require('node-rest-client').Client;
var client = new Client();
  
app.get("/", function(req, res) {
	client.get("http://localhost:4000", function (data, response) {
    	console.log(data.toString());
	});
    res.send(new Date());
});
 
var server = app.listen(3000, function () {
    console.log("Listening on port %s...", server.address().port);
});
```

So this is where it starts to get a bit more interesting. It's easy to write a hundred of small concentrated services. Actually, any service is a microservice when you start it from scratch. When the amount of code needed grows, you start seeing the challenges - and benefits - of modular architecture. By having them all be interconnected via APIs, we get a highly modular and flexible structure with reusable components, ready to face the future with low cost of change.

![Wannabe microservices](/img/microservices-simple/wannabe.jpg)

You can see that our current date microservice is dependent on counter microservice. So we have two points of failure here, to say the least. If counter service suddenly goes down, date service will also stop working. Furthermore, we're not even dealing with it gracefully. And how about things like scalability, and security?

Of course you can see that these microservices are pretty ridiculous. Any service starts up as microservice - it's small and concentrated on some task. Real challenges come when amount of code and responsibilities grow.


## Microservices challenges

Well, there's not much to do about performance. Using APIs carries an overhead. Sure, you can use caches like Redis to share and maintain information, but caches carry their own share of issues and can only be used sometimes. Calls will be a bit slower overall than in monolithic applications. How much slower, depends of course on how often you do them and how much data gets moved, how many horizontal layers your architecture has, etc. As always, there's a lot you can do to optimize by just thinking about these things. But in the end, it will be somewhat slower than monolithic ugly clump of code. That's the price to pay.

How about scalability and robustness? Well, we can take somewhat old ideas to a new context, and do a lot good things here. To scale we can easily add more microservices units, of course we then need some kind of router/load balancer to distribute the calls - furthermore we need it in between every place where we want to have scalability. Perhaps it is wise to write it once and re-use for all services. There exists a host of solutions for this already, naturally. By having at least two units doing the processing, you have redundancy, too. But at this point you get more challenges to solve, too. How about that database? Do you have one, which is the bottleneck and single point of failure, or do you have multiple copies, in which case you need to set up rules for replication?

And on the topic of databases: Services should not really share data, they should own it and regulate it. When another service needs your data, they need to go through the API layer. Otherwise there's dependency and clutter that will take away some of your microservice benefits. 

![Microservices own their data](/img/microservices-simple/microservices.jpg)

For robustness, you need to also consider what happens when a service goes down, and others depend on it. If a failure means that dependent services will also break, you are introducing a nasty chain of failures - to put it bluntly: If anything breaks, all will break. So good microservices design will design for failure. You will spend some time thinking what would happen if this API were not available - perhaps due to network error, API error, database error, etc. There are very useful microservices patterns and even tools to cope with this challenge - circuit breaker, for example. And if you design for failure, you can create a system that actually is tolerant for failure. If some parts fail, some parts will still remain usable, just with missing functionality. This is not just about circuit breakers, but more a mindset for your designs.

API management and API versioning? Once you start running this architecture, you might find yourself in situation where you cannot just evolve a specific API, but you need to maintain a few versions of it. At this point you will be very thankful if you spent a few moments to think about this before writing your first microservice. Microservices are actually pretty easy to version, since they are typically self-contained, but of course you have to deal with database structures, where you put your version info, how does it work in your service catalogs, etc.

![One plate of spaghetti, anyone?](/img/microservices-simple/spaghetti.jpg)

Basically at this point you want to have some kind of pattern/strategy to have your microservices behaving nicely together. One point being that if services all own their data, there must be some place where data from services is merged, used together.

There are some options:

1. UI knows all microservices and uses them all directly as needed
2. Service Orchestration - there's a master-microservice, that will control all the other services. If necessary, it may also act as microservices Facade, hiding complexities from client.
3. Service Choreography - all services are equal, they just converse together. This model works best if there's some kind of bus or channel and loose binding model - definite benefit here is very robust architecture, not dependent on any single module.

This model only describes who is aware of all the services, who knows that a service exists? There are also other patterns/tools, such as API Gateways, which can answer this question and more questions, offering centralized everything. Yet another case of facade pattern in action.

## How secure can that be?

Finally some words about microservices security. In the monolithic days of Enterprise Servers, you would typically only spend time to resolve the security settings once, then reuse them until hell froze over. For example, set up that LDAP registry in your Websphere, and then all applications deployed in that server can use the same identity and grouping information to authorize their access. Well now we don't have those heavyweight servers anymore, in the world of microservices. (They wouldn't be very micro, would they? That's more like put-all-your-egs-in-same-huge-basket-architecture.) 

What we have is integration, and co-operation. So you should have a microservice, or existing single sign-on mechanism deal with identity once, somewhere, then reuse that same information for all services. Technologies like OAUTH are popular here, but simpler versions can also use JWT tokens - or even custom headers with AD authentication. Of course there are also other considerations, such as where and what you need/want to decrypt, how you maintain container level security such as certificates, ssl settings, etc, but there's less new things to discover here.

## Microservices behaving nicely

So, here are some simple indications that what we have created is a real microservice architecture. Some of these can be argued. As with any hype there are many definitions of microservices. This, however, is my definition:

- Do your microservices constrain themselves to only one piece of functionality, or at least a few conjoined ones?
- Are there more than one? If not, it's probably just a trivial application ;)
- Do your microservices own and control their own data?
- Can they tolerate temporary failures of other services they are calling?
- In other words, is the architecture composed of a fault-tolerant network of co-operating independent modules. 

If you passed this test, congratulations. You are getting lots of the benefits of microservices architecture. If you failed in some places, don't feel bad. Not many can do this right at the moment. Also, you do get some benefits even by getting this partially right. You just have to be aware that doing it partially right will also bring you some nasty downsides, such as multiple vulnerability spots, code replication, etc.

So I'm not really interested so much in size limits, like how many lines of code there are. LOC indicators are very boring and pretty much always wrong.

## Microservices evolution

The really difficult stuff begins when you love the microservices so much that you start having them in multiple applications, conversing via APIs, in a style reminiscent of old SOA.

![Microservices evolution](/img/microservices-simple/evolution.jpg)

This is still much valid for microservices, and you're even getting new benefits here. Unfortunately, any problems and risks we discussed in context of single application just went even more severe. For this kind of architecture it's essential to have good monitoring capabilities and good enough logging so when something goes wrong you have some traceability. If you really want to play in the big boys league, you probably want also some self healing capabilities, in addition to building for failure like we discussed in earlier chapter. While it's certainly possible to write all these functionalities (preferably in Scala or Clojure ;) - it would be much more cost effective to take a look at some existing available open source libraries that can accelerate your work. 

But to get this far you need to be really serious about microservices, so I presume you've done your homework and are anxious to take things to a new level.

## Conclusion

So, if you are a master at microservices, there is nothing new here. If you wanted to get an idea what are microservices, hopefully you got that. And if you thought microservices are just services less than 200 lines of code, well, I hope you got re-educated. You can create a truly abhorrent mess with microservices, like with any powerful tool. A bit of thought and planning goes a long way here, too. And this is just the microservices model for 2016 - I bet in 2020 we will be lauhghing at how naive that was.

Idea of using simple examples written from scratch to introduce the idea was to make it easy to approach. I plan to later write out what you can do with some of the existing tools like Eureka and Hystrix. There are also other pretty cool tools out there such as Consul and Ribbon - and Scala Actors are pretty cool stuff, too! 

Meanwhile, if you like to play with the simple examples shown here, they're in The Git: 

[Simple Microservices Repository](https://github.com/crystoll/blog-simple-microservices)

Note that they're not very good or interesting examples, just food for thought, barebones enough to get a taste of what challenges lie ahead when you start doing microservices. Likewise, if you have comments, or disagree or agree strongly with some points made here, please let me know, that's why the comments section exists ;)


