---
layout: post
title: PowerShell is the backbone of .NET DevOps
author: Rinorragi
excerpt: Few ideas how to use .NET to ease the everyday burden of your .NET developers
categories: 
- EPiServer
- Joona Immonen
- .NET 
- PowerShell
- EPiServerJoonaImmonen
tags: 
- EPiServer 
- .NET 
- PowerShell
- Joona Immonen
---

I will not lie: I love PowerShell! Lately I have been trying to figure out how we can ease the life of .NET developers. PowerShell and NuGet has been keywords on that topic. Now I want to show you how PowerShell can ease your life! Open your hearth and let the PowerShell flow within!

## What are the identified problems
We have few things that are happening all the time. 

* We are getting new people on our team
* We are upgrading our development machines to new ones
* We are changing from one project to another 
* Creation of virtual machines for various reasons is common, they need some tools too

All these above will have some kind of impact of installating software, updating components and configuration of various things. I really wanted to cut down the costs that our company and/or our customers are having because of this.

## Enhancement 1: Workstation installation script
Our awesome IT department (you guys are really awesome!) has of course workstation images that they use when they deliver workstations to all employees. Nevertheless there are so many kind of development happening that they don't have time to support all the variations that different developer archetypes would like to have. In some cases developers won't even use same tools in same project. 

To solve this issue we created a PowerShell Chocolatey script that installs all the wanted tools for .NET developers (others can do their own scripts). Developer can himself comment out unwatend tools or add some others. 

Here is an example of it: 


![Tools](/img/powershell-is-backbone-of-dotnet-devops/chocoscript.png)

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

 
![Tools](/img/powershell-is-backbone-of-dotnet-devops/sitecreation.png)

## What next
As having one PowerShell Module that all projects are dependant might be burdensome; we are inspecting possiblity to deliver this module via NuGet for each project independently. Project could then decide to which version of Module it is dependant. But that would be then a subject for another blog post. 

## Cool! I want to do that too!
Because we are such a nice guys we put all the scripts into GitHub for everyone to access. You can get them from our [GitHub repository](https://github.com/solita/powershell-webdevelopertools)