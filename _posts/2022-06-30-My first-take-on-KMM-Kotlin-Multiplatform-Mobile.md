---
layout: post
title: My first take on KMM - Kotlin Multiplatform Mobile
author: michal.guspiel, denzilferreira
date: 2022-06-30 15:00:00 +0200
excerpt: As for a first project and practice assignment in Solita I've had explored new technology - KMM and created Dev Notary, a simple application that lets users create, modify and share notes between other users.

tags:
  - KMM
  - Android
  - Kotlin
  - Mobile
  - Multiplatform
  - iOS
  - Swift
  - Dev Academy
---

# Preface

In order to finish the Dev Academy, I've to develop an application as my practice assignment. I've been provided a mentor - Denzil Ferreira, whom I was guided by throughout the process. The purpose of practice assignment is to provide to freshly recruited junior developers a safe environment, in which they can work on a small feature of an application or simple application of their own. Moreover, thanks to mentor guidance development gets done carefully and is a great way to kickoff start for a new software designer.

On the initial project kick-off meeting, my mentor and I have decided that to mix things up a little I should develop the app in a technology that I am not super familiar with. After going over several different possibilities, we settled with Kotlin Multiplatform Mobile (KMM). Some of the reasons behind this decision were: 1) my familiarity with Native Android Development and 2) KMM is an exciting and emerging technology worth exploring for a streamlined mobile development team.

# Kotlin Multiplatform Mobile

[Kotlin Multiplatform Mobile](https://kotlinlang.org/lp/mobile/) (KMM) is a tool developed by JetBrains to simplify iOS and Android app development. Kotlin Multiplatform empowers cross-platform (e.g., mobile, desktop, web) and yet also supports native- development on such platforms. This article focuses on the Mobile side of things.

## Slicing apps into layers of concern

To create an applications with KMM is to develop one shared codebase for business logic and then separate codebases for each platform specific features. Separate native codebases are usually for UI, and occasionally more, depending on a case for platform related functionality. This approach doesn’t reduce native performance as Kotlin is compiled to native execution code. KMM saves teams' time and effort as you do not have to write redundant business logic in both apps, nor coordinate between teams for feature parity.

![Native and cross-platform development benefits](/img/kmm-my-first-take/kmm-comparison-table.svg)

In addition, KMM offers flexibility to decide how much of the code is shared between the platforms. For instance, we can decide that only business logic will be shared between platforms, or that we will share API calls, or local database and business logic, and so forth.

![Ability to share code survey](/img/kmm-my-first-take/kmm-survey.svg)

## KMM 101

KMM project is made of 3 modules: **androidApp** (Android native project and app code), **iosApp** (Xcode native project and app code) and **shared** module (everything that should be shared across both Android and iOS apps). Code in shared module can be called by the Android or iOS modules, and naturally code in platform related modules cannot be called in shared module. An introduction to KMM is available [here](https://docs.google.com/presentation/d/1qVjRuTgEbw7gyF-ETlRnqL_Lk4MeaQGV66zHwQ9gEUU/edit?usp=sharing).

![Practical project structure - Dev Notary](/img/kmm-my-first-take/package-structure.png)

In **shared** module most of the code is written in **commonMain** package however, sometimes our shared code cannot work without platform dependent stuff. That's why in **shared** module we have **androidMain** and **iosMain** packages. In case of developing the platform depended code in shared module we must use KMM specific Kotlin mechanism of expected and actual declarations. The simplest example is already generated for us by KMM plugin while creating a project: 


In **shared** module we create __expect__ classes inside **commonMain**. Think of them as interfaces, without any implementation code, or a template of what should be converted to native code via KMM compilers:

```Kotlin
expect class Platform() {
   val platform: String
}
```

And then in each platform module, we implement the **actual** class we created as expect: 

In **androidMain**:

```Kotlin
actual class Platform actual constructor() {
    actual val platform: String = "Android ${android.os.Build.VERSION.SDK_INT}"
}
```


In **iosMain**:

```Kotlin
actual class Platform actual constructor() {
    actual val platform: String = "iOS ${UIDevice.currentDevice.systemVersion}" 
}
```

## My Dev Notary implementation

Alright, so the project that gave me opportunity to test KMM in practice was Dev Notary. You can find the project pitch [here](https://docs.google.com/presentation/d/1iQYibISIREyWV02GtvO5TPkzlbcVgZWi-XdXGsPp_5I/edit?usp=sharing). Dev Notary is a simple application that lets developers create notes, documentations or memos and interact with them. Basic CRUD with addition of sharing the notes with other users. The functional requirements were simple:
- Authentication
- Managing a note: create, read, edit, delete, share
- Restore notes
- List, sort, search 

In order to accomplish this, I’ve decided to give myself a day to research other Kotlin Multiplatform Mobile projects, to learn from them, get some inspiration and only after that start planning my app. Thanks to that investigation, I’ve realized that I can actually share quite a lot of code between both platforms. After some planning it was decided that in order to test this untamed technology I should try to share as much code as I possibly can.

While looking for possible libraries that could make my expedition easier, I’ve found a library that implements Firebase SDK with pure Kotlin and therefore, enables usage of Firebase directly from the shared module! 💪 

As for local database, I’ve decided to use safest option SQLDelight and for key value pairs multiplatform settings. Additionally, I’ve picked Kodein DI for dependency injection, Multiplatform UUID for Universal Unique IDs.

Okay but how to keep all this code separated and neat so that it's easily testable and the presentation layers are not actually dependent on any shared module code? With a MVVM and clean architecture!

![Architecture diagram](/img/kmm-my-first-take/architecture.png)

I could have shown here the actual code snippets from my application so that You could see how KMM actually gets done but by doing this, this post would become extremely long and probably dull for most readers. Instead, I'll present some animated parts of the application, to show how it all works and I'll link the [repository](https://github.com/solita-michalguspiel/DevNotary) so whoever's curious can look into the code. 

I recommend having a look at implementation of shared module [iOS package](https://github.com/solita-michalguspiel/DevNotary/tree/main/shared/src/iosMain/kotlin/com/solita/devnotary) and [Android package](https://github.com/solita-michalguspiel/DevNotary/tree/main/shared/src/androidMain/kotlin/com/solita/devnotary) to get a grasp of expect/actual mechanism. In case of Dev Notary I have used it in order to implement iOS working ViewModel, timer and ISO8601 date formatting.

## Application

![Running application](/img/kmm-my-first-take/creating-note.gif)
*Creating notes*

![Sharing note](/img/kmm-my-first-take/sharing-note.gif)
*Sharing notes*

## Looking back

Since my expertise lays in Android, development was done Android first. At the very beginning there were some configuration issues caused by KMM, adding one library dependency resulted in breaking other dependencies, there were mysterious errors while building projects and whatnot. Despite those, development of shared codebase and Android application went relatively effectively. First big blocker was encountered after starting development of iOS application, since I had no knowledge of iOS development and KMM didn't work exactly as I imagined it. I had to slightly adjust shared module while learning Swift, SwiftUI and iOS development in general. This slowed the process significantlly. However, I want to emphasize that development of Android application with KMM wasn't any different than doing completely Native Android App, despite some bumps with configuration of course. What was great though was that in order to create iOS app, I only had to implement the UI. After implementing "AddNoteView" and "NotesListView" for iOS it just worked out of the box. It felt that it could be super effortless only if I would have experience of iOS development. 


## References 

 - [List of sample projects](https://kotlinlang.org/docs/multiplatform-mobile-samples.html)
 - [Dev Notary source code](https://github.com/solita-michalguspiel/DevNotary)
