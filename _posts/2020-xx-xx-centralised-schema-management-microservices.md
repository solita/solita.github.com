---
layout: post
title: Centralized schemas and microservices, match made in hell?
author: vehvis
excerpt: >
  Schemas - love 'em or hate 'em, can't live without 'em &mdash; not even when you're doing microservices. In this post I describe
  how we centralized our schema management into a (hopefully) long-term solution, all the while keeping a tenuous hold of our sanity.
tags:
 - Microservices
 - Clojure
 - Development
 - Architecture
---


# Intro

So you've ended up in the microservice swamp, or somewhere else where you need to deal with a zoo full of fractious, opinionated, distributed systems. Now you've found out that there's a set of common things many of your services need to have a shared understanding about, but don't. You also prefer to retain even a bit of your dwindling sanity until the project is over. What to do?

This article is an attempt to distill into a digestible format the experiences I and my team have had during the last few years building a distributed system around centralized schema management. I'm not entirely sure we were that sane to begin with, but at least in our case the sanity loss has been manageable. Your mileage may vary, caveat emptor, etc.

__Centralized schema__, in its most simplified form, means that you have a *common authority* who can tell every other part of your system (service, API, lambda function, database, etc.) what kinds of objects or data structures your system contains. It's the responsibility of each service to determine what to do with that information &mdash; the assumption being, however, that whenever a service needs to communicate with other services (or the outside world) about a __Thing__ it should use the authority-provided definition of that __Thing__.

Systems that need to work with a large set of __various kinds of data objects across multiple services__ are the prime candidates to benefit from centralized schema management. Many don't, and since CSM means giving up a portion of the flexibility service-oriented architectures (whether micro, midi or macro) bring, it's not a good fit for every system.

In our case we have a system that is supposed to manage all the assets of the Finnish national road network. Assets in this case meaning the roads themselves (surface material, how many lanes, ...), and anything related to them such as traffic signs, surface markings, fences, off-ramps, service areas, various measurements, and so on. Altogether that's roughly a hundred different types of asset. Each of them needs to be imported, stored, validated, exported to interested parties via some API, returned as search results, drawn on a map... you get the idea. 

# Why centralize schema if everything else is distributed?

The common wisdom around microservices is that everything needs to be decentralized. That's how you are supposed to reap their benefits. Unfortunately, that wisdom tends to slink away (looking slightly guilty as it goes, with those benefits in its pocket) whenever you need to have more than two of your services talk about something, because it's a lot of work to keep all parties in agreement on what they're talking about.

CSM is a tool and architectural pattern to manage that problem. It forces all parties interested in a given kind of data to use a standard definition of it &mdash; what properties the data has, what is the set of allowed values for each property, which ones are mandatory, and so forth. This is typically not optimal from the viewpoint of any particular service, since depending on how they're built they usually have a richer set of tools available than the smallest common denominator an external schema represents. For example, a TypeScript-based service would rather use its own type system for defining objects, and a relational schema defined in SQL in the fourth normal form is a thing of beauty compared to any JSON schema document.

For systems that have just a few kinds of data, or just a few different services that deal with it, the tradeoff is likely not worthwhile. But when you have a dozen services that all need to be able to process some or all of the set of 100 data types, implementing CSM is the only way to stave off the impending madness. Even if that results in all of your services having to submit to a jackbooted overlord who controls what they may or may not say in public. (Please do not try to extrapolate this into anything human-related.)

# A portrait of a CSM in three acts

## The MVP

To be of any use, a CSM implementation, whether homebrew or off-the-shelf, needs to include at least the following:

