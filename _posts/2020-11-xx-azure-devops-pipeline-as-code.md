---
layout: post
title: Azure DevOps CI/CD pipelines as code
author: lassiautio
excerpt: >
  TODO: put an excerpt here
tags:
 - Azure DevOps
 - DevOps
 - continuous delivery
 - continuous integration
---

TODO
Jotain klassisista pipelineista ja yaml-pipelineista.

## Azure DevOps

Azure DevOps is Microsoft's development, CI/CD, agile, artifact repository, and testing system ("swiss knife" for doing things). It has the following features:
- Wiki to document things,
- Boards for agile and scrum teams,
- Repos to save source code and do pull requests,
- Pipelines for continuous integration, delivery, and deployment,
- Test Plans, to run tests and
- Artifacts to save various kinds of packages (NuGet, NPM, etc.).

Practically it includes most of the things a software team needs except infrastructure to where to run the software.
Its strength is the smooth integration with all of these features. For example, we can access source code repo from build pipelines, and run build automatically when there is a new commit. Or we can mark tasks on the board as done when its code is deployed via release pipeline.

Even if Azure DevOps is Microsoft's product, it can be used with not-Microsoft programming languages and deploy to any AWS or GCP along with Azure. You can use it even if you're not using Microsoft's products.

In this blog post, we will concentrate on pipelines; as code!

## The example code (v1.0)

We will start with a very simple "Hello API". It will have one API method that will return "Hello Lassi!" like a greeting. Here is the C# code:

    [Route("api/[controller]")]
    [ApiController]
    public class HelloController : ControllerBase
    {
        public string SayHelloTo(string name)
        {
            return $"Hello {name}!";
        }
    }

When I call `GET https://localhost:44375/api/hello?name=Lassi` it will return "Hello Lassi!".

## Pipeline (v1.0)

It is easiest to begin if our code is in Azure (DevOps) repo, so I've put them there. When we navigate to the repo in a browser, we just need to push the "Set up build" button, and choose our base configuration. We will choose "ASP.Net Core".

!["Set up build" button](/img/azure-devops-pipeline-as-code/set-up-build-button.png)

![Choose "ASP.Net Core"](/img/azure-devops-pipeline-as-code/choose-asp-net-core.png)

Now we have our initial build pipeline as code in front of us. Pipeline as code is done with YAML in Azure DevOps.

![Initial build pipeline](/img/azure-devops-pipeline-as-code/initial-pipeline.png)

I will explain the key things in this initial pipeline.

- Trigger (line 6) will tell that this pipeline will run when there is a new commit in the master branch.
- Pool (line) defines on which server this build will be run. There are a few different servers that Microsoft gives out of the box. Here we'll use Ubuntu to run builds (notice that Microsoft itself has put not-Microsoft-OS here - it is not mandatory to use Windows to run builds).
- In variables (line 12) we can define our variables.
- The core is in steps (line 15) where the actual build process is defined. At first we will just run `dotnet build` which will compile our code.

Let's push "Save and run" from the upper right corner and run our build for the very first time:

![Commit after "Save and run"](/img/azure-devops-pipeline-as-code/save-and-run.png)

It will prompt us for a commit message because it is pipeline as code. We will commit it to the master branch for simplicity. Here we are doing this in browser but naturally, we could use any text/code editor to edit our pipeline. Lets run our very first build:

![Successfull build](/img/azure-devops-pipeline-as-code/successful-run.png)

We can see that build was successful and took 15 seconds to run (1). If we want to, we can even see all commits that were run in this build before the previous build (2). There is one warning (3) that warns that even if now this was run with Ubuntu-18.04, in near future this will be run with newer Ubuntu-20.04. If this is important to us, we could change the pipeline code from "ubuntu-latest" to "ubuntu-18.04".

## Use Azure DevOps Web Portal to Change the Pipeline Code

---
**Info**

You don't have to remember the syntax of Azure pipelines because IntelliSense will help and there is also UI in the Azure DevOps web portal that will help us with the syntax. These will help you to switch from classic pipelines to pipeline as code.

---

Next we will improve our pipeline: run unit tests.

We have two MSTest unit tests in our code:

    [TestClass]
    public class HelloControllerUnitTests
    {
        [TestMethod]
        public void SayHelloTo_returns_valid_greeting()
        {
            var sut = new HelloController();
            Assert.AreEqual("Hello Lassi!", sut.SayHelloTo("Lassi"));
        }

        [TestMethod]
        public void SayHelloTo_returns_valid_greeting_for_another_name()
        {
            var sut = new HelloController();
            Assert.AreEqual("Hello Autio!", sut.SayHelloTo("Autio"));
        }
    }

We will use the Azure DevOps web portal to add running unit tests. When we go to edit the pipeline, we can see there are a lot of tasks on the right-hand side. We will choose .NET Core.

![Select .NET Core task](/img/azure-devops-pipeline-as-code/choose-dotnet-core-task.png)

This will show us a dialog from where we can choose the settings we want. This is a very nice feature because at least I can't remember all settings for every task I'm using, nevertheless for the tasks I haven't even used yet.

![Select .NET Core task](/img/azure-devops-pipeline-as-code/task-dialog.png)

Here we have defined that we want to run tests from all *UnitTests.csproj files. When we click the Add button, the new task will be inserted into our code (lines 18-21).

![New task has been inserted into our pipeline code](/img/azure-devops-pipeline-as-code/new-task.png)

Now, if I want to make some change, I can do it easier straight to the pipeline code. But what if I want to change a setting that doesn't appear in the pipeline code and I don't know the syntax? Luckily there is a settings link that will open the previous dialog again and we can make changes also from there.

![Change task settings from the dialog](/img/azure-devops-pipeline-as-code/change-settings-from-dialog.png)

1. Click settings on the task you want to make a change.
1. Task dialog will open.
1. Make a change (here add test run title)
1. Press the Add button
1. The change will appear to the pipeline code

Now when we save changes and run the pipeline, we can see that there is a Tests tab and we can see from there that two tests have been run successfully.

![Tests tab](/img/azure-devops-pipeline-as-code/tests-tab.png)

The web portal has also IntelliSense that helps if we make changes to the pipeline code directly.

![IntelliSense in the web portal](/img/azure-devops-pipeline-as-code/intellisense-in-web-portal.png)

## Use Visual Studio Code to Change the Pipeline Code

Using the web portal is an easy but not so developer-like thing. Because pipeline code is in a plain text file, it can be edited with any text/code editor. Fortunately, there is a plugin for this for Visual Studio Code and probably also for other popular code editors.

## Muistiinpanot

TODO

- build
- deploy to staging
- smoke test
- check logs
- swap to production