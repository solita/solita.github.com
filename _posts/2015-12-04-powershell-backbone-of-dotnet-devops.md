---
layout: post
title: PowerShell: Backbone of .NET DevOps
author: Rinorragi
excerpt: Few ideas how to use .NET to ease the everyday burden of your .NET developers
categories: EPiServer
tags: 
- EPiServer
- .NET
- PowerShell
---

I will not lie: I love PowerShell! Lately I have been trying to figure out how we can ease the life of .NET developers. 

## What are the identified problems
We have few things that are happening all the time. 

1. We are getting new people on our team

2. We are upgrading our development machines to new ones

3. We are changing from one project to another 

4. Creation of virtual machines for various reasons is common, they need some tools too

All these above will have some kind of impact of installating software, updating components and configuration of various things. I really wanted to cut down the costs that our company and/or our customers are having because of this.

## Enhancement 1: Workstation installation script
Our awesome IT department (you guys are really awesome!) has of course workstation images that they use when they deliver workstations to all employees. Nevertheless there are so many kind of development happening that they don't have time to support all the variations that different developer archetypes would like to have. In some cases developers won't even use same tools in same project. 

To solve this issue we created a PowerShell Chocolatey script that installs all the wanted tools for .NET developers (others can do their own scripts). Developer can himself comment out unwatend tools or add some others. 

Here is an example how it looks 
```
# Install chocolatey 
ex ((new-object net.webclient).DownloadString('https://chocolatey.org/install.ps1'))

# Setup Windows Features
$features = @(
	"IIS-WebServerRole"
	"IIS-ISAPIFilter"
	"IIS-ISAPIExtensions" 
	"IIS-NetFxExtensibility" 
	"IIS-ASPNET"
)
foreach ($task in $tasks) {
	Enable-WindowsOptionalFeature -Online -FeatureName $task
}

# Install tools
cinst putty -y
cinst 7zip -y
cinst googlechrome -y
```

## Enchancement 2: Project specific environment setup
We have currently many EPiServer projects going on. Common for these projects is the need to support multiple different bindings for the same IIS site. If we bind to *:80 then we are able to develop only one project per machine and we have need to support multiple projects at the same time. Some of the sites have also need to install some certificates for integrations and to create test sites and all other stuff. To achieve this we created a PowerShell Module that can be used. 

#### List of needed functionality
* IIS site creation
* Application pool creation
* IIS site bindings creation 
* Certificate creation
* Certificate installation
* Test that all mandatory .NET and IIS stuff is installed correctly

And here is how it looks like: 
```
$ErrorActionPreference = "Stop"
# Import the module where all the goodies are 
import-module .\..\solita-webdevelopertools.psm1

# Sanity checks
Test-IsElevated
Test-EverythingIsInstalled

# Set environment settings 
$siteName = "ExampleSite"
$pool = "TheTestPool"
$path = "C:\Temp\TestWebSite"
$bindSiteName = $false
$Bindings = "test1.solita.fi","test2.solita.fi","test3.solita.fi" 

# Create the website 
Set-WebDevWebSite -SiteName $siteName -PhysicalPath $path -AppPoolName $pool -BindAlsoSiteName $bindSiteName -Bindings $Bindings -RemoveApplicationPool $true
```
## What next
As having one PowerShell Module that all projects are dependant might be burdensome; we are inspecting possiblity to deliver this module via NuGet for each project independently. Project could then decide to which version of Module it is dependant. But that would be then a subject for another blog post. 

## Cool! I want to do that too!
Because we are such a nice guys we put all the scripts into GitHub for everyone to access. You can get them from here: https://github.com/solita/powershell-webdevelopertools
