---
layout: post
title: Programming - but in Which Language?
author: riikkanen
excerpt: This time the language options discussed are English and Finnish. Should I write a method called addApplication or addHakemus?
tags:
- programming
- domain
- language
- culture
---

Usually there is a debate over which programming language the project should use. Is Clojure better than Java? Should we use Python? Even JavaScript? This time we do not care what programming language is chosen, but what language is used to describe the domain. Should all the code be in English, or should method names and variables be in Finnish? This is a relevant question, when we, mostly Finnish speaking developers, build a software to a Finnish customer. 

## addApplication() - everything in English 

This is fine. We developers are used to reading and writing program code in English. If the code base, comments and even commit messages are totally in English it is even possible to have non-Finnish-speaking developers in the team. That is very likely to happen even in near the future, because Solita is now recruiting also in Sweden. According to comments from our developers, all code in English is seen as the natural way to do it.

Using English is always a natural choice if the customer operates internationally or the domain is already in English. If the domain vocabulary is given from the customer, it is easy to adopt and probably the conversation about business logic is not distracted by misunderstood semantics.

If the domain can be easily translated into English, it can be done. This should be done carefully, maybe in cooperation with the customer. The translation might require some expertise, because it makes difference if you translate Finnish 'asiantuntija' literally as 'thingKnower' instead of more sensible 'expert'. After the translation, the vocabulary should be documented. Without shared vocabulary the code will soon be full of 'experts', 'specialists' and 'professionals' when every developer making own translations. The documentation also helps when new developers come to the project.

If the domain is translated, the translation should be used in all layers. Keep your database, server, client and front consistent and use the same language and vocabulary in every level.

## addHakemus() - domain in Finnish

But. Let us think that the customer is a Finnish company operating only in national business with a complex domain. Maybe the domain is even regulated by legislation. All the domain concepts might not even have an exactly equivalent word in English. There is no point of just making words up, it just leads to misunderstandings. When the lack of exact vocabulary is seen as a risk, it might be reasonable to keep the domain vocabulary in Finnish. Using the legit domain vocabulary in throughout the database, software, and documentation guarantees also a common language for the developers and the customer.

Usually the decision of using the Finnish domain language is made with the customer. This, of course, makes difficult to adapt non-Finnish-speaking developers to the project. The domain names can surely be learned, and if the code, comments and commit messages are in English, it might be possible to enter the project. However, in the real life, the method names can be quite complicated and impossible to understand despite the few English words in the middle, or what would you say about actual test method 'jotainWithjotainMuutaWithVireillaolevaJokuHasOnlyVoimassaolevatJotkut'.


