---
layout: post
title: Simple Deployment Pipeline
author: lokori
excerpt: It is possible to create a professional deployment pipeline and do continuous delivery with few simple tools. When you remove the hype, CD and DevOps are not magic. I will present a real example from our project to show what can be achieved with a minimal effort by normal developers. Quite a lot actually.
---

This artice shows how we created a simple deployment pipeline using open source components, but is not a detailed tutorial. Obviously you must first do Continuous Integration to enable DevOps and [Continuous Delivery](http://en.wikipedia.org/wiki/Continuous_delivery), but then what? What is between [the elite](http://codeascraft.com/) and simple CI? That will be shown.

## The first rule of DevOps is you don't talk about 'DevOps'

It is good to remember that [DevOps is about culture, not tools](http://www.activestate.com/blog/2014/08/devops-tools-vs-culture). I dislike the notion that "DevOps brings together two kinds of people, Developers and Operators". It's a start, but as a project manager I have little use for a "developer" unwilling to learn linux administration, and even less use for an "operator" uncapable of writing clean code.

## We are not Twitter. Neither are you. 

Some of the "best practice" references come from famous product shops, such as Twitter, Etsy, Google and Facebook. Their context is very different from
average project team's context. Most of the software teams are not running hundreds of servers with dozens of applications. My context is basically
handling few applications, one team and perhaps a dozen servers or so. Still, I prefer that installations are automated and servers do not break arbitrarily
because of human errors.

## [Shipping is a feature!](http://www.joelonsoftware.com/items/2009/09/23.html)

Let's separate the concerns of this fundamental feature. We need to decide about many basic things:

* how to use version control to manage changes in source code
* building the package (compilation and dependency management)
* tagging the installation package with version number
* storing and distributing installation packages 
* running automated test suites
* configuring the environment
* deploying software
* monitoring

There are a number of companies and products who promise to take care of most or all of these problems. Easy and quick is a tempting proposal, but is it a *enabling platform* or a *framework solution*? What happens if you need to go beyond the planned roadmap? With frameworks, Pain happens. 

You shouldn't take for granted anything said about the "optimal" tool or solution. The context of the project defines what is appropriate and valuable.

## Jenkins is a hammer

Our solution provides automated configuration management, automated deployments and build promotion. Our only special "DevOps tool" is currently 
[Ansible](http://www.ansible.com/home). Jenkins is our hammer. 

1. [Jenkins](http://jenkins-ci.org/) is used as a nice `cron` UI and dependency orchestrator. It glues together the steps of the deployment pipeline, but doesn't really know that it's even building a software package or doing any deployment. We use freestyle project + shell commands instead of Jenkins "Maven project". 
[Build pipeline plugin](https://wiki.jenkins-ci.org/display/JENKINS/Build+Pipeline+Plugin) allows visualization of the pipeline and dependency graph shows the trigger paths. 

Here's how our delivery pipeline looks like in Jenkins.

![Delivery pipeline in action...](/img/simple-cd/aipal-pipeline.png)

2. As suggested by [The Book](http://www.amazon.com/dp/0321601912) we have separate [git](http://git-scm.com/) repositories for appplication source code, data and server configurations. [Our source code](https://github.com/Opetushallitus/aitu) is public, but data is not. [Multi SCM plugin](https://wiki.jenkins-ci.org/display/JENKINS/Multiple+SCMs+Plugin) was needed to make multi repository checkouts work properly. 


### Build promotion

Here's our pipeline start. Jenkins doesn't know it, but the script creates version numbers for our binaries to enable proper build promotion. Our version numbers are not Maven component versions, but simply Git hashes. It could be simpler, but the version number has additional use which is beoynd the scope of this article.

![Jenkins isolated](/img/simple-cd/jenkins-job.png)

For simplicity, Jenkins also hosts the packages. This solution is not ideal for all projects but we have no need for a separate Maven repository or something fancier. See our post about [Jenkins build pipelines](http://dev.solita.fi/2013/05/30/jenkins-build-pipelines.html) for more information regarding Jenkins build pipelines and the limitations of this approach.

### After packaging

1. Jenkins runs automated test suites. For fast failure the test suites are separated to multiple Jenkins jobs which run in a sequence. 

2. Environment configuration is handled with [Ansible](http://www.ansible.com/home). Jenkins polls git repository and asks Ansible to do things. Cloud provisioning happens with a few shell commands.

3. Deployment happens with Ansible. Again, Jenkins is used to call Ansible whenever necessary. Only packages which have passed the test suites
can be deployed. 

### Poor man's monitoring

Simple monitoring can be arranged with Jenkins, [wget](http://www.gnu.org/software/wget/) and Ansible. This is not suitable for "real work" but there's [New Relic](http://newrelic.com/) and others for more complex monitoring. Running `uptime` through Ansible to all hosts is far easier than setting up [Nagios](http://www.nagios.org/) to provide the same information. 

To see that our demo environment is responding we use this simple script triggered with Jenkins cron. If ping fails, Jenkins sends email and it shows red in our radiator. 

{% highlight bash %}
#!/bin/bash

if wget -q --user=xx --password=yy "http://1.2.3.4/demo/" > /dev/null; then
  echo "ok"
  exit 0
fi

echo "FAILED"
exit 1
{% endhighlight %}

## I want a cordless screwdriver

Jenkins is our hammer and shell scripts are nails, but I don't actually want a hammer. 

![Future awaits...](/img/simple-cd/future-grimlock.jpg)

(Photo from the mighty and most awesome [FAKEGRIMLOCK](http://fakegrimlock.com/))

I do not know how our pipeline evolves, but we are using a small subset of Jenkins features currently. Used in this manner, Jenkins has become our *enabling platform* for continuous delivery. It wasn't designed to be that and I believe a better replacement will soon emerge. The replacement should have these qualities:

* better implementation of security and access control. 
* pipeline view, multi SCM, parallel jobs available as default.
* jobs and configuration as code. Jenkins stores them in XML files. This makes automated configuration and provisioning of Jenkins difficult.
* support for build promotion. 
* plugins/API for provisioning with Ansible or other tools. 
* better support for radiators. Provide sane templates for radiators out-of-the box.

## Getting things done

The strength of this solution is that there is nothing really complicated about it. One doesn't need special tools and skills to maintain it. Understanding basic linux administration does not count as a special skill in my opinion. There are other projects in Solita with zero downtime deployments, SMS alarms and other Etsy-style blingbling practices, but they operate in a different context. The bells and whistles have a price tag - more tools, more complexity, more maintenance work. Seek the sweet spot which maximizes the value in your context and go there.

