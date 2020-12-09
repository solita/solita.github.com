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

My first interaction with Android was with the very first device during the summer of 2006. As a device, the HTC Dream (T-Mobile G1 in the US) Android phones were revolutionary, especially if you were coming from other feature phones (Nokia, Blackberry, Motorola). Android devices promised to bring into someone's pocket a tiny "laptop" that also did phone calls. The keyboard made it easy to relate. However, when Apple announced the iPhone in January 2007, everything changed: touch and swipes are here to stay.

<center>![HTC Dream]('/img/cross-platform-juggle/htc_dream.png')</center>

<center>![Apple iPhone]('/img/cross-platform-juggle/iphone.png')</center>

There is no denying smartphones have significantly changed. The same applies to the look and feel of the apps on Android and iOS devices. With each iteration, the design language evolved. Under the hood, the programming languages changed too (Java -> Kotlin on Android, Objective-C -> Swift on iOS), further complicating things to someone just starting.

# Take your pick: Android or iOS?

It's **extremely** hard to find someone who has equal development experience with both Android & iOS app development (also known as "Developer Unicorns"). It takes a significant amount of hands-on development experience to truly understand the inner workings of both platforms. And designing an application that feels right at home for each OS requires different ways of thinking on what and how we present an interface. This rationale pushes aspiring mobile developers to focus on one platform. The demand for experienced mobile developers is high, allowing one to find often a place where their honed skills - whether on Android or iOS - fit right in. However, to create a mobile app, the app requirements are assigned to two distinct teams, working in tandem to produce the same experience for both smartphone environments. This creates an overhead of planning and coordination across two teams. Depending on the complementary experience of the team, certain features may be delayed, out of sync, or just outright unimplemented on the other platform.

<div style="width:100%;height:0;padding-bottom:56%;position:relative;"><iframe src="https://giphy.com/embed/THyHTImnrY2sRbgrZb" width="100%" height="100%" style="position:absolute" frameBorder="0" class="giphy-embed" allowFullScreen></iframe></div><p><a href="https://giphy.com/gifs/christinegritmon-why-not-both-THyHTImnrY2sRbgrZb">via GIPHY</a></p>

# Silver Bullet: Cross-platform Frameworks?

Several platforms have emerged to solve this division. Before I dived into Flutter, I wanted to know the pros and cons of what's out there. Most importantly, I wanted to know if Flutter was just another one pilled into a list of contenders. Here's a summary of what I found.

Native | Cross-Platform | ||
-|-|-|-
|| Hybrid app || Web apps ||
iOS (Obj-C/Swift) | Compile to native | Webview | PWA
Android (Java/Kotlin)| React Native <br/> Xamarin <br/> NativeScript | Ionic | PolymerJS <br/> Angular <br/> React

First, the obvious: the **pros for native** are along the lines of "we can fully leverage the platform APIs and thus deliver the best performance and user experience." The **cons for native** are the need for separate codebases and two distinct development teams and the overhead of feature coordination.




# How is Flutter different from Xamarin, React Native, ...?

## UI as Code

## Performance

## Native compiled applications 

## Beyond smartphones

# Read more