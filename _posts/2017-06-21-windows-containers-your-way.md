---
layout: post
title: Microsoft Build 2017 - Windows Containers your way
author: tommiraunio
date: 2017-06-21 14:00:00 +0200
excerpt: Windows Containers for .NET developers. State in 2017.
tags:
- windows containers
- docker
- DOTNET
- Msbuild
---

# Microsoft Build 2017: Windows Containers your way
**This year Solita sent a two-man strike team to Microsoft Build at Seattle in the beginning of May. There were a lot of takeaways from the conference, but what I found most intriguing was the arrival of Docker Containers to the Windows ecosystem. At Build there were not only conference sessions but also an additional pre-day that focused only on Windows Containers. In the Linux ecosystem, Docker containers have been gaining popularity rapidly and now Windows Containers aim to follow suit. In this post, I'll share my view as a .NET developer on Windows Containers.**

![MSBuild. Containers your way](/img/windows-containers-your-way/msbuild_containers_your_way.jpg)

_View over Seattle port. Containers for everybody_ 

## Container crash course

Docker Containers are sort of new thing for the .NET developers. My first run in with them was when Microsoft demoed a .NET app running inside a Windows container during Build 2015. Therefore, like many other .NET developers, I am just beginning my Docker journey.

Short recap: Containers are the next evolutionary step in virtualization technology. While the current virtualization technology enables IT departments to run multiple operating systems inside another operating system on top of single hardware, containers _share_ the host operating system kernel. This means that we do not have to duplicate the guest O/S in containers as we do today with traditional virtual machines. A container does not include a full O/S, but instead only the settings and libraries that are needed for the app the run. This is illustrated in the image below:

<div align="center">
    <img src="/img/windows-containers-your-way/vm_vs_container.png"/>
</div>

The virtualization technology from the 2000s was revolutionary as it made possible to run more apps on the same hardware. Containers take this trend further, as containers can be deployed even more densely as the containers have a much smaller footprint in terms of size when compared to a VM image. 

However, the virtualization technology from the 2000s did not affect developers directly. Containers do as they change both how software is developed and deployed.

## Driving factors for Windows Containers, developer perspective

