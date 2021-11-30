---
layout: post
title: Can you keep a secret?
author: denzilferreira, eetupajuoja, spheroid-

excerpt: 
> Building a mobile application that keeps secrets (API, tokens, certificates, server URLs) safe is hard. In this post, we share 
  a strategy to create an app that is OWASP compliant and prevents deobfuscation and 
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
We are currently building an app that has sensitive data. Both applications are available 
worldwide and therefore our backend is not geofenced. Our apps communicate with the backend for several read-only RESTful 
API endpoints, except for one write-only for statistics. This write-only endpoint is offered over HTTPS POST, 
and is protected with an API key and an [HMAC](https://en.wikipedia.org/wiki/HMAC) signature code.

# Watching out for tinkerers 🕵️

So, how do we keep these "secret" values (API key, HMAC code, server URL...), secret? Rooted/jailbroken smartphones, allow access to the 
device internal storage and the retrieval of application binaries (**.ipa** and **.apk**, for iOS and Android respectively)
is possible... a technically and driven individual could deconstruct the binary and dig out exploitable API keys, tokens, 
especially if they are injected via a CI pipeline and stored internally in clear text.

What can we do? Fortunately, there are tools to help us and a set of steps we can follow to protect our secrets. Shall we 
"spill the beans"? 😅 Let's start with Android and then iOS.

## Android

On Android, Gradle compiles the application. To safely prevent a secret from being ever committed to version control
systems (VCS) e.g., GitHub, the recommended strategy is to declare these within **yourUser** directory:

> - Mac/Linux: /Users/**yourUser**/.gradle/gradle.properties
> - Windows: C:\Users\\**yourUser**\\.gradle\gradle.properties

### Keep your secrets in ~/.gradle/gradle.properties

```properties
api_key=hk5j43hk5jh34k5jh345kj34h5kjg345kjg34k5jg3kj45
hmac_code=kj3h45kj3h4k5hjg34lö23hl423lk4h23lk4h23g4kl1k2h3
server_url=https://hacker-honeypot.fi
```

The benefit of this approach is that such variables will be available to any project that uses Gradle we may be working
on for our local machine, and there is no risk of having this gradle.properties committed to VCS. This allows you to 
compile, test and deploy the app to a development unit or environment without relying on a third-party source for the 
keys or tokens. Reading the values is as simple as reading them as a Gradle property and using them as we wish.

### App module build.gradle configuration

To support both local deployments, and CI/CD deployments, create a tiny utility
Groovy function before the **android** code block:

```groovy
String getSecret(String key) {
    return project.findProperty(key) ? System.getenv(key) : ""
}

android {
  //...
}
```

Then inside the **defaultConfig** code block, we retrieve these values:

```groovy
defaultConfig {
  //...
  buildConfigField "String", "API_KEY", "\"${getSecret("api_key")}\""
  buildConfigField "String", "HMAC_CODE", "\"${getSecret("hmac_code")}\""
  buildConfigField "String", "STATS_URL", "\"${getSecret("stats_url")}\""
}
```

Now our "secrets" are available in Kotlin/Java from the Gradle generated BuildConfig object for our app module.
Doing this will prevent us from committing the secrets to VCS, but doesn't protect the secrets from being in the clear
inside the binary 😱 Luckily for us, there is a solution for this, which is endorsed by OWASP: a cross-platform
high-level cryptographic library called **[Themis](https://www.cossacklabs.com/themis/)**.

### Themis to the rescue 🔐

Let's start by adding Themis as a project dependency, editing **build.gradle** inside the app module:

```groovy
dependencies {
  implementation 'com.cossacklabs.com:themis:0.13.1'
}
```



## iOS

