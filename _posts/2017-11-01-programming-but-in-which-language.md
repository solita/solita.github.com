---
layout: post
title: Programming - but in Which Language?
author: riikkanen
excerpt: This time the language options discussed are English and Finnish. Should I write a method called addApplication or addHakemus (hakemus being application in Finnish)?
tags:
- programming
- domain
- language
- culture
---

Usually there is a debate over which programming language the project should use. Is Clojure better than Java? Should we use Python? Even JavaScript? This time we do not care what the programming language is, but what language is used to describe the domain. Should all the code be in English, or should method names and variables be in Finnish? This is a relevant question, when we, mostly Finnish speaking developers, build a software to a Finnish customer. 

## addApplication() - everything in English 

This is fine. We developers are used to reading and writing program code in English. If the code base, comments and even commit messages are totally in English it is even possible to have non-Finnish-speaking developers in the team. That is very likely to happen even in the near future, because Solita is now recruiting also in Sweden. According to comments from our developers, all code in English is the natural way to do it.

Using English as the domain language is a natural choice if the customer operates internationally or the domain is already in English. If the customer gives the domain vocabulary, it is easy to adopt in the project and the conversation about business logic is not distracted by misunderstood semantics because of language.

If the domain can easily be translated into English, it can be done. This should be done carefully, maybe in cooperation with the customer. The translation might require some expertise, because it makes difference if you translate Finnish 'asiantuntija' literally as 'thingKnower' instead of more sensible 'expert'. After the translation, the vocabulary should be documented. Without shared vocabulary the code will soon be full of 'experts', 'specialists' and 'professionals' when every developer is making own translations. The documentation also helps new developers entering the project.

If the domain is translated, the translation should be used in all layers. Keep your database, server, client and front consistent and use the same language and vocabulary in every level.

## addHakemus() - domain in Finnish

But. Let us think that the customer is a Finnish company operating only in national business with a complex domain. Maybe the domain is even regulated by legislation. All the domain concepts might not even have an exactly equivalent word in English. There is no point of just making words up; it just leads to misunderstandings. When the lack of exact vocabulary is seen as a risk, it might be reasonable to keep Finnish as the domain language. Using the legit domain vocabulary throughout the database, software, and documentation guarantees also a common language for the developers and the customer.

Usually the decision of using the Finnish domain language is made with the customer. This, of course, makes difficult to adapt non-Finnish-speaking developers to the project. One can surely learn the domain names, and if the code, comments and commit messages are in English, it might be possible to enter the project. However, in the real life, the method names can be quite complicated and impossible to understand despite of the few English words in the middle, or what would you say about actual (anonymized) test method 'jotainWithjotainMuutaWithVireillaolevaJokuHasOnlyVoimassaolevatJotkut'.

## lisaaHakemus() - all naming in Finnish

If we decide to keep the domain in Finnish why would not use Finnish in every method, variable, package, class, etc. names. The Finnish domain vocabulary has already made difficult to really adapt non-Finnish-speaking developers in the project, so why not use Finnish everywhere it is possible. Some developers rather use consistently Finnish in all naming than mix English and Finnish but there are also opposite opinions. 

## How do we do?

I made a simple poll to our developers to find out how the real project life in Solita looks like. I got 43 answers from different projects. The programming languages utilized in the projects varied; there were Java, Clojure, NodeJS, JavaScript, Python, C/C++ and C# projects.

It seems that the language decicions depend mostly on the domain of the project. According to the poll, the Finnish domain language is used mostly in the projects where the customer belongs to the public administration of Finland (e.g. Finnish Transport Agency, Social Insurance Institution of Finland or National Land Survey of Finland). In some of these cases, the programming in Finnish is required by the customer.

In the cases were the chosen domain language is Finnish, it is more popular to write domain-specific code entirely in Finnish than to mix English and Finnish. However, there can be some exceptions, such as the names of non-domain-specific utility library functions and lower lever functions, which can use English, such as 'insertHakemusUsingJdbc'. 

It seems like the chosen domain language does not affect to the chosen programming language or vice versa. There is Clojure code both in English and in Finnish, same with Java. The JavaScript projects reported were all in English, same as few Python projects. The C projects reported were either entirely in English or just domain in Finnish.

Mostly the developers coding in Finnish were satisfied with the chosen language. To start with it has been awkward but after a while it came really fluent. Some even say that it is much better than clumsy translations or mixing two languages.

## Keep the practice

The poll also revealed that some long-lasting projects have evolved containing mixed practices. For example, the language has changed during the years, or the methods are named in several ways depending on the developer. 

The domain language and the code style related are decicions that should be discussed carefully and made in the beginning of the project. The decicion (and possible translations) should be documented, maybe included in the development guide of that project, and also introduced to the new developers entering the project. 


