---
layout: post
title: Why does EPiServer Add-On Store matter?
author: jarno
---
[EPiServer 7](http://www.episerver.com) was released last week. One of the features I have a good feeling about is the add-on store. In theory it would allow non-techies to install new site features using a web user interface. Actually it sounds quite scary at first. On the other hand Wordpress and it's kin have had similar features for ages.

### Feature packaging ###
In the past we've had a customer ask us to reuse blog module from the EPiServer templates. It makes perfect sense not to implement everything from the scratch. Unfortunately there ain't a real blog module available from EPiServer. You could only install "Demo Templates" and have a lot of garbage installed at the same time. It's not something we want on a production site. 

Thinking a bit in the future we'd have a couple of alternative Blog Add-Ons to choose from in a similar situation. The Add-On store would encourage developers to package the modules as sane-sized bundles and we wouldn't have too much garbage to get rid of. The Add-On installation has to be made as easy as clicking install on the Add-On store. That's better results with less hassle.

### It's all about Prototyping ###
Add-On store will give us feature packaging to manage the solution better. But it's not the reason I actually like the concept. *The main benefit of Add-On store is fast prototyping.* There are many typical website features we're discussing from case to case. With Add-On store we can install a basic implementation and start the discussion from there. It's a lot more concrete, more visual and more immediate way to do the design process. Most likely the need is a bit different than what the Add-On provides. Sure we might get lucky sometimes.
