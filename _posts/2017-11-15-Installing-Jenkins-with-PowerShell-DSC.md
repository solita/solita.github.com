---
layout: post
title: Installing Jenkins with PowerShell DSC
author: Rinorragi
date: 2017-03-01 17:20:00 +0200
excerpt: How to use PowerShell DSC in installing your continuous integration server.
categories: 
- Episerver
tags: 
- Episerver 
- DOTNET 
- DevOps
- PowerShell
- Jenkins
---
I have been struggling to find a good reference about how to setup a Jenkins environment in Microsoft environment with automatic installation script. So I decided to write a blog post about it. I also want to write about how to do continuous integration with Episerver DXC but felt that I need to first tell how to setup the Jenkins.

## About the PowerShell DSC

You might not be familiar about the PowerShell DSC and it comes from Desired Stage Configuration. DSC exists for various reasons:

* Make scripting less complex
* Make scripting to look the same for smaller learning curve 
* Make scripting pieces to be more reusable

The DSC is all about the setting the state of a machine to be certain. Most used example is to make sure that a service is running or that certain file is found on certain location. If you dig further on to this world you will find concepts of pull and push servers that would help you to set a farm of machines into certain state. We will not use those but we run the script locally with the help of LCM which is "local configuration manager". 

## DSC resources 

Before we start the configuration we need to talk about DSC resources which are libraries for DSC. Resources provide you functionality for DSC. For our purpose we are needing needing at least one that helps us to grab software from [Chocolatey](https://chocolatey.org/) (a package repository for windows). These resources would normally be where you start the script from (which might take you back to push and pull servers). In this scenario I just install them locally. Here is what my Install-Modules.ps1 script has inside.

```powershell
Install-Module cChoco -f
Install-Module xNetworking -f
Install-Module xWebAdministration -f
```

Three modules that provide you three type of functionality. Something to get stuff for Choco, configuring network stuff and managing IIS. If you run this for the first time you might get question about if you want to install nuget package provider for PowerShell. You should if you want to follow this path. It grabs you the wanted modules from [PowerShellGallery](https://www.powershellgallery.com/packages/cChoco/2.3.1.0). 

## Starting the scripting



![Tools](/img/azure-certification/mcsd_pyramid.png)s/learning/mcse-cloud-platform-infrastructure.aspx)
