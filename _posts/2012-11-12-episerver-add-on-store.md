---
layout: post
title: Why does EPiServer Add-On Store matter?
author: jarno
excerpt: EPiServer 7 ships with the Add-On Store. It will give us feature packaging to manage the solution better. But it's not the real reason I like the concept.
tags: episerver cms appstore prototyping
---
[EPiServer 7](http://www.episerver.com) was released last week. One of the features I have a good feeling about is the [add-on store](http://www.episerver.com/Products/EPiServer-7-CMS/CMS-functions/). In theory it would allow non-techies to install new site features using a web user interface. Actually it sounds quite scary at first. On the other hand Wordpress and its kin have had similar features for ages.

### Feature packaging ###
In the past we've had a customer ask us to reuse a blog module from the EPiServer templates. It makes perfect sense not to implement everything from scratch. Unfortunately there isn't a real blog module available from EPiServer. You can only install "Demo Templates" and have a lot of garbage installed at the same time. It's not something we want on a production site.

In the future we could have a couple of alternative Blog Add-Ons to choose from in a similar situation. The Add-On store encourages developers to package the modules as sane-sized bundles so we wouldn't have too much garbage to get rid of. If the Add-On installation is as easy as clicking "install" in the Add-On store, we get better results with less hassle.

### It's all about Prototyping ###
The Add-On store will give us feature packaging to manage the solution better. But it's not the real reason I like the concept. *The main benefit of the Add-On store is fast prototyping.* There are many typical website features we discuss in every project. With the Add-On store we can install a basic implementation and start the discussion from there. It's a lot more concrete, more visual and more immediate way to drive the design process. Most likely the need is a bit different than what the Add-On provides, but sometimes we might get lucky.
