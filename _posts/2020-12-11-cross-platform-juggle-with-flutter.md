---
layout: post
title: Cross-Platform Juggle with Flutter
author: denzilferreira
excerpt: >
  Creating a mobile app is usually tasked to two distinct teams, working in tandem to produce the same experience for Android & iOS users. What if I told you that there is a platform in town that offers a shortcut to create a mobile app in record time, simultaneously on Android, iOS, and maybe beyond towards a web, and as a desktop app?
tags:
 - Software Development
 - Dart
 - Flutter
---

> Author disclaimer: This is my personal view on Flutter and may not reflect the opinion of other Solitans nor the company's stance on Flutter.

# Once upon a time...

My first interaction with Android was with the very first device during the summer of 2006. As a device, the HTC Dream (T-Mobile G1 in the US) Android phones were revolutionary, especially if you were coming from other feature phones (Nokia, Blackberry, Motorola). Android devices promised to bring into someone's pocket a tiny "laptop" that also did phone calls. The keyboard made it easy to relate. I started learning to develop on Android 1.0 and Eclipse. When Apple announced the iPhone in January 2007, everything changed: touch and swipes are here to stay. Android completely changed after that.

<center>![HTC Dream]('/img/cross-platform-juggle/htc_dream.png')</center>

<center>![Apple iPhone]('/img/cross-platform-juggle/iphone.png')</center>

There is no denying smartphones have significantly changed. The same applies to the look and feel of the apps on Android and iOS devices. With each iteration, the design language evolved. Under the hood, the programming languages changed too (Java -> Kotlin on Android, Objective-C -> Swift on iOS), further fragmenting developers.

# Choose your poison: Android or iOS?

It's **extremely** hard to find someone who has equal development experience with both Android & iOS app development (also known as "Developer Unicorns"). It takes a significant amount of hands-on development experience to truly understand the inner workings of both platforms. And designing an application that feels right at home for each OS requires different ways of thinking on what and how we present an interface. This rationale pushes aspiring mobile developers to focus on one platform. The demand for experienced mobile developers is high, allowing one to find often a place where their honed skills - whether on Android or iOS - fit right in. However, to create a mobile app, the app requirements are assigned to two distinct teams, working in tandem to produce the same experience for both smartphone environments. This creates an overhead of planning and coordination across two teams. Depending on the complementary experience of the team, certain features may be delayed, out of sync, or just outright unimplemented on the other platform.

<div style="width:100%;height:0;padding-bottom:56%;position:relative;"><iframe src="https://giphy.com/embed/THyHTImnrY2sRbgrZb" width="100%" height="100%" style="position:absolute" frameBorder="0" class="giphy-embed" allowFullScreen></iframe></div><p><a href="https://giphy.com/gifs/christinegritmon-why-not-both-THyHTImnrY2sRbgrZb">via GIPHY</a></p>

>##### My first project at Solita
>This challenge was evident for a customer project, a 5 Sprint-long project assignment. Our starting point: one mobile app, two codebases, not in sync in terms of functionality. The customer had an upcoming rebranding and reassessment of the functionalities that made sense for their customers. The customer wanted to integrate with a major CRM provider, for which native libraries were available and provide new services down the line.
>
>My options: 1) learn iOS fast, figure out what is missing on both projects after re-evaluating the requirements, perform app rebranding, change the apps to satisfy the requirements, and (lots of) refactoring; or 2) start over, with a cross-platform framework that supported native libraries and had good support for platform look and feel.

# Cross-platform Frameworks

Several platforms have emerged over the years. I wanted to know the pros and cons of what is out there. There are hundreds of posts that compare these. Here is a curated (top-5) list of the reading if you are interested in getting a technologies overview in 2020:

