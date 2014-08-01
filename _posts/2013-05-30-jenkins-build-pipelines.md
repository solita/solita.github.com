---
layout: post
title: Interdependent Build Pipelines with Jenkins
author: orfjackal
excerpt: When doing continuous delivery for multiple interdependent projects, each project's build pipeline needs to be parameterized with the version numbers and binaries of upstream pipelines. It's easy to do in Go, but Jenkins doesn't support it that well. Here is how I was able to twist Jenkins to my use case.
---

In my current project we have multiple projects that depend on each other. There are some libraries that are used by multiple projects and some projects whose web services are called by other projects. We even have a diamond dependency. The versions that are deployed from each project should be compatible with other deployed projects.

The goal now is to implement [continuous delivery](http://en.wikipedia.org/wiki/Continuous_delivery) (or even just continuous integration done well). The first step is to make each build produce binaries with unique version numbers, [as I have written earlier](http://blog.orfjackal.net/2012/08/continuous-delivery-with-maven-and-go.html), and then make all the build pipelines use the latest versions produced by upstream build pipelines. Preferably it should also be possible to handpick the versions of the various projects, in case you don't want to deploy the latest of some project.

As a proof of concept I created the interdependent build pipelines for three of these projects using [ThoughtWorks Go](http://www.go.cd/). I got it all working in one day, ~~but the other team members didn't consider Go's free edition adequate and considered the price tag too high (we have 20+ team members and multiple build agents)~~ (**Update: Go is now fully open source, so the original argument is no more valid**), so I set to do a proof of concept using [Jenkins](http://jenkins-ci.org/). After a couple of days of research and experimentation I think I found a compromise that might work.


![My God, it's full of plugins!](/img/jenkins-build-pipelines/full-of-plugins.jpg)

Though there are [many](http://antagonisticpleiotropy.blogspot.com.au/2012/02/implementing-real-build-pipeline-with.html) [build](http://www.agitech.co.uk/implementing-a-deployment-pipeline-with-jenkins/) [pipeline](http://java.dzone.com/articles/how-build-true-pipelines) [articles](http://www.lordofthejars.com/2012/08/build-flow-jenkins-plugin.html) about Jenkins, none of those I found matched our use case of multiple interdependent projects. Most of them just had a simple linear pipeline, maybe with a [diamond dependency](http://stackoverflow.com/questions/9012310/how-do-i-make-a-jenkins-job-start-after-multiple-simultaneous-upstream-jobs-succ) here and there. Even Stack Overflow [gave no answer](http://stackoverflow.com/questions/16420402/parameterizing-a-jenkins-job-with-the-versions-of-multiple-upstream-jobs).

In Go, the downstream pipelines receive as environment variables the information about all upstream pipelines, which makes it easy get access to the version number and binaries of the dependee projects. So I was looking for something that lets you pass information in a similar way transitively through many Jenkins jobs. After wading through [lots of plugins](https://wiki.jenkins-ci.org/display/JENKINS/Plugins) I found [a hint](http://russellallen.info/post/2011/06/04/Creating-a-Simple-Build-Pipeline-with-JenkinsHudson-and-NAnt.aspx) of something that could emulate the desired behavior.


## Configuration

Here is what you would do in an upstream project:

1. Generate the version number for the current build, for example with [Version Number Plugin](https://wiki.jenkins-ci.org/display/JENKINS/Version+Number+Plugin) or a custom shell script.
2. Write the version number to a file, e.g. `echo "$FOO_VERSION" > foo.version`
3. Set the version number to the project, build it and save the binaries in a repository (either an external repository or using Jenkins' archiving). In Maven the version number can be set with [mvn versions:set](http://mojo.codehaus.org/versions-maven-plugin/set-mojo.html).
4. Configure Jenkins to archive the `*.version` artifacts after the build is finished.
5. Trigger the immediate downstream projects.

![Upstream project configuration](/img/jenkins-build-pipelines/upstream-config.png)

Then in a downstream project you would use the [Copy Artifact Plugin](https://wiki.jenkins-ci.org/display/JENKINS/Copy+Artifact+Plugin) to get access to that version number information. The thing that makes it possible to use this plugin, is using both the *Upstream build that triggered this project* and *Use "Last successful build" as fallback* options together. The downstream projects can be triggered independently of their upstream projects, typically due to a commit to the downstream project, and there can be multiple builds building in parallel, so both of those options are necessary.

Here is how you would configure the downstream project:

1. Use the [Copy Artifact Plugin](https://wiki.jenkins-ci.org/display/JENKINS/Copy+Artifact+Plugin) to copy the `*.version` artifacts from the upstream projects. Select the *Upstream build that triggered this project* and *Use "Last successful build" as fallback* options.
2. Read the version number from the file, e.g. `` FOO_VERSION=`cat foo.version` ``
3. Set the version number to the project's dependency information. If you need to edit XML, prefer using a scripting language with XML support, but when everything else fails, there are regular expressions: `sed -e "s/<foo-version>.*<\/foo-version>/<foo-version>$FOO_VERSION<\/foo-version>/" pom.xml > pom.xml.new && mv pom.xml.new pom.xml`
4. Build the project so that the build tool retrieves the dependencies from whatever repository you put them in.

![Downstream project configuration](/img/jenkins-build-pipelines/downstream-config.png)

If you have lots of such projects chained together, then the projects in the middle would have both the upstream and downstream configurations. The use of a common naming pattern `*.version` for the version metadata will archive in each project its own version number and its dependencies' version numbers transitively. That may be useful in seeing what versions are included in a build. It may also be used to detect a diamond dependency problem and fail the build if it happens.


## Conclusions

The above setup at least makes it possible to create non-trivial build pipelines in Jenkins. The configuration feels like a hack and it makes it hard to choose a particular upstream build to use (e.g. when deploying). Also I don't think that Jenkins can handle [fan-out and fan-in](http://www.thoughtworks-studios.com/go-continuous-delivery/features-benefits#fanin-fanout) intelligently; the [Join Plugin](https://wiki.jenkins-ci.org/display/JENKINS/Join+Plugin) works only for simple situations and also the [Build Flow Plugin](https://wiki.jenkins-ci.org/display/JENKINS/Build+Flow+Plugin) seems too limited.

I would choose Go any day over Jenkins when there are multiple projects that closely depend on each other. But if need be, something like this might let you avoid changing your CI tool. Jenkins has lots of plugins, but the plugin quality varies widely, though there is always the option of writing your own plugin. Go doesn't support plugins, but it has a REST API and I hear [plugins are on its roadmap](http://support.thoughtworks.com/entries/22863188-Where-are-the-plugins-).
