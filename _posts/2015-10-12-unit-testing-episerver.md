---
layout: post
title: Automated testing of EPiServer websites
author: riipah
excerpt: How to make it feasible by using mocks and fakes
---

I'm a big fan of automated testing, having had good experiences with keeping complex pieces of software maintainable by having a comprehensive automated test suite. 
When developing websites based on a complex CMS platform such as [EPiServer CMS](http://www.episerver.com/), I often hear opinions saying it's too difficult and not worth the effort. 
However, almost all CMS-based sites have some custom business logic, some more than others, and whenever there's custom logic, there's code that can break when changes are made, 
so regression tests are needed.

## What to test?

The point of this post is not to explain why automated testing should be done, or how to write tests in general. 
I'm also not going to talk about the technical differences between various types of testing, such as unit vs. integration testing. 

That said, I will start by saying that not all code needs to be tested.
When working on any piece of code, but especially one based on a CMS platform, there's plenty of "trivial" code, such as class constructors and accessors, and loops in views for example.
Achieving 100% code coverage by testing such trivial code is usually pointless - it's better tested with end-to-end (system) tests, if at all. 
That said, having some of those end-to-end tests is definitely a good idea, but you have to understand that the more layers your test covers, 
the more difficult writing and maintaining such tests becomes, so there can't be too many of those complex tests. 
Good tests, especially unit tests, are very simple, quick to write and execute, as well as easy to maintain.

Some examples of good candidates for automated tests are:

* Algorithms, such as calculating store opening hours based on a set of rules.
* Systems integration code, such as XML/JSON/CSV parsing and processing.
* Database queries and mappings.
* Any sufficiently complex code that deals with the site structure, such as crawling and listing pages.

## Testing EPiServer-specific code

When working with EPiServer websites, I've noticed that large parts of the code tend to be tightly tied to the EPiServer content repository, 
either by creating and saving content, or by traversing the content tree. I have to admit I don't have much experience with other CMS systems, but I can imagine this will apply to
most of them, or to any other complex software platform. 
The main problem with testing such code is that, similar to having a database backend, initializing the whole system complicates the tests unnecessarily and can't be considered very testable.

The content repository (IContentRepository), as well as most of the core types in EPiServer, are nowadays provided as interfaces, 
so mocking them either by hand or by using a mock framework (such as [Moq](https://github.com/Moq/moq4)) is fairly easy. 
However, I dislike mocking such low-level general purpose interfaces, because as the code is refactored and new features added, it tends to be those low level details that change the most frequently,
and if your tests are tied to too low level details that makes those tests very fragile.

In order to make such code testable, I've used two different strategies:

* Creating another layer of abstraction between the code and the content repository.
* Using a simplified in-memory implementation of the content repository that mimics the behavior of the original EPiServer content repository. This is also called a "fake".

## Writing an abstraction layer

Creating another layer of abstraction is a common method of mocking a general purpose interface. 
For example, a code that deals with product pages on an EPiServer website can manage those pages through an interface called IProductPageRepository, 
with methods for listing, loading and saving those pages. 
Testing against such a simplified, per-task interface is a lot more straighforward than mocking the general purpose interface.