- [Native vs Hybrid vs Cross-Platform - What To Choose?](https://medium.com/flutterdevs/native-vs-hybrid-vs-cross-platform-what-to-choose-3221130f7cc5)
- [React Native vs Flutter vs Ionic vs Xamarin vs NativeScript](https://www.icicletech.com/blog/react-native-flutter-ionic-xamarin-nativescript)
- [React Native vs. Flutter: What to Choose in 2020](https://nordicapis.com/react-native-vs-flutter-what-to-choose-in-2020/#:~:text=React%20Native%20and%20Flutter%20are,popularity%20and%20loyalty%20since%202017.)
- [11 Popular Cross-Platform Tools for App Development in 2020](https://hackernoon.com/9-popular-cross-platform-tools-for-app-development-in-2019-53765004761b)
- [Cross Platform Mobile Apps and Its Pros and Cons](https://medium.com/andolasoft/cross-platform-mobile-apps-and-its-pros-and-cons-9c257ec64e94)

No matter which one we choose as a cross-platform framework, one needs to use a different programming language other than the native (iOS - Swift/Obj-c, Android - Kotlin/Java), in some cases. For example:

Platform | Programming Language | Led by
-|-|-
[React Native](https://reactnative.dev/) | Javascript | Facebook |
[NativeScript](https://nativescript.org/) | TypeScript | Progress/Telerik
[Xamarin](https://dotnet.microsoft.com/apps/xamarin) | C# (.Net) | Microsoft 
[Flutter](https://flutter.dev/) | Dart | Google 

# Why Flutter?

In StackOverflow's 2020 Developer Survey, Flutter came ranked #3 in the [Most Loved, Dreaded and Wanted Other Frameworks, Libraries and Tools](https://insights.stackoverflow.com/survey/2020#technology-most-loved-dreaded-and-wanted-other-frameworks-libraries-and-tools) (with 68.8% of the developer responses), followed by React Native at #10 (57.9%), and Xamarin #16 (45.4%). So clearly, Flutter is a favorite. And there are several reasons for that. 

### Popularity & Community Support
Flutter was initially released in May 2017. The popularity of Flutter exploded, and now has more GitHub stars than React Native ~100K, up from just 30K in August 2018 [[1]](https://www.icicletech.com/blog/react-native-flutter-ionic-xamarin-nativescript)! Powered by [**Dart**](https://dart.dev/), Flutter feels familiar to one **familiar with JavaScript and Java**. Google, Alibaba, and many other software powerhouses have adopted Flutter and considered production-ready [[2]](https://medium.com/capital-one-tech/flutter-a-production-ready-checklist-c202525fab48). As popularity rose, so did the [community](https://flutter.dev/community) around Flutter. As an open-source project, issues and fixes are rapidly addressed. 

### Regularly updated

This may come across as a weakness: why so many updates all the time? Is Flutter that buggy? No, not at all. These updates are more often in performance tweaks and under-the-hood libraries than anything else and they are not breaking changes. During the 5-Sprint long development, I did not encounter a single showstopper due to Flutter. 

I did, however, witness a pause in deployment for my iPhone running iOS 14 with Xcode. Apple released an update on iOS before updating XCode, blocking any development of native iOS apps in the process [[4]](https://appleinsider.com/articles/20/09/16/be-patient-with-developers-as-a-one-day-warning-before-the-full-ios-14-release-is-too-short). As a native developer, all we could do was wait for XCode to be updated (about a week...) to be able to deploy. As I was on Flutter, I continued development as if nothing happened using an Android smartphone as a test device.

### Modularity & reusability
There is a **MASSIVE** [repository](https://pub.dev/) of _plugins_ (cross-platform - not just UI!) that streamline greatly our ability to make a mobile, desktop, backend, all sharing the same language, data models, and business logic. This is a great strength for Flutter, as it offers the opportunity for code reuse, to build upon prior work and testing.

### Flexibility & performance

Flutter is better understood as a rendering engine. For example, with iOS 14 and the introduction of SwiftUI, Flutter had support for the new design language after ONE day [[3]](https://medium.com/better-programming/flutter-for-swiftui-developers-3ee038ef1d4f)! This was possible because Flutter is akin to the native platform UI rendering engine: tell me what you want and where - here it is, painted with pixel-perfect accuracy. There is no converting between a Flutter's UI and native's UI widget. They are both renders on the screen. In fact, in comparison to other cross-platform frameworks, Flutter is the only one that provides reactive views without requiring the JavaScript bridge.

Initially, "mobile apps" cross-platform support took shape as web views, running on [WebKit](https://webkit.org/) - a browser rendering engine. In other words, an embedded web page. The bottleneck is that manipulating the DOM does not offer a great mobile experience: it is slow and inefficient, and animations and touch are sluggish. Not to mention the absence of accessibility support [[5]](https://www.telerik.com/blogs/what-is-accessibility-for-web-apps-and-why-do-i-care).

Other more recent platforms, such as React Native, Xamarin, and others, solved this issue by building a JavaScript bridge, an interface for native code. This was better than the original approach as it bypasses completely the DOM. Let's imagine this scenario: the user presses a button on the interface. How does this work in practice for frameworks like React Native? Let me explain it, based off what is described here [[6]](https://www.manning.com/books/flutter-in-action):

##### Protocol in React Native, Xamarin, etc...

<center>
![JavaScript bridge approach]('/img/cross-platform-juggle/javascript-bridge-protocol.png')
</center>

Every time an application (1) needs to talk with the rendering engine (4), it has to be compiled to native code (2) to communicate with the platform widgets (3) using the JavaScript bridge. In a single interaction in (1), say a touch, the bridge needs to be crossed twice: once from the application to the device, and then back from the device back to the application.

##### Protocol in Flutter

<center>
![Flutter approach]('/img/cross-platform-juggle/flutter-protocol.png')
</center>

Flutter, being a rendering engine on itself (2), eliminates the need for a bridge. Being compiled to native code, Flutter handles the rendering of the visuals: the canvas (where the rendering occurs) and events are handled on the device itself (3) and there is no conversion between non-native and native counterparts.

### Beyond smartphones

**Web**: Currently in [Beta](https://flutter.dev/web), you can build responsive, offline-first, PWAs, websites, blogs using Flutter, supported across a multitude of web browsers, shielded from Javascript and DOM compatibility woes. A nice overview of what is currently supported in Flutter Web is [here](https://medium.com/fluttersg/the-art-of-flutter-flutter-web-383d5db568a0). And see this [DEMO](https://sbis04.github.io/explore/#/) if you are looking for a demo, opening it on your mobile phone and desktop browsers.

**Desktop**: Currently in [Alpha](https://flutter.dev/desktop), you can build native Windows, macOS, or Linux desktop applications. To compile targeting a specific platform, you need to be on that platform, i.e., you can not create a macOS app on a Windows machine. Once could assume that by being alpha the support would be lacking. There is already a plethora of plugins for each of the OS ([Windows](https://pub.dev/flutter/packages?platform=windows), [macOS](https://pub.dev/flutter/packages?platform=macos), and [Linux](https://pub.dev/flutter/packages?platform=linux)). To get started, you can find a guided CodeLab [here](https://codelabs.developers.google.com/codelabs/flutter-github-graphql-client/index.html#0).

**Backend**: [Aquaduct](https://aqueduct.io/) - OK! This is not Flutter... but it is built with Dart! :sweat_smile: Aqueduct is an object-oriented, multi-threaded HTTP server framework, running on top of Dart VM. It has an integrated test library allowing for end-to-end integration tests without requiring mocking, and supports the continuous integration tools we love.

To showcase Flutter across platforms, you can take a look at [Flutter Gallery](https://github.com/flutter/gallery), a truly cross-platform app shared by Google. All in all, I'm excited for Flutter. There is a fear that Flutter will disappear. However, given the ongoing secrecy on [Fucshia OS](https://www.theverge.com/2020/12/8/22163225/google-fuchsia-os-call-contributors-mailing-list-governance), I would not be surprised to find Flutter powering future devices, in all shapes and forms.

# Final Thoughts

> In regards to my first assignment, the use of Flutter was a joyful experience. We were able to create both an Android and iOS application, using one codebase, that included the rebranding (approved on Sprint 3 and implemented throughout the app in under 2 weeks!), the approved functionality, and native visuals on both Android and iOS. It made sense to use Flutter for this project! In fact, in a couple of pair-programming sessions, our app designer could visually inspect and suggest tweaks to the UI and see the results immediately due to Flutter's hot-reload capabilities, greatly reducing the overhead of the rebranding.

Would I use Flutter again? "Yes, please." The non-biased answer though is: **it depends**.

At the end of the day, all comes down to the project resourcing and the shared knowledge within a team. As I see it, with Flutter, we could have a unified team - **we are stronger together** <3 - where iOS and Android (and perhaps backend and desktop?) are all embraced and have a shared role, working within the "app" for native-only dependencies. An "app" then transcends from mobile-only to omnipresent across platforms and form factors. Given the plugin architecture of Flutter and Dart, one can build reusable cross-platform plugins for mobile, desktop, and web, useful to any future projects. And to me, that is a future I look forward to. One that we leverage our shared collective know-how.

# References
* [1] https://www.icicletech.com/blog/react-native-flutter-ionic-xamarin-nativescript
* [2] https://medium.com/capital-one-tech/flutter-a-production-ready-checklist-c202525fab48
* [3] https://medium.com/better-programming/flutter-for-swiftui-developers-3ee038ef1d4f
* [4] https://appleinsider.com/articles/20/09/16/be-patient-with-developers-as-a-one-day-warning-before-the-full-ios-14-release-is-too-short
* [5] https://www.telerik.com/blogs/what-is-accessibility-for-web-apps-and-why-do-i-care
* [6] Flutter in Action, by Erin Windmill - https://www.manning.com/books/flutter-in-action