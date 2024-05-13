---
layout: post
title: Devcontainers - Goodbye to dependency hassle
author: mikaelstr
excerpt: Describes devcontainers and how to use them to setup development environments easily.
tags:
 - Devcontainers
 - Development
---


![Illustration of devcontainers](/img/2024-05-13-devcontainers/devcontainer.png)

## Devcontainers: Goodbye to dependency hassle

Every time a developer start on a project they need to go through the process of setting up a development environment. This can be a smooth half day work, or an installation / googling frenzy for a week, specially for legacy code.  

This is where devcontainers could be a helper.

Devcontainers, or development containers, are a type of containers used specifically for development purposes. They allow you to use containers as a full-featured development environments, providing a way to separate tools, libraries, or runtimes needed for working with a codebase.

## How do they work

Devcontainers are using a devcontainer.json file and a Dockerfile to define the container's configuration. This allows you to customize your dev container with additional tools, extensions, ports, and features.

Benefits of using devcontainers

Consistent environment: Devcontainers provide a consistent development environment for everyone working on a project, reducing the "it works on my machine" problem.
Isolation: Devcontainers allow you to isolate your development environment from your local machine, reducing the risk of conflicts between different projects.
Easy setup: Devcontainers make it easy to set up a development environment, especially for complex projects with many dependencies.

## When to use devcontainers

Devcontainers are particularly useful when working on projects with complex dependencies or when multiple developers are working on the same project. They can also be helpful when working with different versions of tools or libraries, or when you need to switch between different projects frequently.

## When not to use devcontainers

Devcontainers may not be necessary for simple projects with few dependencies. They can also add some overhead, so they may not be the best choice for projects where performance is critical. It needs to have a container environment installed (Ex. Docker).

## IDE examples

Devcontainers supports a lot of different IDEs and extensions. Here are some examples:

- Visual Studio Code
- Github Codespaces
- IntelliJ IDEA


## Test example

- **IDE:** Visual Studio code dev container extension.
- **Code:** ASP.NET Core Web API Backend.
- **Tested on:** Both on Mac and Windows.


How to test: Get [code](https://github.com/MikaelStr/DevContainerRESTBackend) from git, launch VSCode (Ext. Devcontainer) . Ready!

Devcontainer file uses a "ms-dotnettools.csharp" extension wich is a C# extension provided by Microsoft. This extension provides features like IntelliSense, code navigation, and debugging support for C# code.
```
{
    "name": "ASP.NET Core",
    "dockerFile": "Dockerfile",
    "forwardPorts": [5000, 5001],
    "settings": { 
        "terminal.integrated.shell.linux": "/bin/bash"
    },
    "extensions": ["ms-dotnettools.csharp"]
}
```

## Thoughts

The devcontainer could be verified in a step in the CI / CD. This way keeping it validated automatically and even used to drive the build process.

## Last words

I hope this article will help you tackle some of the challenges that comes with setting up new development environments.

[Here](https://devblogs.microsoft.com/ise/dev-containers/) is a good post to start from if you want to learn more.
