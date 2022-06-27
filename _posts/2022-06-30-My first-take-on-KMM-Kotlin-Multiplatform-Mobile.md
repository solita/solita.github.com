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
  - Dev Academy
---

## Backstory

In order to finish the Dev Academy I've had to develop an application as my practice assignment. I've been provided a mentor - Denzil Ferreira, whom I was guided by throughout the process. The purpose of practice assignment is to provide to a freshly recruited junior developers a safe environment, in which they can work on a small feature of an application or simple application of their own. Moreover, thanks to mentor guidance development gets done in a very proffessional fashion and is a great way to kickoff start for a new software designer.

On the initial project kick off discussion, my mentor and I have decided that to mix things up a little I should develop the app in a technology that I am not super familiar with. After talking over several different possibilities we settled with KMM - Kotlin Multiplatform Mobile. Some of the reasons behind this decision were: my familiarity with Native Android Development and the fact that KMM is just an emerging technology and what's new is exciting and worth exploring.

## KMM

Kotlin Multiplatform Mobile (KMM) is a tool developed by JetBrains that tries to simplify iOS and Android app development. It aims to connect cross platform and native- development.

### Wait, how?

The way to create an applications with KMM is to develop one shared codebase for business logic and then separate codebases for each platform specific features. Separate codebases are always for UI and depending on a case for platform related functionality. This approach doesn’t reduce native performance but still saves time and effort as you do not have to write redundant business logic in both apps. 

![Native and cross-platform development benefits](/img/kmm-my-first-take/kmm-comparison-table.svg)

On top of that, KMM also lets us decide how much of the actual code we want to share between the platforms and what parts will be written separately. For instance, we can decide that only business logic will be shared between platforms or that we will share API calls, local database and business logic, you get the point.

![Ability to share code survey](/img/kmm-my-first-take/kmm-survey.svg)

## Okay… we get it, but how does that work in practice?

KMM project is made of 3 modules: Android, iOS and shared module. Code in shared module can be called by Android or iOS module, and naturally code in platform related modules cannot be called in shared module. In other words shared module is available for the other modules but not other way around. 
![Project structure](/img/kmm-my-first-take/package-structure.png)

In shared module most of the code is written in commonMain package however, sometimes our shared code cannot work without platform dependent stuff. That's why in shared module we have androidMain and iosMain packages. In case of developing the platform depended code in shared module we must use KMM specific Kotlin mechanism of expected and actual declarations. The simplest example is already generated for us by KMM plugin while creating a project: 


In shared module we create class without any implementation code

```
expect class Platform() {
   val platform: String
}
```

And then in each platform module by using actual keyword we provide the actual implementation of expected code. 

In Android module:

```
actual class Platform actual constructor() {
    actual val platform: String = "Android ${android.os.Build.VERSION.SDK_INT}"
}
```


In iOS module:

```
actual class Platform actual constructor() {
    actual val platform: String = UIDevice.currentDevice.systemName() + " " + UIDevice.currentDevice.systemVersion
}
```

## My implementation

Alright, so the project that gave me opportunity to test KMM in practice was Dev Notary. A simple application that lets developers create notes, documentations or memos and interact with them. Basic CRUD with addition of sharing the notes with other users. App requirements were simple:
- Authentication
- Managing a note: create, read, edit, delete, share
- Restore notes
- List, sort, search 

In order to get this done properly I’ve decided to give myself a day to research other Kotlin Multiplatform Mobile projects, to learn from them, get some inspiration and only after that start planning my app. Thanks to that investigation, I’ve realized that I can actually share quite a lot of code between both platforms. After some planning it was decided that in order to test this untamed technology I should try to share as much code as I possibly can.

While looking for possible libraries that could make my expedition easier, I’ve found a library that implements Firebase SDK with pure Kotlin and therefore, enables usage of Firebase directly from shared module. Excellent! For local database I’ve decided to use safest option SQLDelight and for key value pairs multiplatform settings. Additionally, I’ve picked Kodein DI for dependency injection, Multiplatform UUID for well... UUIDs and several other libraries for minor tasks.

Okay but how to keep all this code separated and neat so that it's easily testable and the presentation layers are not actually dependent on any shared module code? With a MVVM and clean architecture!

![Architecture diagram](/img/kmm-my-first-take/architecture.png)

I could have shown here the actual code snippets from my application so that You could see how KMM actually gets done but by doing this, this post would become extremely long and probably dull for most readers. Instead, I'll demonstrate some gifs of the application to show that it actually works smoothly and I'll link the [repository](https://github.com/solita-michalguspiel/DevNotary) so whoever's curious can look into the code. I recommend having a look at implementation of shared module [iOS package](https://github.com/solita-michalguspiel/DevNotary/tree/main/shared/src/iosMain/kotlin/com/solita/devnotary) and [Android package](https://github.com/solita-michalguspiel/DevNotary/tree/main/shared/src/androidMain/kotlin/com/solita/devnotary) to get a grasp of expect/actual mechanism. In case of Dev Notary I have used it in order to implement iOS working ViewModel, timer and ISO8601 date formatting.

## Application

![Running application](/img/kmm-my-first-take/creating-note.gif)
*Creating notes*

![Sharing note](/img/kmm-my-first-take/sharing-note.gif)
*Sharing notes*

## Looking back

Since my expertise lays in Android, development was done Android first. At the very beginning there were some configuration issues caused by KMM, adding one library dependency resulted in breaking other dependencies, there were mysterious errors while building projects and whatnot. Despite those, development of shared codebase and Android application went relatively effectively. First big blocker was encountered after starting development of iOS application, since I had no knowledge of iOS development and KMM didn't work exactly as I imagined it. I had to slightly adjust shared module while learning Swift, SwiftUI and iOS development in general. This slowed the process significantlly. However, I want to emphasize that development of Android application with KMM wasn't any different than doing completely Native Android App, despite some bumps with configuration of course. What was great though was that in order to create iOS app, I only had to implement the UI. After implementing "AddNoteView" and "NotesListView" for iOS it just worked out of the box. It felt that it could be super effortless only if I would have experience of iOS development. 


## References 

 - [KMM](https://kotlinlang.org/lp/mobile/)
 - [List of sample projects](https://kotlinlang.org/docs/multiplatform-mobile-samples.html)
