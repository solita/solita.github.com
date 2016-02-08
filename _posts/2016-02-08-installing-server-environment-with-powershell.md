---
layout: post
title: Installing development environment with PowerShell
author: Rinorragi
excerpt: Automize your IIS webserver installation with PowerShell 
categories: 
- EPiServer
tags: 
- EPiServer 
- DOTNET 
- PowerShell
---

This blog is about how to make your brand new Windows Server ready for webdeployments with just pressing enter once. Azure websites can make your infrastrucute lifecycle handling very easy still we are often encountered situation where we need to host our ASP.NET applications in virtual machines or directly on physical hardware. On those situations installation procedures in Windows operating systems are often done with some "clickety click" magic that won't take too long. Still the "clickety click" installations has lots of long-term problems: 

* Installations can't be reproduced 
* Only the one who installed knows how he did it
* If you have multiple servers you are doing same manual steps multiple times
* Base of the installations does not differ much from project to project 
* After few years when your windows server is not the latest one anymore you will need to repeat this
* There is no way to test "clickety click" installations 

One could argue that documentation and clear processes would take care of all the problems above. Maybe they could but I have never seen installation documentation that has 100% coverage over how the installation has been done and installation script works as document as well! 

## What is needed to install on fresh Windows server
Here is my list what I would do for new Windows Server 

* Install IIS
* Install WebPI 
* Install newest ASP.NET 
* Install webdeploy
* Install various modules for IIS from windows feature list or from webPI 
* Install tools for administration (7zip, text editor etc) 
* Create IIS site and application pool and change some defaults for better

## Is there PackageManagement for Windows?
Oh yes there is! It is called [Windows PackageManagement](http://blogs.technet.com/b/packagemanagement/archive/2015/04/29/introducing-packagemanagement-in-windows-10.aspx) (aka OneGet). Unfortunately it is not available for Windows Servers yet. Production preview of Windows Management Framework 5 is already [available](https://www.microsoft.com/en-us/download/details.aspx?id=48729). Windows PackageManagement is actually a manager that can access multiple type of repository to have unified way to download and install software from multiple sources. The thing still missing is grown up economy where all the toys would be easily available. Chocolatey is pretty good already but it is missing a lot of software and I'm still sceptical about security of software packages. So instead of using Chocolatey I provide examples how to do silent installations with different type of software packages. 

## How stuff is installed without Chocolatey 
If you are familiar with Windows Server installation you might notice that there are multiple different types of installation involved in the process. Windows features, executables, msi files and software specific plugins are all in the same process. This is the part where I wish that Windows PackageManagement (aka OneGet) or chocolatey can one day solve unifying installation. 

#### Windows features (e.g. IIS)
The first question you should be looking is "what are the windows features"? To be able to install the features you must first learn how to find them. Here is a oneliner that will give the available features to you. 
```
Get-WindowsOptionalFeature -Online 
```
Great! Now we know how to find the windows features. Now we just need to change the oneliner a bit to be able to Install them. 
```
Enable-WindowsOptionalFeature -Online -All -FeatureName $task
```


#### Executables (newest .NET)
#### MSI files (WebPi)
#### WebPI modules (WebDeploy)

## How stuff is configured

#### WebDeploy
#### IIS website 

## Summing up 
Instead of huge scripts I like to put my PowerShell stuff to modules and also I like to be able to configure my installations. Thus I created few modules, an example script and an example configuration. I am using XML configuration because it was way to go earlier with the PowerShell (it was easy to load unlike json). Now newer PowerShell has "ConvertFrom-JSON" function that makes it possible to use also JSON configuration. 

## Cool! I want to do that too!
Because we are such a nice guys we put all the scripts into GitHub for everyone to access. You can get them from our [GitHub repository](https://github.com/solita/powershell-webdevelopertools) Here is more specific list of things mentioned before.

* (IIS tools module)[https://github.com/solita/powershell-webdevelopertools/blob/master/solita-iistools.psm1]
* (Server tools module)[https://github.com/solita/powershell-webdevelopertools/blob/master/solita-servertools.psm1]
* (Example script using modules)[https://github.com/solita/powershell-webdevelopertools/blob/master/scripts/solita_example_server_install.ps1]
* (Config used by example script)[https://github.com/solita/powershell-webdevelopertools/blob/master/scripts/solita_example_server_install_config.xml]