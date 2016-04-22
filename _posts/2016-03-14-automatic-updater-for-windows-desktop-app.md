---
layout: post
title: Automatic updates to your Windows desktop application
author: timovi
excerpt: How to use Squirrel to create an automatic updater for a Windows desktop application 
tags:
- Squirrel
- DOTNET 
- PowerShell
---
Modern desktop applications like Spotify and Google Chrome have automatic update features that take care of the application's update process behind the scenes. This way the end user only needs to restart the application after the sofware has been updated to its latest version. 

We were developing a software that had a basic set of requirements for an automated updating process:

* Updates must be checked on software launch.
* User must be able to use the obsolete version while the program updates itself on the background.
* Software update should only load a set of changed files instead of the whole software in order to save as much network bandwith as possible.
* User must be notified when the new version has been installed.
* Releases have to be signed in order to prevent the Windows SmartScreen filter popups.
* The release process should be as simple as possible so that we could glue it together with our continuous deployment tools and release a new version without any additional manual steps.

Since these requirements seemed fairly common, we figured that there had to be a library or a framework that would handle all the heavy lifting for us. We tried out few alternative tools before we discovered Squirrel.

## Squirrel

[Squirrel](https://github.com/Squirrel/Squirrel.Windows) is an open source tool that handles the installation and updating of a Windows desktop application. It uses user's local application directory to install the software and therefore it's best suited for per user installations. There's also a machine wide installation option, but we haven't used that feature yet.  

Squirrel creates [NuGet](http://docs.nuget.org/) packages for the full installation and delta updates. The size of our software's full installation package is about 40MB (80MB unpacked) and our typical update delta packages with Squirrel require only about 700KB space so the download time savings are huge especially when we are dealing with users operating behind low bandwith networks.

### Creating the installation and update packages

The application has to be built and then packaged to a NuGet package. Squirrel comes with a Powershell cmdlet (`Squirrel --releasify`) that handles the creation of the release packages from there on by

1. Creating the full installation and delta NuGet packages
2. Creating an executable installer
3. Signing all the necessary executables

The result of this are four files that have to be deployed to a server:

* *Setup.exe*: An installer that the user runs when installing the software for the first time.
* *&lt;appname&gt;-&lt;version&gt;-full.nupkg*: NuGet package that contains the whole software.
* *&lt;appname&gt;-&lt;version&gt;-delta.nupkg*: NuGet package that contains only the changed files in the latest version.
* *RELEASES*: A file that lists all the available versions and their nuget-package file sizes (full and delta).

The script below is a simplified version of the script we are running on our build server.

```powershell
msbuild <appname>.csproj /t:build /p:Configuration=<configuration> /p:ApplicationVersion=<version_number>
nuget pack "<appname>.nuspec" -Properties "configuration=<configuration>;name=<name>;assemblyName=<assembly_name>" -Version <version_number> -OutputDirectory <nuget_output_directory>
Squirrel --releasify <nuget_output_directory>\<assembly_name>.<version_number>.nupkg --releaseDir <squirrel_output_dir> --packagesDir <nuget_output_directory>\packages --loadingGif splash.gif --shortcut-locations Desktop,StartMenu --icon <application_icon> --setupIcon <application_icon> --signWithParams '<sign_tool_parameters>' | Write-Output
````

Our *&lt;appname&gt;.nuspec* file looks roughly like this:  

```xml
<?xml version="1.0"?>
<package >
  <metadata>
    <id>$assemblyName$</id>
    <version>$version$</version>
    <title>$name$ $configuration$</title>
    <authors>Solita Oy</authors>
    ...
  </metadata>
  <files>
    <file src="..\packages\squirrel.windows.*\tools\squirrel.exe" target="lib\net45\" />
    <file src="bin\$configuration$\*.dll" target="lib\net45" />
    <file src="bin\$configuration$\*.xml" target="lib\net45" />
    <file src="bin\$configuration$\Images\**\*" target="lib\net45\Images" />
    <file src="bin\$configuration$\$name$.exe" target="lib\net45" />
    <file src="bin\$configuration$\$name$.exe.config" target="lib\net45" />
    <file src="bin\$configuration$\$name$.application" target="lib\net45" />
    ...
  </files>
</package>
```

NuGet package ID, version, title and file locations are populated from the parameters given in the `nuget pack` command. Update package file names and Windows Application Uninstaller information are generated from the NuGet metadata. See [Squirrel documentation](https://github.com/Squirrel/Squirrel.Windows/blob/master/docs/using/naming.md) for a more detailed explanation on the naming conventions used by Squirrel.


### Initial installation on the client

The end user has to download and run the *Setup.exe*. This installs the software to the users local application data folder eg `C:\Users\<username>\AppData\local\<appname>\<version>` and creates all the necessary shortcuts defined by the *releasify*-cmdlet parameters. All the shortcuts point to an *Update.exe* located in the *&lt;appname&gt;*-folder. *Update.exe* handles the startup of the program by finding the latest version on the disk and firing it up. It also cleans up all the previously installed/updated versions of the software.

## Updating the client

Squirrel comes with a set of fairly simple APIs that can be used to control when the updates are to be checked, downloaded and installed. In our case we created wrapper class that is called on startup to check for updates and to apply them.

```java
public class UpdateManager : IDisposable
{
    private readonly IUpdateManager _updateManager;

    public UpdateManager(string updateUrl)
    {
        _updateManager = new Squirrel.UpdateManager(updateUrl);
    }

    public event EventHandler VersionUpdatesPending;
    public event EventHandler VersionUpdated;

    public void CheckForUpdate()
    {
        InvokeUpdate();
    }

    public void Dispose()
    {
        _updateManager.Dispose();
    }

    protected virtual void OnVersionUpdated()
    {
        if (VersionUpdated != null) VersionUpdated(this, EventArgs.Empty);
    }

    protected virtual void OnVersionUpdatesPending()
    {
        if (VersionUpdatesPending != null) VersionUpdatesPending(this, EventArgs.Empty);
    }

    private async void InvokeUpdate()
    {
        var updateInfo = await _updateManager.CheckForUpdate();
        if (updateInfo.ReleasesToApply.Any())
        {
            OnVersionUpdatesPending();
        }

        var releaseEntry = await _updateManager.UpdateApp();
        if (releaseEntry != null)
        {
            OnVersionUpdated();
        }
    }
}
``` 

You also need to add this magic line to your *AssemblyInfo.cs*

```java
[assembly: AssemblyMetadata("SquirrelAwareVersion", "1")]
```

When the *CheckForUpdate()* method is called, Squirrel downloads the *RELEASES* file from the server and compares it to the local *RELEASES* file. If there are new versions available on the server, it calculates whether to load a single full update package or a series of delta packages over the internet. File sizes for the packages are told in the *RELEASES* file. 
If Squirrel chooses to download delta packages, the latest version is built locally by applying the delta packages on top of the current version package. The new version is then installed alongside the running version. Squirrel deletes the outdated version on the next application startup.

There are also few hooks where you can register your own methods to run:

```java
SquirrelAwareApp.HandleEvents(
    onFirstRun: () => { ... },
    onInitialInstall: v => { ... },
    onAppUpdate: v => { ... },
    onAppUninstall: v =>  { ... },
    onAppObsoleted: v => { ... });
```

## Alternatives 

Microsoft has created a set of tools called [ClickOnce](https://msdn.microsoft.com/en-us/library/t71a733d.aspx) and even added some support for it to Visual Studio. ClickOnce looked promising to us but unfortunately we didn't manage to get our software working with it as ClickOnce didn't handle the executable signing properly. There are a lot of forum posts with other developers experiencing same kind of problems. Funny thing is that Squirrel has a tagline "It's like ClickOnce but Works".

[WiX Toolset](http://wixtoolset.org/) is a mature and well known installer toolkit with an impressive list of features, but it seemed to be too complicated for our purposes with extensive XML configurations and a requirement for a server side database to store the software versions.

## Conclusion

If you're looking for an installation and update framework for your Windows desktop application and your requirements meet with the features of Squirrel you should definitely at least try it out. First version came out on January 2015 and since then the team has been pushing out new releases roughly once a month.
