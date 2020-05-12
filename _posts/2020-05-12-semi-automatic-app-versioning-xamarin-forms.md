---
layout: post
title: Semi-Automatic App Versioning in Xamarin.Forms
author: spheroid-
excerpt: Implementing a reasonable versioning scheme in a cross-platform Xamarin.Forms project
tags:
- Xamarin
- iOS
- Android
- Git
---

After you've set up a fresh Xamarin.Forms project (_or a Solution_, as they say), you quickly learn that there's not just one place to adjust the app version, but many, and in some places they even ask for multiple _different_ versions. So how to tame the version number jungle in a reasonable way? I'll show you how I've done it, but first, some basics:

Both Android & iOS apps have two different version numbers we need to care about:

1. The user-visible version string: [CFBundleShortVersionString](https://developer.apple.com/documentation/bundleresources/information_property_list/cfbundleshortversionstring) on iOS and [versionName](https://developer.android.com/studio/publish/versioning) on Android. On iOS it's _a string of three period-separated integers_ but Android is more liberal about it. To keep things simple, we can go with the iOS format on both platforms. This is what I'll mean with **version number** later on.

2. The actual internal version that the system uses to determine whether _version A_ is greater than _version B_. This is not visible to the user so the format here does not matter much – iOS uses a similarly formatted [CFBundleVersion](https://developer.apple.com/documentation/bundleresources/information_property_list/cfbundleversion) as above and on Android it's a single integer [versionCode](https://developer.android.com/studio/publish/versioning). We can, however, use the same format on both platforms as the iOS version can be abbreviated to a single integer. We'll call this one a **build number**.

These are the versions that actually matter in the grand scheme of things, but a Xamarin.Forms project has even more versions (assembly versions, project versions and the solution version to name a few). What should we do with them?

### My Prequisites

* I want to be able to set the current app version in just one place.
* I don't want to touch it until I've released the previous version and it's time to work on a new one.
* Every build must be automatically numbered according to the Git revision (in a sensible way).
* And there needs to be a way to work in a release branch that does not mess up the [trunk based development](https://trunkbaseddevelopment.com).

## The Version Number

There's a logical place where to set the canonical app version in Visual Studio – the **Solution Options**. On the **Main Settings** tab (it should be the default one when you open the settings window), you can enter the **Version** number. If you haven't modified the Android and iOS project configurations, they should inherit the version number from this value[^1].

You'd think that the version number would trickle down to the actual app resources, too? Well, it doesn't. But this is easily fixed with custom MSBuild targets in the .csproj files. For some reason these are not very well documented officially, but fortunately all the Xamarin MSBuild sources are in GitHub for us to peruse.

### Setting Up the Android Version

The Android build process has a [secret feature](https://github.com/MicrosoftDocs/xamarin-docs/issues/2774) called `AndroidManifestPlaceholders` which lets us set variables in the AndroidManifest.xml that will be substituted with the provided values. We can use this feature by injecting a custom target that is run before the build starts[^2].

Convieniently the app version is already defined in the `ReleaseVersion` property of the .csproj file, so our target ends up being very simple:

```xml
<Target Name="SetAppVersion" BeforeTargets="BeforeBuild">
  <PropertyGroup>
    <AndroidManifestPlaceholders>versionName=$(ReleaseVersion)</AndroidManifestPlaceholders>
  </PropertyGroup>
</Target>
```

Now all we need to do is that we add the placeholder into the _AndroidManifest.xml_ – set the Version name property to `${versionName}` either in the Manifest editor or in XML.

### …And the iOS Version

I could not find a similar, easy injection method in the iOS build targets, but we can modify the _Info.plist_ file after the build process has compiled it. This is done in the `_CompileAppManifest` target, so we can trigger our custom target to run just after. There's just one more gotcha: the compiled _Info.plist_ file is no longer XML but an optimized binary file that we cannot `XmlPoke` – we need to use the built-in macOS `plutil(1)` tool to do that:

```xml
<Target Name="SetInfoPlistAppVersion" AfterTargets="_CompileAppManifest">
  <Exec Command="plutil -replace CFBundleShortVersionString -string '$(ReleaseVersion)' '$(_AppBundlePath)Info.plist'" />
</Target>
```

## Build Numbering

For the build number then, I want to use a single digit that we can use in the app resources and that is unique to a commit in the Git repository. We could use a CI/CD environment to keep track of these build numbers, but what if we need to be able to package the distributed binaries on the local machines as well?

A common technique is to determine the Git commit count and use that. It does, however, have one problem: Should you do the actual development work in the master branch and build the releases and hotfixes in separate branches, you may end up having same build numbers for different commits. This would not be a problem if the development was done in feature branches and every release would be merged into master, but that's just not how I roll.

To overcome this problem, we can fortunately determine the commit count in the current branch in addition to the total commit count, which then lets know if we've branched away from master and how long ago that was. The magic lies in `git rev-list`. After the three initial commits into my project, we can run:

```console
$ git rev-list --count --first-parent HEAD
3
$ git rev-list --count --first-parent master..
0
```

Should we then branch out and make two more commits there, it will look like this:

```console
$ git rev-list --count --first-parent HEAD
5
$ git rev-list --count --first-parent master..
2
```

To format this build number so that it increases monotonically and in a logical way, we can use the build number of the branch point concatenated with the zero-padded branch commit count, by subtracting the latter from the former:

```console
$ printf "%d%03d\n" `expr 5 - 2` 2
3002
```

So there we have it, our build number within the hotfix branch would now be **3002**. The next commit on the master branch would then be **4000** and so forth.

### Setting It Up In MSBuild

We can extend the MSBuild targets we defined above by prepending these tasks to both of them:

```xml
<Exec Command="git show-ref --quiet refs/heads/master &amp;&amp; echo master || echo origin/master" ConsoleToMsBuild="true">
    <Output TaskParameter="ConsoleOutput" PropertyName="GitBranchName" />
</Exec>
<Exec Command="git rev-list --count --first-parent HEAD" ConsoleToMsBuild="true">
    <Output TaskParameter="ConsoleOutput" PropertyName="GitCommitCount" />
</Exec>
<Exec Command="git rev-list --count --first-parent $(GitBranchName).." ConsoleToMsBuild="true">
    <Output TaskParameter="ConsoleOutput" PropertyName="GitBranchCommitCount" />
</Exec>
<CreateProperty Value="$([System.String]::Format('{0}{1:000}', $([MSBuild]::Subtract($(GitCommitCount), $(GitBranchCommitCount))), $([System.Int32]::Parse($(GitBranchCommitCount)))))">
    <Output TaskParameter="Value" PropertyName="BuildNumber" />
</CreateProperty>
```

The first `Exec` task is for figuring out the master branch name. This is an optional step, but I found out that [Visual Studio App Center](https://appcenter.ms/) does not checkout the local `master` branch so we have to use the `origin/master` instead.

The following `Exec` tasks retrieve the commit counts, just like in the shell example above and the build number is then formatted correctly and assigned into the `BuildNumber` property, which we can then use in the target later on.

Finally, it's time to output the build number into the _AndroidManifest.xml_ and _Info.plist_ files, just like we did with the version number. Add the `${versionName}` variable to the _AndroidManifest.xml_ and change the `AndroidManifestPlaceholders` property in the `SetAppVersion` target of the Android .csproj to:

```xml
<AndroidManifestPlaceholders>versionCode=$(BuildNumber);versionName=$(ReleaseVersion)</AndroidManifestPlaceholders>
```

And add a new `Exec` task to the `SetInfoPlistAppVersion` in the iOS .csproj file:

```xml
<Exec Command="plutil -replace CFBundleVersion -string '$(BuildNumber)' '$(_AppBundlePath)Info.plist'" />
```

## Putting It All Together

You can find the example project in [my GitHub](https://github.com/spheroid-/xamarin-forms-version-sample). Clone it, open the solution and rebuild the project. Change the version number, play around with the branches and commits and rebuild again. You can verify that the changes have been applied by looking into the build directories:

```console
$ grep versionName VersionSample.Android/obj/Debug/android/AndroidManifest.xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android" android:versionName="1.0" package="fi.solita.versionsample" android:versionCode="4000">
$ plutil -p VersionSample.iOS/bin/iPhoneSimulator/Debug/VersionSample.iOS.app/Info.plist |grep -E 'CFBundle(Short)?Version'
  "CFBundleShortVersionString" => "1.0"
  "CFBundleVersion" => "4000"
```

That's it! If you have any comments or thoughts about this, feel free to comment below or you can also [tweet at me](https://twitter.com/spheroid).

---

[^1]: Well, technically it does not inherit the value per se, but Visual Studio will update all the .csproj files automatically when the version is updated in the Solution Options. Therefore it is important to commit every change it makes in the project files, too! Also, I found out that the initial .csproj files do not have a ReleaseVersion defined – when you adjust the Solution version for the first time it will add the missing project values.

[^2]: I found out that you cannot inject your targets to run before the `Build` target. There's a special `BeforeBuild` target you can define that is run, like the name implies, before the build and turns out you can, actually, inject your targets to run before it. Weird!
