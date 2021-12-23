---
layout: post
title: Can you keep a secret?
author: denzilferreira, eetupajuoja, spheroid-

excerpt: > 
  Building a mobile application that keeps secrets (API, tokens, certificates, server URLs) safe is hard. In this post, we share 
  a strategy to create an app that uses Themis as a safeguard against deobfuscation and 
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

So, how do we keep these "secrets" (API key, HMAC code, server URL...)? Rooted/jailbroken smartphones, allow access to the 
device internal storage and the retrieval of application binaries is possible... 
(**.ipa** and **.apk**, for iOS and Android respectively). A technically and driven individual could deconstruct the binary 
and dig out exploitable API keys, tokens, especially if they are injected via a CI pipeline and stored internally in clear text.

What can we do? Luckily for us, there is a solution for this which is acknowledged by OWASP: a cross-platform
high-level cryptographic library called **[Themis](https://www.cossacklabs.com/themis/)**. Let's start with Android and then iOS.

## Android

On Android, Gradle compiles the application. To safely prevent a secret from being ever committed to version control
systems (VCS) e.g., GitHub, the recommended strategy is to declare these within **yourUser** directory:

> - Mac/Linux: /Users/**yourUser**/.gradle/gradle.properties
> - Windows: C:\Users\\**yourUser**\\.gradle\gradle.properties

### Keep your secrets in ~/.gradle/gradle.properties

```properties
secret1=hk5j43hk5jh34k5jh345kj34h5kjg345kjg34k5jg3kj45
secret2=kj3h45kj3h4k5hjg34lö23hl423lk4h23lk4h23g4kl1k2h3
secretUrl=https://hacker-honeypot.fi
```

The benefit of this approach is that such variables will be available to any project that uses Gradle we may be working
on for our local machine, and there is no risk of having this gradle.properties committed to VCS. This allows you to 
compile, test and deploy the app to a development unit or environment without relying on a third-party source for the 
keys or tokens. Reading the values is as simple as reading them as a Gradle property and using them as we wish.

### App module build.gradle configuration

To support both local deployments, and CI/CD deployments, create a tiny utility
Groovy function before the **android** code block:

```groovy
String getValue(String key) {
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
  buildConfigField "String", "SECRET_1", "\"${getValue("secret1")}\""
  buildConfigField "String", "SECRET_2", "\"${getValue("secret2")}\""
  buildConfigField "String", "SECRET_URL", "\"${getValue("secretUrl")}\""
}
```

Now our "secrets" are available in Kotlin/Java from the Gradle generated BuildConfig object for our app module.
Doing this will prevent us from committing the secrets to VCS, but doesn't protect the secrets from being in the clear
inside the binary 😱

### Using Themis 🔐

Let's start by adding Themis as a project dependency, by editing **build.gradle** inside the app module:

```groovy
dependencies {
  implementation 'com.cossacklabs.com:themis:0.13.1'
}
```

Themis encrypts and decrypts in runtime our secrets using an encryption key. So we'll an encryption key into our
user's gradle.properties file:

```groovy
xpto=3hgjkh6g23jlhg65hj345g6kjh3g456uhyjg
```

and then in the application build.gradle, in the defaultConfig block:

```groovy
defaultConfig {
  //...
  buildConfigField "String", "SECRET_1", "\"${getSecret("secret1")}\""
  buildConfigField "String", "SECRET_2", "\"${getSecret("secret2")}\""
  buildConfigField "String", "SECRET_URL", "\"${getSecret("secretUrl")}\""
  buildConfigField "String", "XPTO", "\"${getSecret("xpto")}\""
}
```

#### Obfuscating the encryption key

This encryption key will then be manipulated in runtime and used to encode/decode the secrets. We start by creating an 
encryption key obfuscation function. It is good practice naming this function as something 
that would make it harder to identify in deconstructed binaries (in this example, **crashIt()**) so be creative here!

```kotlin
private fun crashIt() : ByteArray {
    val rawKey = buildString(5) {
        append(byteArrayOf(0x11, 0x07, 0x10).toBase64())
        append(BuildConfig.XPTO)
        append("87bvc765bds876fg87sfd6g876309480")
    }
    return rawKey.toByteArray()
}
```

#### Creating encoded versions of the secrets

Then we create an encoding function to encrypt the original keys as a Base64 string - **be creative here and call it something else**!:

```kotlin
fun String.encode(): String {
    val encodingKey = crashIt()
    val cell = SecureCell.SealWithKey(encodingKey)
    val protected = cell.encrypt(this.toByteArray())
    return Base64.encodeToString(protected, Base64.NO_WRAP)
}
```

We can then replace the secrets in our CI/CD pipeline with these encoded Base64 strings. This means that even the CI/CD
will not know what the secrets are! The only key that is on the CI/CD is the encryption key. Because we are obfuscating
the encryption key in runtime as well, even if someone found the encryption key, they would still need to find what 
runtime operations we do to it in order to restore the real encryption key.

#### Decoding the encoded versions of the secrets

To decode the encrypted Base64 strings, we then need a function to restore the original secret in runtime - **be creative here and call it something else**:

```kotlin
fun String.decode(): String? {
    val encodingKey = crashIt()
    val cell = SecureCell.SealWithKey(encodingKey)
    return try {
        val decoded = Base64.decode(this, Base64.NO_WRAP)
        val unprotected = cell.decrypt(decoded)
        val decrypted = String(unprotected)
        decrypted
    } catch (error: SecureCellException) {
        Timber.d("Failed to decrypt")
        null
    }
}
```

Now we can use the decode() function on the Base64 string to restore in runtime the original value:

```kotlin
val endpoint = BuildConfig.SECRET_URL.decode()
```

This whole process should make it very time consuming to dig out all the steps required to restore your secrets. Using
code obfuscation on top of this, and recreating the encryption key and restoring the secrets makes this task as hard as finding a needle
in a haystack.

## iOS

The way of keeping secrets on iOS is somewhat similar to that of Android's. To prevent the API secrets from leaking to the VCS the plan is to have a configuration file that is populated locally with local test values and then in the CI/CD pipeline with production values. This file is committed to git as an empty configuration file. This way we don't have to worry about the secrets leaking to our repository. Let's see how we can achieve this. (Please note that all the names of functions and variables are quite obvious here for the sake of an example. In the real implementation it might be a good idea to name them something completely unrelated to encrypting/decrypting secrets.)

### Keep your secrets in .../Secrets.xcconfig

First we will create a file called Secrets.xcconfig. Then we can add this file to the project's configurations. We can do this by selecting the top level project in Xcode's project navigator, selecting the info tab and setting **Secrets** as the configuration set for each configuration under **Configurations**. Now we can push this empty configuration file to the VCS. This way any new developer pulling our project should be able to build it without the need to set configurations.

Next we need to make sure that changes to this file will not be committed to the VCS. We can tell git to ignore changes to the file by setting

```properties
git update-index --skip-worktree .../Secrets.xcconfig
```

This way git will always consider this file to be up to date and so it ignores changes made to it. One caveat of this approach is that if changes have been made to the file, git will not allow you to switch branches. Depending on the way git branches are used in your project this might be a bit of a show stopper.

In the xcconfig file we can store the secrets like so:

```properties
SECRET = hk5j43hk5jh34k5jh345kj34h5kjg345kjg34k5jg3kj45
```

We can read the values stored in the file like this:

```swift
if let secret = Bundle.main.object(forInfoDictionaryKey: "SECRET") {
    print("We got it.")
}
```

Now we just need to make sure the CI/CD pipeline populates the Secrets.xcconfig based on the environment variables set there. This way the secrets will be safe from whoever gains access to our repository. Next we will see how to encrypt the secrets using Themis on iOS to prevent the actual secrets from being visible in a decompiled binary.


### Using Themis 🔐

Using Themis on iOS is very similar to using it on Android. Some differences do exist in the libraries though so let's check them out.

Let's start by adding Themis as a project dependency, by adding **https://github.com/cossacklabs/themis** to swift packages

We will also need an encryption key that we use to encode and decode our secrets. We'll store the key in Secrets.xcconfig:

```properties
KEY = 3hgjkh6g23jlhg65hj345g6kjh3g456uhyjg
```

#### Obfuscating the encryption key

We will also manipulate the key in runtime by adding some junk around it:

```swift
static func getKey() -> String {
    let key = Bundle.main.object(forInfoDictionaryKey: "KEY")
    return "97HkkQEmdf44AMio569n".toBase64()! +
        "\(key)" +
        "\(777 * 4 / 99.2)"
}
```

#### Creating encoded versions of the secrets

Then we create an encoding function that encrypts the original secrets with Themis and encodes the encrypted values with Base64:

```swift
static func encode(secret: String) -> String? {
    let key = getKey().data(using: .utf8)!
    let cell = TSCellSeal(key: key)
    let data = secret.data(using: .utf8)!
    let encryptedData = try? cell?.encrypt(data)
    return encryptedData?.base64EncodedString()
}
```

Notice here how the class used to encrypt the secrets differs from the one of the Android library. Using this function we can generate the encrypted values of our secrets that we can then add to our CI/CD pipeline and the local config.

#### Decoding the encoded versions of the secrets

To decode the encrypted Base64 strings, we then need a function to restore the original secret in runtime

```swift
static func decode(configKey: String) -> String? {
    let key = getKey().data(using: .utf8)!
    let cell = TSCellSeal(key: key)
    let encryptedSecret = try? Configuration.value(for: configKey)

    if let es = encryptedSecret, let esDecoded = es.fromBase64() {
        let decodedData = try? cell?.decrypt(esDecoded)
        return String(data: decodedData, encoding: .utf8)
    } else {
        Log.e("Failed to fetch config value for \(configKey)")
    }
}
```

Now we can pass the Themis encrypted and Base64 encoded string to the decode(configKey: String) function to figure out the original secret value:

```swift
let originalSecretValue = decode(configKey: "SECRET")
```

# Closing thoughts

Is Themis a 100%-guarantee in keeping secrets away from preying eyes? Unfortunately, no. According to the documentation,
on its own, Themis addresses 90% of the exploits surrounding safeguarding secret encryption and decryption. Those remaining 10% 
often fall onto external factors that can and do compromise your application security, e.g., the backend or the CI/CD itself may be compromised, 
or simply human-error: one may commit the secrets to VCS. Themis is no silver-bullet to security, but it is better than providing
secrets in the clear on an application binary.