---
layout: post
title: Publishing to Maven Central Repository
author: orfjackal
excerpt: The Central Repository is the de facto place for publishing JVM-based open source libraries. Publishing your own libraries there is not hard and it will benefit your users.
---

One of the core contributions of the Maven ecosystem is the [Central Repository](http://central.sonatype.org/) which is the de facto place for publishing JVM-based libraries. It lets you declare in a project file those library versions you depend on, and then all the tools will automatically find them for you. It's easy to [check for new versions](http://mojo.codehaus.org/versions-maven-plugin/) of your dependencies and maybe your IDE even provides [code completion](https://www.jetbrains.com/idea/features/build_tools.html) for dependency IDs and versions.

The benefits of the Central Repository over other Maven repositories are that it has some minimum requirements to ensure [good quality artifacts](http://blog.sonatype.com/2010/01/nexus-oss-ecosystem/), and the confidence that it won't disappear in the future, unlike many other repositories which have disappeared in the past. Thankfully some of the biggest long-buried repositories have been migrated into the Central Repository, for example [Java.net](http://blog.sonatype.com/2010/02/java-net-maven-repository-rescue-mission-on-march-5th/) and [Scala-tools.org](http://blog.sonatype.com/2012/02/scala-artifacts-now-on-central/), keeping the artifacts available and also [improving their meta data](http://blog.sonatype.com/2011/08/java-net-moves-to-central/).

Now if you have an open source library that you would like to publish to the Central Repository, how should you proceed? The [OSSRH Guide](http://central.sonatype.org/pages/ossrh-guide.html) will tell you everything about using Sonatype's OSS Repository Hosting, but some have found its documentation hard to read, so I'm writing this article in hopes of explaining it more simply. This article gives an overview of what is needed - for more details follow the links to the official OSSRH documentation.


## One-Time Setup ##

At first you will need to [register](http://central.sonatype.org/pages/ossrh-guide.html#initial-setup) at Sonatype's JIRA and create a ticket for claiming [your groupId](http://central.sonatype.org/pages/choosing-your-coordinates.html). If you own the domain `example.com`, just register the top-level groupId `com.example` and you can use any sub-groupIds for your projects without needing a ticket for each of them (e.g. `com.example.foo` and `com.example.bar`).

You will need to wait for a human to respond to your ticket, because Sonatype wants to make sure that nobody will claim your domain or project address without your permission.

After your first release is ready, you will need to go write a comment to the same JIRA ticket, so that Sonatype will do some final manual checks before enabling the automatic syncing of your groupId to the Central Repository.


## Per-Project/User Setup ##

### Central Requirements ###

There are some [minimum requirements](http://central.sonatype.org/pages/requirements.html) for artifacts which are published to the Central Repository:

* The `pom.xml` needs to contain some project and license information. It may *not* contain `<repositories>` or `<pluginRepositories>` elements.
* In addition to the binary artifact you must also publish the source code and Javadocs as separate artifacts.
* All the artifacts must be signed with GPG/PGP, which requires [generating and distributing a key](http://central.sonatype.org/pages/working-with-pgp-signatures.html).

An easy way to configure the necessary Maven plugins for producing those artifacts is to extend the [org.sonatype.oss:oss-parent](http://search.maven.org/#search%7Cgav%7C1%7Cg%3A%22org.sonatype.oss%22%20AND%20a%3A%22oss-parent%22) POM which contains the profile `sonatype-oss-release` for activation on release.


### Deployment Configuration ###

[Deploying to OSSRH](http://central.sonatype.org/pages/ossrh-guide.html#deployment) can be done with all the major build tools. [To deploy with Maven](http://central.sonatype.org/pages/apache-maven.html) you can use the [Nexus Staging Maven Plugin](http://books.sonatype.com/nexus-book/reference/staging-sect-deployment.html). The deployment works so that (1) the build artifacts are uploaded to OSSRH's Nexus into a temporary staging repository, (2) the staging repository is closed for modifications, and finally (3) the staging repository is either dropped or released into the Central Repository. At step 2 the artifacts are available under a temporary URL to allow integration testing them.

You will need to store your Sonatype username and password (the ones for logging into the Sonatype JIRA) in Maven's user-specific `~/.m2/settings.xml` file, under the `<servers>` element.

```xml
<servers>
  <server>
    <id>ossrh-releases-com.example</id>
    <username>example</username>
    <password>secret</password>
  </server>
</servers>
```

In the project's `pom.xml` you will need to configure the plugin to use OSSRH's Nexus instance with your credentials.

```xml
<build>
  <plugins>
    <plugin>
      <groupId>org.sonatype.plugins</groupId>
      <artifactId>nexus-staging-maven-plugin</artifactId>
      <version>1.6.4</version>
      <extensions>true</extensions>
      <configuration>
        <nexusUrl>https://oss.sonatype.org/</nexusUrl>
        <serverId>ossrh-releases-com.example</serverId>
        <stagingProfileId>46cd48d84135</stagingProfileId>
      </configuration>
    </plugin>
  </plugins>
</build>
```

The `<stagingProfileId>` in the above code sample is specific to your groupId and you can find it out by logging into <https://oss.sonatype.org> where you will need to (1) click Staging Profiles, (2) select your groupId from the list, and (3) copy the hexadecimal ID from the browser's address bar.

![How to find your stagingProfileId](/img/publishing-to-maven-central-repository/staging-profile-id.png)

The plugin will hook into Maven's `deploy` command and stage the artifacts automatically. Additionally it provides goals for releasing or dropping the staging repositories, so that you can fully automate the release. To find out the Nexus plugin's available goals and parameters, use the `mvn nexus-staging:help` and `mvn nexus-staging:help -Ddetail=true -Dgoal=<goal-name>` commands.


## Per-Release Actions ##

When everything is configured as shown above, releasing a new version happens like this:

1. [Set the release version number](http://mojo.codehaus.org/versions-maven-plugin/set-mojo.html)
2. `mvn clean deploy -P sonatype-oss-release`
3. Login to <https://oss.sonatype.org>
4. Select your just created staging repository under Staging Repositories
5. [Click the Release button to release it](http://central.sonatype.org/pages/releasing-the-deployment.html)

The artifacts will be immediately available under <https://oss.sonatype.org/content/groups/public/> and in a couple of hours it will be synced into the Central Repository (assuming you have done the one-time setup of commenting on the JIRA ticket on your first release).


### Automating the Release ###

I recommend you to write a shell script for doing all the above mentioned release steps. The shell script should just take the version number as parameter and do everything else automatically. Have a look at [this release script](https://github.com/orfjackal/retrolambda/tree/master/scripts) for a complete example.

Releasing the staging repository can be automated with the Nexus Staging Maven Plugin. With more complex projects it may be useful to stage the artifacts into a local directory, which is then uploaded as a whole to Nexus:

```bash
# save the artifacts under the "staging" directory
mvn clean deploy \
    --errors \
    -P sonatype-oss-release \
    -DaltDeploymentRepository="staging::default::file:staging"

# upload everything from the "staging" directory into a Nexus staging repository
mvn nexus-staging:deploy-staged-repository \
    --errors \
    -DrepositoryDirectory=staging \
    -DstagingDescription="any description of the release"

# release the Nexus staging repository (reads repository ID from 'staging/*.properties' under altStagingDirectory, as generated by deploy-staged-repository)
mvn nexus-staging:release \
    --errors \
    -DaltStagingDirectory=. \
    -DstagingDescription="any description of the release"
```


## Summary ##

Releasing open source libraries to the Central Repository is not hard. It just requires reading relatively much documentation, but thanks to that everybody can benefit from good quality artifacts. Once all the steps of a release are automated, you can easily push out [multiple releases per day](https://github.com/solita/datatree#version-history) without hassle.
