---
layout: post
title: My first take on KMM - Kotlin Multiplatform Mobile
author: michal.guspiel
date: 2022-?-? 08:00:00 +0200
excerpt: As for a first project and practice assignment in Solita I've had explored new technology - KMM and created Dev Notary, a simple application that lets users create, modify and share notes between other users.

tags:
  - KMM
  - Android
  - Kotlin
  - Mobile
  - Kotlin MultiPlatform Mobile
  - iOS
  - Swift
---

## Backstory

In order to finish the Dev Academy I've had to develop an application as my practice assignment. I've been provided a mentor - Denzil Ferreira, whom I was guided by throughout the process. The purpose of practice assignment is to provide to a freshly recruited junior developers a safe environment, in which they can work on a small feature of an application or simple application of their own.

On the initial project kick off discussion, my mentor and I have decided that to mix things up a little I should develop the app in a technology that I am not super familiar with. After talking over several different possibilities we settled with KMM - Kotlin Multiplatform Mobile. Some of the reasons behind this decision were: my familiarity with Native Android Development and the fact that KMM is just an emerging technology and what's new is also exciting and worth exploring.



## KMM

Kotlin Multiplatform Mobile (KMM) is a tool developed by JetBrains that tries to simplify iOS and Android app development. It aims to connect cross platform and native- development.

## Wait, how?

The way to create an application with KMM is to develop one shared codebase for business logic and two separate codebases for each platform specific features. Separate codebases are always for UI and depending on a case for platform related functionality. This approach doesn’t reduce native performance but still saves time and effort as you do not have to write redundant business logic in both apps. 

![Native and cross-platform development benefits](/img/kmm-my-first-take/kmm-comparison-table.svg)

On top of that, KMM also lets us decide how much of the actual code we want to share between the platforms and what parts are meant to be written separately. For instance, we can decide that only business logic will be shared or business logic, API calls and local databases. You get the point.

![Ability to share code survey](/img/kmm-my-first-take/kmm-survey.svg)

## Okay… we get it, but how does that work in practice?

Alright, so the project that gave me opportunity to test KMM in practice was Dev Notary. A simple application that lets developers create notes, documentations or memos and interact with them. Basic CRUD with addition of sharing the notes with other users. App requirements were simple: • Authentication • Managing a note: create, read, edit, delete, share • Restore notes • List, sort, search notes

In order to get this done properly I’ve decided to give myself a day to research other Kotlin Multiplatform Mobile projects, to learn from them, get some inspiration and only after that start planning my killer app. Thanks to that investigation, I’ve realized that I can actually share quite a lot of code between both platforms. So, I decided that in order to test this untamed technology I should try to share as much code as I possibly can.

While looking for possible libraries that could make my expedition easier, I’ve found a library that implements Firebase SDK with pure Kotlin and therefore, enables usage of Firebase directly from shared module. Excellent! For local database I’ve decided to use safest option SQLDelight and for key value pairs multiplatform settings. Additionally, I’ve picked Kodein DI for dependency injection, Multiplatform UUID for well... UUIDs and several other libraries for minor tasks.

Okay but how to keep all this code separated and neat so that easily testable and presentation layers are not actually dependent on any shared module code? With a MVVM and clean architecture!

![Architecture diagram](/img/kmm-my-first-take/architecture.png)



### References 

 https://kotlinlang.org/lp/mobile/
