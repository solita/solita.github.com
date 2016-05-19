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

###He started using microservices and you won't believe what happened....

Okay, that was a total clickbait, and a sad one at that. But this article is about microservices, so listen up. Microservices can be a wonderful thing to have, especially in agile projects, but it can also an extremely dangerous tool to use in your architectures. I'm going to try and explain some points here.

Microservice is a suitable-sized and independent processing unit, that provides a value increment all by itself. Meaning, it does something useful, and only communicates via APIs, doesn't expose for example its database directly or go to other databases except through APIs. Well, anyways, that's what a good microservice is, isolated and useful.

Here's a microservice in node.js.

´´´javascript
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
´´´

Not what you expected? Disappointed? Well, it's still a microservice. It provides a service, and it is isolated and independent. More importantly, it's perfect for sake of explaining some things, since it's simple enough to easily understand. You can compose something bigger with it, and other services like it, a bit like we did in good old days of SOA. 

## Interconnected Microservices

Here's another microservice. This one is a counter.

´´´javascript
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
´´´


So, for sake of conversation, let's say that our first microservice wants to use the second one, naturally through the APIs. Let's do that modification:

´´´javascript
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
´´´

So this is where it starts to get a bit more interesting. It's easy to write a hundred of small concentrated services. Actually, any service is a microservice when you start it from scratch. When amount of code needed grows, you start seeing the challenges - and benefits - of modular architecture. By having them all interconnect via APIs, we get a highly modular and flexible structure with reusable components, ready to face the future with low cost of change.

You can see that our current date microservice is dependant on counter microservice. So we have two points of failure here, to say the least. If counter service suddenly goes down, date service will also stop working. Furthermore, we're not even dealing with it gracefully. And how about things like scalability, and security?

Of course you can see that these microservices are pretty ridiculous. Any service starts up as microservice - it's small and concentrated on some task. Real challenges come when amount of code and responsibilities grow.


## Microservices challenges

Well, there's not much to do about performance. Using APIs carries an overhead. Sure, you can use caches like Redis to share and maintain information, but caches carry their own share of issues and can only be used sometimes. Calls will be a bit slower overall, than in monolithic applications. How much slower, depends of course on how often you do them and how much data gets moved, how many horizontal layers your architecture has, etc. As always, there's a lot you can do to optimize by just thinking about these things. But in the end, it will be somewhat slower than monolithic ugly clump of code. That's a price to pay.

How about scalability and robustness? Well, we can use somewhat old ideas in a new world to do a lot here. To scale we can easily add more microservices units, of course we then need some kind of router/load balancer to distribute the calls - furthermore we need it in between every place where we want to have scalability. Perhaps it is wise to write it once and re-use for all services. There exists a host of solutions for this already, naturally. By having at least to units doing the processing, you have redundancy, too. But at this point you get some more challenges to solve, too. How about that database? Do you have one, which is bottleneck and single point of failure, or do you have multiple copies, in which case you need to set up rules for replication.

And on topic of databases: Services should not really share data, they should own it and regulate it. When another service needs your data they need to go through the API layer. Otherwise there's dependency and clutter that will take away some of your microservice benefits. 

For robustness, you need to also consider, what happens when a service goes down, and others are dependent on it. If a failure means that all other services dependent on this API will also break, you are introducing a nasty chain of downtimes - to put it bluntly: If anything breaks, all will break. So good microservices design will design for failure. You will spend some time thinking what happens if this API is not available - perhaps due to network error, API error, database error, etc. There are very useful microservices patterns and even tools to cope with this challenge - circuit breaker for example. And if you design for failure, you can create a system that actually is tolerant for failure. If some parts fail, some parts will still remain usable, just with some missing functionality. This is not just about circuit breakers, but more a mindset for your designs.

API management and API versioning? Once you start running this architecture, you might find yourself in situation where you cannot just evolve a specific API, but you need to maintain a few versions of it. At this point you will be very thankful if you spent a few moments to think about this before writing your first microservice. Microservices are actually pretty easy to version, since they are typically self-contained, but of course you have to deal with database structures, where you put your version info, how does it work in your service catalogs, etc.

Finally microservices security. In monolithic days of Enterprise Servers, thinking was to resolve the security settings once, then reuse them until hell freezes over. For example, set up that LDAP registry in your Websphere, and then all applications deployed in that server can use same identity and grouping information to authorize access. Well we don't have those heavyweight servers anymore, in world of microservices. (They wouldn't be very micro, would they? That's more like put-all-your-egs-in-same-huge-basket-architecture.) 

What we have is integration, and co-operation. So have a microservice - or non-microservice deal with identity once, somewhere, then use that same information for all services. Technologies like OAUTH are popular here, but simpler versions can also use JWT tokens - or even custom headers with AD authentiation. Of course there are also other considerations, such as where and what you need/want to decrypt, how do you maintain container level security such as certificates, ssl settings, etc, but there's less new things to discover here.

So, if you are a master at microservices, there is nothing new here. If you wanted to get an idea what are microservices, hopefully you got that. And if you thought microservices are just services less than 200 lines of code, well, I hope you got re-educated. You can create a truly abhorrent mess with microservices, like with any powerful tool. A bit of thought and planning goes a long way here, too. And this is just the microservices model for 2016 - I bet in 2020 we will be lauhghing at how naive that was.

Idea of using simple examples written from scratch to introduce the idea was to make it easy to approach. Next time I'll write about using some building blocks to accelerate your work. You will hear about things like Seneca, Eureka, Consul, Ribbon, and Hystrix - well at least some of them. Or you can go look them up right now. Pretty cool stuff! Also, read up on Scala Actors - they're pretty cool stuff if you want to go all reactive with your microservices.

Meanwhile, if you like to play with the simple examples shown here, they're in The Git: 

[Simple Microservices Repository](https://github.com/crystoll/blog-simple-microservices)
