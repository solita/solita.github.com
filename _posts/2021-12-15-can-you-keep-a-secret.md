---
layout: post
title: Can you keep a secret?
author: denzilferreira, eetupajuoja
excerpt: >
    Building a mobile application that keeps secrets (API, tokens, certificates) safe is hard. In this post, we share 
    what strategy we followed to create an app that is OWASP compliant and prevents deobfuscation and 
    binary deconstruction exploits to flood our backend.
tags:
 - Mobile
 - Android
 - iOS
 - OWASP
 - Themis
 - Secrets
---

# Preface
We are currently building an app (**Koronatodistus Lukja** - [Android](https://play.google.com/store/apps/details?id=fi.thl.koronatodistus), [iOS](https://apps.apple.com/fi/app/koronatodistuksen-lukija/id1583958695?l=fi)). 
Both Android and iOS applications are available worldwide and therefore our backend is not geofenced. Our apps 
communicate with the backend for several read-only REST endpoints, except for one write-only REST endpoint. This 
endpoint is available over HTTPS POST, protected with an API key and an [HMAC](https://en.wikipedia.org/wiki/HMAC) code.

# Watching out for tinkerers

How do we keep a "secret", secret? Rooted/jailbroken smartphones, allow access to the device internal storage and 
retrieval of application binaries (**.ipa** and **.apk**, for iOS and Android respectively)... so a technically and driven
individual could deconstruct the binary and seek for any exploitable API keys, tokens, especially if they are injected
via a CI pipeline.

### Android

On Android, Gradle compiles the application. To safely prevent a secret from being ever committed to version control
systems VCS (e.g., GitHub), the recommended strategy is to declare these within **yourUser** directory:

> - Mac/Linux: /Users/**yourUser**/.gradle/gradle.properties
> - Windows: C:\Users\\**yourUser**\\.gradle\gradle.properties

The benefit of such approach is that such variable will be available to any project that uses Gradle and there is no
risk of having gradle.properties committed to VCS. This allows you to compile, test and deploy the app to a development
unit without relying on a third-party source for the keys or tokens. Reading the values is as simple as reading them as 
a Gradle property and using them as we wish.



### iOS