So why should a .NET developer care about containers? Here are a few reasons:
* **Microservice architecture.** When developing to an actual microservice architecture (opposed to something that's just renamed Service Oriented Architecture) Docker containers help to manage the development environment when there are multiple microservices and each of which have their own database. This can be done without containers too, but they do ease up the task.
* **"Works on my machine"** is something that we have all heard of... and said. Containers ease up the pain as the testing during development can be done within exact same kind of environment as the production environment. This is because containers contain not only the app but also the environment that the app runs in.
* **Scripting**. Usually a Windows Container is running a Nano or Core version of Windows Server 2016. Neither of these versions have a GUI. This means that all the O/S configuration has to be scripted in. I.e. Docker containers force configuration through code. This means that containers are also documented through code and can be recreated easily from [Docker file](https://docs.microsoft.com/en-us/virtualization/windowscontainers/manage-docker/manage-windows-dockerfile). For me this is a huge bonus because I think that Windows Server environments should always be scripted, containers or no containers.
* **Operating system updates**. Need the newest security updates? No problem, just pull the newest O/S base image from the [Docker repository]( https://docs.docker.com/registry/), rebuild your container image and deploy it along your code changes. No more rebooting on guest O/S patching.

Additionally, the main driver on the DevOps side of things is that containers can be deployed more densely than traditional VM's. Which means that more apps can run on the same hardware than before. In addition, containers offer a clear boundary between the app and the environment. The app comes with the container and contains all the libraries it needs to run.

## Running the container: Windows Containers vs. Hyper-V containers

Currently in the Windows Container ecosystem there are actually two options on how to run containers. 
* The first is the Windows Container option, in which the containers share the container host kernel. 
* The second option is the Hyper-V container. 

In latter option Windows creates a Hyper-V VM in between the host kernel and container, thus providing more isolation from the actual host machine. This is useful especially in a multi-tenant environment, where you don't necessary fully trust all your tenant apps. Also, at least for now Windows 10 always runs Windows Containers [through Hyper-V](https://docs.microsoft.com/en-us/virtualization/windowscontainers/about/index).

<div align="center">
    <img src="/img/windows-containers-your-way/hyper-v_container.png"/><br />
    <i>Hyper-V Container stack</i>
</div>

## Getting started and demo

To get started you need either Windows Server 2016 or a Windows 10 Anniversary Edition or Creators Update (Professional or Enterprise). For Windows 10 there's an excellent getting started guide [here](https://docs.microsoft.com/en-us/virtualization/windowscontainers/quick-start/quick-start-windows-10).

Once the Docker Container engine is running on the machine, Powershell is your friend. In this demo I will quickly show, how to run a full IIS inside a Windows Container.

First, lets create a new container from microsoft/iis base image and run it right away:

![Run a Docker image](/img/windows-containers-your-way/demo1.png)

This creates a new container from newest version of Microsoft's micrsoft/iis image and runs it. 

-d says that we'll detach from the container after it's started and leave it running in the background. 

-p 80:80 says that we will map the host machine's port 80 to container's port 80. This allows us to access the container website from outside the container.

Lets see that the container is still running:

![List Containers](/img/windows-containers-your-way/demo2.png)

Container List tells us that the container is still running in the background. But in order to access the website from the current host machine, we need to go through some hoops. You see, the "localhost" loop back does not yet work with Windows Containers (more details [here](https://blog.sixeyed.com/published-ports-on-windows-containers-dont-do-loopback/)), so first we need to actually find the IP  that our host gave to the container:

![Find IP for the container](/img/windows-containers-your-way/demo3.png)

Now that we know where to find our container, we can access the container from our machine and see the familiar IIS start page:

![IIS start page from inside the Container](/img/windows-containers-your-way/demo4.png)

Naturally in real life situation we'd want to run our own app inside the container. In this case, we would build a new container image that would base on the microsoft/iis base image. Our app binaries could be added to the container through ADD command in the [Docker file](https://docs.microsoft.com/en-us/virtualization/windowscontainers/manage-docker/manage-windows-dockerfile). In other words, we would build a new custom container image that would base on the microsoft/iis base O/S image.

## Current state of Windows Containers

Although we've now gotten to a point where anybody can run Windows Containers on their laptop, it still feels that Windows Containers are not ready. Or at least not production ready. There are all kinds of smaller and bigger issues. For example, while the missing localhost loopback issue is not a huge issue by itself, it is one indication that Microsoft is wrestling a huge beast when trying to make Windows container-compatible. It’s not easy work. They’ve come a long way but they’ve still some way to go.

Another indication is that the especially the Docker images that are based on Server Core are quite large. For example, the microsoft/iis image that I used in the demo sizes 10.5 GB. While this is not a huge concern, because a certain version of a container O/S image is stored only once per container host, it's a nuisance. However, Taylor Brown, Principal Lead Program Manager on the group that develops Windows Server, said during Build sessions that they do aim to bring the size down. By a lot.


## Current use cases

A natural use case for Windows Containers is a ASP.NET Core app running on microsoft/nanoserver image that's part of some system that follows a microservice architecture. Nanoserver is the minimal version of Windows (it does not contain IIS althoug it can be [installed](https://docs.microsoft.com/en-us/aspnet/core/tutorials/nano-server) on it), but ASP.NET Core is able to run in there on top of its Kestrel HTTP server. 

Another use case for the Docker Containers is to use them to build a complete build pipeline from scratch quickly. This would include containers that contain both the CI and the CD system. This is because we have noticed that one monolith CI system that spans across multiple projects is a maintenance nightmare. Containers solve this issue, as they enable the possibility to construct a build pipeline from scratch quickly per project.

Also, although it's possible to lift & shift existing ASP.NET apps to containers (see [here](https://github.com/docker/communitytools-image2docker-win)), personally I don't see much that interest in that, at least not at this point yet. The investment that is needed to move an old ASP.NET app into a Windows Container could be spent more wisely elsewhere at the moment.

## Finally

The popularity of Docker in the Linux ecosystem is a strong proof of concept as good ideas tend to spread easily. On Windows side of things Microsoft is doing some heavy lifting to make Windows Server fully container capable and they are getting closer to the target all the time.

So, should you run Windows Container in production today? Probably not. Although you probably could, that would mean a lot of quality time spend with Google and solving bleeding edge problems.

However, as a .NET developer, should you start to get familiar with containers? Absolutely. My personal prediction is that in another two years the Windows Containers will have a big role to play in how green field development is done and deployed. 

Windows Containers your way.