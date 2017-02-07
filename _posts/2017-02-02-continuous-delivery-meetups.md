---
layout: post
title: Continuous delivery meetups at Solita
author: pkalliok
excerpt: >
  When automating the deployment and delivery of services, I firmly believe
  that we should push for technologies that make the process predictable,
  lightweight, tweakable and fun in general.  I'm very happy of the current
  trends in CD, and I hope that we will gradually see at least some
  semi-standard practices emerge.
tags:
- continuous delivery
- continuous integration
- deployment pipeline
- meetup
- culture
---

In January, Solita hosted two meetups whose themes fall under the general category of *continuous delivery*.  Both of these meetups were centered around particular tools, one of them being the [Ansible Helsinki](https://www.meetup.com/Ansible-Helsinki/events/235535175/) meetup and the other, the [Docker Helsinki](https://www.meetup.com/Docker-Helsinki/events/235753507/) meetup with a general topic of "running Docker in production".  It was a rewarding experience for me personally to have these motivated, enthusiastic people in our premises discussing interesting technical topics, and I thank the presenters and participants for making these meetups happen.

The meetups had a relatively different atmosphere, the Ansible meetup being a cosy and comfortable one, while the Docker meetup was quite a hit with 120 participants, a lot of proposed talks, and a tight schedule.  What was clear in both meetups, however, is that automation is really making a difference in how we configure, develop and test both the code that provides services and the environments and systems we run that code in.  This is an area of very active experimentation and research, and we are quite far from having a well-known set of best practices.  But there are nowadays great tools for building a deployment pipeline from start to finish, and in the meetups, we saw quite a few ways to combine these tools to make everyone's life easier.

## Ansible - the (remote) configuration tool

If you haven't heard of [Ansible](http://docs.ansible.com/), it's a program that makes changes to remote hosts (or ensures they have already been made).  It provides numerous ready-made modules for editing file contents, adding users, running miscellanous commands, etc.  Ansible is currently one of the tools of choice for setting up (virtual) servers or containers in an automated and predictable way.  It also provides modules to *create* these servers or containers if there is some well-known API for that, such as [OpenStack](http://developer.openstack.org/), Docker, or cloud services such as AWS.

Timo Mihaljov's [presentation](http://dev.solita.fi/jenkins-ansible-slides/) was about combining the merits of Ansible and Jenkins.  Jenkins is used on many sites to automate the build and deployment process, starting from changes in source code and ending with actually having the change in a working service.  Timo presented a process where Jenkins installation and configuration is automated with Ansible, and Jenkins uses Ansible to automate software installation and configuration.  One of the important points in the presentation was that Jenkins (or any continuous integration environment) is usually a critical part of the development environment and so changes to the build and deploy pipeline have to be tested as other changes to the software.  Having reproducible Jenkins installs is the only sane way to do this.

![a typical Jenkins installation](/img/continuous-delivery-meetups/20170110_161243.jpg)

The second presentation, of Jonni Larjomaa of Solinor, made the point that Ansible is actually "yet another command language" that can be used for many kinds of automation - one does not need to use the remote control features of Ansible.  The audience also suggested that Ansible could be (and has been) used for e.g. just collecting facts about the current network and verifying that everything has been set up correctly - something that one would normally use monitoring services for.

As it comes to Ansible's base use case, remote configuration automation, Ansible is *not* the tool to ensure a specific environment where to run services in.  This is because Ansible does not touch anything you don't explicitly request it to, and so manually made configuration changes will stay unless they happen to be to the same stuff you configure with Ansible.  To get a guaranteed, isolated environment with exactly the configuration you want, you need a way to easily create new servers - or containers - from scratch.  And that's where Docker comes in.

## Docker - the light-weight complement to virtual servers

[Docker](https://docs.docker.com/) is a tool that has gained popularity very quickly over the last few years.  It is an easy-to-use interface for running software - either your own or someone else's - in an isolated environment, all with its own filesystem, process space, network, etcetera.  The end result looks very much like a virtual server, but it is actually not running its own operating system, and neither are the standard system services usually there.  Creating new isolated environments, *containers*, is extremely fast, and if they originate from the same image, they can share the file system up to container-specific changes.  This makes the containers very space efficient if managed properly.

Given Docker's ease of use and numerous use cases, people are building a lot of infrastructure on Docker containers.  When you set up a swarm of containers to produce a service, there is an evident need to set up logging, wiring of these containerized services together, setting these containers up and rebuilding them on need, and if we are talking about production services, also monitoring, recovering, and scaling these services.  It is a lot of job for which numerous tools, both free and commercial, exist.  And the message from all presentations in the meetup was that usually you do it first wrong at least once before you learn to do it right.

![Docker on railways](/img/continuous-delivery-meetups/IMG_20170117_172620.jpg)

Heikki Simperi's presentation was about how certain services in the Finnish railway system are run in Docker containers.  The presentation had interesting insights, for example about using Nginx to route traffic between containers instead of using container links or a more specific integration bus.

![Docker at Zalando](/img/continuous-delivery-meetups/IMG_20170117_181434.jpg)

Rami Rantala from Zalando opened the way Docker is used at the Zalando stores.  Basically all services run in the cloud in Docker containers, and developer teams are given a lot of freedom to choose the technologies they run in their containers.  Apparently Zalando's way of running Docker in cloud is not a cheap one, but they are developing new and better ways to do it.

![Docker at Pipedrive](/img/continuous-delivery-meetups/IMG_20170117_184849.jpg)

Renno Reinurm of Pipedrive presented their way of running services on Docker.  This presentation was especially full of technical examples about what may and has gone wrong.  For instance, there are numerous ways to bog down the performance of container image builds, to a point where it becomes a serious threat to (developer) productivity.  There are also enormous performance differences between the different filesystem technologies that Docker can use to make the isolated filesystems for containers.  Renno suggested using the AUFS driver for storage, as did Jari Kolehmainen in the next presentation, too.

This presentation also made the interesting point that automation of Docker installations across a cluster is [problematic](https://youtu.be/PivpCKEiQOQ).  A misbehaving container might be able to bring the whole server down, and automating this to the whole cluster might mean bad things.

![We lost 70 per cent of the cluster](/img/continuous-delivery-meetups/IMG_20170117_190611.jpg)

Even with its pains of growing up, the technology presented in these meetups is vastly superior to any ad-hoc, non-reproducible delivery pipeline.  When automating the deployment and delivery of services, I firmly believe that we should push for technologies that make the process predictable, lightweight, tweakable and fun in general.  I'm very happy of the current trends in CD, and I hope that we will gradually see at least some semi-standard practices emerge, so that the delivery process of a software project need not be always another wonderland of stacked, forgotten design decisions.

Again, I present my heartfelt thanks for all the participants.  It was a great joy to have you here.

