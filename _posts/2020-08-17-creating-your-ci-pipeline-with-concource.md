---
layout: post
title: Creating your CI/CD-pipeline with Concource
author: alperttiti
excerpt: >
  Choosing a CI/CD system is very much a same thing than choosing a good server name.
  You probably have a long ride with your decision ahead. Concource CI is one option.
tags:
 - Concource CI
 - Build pipeline
 - Continuous Integration
 - Continuous Delivery
 - DevOps
---

There are many CI/CD systems available. If you are using Github you are probably already
tried Github Actions which are a great way to build and deploy your *things*, even it is
still on its early days. If you work mainly in some cloud environment you probably have
tried tools available on that specific environment. There is also *good old Jenkins* and many more.

However, this blog post is about Concource CI. Concourse is an open-source continuous
*thing-doer*, like they have put it on their [website](https://concourse-ci.org/).
Most common way to run concource binary is to use [Docker](https://www.docker.com/), so
let's go on that path. I will show you how to start Concource with Docker Compose and
how to create a simple pipeline with it.

Before we'll get further, it's good time for a disclaimer. Before you just start *hacking*,
it's good to read a little what Concourse is and what are plans for future. Good place to start is
their [blog post about roadmap towards v10](https://blog.concourse-ci.org/core-roadmap-towards-v10/).
Core developers behind Concourse has also said, that it is not for everyone and for every need.
In example, [they have ruled parametrized build out of their scope.](https://github.com/concourse/concourse/issues/783)
Also, Concource is nothing new and fancy, it has been here from year 2014.

Anyway, because you still be reading this, you probably think like I do, 
you cannot know if it's for you, if you don't even try it. So, let's get on.

Basic concepts
----

Concource pipelines are defined with [YAML](https://yaml.org/). Core concepts
are [resources](https://concourse-ci.org/resources.html), tasks and jobs. For every pipeline there are
inputs and outputs which are conceptually resources. Concourse itself does not know
any details about these. Those are just some external sources to get and put *things*.
Each resource has a resource type. If resource is abstraction for some project artifact,
Ie. your codebase in Git, then resource type is an abstraction for an actual implementation how your
pipeline communicates with your git repository.

There is some core resources available and [also third-party resources
are listed on Concourse website](https://resource-types.concourse-ci.org/). In addition, there is
also many other in the wild Internet.

However, **keep security issues in mind** whenever you use third-party resource types and especially
with some others. Resource types are in practice just Docker images, so contents can be change to
something nasty. Fortunately, it is quite an easy job to make your own resource type. So, if you feel like
you don't trust enough for the publisher of some resource, you can get ideas from it and make your own resource type
based on these. However, remember to contribute to the base project if you make good improvements or bug fixes. 

Let's build and deploy some dummy docker images into the Docker Hub 
------------------

I don't go into details how to start and run Concourse, but I have provided some instructions
in [my example project in Github](https://github.com/solita-alperttiti/concource-ci-example).
Also, fully runnable pipeline example can be found from there.

Every pipeline has its main pipeline definition file. This is good starting point.

In our case it's called concource-example.pipeline.yml, but you can name it whatever you like.
Because every pipeline has least one input, let's start with it.

```yaml
- name: concource-example
  type: git
  source:
    uri: ((git-source))
    branch: ((git-branch))
```

So, now we have our input. Its type is *git*, which is one of core types of Concource, and you
don't have to define actual type in your definitions. So, this is quite easy to understand,
it's an abstraction of some Git-branch in some repository. This example snippet doesn't tell
much about which branch and which repository we are using, though.

You can use exact path to your repository in pipeline configuration if you wish, but I have used
variables. My main goal has been to create pipeline definition which is more like a template for
set of pipelines than just one pipeline for specific use. In this way you can easily create multiple
pipelines from same template and just provide a different configuration for each. This is especially
useful if you wish to use it with artifacts which have similar steps on the process. One real world
example could be software with microservice architecture pattern, so you have a shared pipeline definition
for all of your services.

In my example project variables are defined in files on local disk with a prefix *runtime_variables*.
So, there is a snippet which gives us more details about our git resource.

```yaml
git-source: https://github.com/solita-alperttiti/concource-ci-example.git
git-branch: master
``` 

Variables are loaded into the Concourse when the pipeline is created. Be noted, that 
variables can be loaded out from the concourse afterwards, so in real world cases it
might be useful to consider using some credentials' manager if you have some sensitive data
in your variables. [Concourse supports many out-of-the-box](https://concourse-ci.org/creds.html).
By using external manager you only need to provide api key to your pipeline.
You can also have multiple configuration files if you wish to split them up.

Right, now we have some input. Goal in this example is to get some input from git,
make some *things* and then push the result to the output which in this time is Docker Hub.
Output can be whatever is needed, ie. rsync your project artifacts to some server.

```yaml
- name: concource-example-registry
  type: registry-image-resource
  source:
    repository: ((docker-source))
    tag: ((docker-tag))
    username: ((docker-username))
    password: ((docker-password))
```

So, now we input and output. Next phase is to define a job which uses those. Let's use
our imagination and call our job *build-and-publish*. You could define as many jobs you wish,
but in this case one is enough.

```yaml
jobs:
- name: build-and-publish
```

Every job has some series of steps which is called a *plan*.

```yaml
plan:
    - get: concource-example
      trigger: ((trigger-build))
    - task: prepare-build
      file: concource-example/concource/pipelines/concource-example/concource-example-prepare-build.yml
      vars:
        docker-file: ((docker-file))
        docker-tag: ((docker-tag))
    - task: build
      file: concource-example/concource/pipelines/concource-example/concource-example-build.yml
      privileged: true
      params:
        DOCKERFILE: prebuild-output/((docker-file))
    - put: concource-example-registry
      params: {
        image: image/image.tar
      }
```

So, while definition itself is very self-explanatory let's walk it through. First we fetch our input
from Git. Then we do some preliminary *things* before building our complex Docker image. Finally, we
push image into the Docker Hub. One point to note is keyword in our first get. This boolean value
controls if job should be triggered when resources state changes (Ie. you push something into your repository).

I have divided my more complex tasks into separate files, so it's easier to see top-level flow from main pipeline file.
For every task we can also define different running environment.

```yaml
image_resource:
  type: registry-image
  source:
    repository: ubuntu
    tag: "bionic"
```

Also, tasks can have their own inputs and outputs. These are basically folders to pass by in your pipeline. In my example,
I make minor tuning to Dockerfile, based on pipeline variables, and then pass it on to actual build task.

Beyond inputs and outputs there is also caches available in Concourse.

```yaml
caches:
  - path: image-cache
```
Caches are to preserve state of your task running environment between builds. Many times this is a useful feature to use
with your build tasks, so Concourse does not need to download every dependency on every build.  
 
Summary
-------

I have tried to keep my example project for this blog post as simple as possible, but although in a level to provide
some useful tips on the first steps with Concourse.

Concourse has some rough edges, that fact cannot be bypasses. It's also good to understand, that it's not
suitable for every need. It's definitely not a swiss-knife. Also, some flexibility in your mindset might
be needed if you don't already share the same ideas with authors. There is also steep learning curve if you
are just fine with Ie. Jenkins.

Anyway, it's good we have alternatives and especially ones which are [FOSS](https://en.wikipedia.org/wiki/Free_and_open-source_software).
I myself have used Concourse in a couple of projects. There has been some hard moments, but at overall I have liked it.
However, I'm not here to tell which tool is the best, but just trying to provide first steps if you are interested to
get familiar with Concourse. It's up to you to choose what suits best for your needs.

Feel free to share you thoughts and provide for me new way if you think my approach have some flaws.
Every feedback is appreciated. Remember to check out the code behind this blog post at 
[GitHub](https://github.com/solita-alperttiti/concource-ci-example).