- __Some way to distribute schemas__ in a format or formats that are understood by all parts of the system.
   - Your options format-wise include [JSON Schema](https://json-schema.org/), [Apache Avro](https://avro.apache.org/docs/current/spec.html), [Protobuf](https://developers.google.com/protocol-buffers/docs/proto) schemas, and the comedy options of XML Schema or RELAX-NG. (Not going to link to those two.)
   - Ideally you define your schema just once, and distribute it in multiple formats.
   - If you have, or suspect you'll have in the future any external APIs, then your selection narrows. There are not many formats that are widely accepted, and JSON Schema is probably the least problematic option.
- For each of your services, a means of __consuming (using) the schema__. Having multiple formats available makes it easier to find a nice consumer or validator.
   - It's a nice bonus if your consumer can process the schema into something native for your under-the-hood implementation. This includes F# type providers, Clojure spec or Plumatic schema, or even just plain old Java code generators. (Let's not mention JAXB.)
   - If you can do this runtime, that's even better. But you can often get by with compile-time consumption.
- Schema distribution to consumers can be done during compilation or packaging, but it's more microservicey if you have a __schema registry service__. It can just be nginx serving static files, in a pinch.

## We're not in MVP land anymore

The above is fine for a workshop demo. However, it's likely your system will need something a bit more advanced to survive in the wild.

- __Support for schema evolution__. Schemas are like war plans, they never survive enemy contact. You need to prepare for this by having a way to handle changes to your schemas without the need to rebuild everything and breaking all your external APIs.
  - But what to do if you end up with an object of version 1, and you need to upgrade it into version 3? Or the reverse?
  - __Transform__ is what you do. Your CSM system can help by providing transformation services, or supplying transformation instructions alongside your schemas. To do this efficiently and in a way compatible with as many languages and platforms as possible is difficult, though. More on this later on.
- __Support for schema composition__. If you need CSM to begin with, then your data types probably have things in common between them. You'll want to be able to compose your schemas from components. It's boring and error-prone to copy-paste the same list of `create-time`, `created-by`, `modify-time` and `modified-by` properties to every schema.
  - I don't need to mention this complicates evolution and transformation somewhat, do I?
  - You could also consider deriving schemas from other schemas, but that smells like OOP-style inheritance and we don't do that.
- __Enumerations as first class citizens__. Real-world systems always have various lists of enumeration-type values which evolve over time. You need to be able to apply the same tools to them as the rest of your schemas: evolution, transformation, etc.
- __API management integration__ &mdash; if you can connect your CSM with your API management solution you can have it handle inbound/outbound data validation for you.

## Nah, man. I'm pretty friggin' far from MVP

In for a penny, in for a pound? Why not go for the whole hog? Since you're already committed, why leave money on the table by not extracting some more value from your fancy bespoke CSM? Such as:

- __Embed business logic into your schemas.__ If your CSM supports arbitrary metadata you can include things such as UX rendering instructions alongside your property definitions.
  - This opens up the rabbit hole of dynamically constructing forms and other UX layouts purely based on your schema. Don't say I didn't warn you.
  - Other possibilities include having things like embedded Elasticsearch mappings (for the special cases where you can't generate them automatically from your schema, of course.)
- __Allow runtime end-user modifications to your schemas__ (probably just administrators, but still.) If the previous item was a rabbit hole, then this is a portal to the netherworld. All of your services would need to be capable of runtime schema reloading for this to work.

This will quickly veer into "if all you have is a hammer" territory so let's stop here.

# Are there existing options?

Yes.

There are things like [Confluent Schema Registry](https://docs.confluent.io/current/schema-registry/index.html) which provides tight integration with Apache Kafka but also works with anything else that can consume JSON Schema, Avro or Protobuf. I don't have any hands-on experience with it, but looks like it provides most, but not all of the functionality described above.

In any case, we rolled our own because we could not find anything fitting our requirements. This article is too long to include a market survey in any case.

# How we did it (and why)

As I said above, in our project ([Velho](https://vayla.fi/hankkeet/digitalisaatiohanke/tieverkon-kunnonhallinta/velho-allianssi), for the [Finnish Transport Infrastructure Agency](https://vayla.fi/)) we ended up creating our own, custom centralized schema management solution. This was due to a few reasons:

- Our project has to produce a long-lived system, and our architectural solution to that was a "midi-service" (i.e. less granular than micro, but definitely not a monolith) approach. So we would have a moderately large amount of independent services, each with their own responsibility of data storage etc.
- To allow for a [ship of Theseus](https://en.wikipedia.org/wiki/Ship_of_Theseus) -type evolution path for the entire system, our internal architecture would explicitly and consistently support a polyglot implementation. This means every service chooses its own tech stack, and disallows the use of any integration technologies specific to any single language or platform. To keep us honest we dogfood, i.e. consume internally the same protocols and APIs we provide externally.
- The number of data types our system needs to manage is around 100, of varying complexity, each with their own properties, quirks etc.
- The above made the need for a CSM evident early on.
- The existing options did not feel suitable. Granted, we didn't do any really comprehensive research. So sue us.

## Our stack

[AWS native](https://aws.amazon.com/architecture/well-architected/). Containerized with AWS Fargate, FaaS with AWS Lambda. Multiple independent SQL databases (Aurora PostgreSQL). Elasticsearch. Redis. S3. AWS API Gateway. Infrastructure-as-Code via CloudFormation.

Languages: [Clojure](http://clojure.org) backend services. [ClojureScript](https://clojurescript.org/) frontend with [Reagent](https://reagent-project.github.io/), [Re-frame](https://github.com/day8/re-frame) and [Web Components](https://www.webcomponents.org/introduction). Lambdas in Clojure, Python and Javascript.

## What we use CSM for

- We validate incoming data (APIs, import jobs, etc) using CSM-provided schemas.
  - Old schema versions are supported for inbound data, and we automatically transform them into the latest schema if needed.
- We use [Elasticsearch](https://aws.amazon.com/elasticsearch-service/) to provide advanced search capabilities, and generate ES indexes automatically based on our schemas, with custom mappings embedded in the schema metadata
- When we read data from our own storage, we validate and (if needed) upgrade its schema version. This allows us to not bother with updating our data in storage whenever our schemas change &mdash; we have multiple kinds of storage backends, not all of which are suited for in-place update.
- We provide schema definitions for our external partners in [OpenAPI](https://openapis.org) format
- We provide a "data catalog" user interface for our end users, which includes human-friendly descriptions of the various data types we manage
- We construct various UX views into our data dynamically based on our schemas. This includes...
  - schematic views of the road network
  - a search builder allowing the end user to graphically construct a complex query into our data
  - in the future we'll provide asset view and update forms generated from our schema

## Get to the point already

It's built in [Clojure](http://clojure.org) like most of the rest of our project and deployed as a Docker container. The schemas themselves are written as [EDN](https://github.com/edn-format/edn) files, which are more-or-less equivalent to JSON or YAML files, but with added Clojureness (including the ability to embed code). Each of the schema definitions contains the complete description of a single datatype, including
- All of its __versions__ from the beginnings of time until the current day. Versions are identified by monotonically increasing numbers (1,2,3,5...)
- __Transformations__ from one version into the next. We only support transformations upward (i.e. increasing versions). A gap in version numbering indicates that an automatic transformation would not be possible.
- For each version, a __specification of its properties__: their types, cardinalities, whether optional or mandatory... Collections including lists and sets are supported, as are nested objects. We are limited mainly by what's possible to express in JSON Schema.
- __Arbitrary metadata__ for the asset and all its properties. This includes human-readable names, Elasticsearch mappings and anything else we'll come up with. We also use metadata for routing: each asset defines which of our services "owns" it and thus requests for it can be routed to the correct service.


Here's a (sanitized, redacted and translated) example of the schemas for __Fence__, which is part of the __Road Furniture__ namespace (and therefore owned by the `furniture-registry` service). There are two schema versions, a transformation from v1 to v2, and some metadata. The schemas refer to two generic components (the `velho/import` directive) which include properties defined elsewhere, and there's a property whose type is an enum schema (`velho/enum`).

```clojure
{:latest-version 2
 :versions {1 (velho/import
                   [:general/basic-props
                    :location/linear-location]
                   {:properties {:code string?
                                 (ds/opt :material) (velho/enum :furniture/material)
                                 :type (velho/enum :furniture/type)
                                 :size (ds/maybe pos-int?)}})

            2 (velho/import
                   [:general/basic-props
                    :location/linear-location]
                   {:properties {:code string?
                                 (ds/opt :material) (velho/enum :furniture/material)
                                 :type (velho/enum :furniture/type)
                                 :width (ds/maybe pos-int?)}})}

 :transforms {1 "$merge([$, {'properties': $merge([$sift($, function($v, $k) {$k != 'size'}), {'width': $.'size'}]),
                             'version': 2}])"}

 :metadata  {:oid-prefix "1.2.246.578.5.100"
             :owner-service :furniture-registry
             :indexing true
             :name "Fence"
             :fields {:properties {:_metadata {:name "Properties" :indexing true}
                                   :code {:_metadata {:name "Code" :index true}}
                                   :material {:_metadata {:name "Material" :index true}}
                                   :type {:_metadata {:name "Fence type" :index true}}
                                   :height {:_metadata {:name "Fence height" :index true}}}}}}
```

We don't serve these EDNs outside our schema registry service. EDN is a Clojure-specific format, therefore it's an implementation detail, and we want to punish everyone equivalently. Our schemas are transformed into an [OpenAPI 3](https://openapis.org) definition (which is an extension of JSON Schema) and served via a REST API.

## Eat it up

Currently we consume our schemas only from Clojure or ClojureScript code. We have a reverse transformer, from OpenAPI to EDN, after which we can feed the resulting data to [Data Spec](https://github.com/metosin/spec-tools), ending up with Clojure specs. (It's not a coincidence that the "native" data format is so close to Data Spec already. Hooray for dynamic languages and runtime `eval`).

__Yes, we do runtime consumption of schemas and our services (both frontend and backend) can handle schemas that change on-the-fly.__

## About those transforms...

More than meets the eye, isn't it?

As I alluded to somewhere above, transformations between schema versions are an issue, primarily because we can't really define them in a language/platform-independent way. (Unless we go full XML Schema in which case XSLT would work. But we don't want to. Never go full XML.) Fortunately we have a good-enough solution in [JSONata](https://jsonata.org/) which is an expression language for querying and transforming JSON-like data. It has implementations for Java, JavaScript, Python and .NET (at least), covering the common platforms nicely.

In the example above, the JSONata transform takes a version 1 object, adds a key `properties.width` which is set to the value of the `properties.size` key, and removes the now-unnecessary `size`. It additionally sets the `version` property to equal 2, as is good and correct for a version 2 object. (The version is not defined here, since it is imported from the `general/basic-props` component schema alongside many other properties).

An astute reader would at this point note that JSON Schema and OpenAPI do not have support for these kinds of transformations. That's entirely correct &mdash; we have custom consumer-side code to run them, and we deliver the transformations via OpenAPI extensions. Our consumers so far have been solely Clojure or ClojureScript-based, so we only have client code for browsers (JSONata/JS used from ClojureScript) and the JVM (JSONata/Java via interop from Clojure).

# Can I play with your toys?

Hopefully yes, in the near future! We'd like very much to open-source our CSM implementation but there's a few bureaucratic hurdles to overcome yet (and it needs some cleanup).

# Final words

To summarize:
- Centralized schema management is necessary when you have a distributed system with many data types handled by many services. 
- There are a lot of decisions you need to make when implementing CSM related to formats, schema evolution, transformations etc.
- Planning for the future is _haram_ in the Agile methodology, but in this case you might want to make an exception, since CSM tends to infiltrate all parts of your system whether you want it to or not.
- Properly done CSM makes microservice architecture slightly more manageable.
- You can throw together a bespoke CSM if you need to and be pretty happy in the end.
- I know this because we did it.
- We ended up implementing quite a lot of advanced features, including schema evolution with embedded transformations, runtime schema loading, etc. 

This took a long time to write. I sincerely hope it's not been completely boring and you got something useful out of it. 


## Acknowledgements

The things described in this post are a result of a lot of teamwork. While I might have written the largest number of lines (easy enough when you end up throwing away the entire first implementation!) the good stuff wouldn't have been possible without the rest of the Velho team. Thank you, Mikko, Kimmo and the rest &mdash; you know who you are and you're awesome! The dumb metaphors are my own.
