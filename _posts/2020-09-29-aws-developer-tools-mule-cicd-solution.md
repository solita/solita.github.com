---
layout: post
title: Using AWS CodePipeline as CI/CD solution for MuleSoft Apps
author: atteheino
excerpt: Thoughts on using AWS Developer Tools to replace Jenkins as the CI/CD solution for MuleSoft Apps to be deployd to CloudHub
tags:
 - AWS CodeCommit
 - AWS CodePipeline
 - AWS CodeBuild
 - MuleSoft
 - Jenkins
 - CloudHub
 - CI/CD
---

A typical tooling setup for a integration project consists of a Git repository somewhere, Jenkins on some host, Application Server either on-premise or hosted somewhere. Git stores the source code, Jenkins builds and deploys the code to the application server running the application. 

I was given the option to try out AWS alternative to this setup. AWS has [CodeCommit](https://aws.amazon.com/codecommit/) for source control, [CodeBuild](https://aws.amazon.com/codebuild/) for building your software and [CodePipeline](https://aws.amazon.com/codepipeline/) for automating the whole CI/CD process.

Typically it would be a good idea to document your infrastructure as code, for example by creating the services you need via CloudFormation templates. Here I was doing a Proof Of Concept, so I did all of the setup via the AWS Console UI.

# CodeCommit to store the source code

It's not a requirement to use AWS CodeCommit to be able to utilize CodeBuild or CodePipeline, but in my case it made sense as the original source code was not in a public repository like GitHub.

It's simple to create a new repository to CodeCommit. All of the repositories are Git-based.
I needed to migrate an existing repository to CodeCommit and I did it by following [these simple instructions](https://docs.aws.amazon.com/codecommit/latest/userguide/how-to-migrate-repository-existing.html).

To be able to access your new repository:
- Create a IAM user for CodeCommit access. Grant it a suitable policy to work with CodeCommit.
- Create HTTPS Git Credentials for Git to access the CodeCommit repository. (You can do this from IAM user's Security Credentials tab)
- Configure Git on your computer to access CodeCommit, by using the credentials created on the previous step.

The rest is pretty much trivial by following the instructions on the guide.

# CodePipeline to run the entire process

After having the sources in CodeCommit, I took a look at the documentation on how to proceed. I figured out that I would first create the CodePipeline that is triggered whenever the sources change in the Git repository. Second step would be to create the CodeBuild step and it's simple to add while building the CodePipeline. The CodePipeline I created is really simple:

![CodePipeline example](/img/aws-developer-tools-mule-cicd-solution/pipeline.png)

Just two steps. One for reacting to the source code change, and one for building the software.

Here are a few things you must do and can do to configure the CodePipeline:
- You must create a Service Worker Role or use an existing one to run the pipeline.
- You can select the source for the CodePipeline. There are several sources for the CodePipeline that one can choose from: AWS S3, AWS CodeCommit, GitHub, Bitbucket etc.
- You can select the Artifact Store. Artifact Store is simply a AWS S3 bucket. Use the default artifact store, create a new one or use an existing bucket.
- You can select an encryption key to encrypt the data in the artifact store.

There is also possibility to define a Deploy Stage, but it's mostly about deploying to AWS infra, so it was not for me.

# CodeBuild to build the software

Final step is to use AWS CodeBuild to run Maven to build the MuleSoft app. MuleSoft apps use Maven by default, so it's a clear choice to use.

There are several ways you can create a CodeBuild Build Project. You can create one from scratch or you can create one by creating a CodePipeline and then defining the build-step to be implemented by CodeBuild. Either way, you define the source for the Build Project, the actual buildSpec, where to store artifacts and finally logging. I created the Build Project via CodePipeline so the source is automatically set to be CodePipeline (where you define the source originally).

CodeBuild uses AWS S3 as the default Artifact Store. So anything you build in CodeBuild and specify to be published as an artifact is published to a S3 bucket you define in the creation process or have previously created. 

BuildSpec is at the heart of CodeBuild. It's a yml file, that describes the build process. You can find the specification from [here](https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html).

## buildSpec file for running Maven

You can either have the buildSpec inline in the CodeBuild Build Project or it can reside on the root of the source code. The buildSpec can become complex and it's also nice to be able to version all the changes to it so I placed the buildSpec file to CodeCommit with the rest of the sources.

```yml
version: 0.2

env:
  variables:
    app_runtime: "3.8.2"
    anypoint_platform_environment: "Demo"
    anypoint_platform_workertype: "SMALL"
    anypoint_platform_workers: "1"
    anypoint_platform_region: "eu-west-1"
  parameter-store:
    anypoint_platform_client_id: "demo-anypoint-client-id"
    anypoint_platform_client_secret: "demo-anypoint-client-secret"

phases:
  install:
    runtime-versions:
        java: openjdk8
    commands:
      - cp ./settings.xml /root/.m2/settings.xml
      - cp ./settings-security.xml /root/.m2/settings-security.xml
  build:
    commands:
       - cd demo-custom-connector
       - mvn install -B
       - cd ../example-service
       - mvn package deploy -B -DmuleDeploy -Dapp.runtime=$app_runtime -Danypoint.platform.environment=$anypoint_platform_environment -Danypoint.platform.workers=$anypoint_platform_workers -Danypoint.platform.workertype=$anypoint_platform_workertype -Danypoint.platform.region=$anypoint_platform_region -Danypoint.platform.client_id=$anypoint_platform_client_id -Danypoint.platform.client_secret=$anypoint_platform_client_secret

artifacts:
  files:
    - demo-custom-connector/target/*.jar
    - demo-custom-connector/target/*.zip

cache:
  paths:
    - '/root/.m2/**/*'
```

### env-section

This is where local variables are defined for the Build Project and also the variables that are retrieved from Parameter Store. [See Secrets chapter](#secrets). 
The value for the varible is the key from Parameter Store and CodeBuild replaces the value with the actual value from Parameter Store during execution.

```yml
env:
  variables:
    key: "value"
  parameter-store:
    key: "value-name-for-parameter-store"
```

### phases-section

Phases-section is where the actual build execution is defined. It is split into two sections: install and build.

In the *install*-section the environment for the build is defined. Here I have selected the JDK to use in the build and set custom Maven profile for the build to use.
The custom settings files are copied from the sources directory (checked out automatically from Git) in the machine running the build to a special location */root/* so that they are taken into use during execution.

In the *build*-section the commands are listed that actually perform the build. For the `mvn package deploy` step the parameters come from the variables defined in the env-section. In the builds stage, I first build and package a custom connector that is used by the MuleSoft application internally.

### artifacts-section

Here is where you can spcify artifacts from the build process to be stored in the S3 bucket. These can then later on be used in deployments to other Amazon Services or other services that can download from S3.

### cache-section and how to configure a cache for Maven repository

Notoriously, Maven tends to download half of the internet to do a build. To speed up builds we should setup a cache.

In the *cache*-section of the buildSpec we define the path for the local Maven repository to cache. 

There is a good guide on how to specify the cache for the CodeBuild Project: [https://aws.amazon.com/blogs/devops/how-to-enable-caching-for-aws-codebuild/](https://aws.amazon.com/blogs/devops/how-to-enable-caching-for-aws-codebuild/)

Basically all you do is specify a AWS S3 bucket that should be used as the cache location and some additional information. 

There is one misleading part of information in the guide that I had some issues while enabling the cache:
You will get this error if you specify the Cache path prefix to be `cache/archives/`:

`Invalid cache: location must be a valid S3 bucket, followed by slash and the prefix`

The correct form is `/cache/archives/`.

## Secrets

Storing secrets and providing them to the pipeline and build process is something one must almost always do. Documentation guides the developer to use AWS Systems Manager Parameter Store. CodeBuild is then able to access the secrets during runtime. 

After adding the secrects to the Parameter Store, you must add *ssm:GetParameters* permission to the CodeBuild Service Worker role for it to be able to access the secrets. The easiest way to do so is by adding *AmazonSSMReadOnlyAccess* policy for the CodeBuild Service Worker Role.

Maven Secrets are also used to encrypt the credentials needed to access the private Maven repository of MuleSoft and the deployment keys to CloudHub. The process is explained [here](https://docs.mulesoft.com/mule-runtime/3.9/mule-maven-plugin#encrypting-credentials). The actual Maven Master Password needs to be stored somewhere securely. I used AWS Secrects Manager, but any Password manager would do. 

### Cache for Maven repository

There is a good guide on how to specify the cache for the CodeBuild Project: [https://aws.amazon.com/blogs/devops/how-to-enable-caching-for-aws-codebuild/](https://aws.amazon.com/blogs/devops/how-to-enable-caching-for-aws-codebuild/)

Basically all you do is specify a AWS S3 bucket that should be used as the cache location and some additional information. 

There is one misleading part of information in the guide that I had some issues while enabling the cache:
You will get this error if you specify the Cache path prefix to be `cache/archives/`:

`Invalid cache: location must be a valid S3 bucket, followed by slash and the prefix`

The correct form is `/cache/archives/`.

# Maven POM for CloudHub deployment

In the POM of the Mule Application you need to define the *cloudHubDeployment* configuration section, for the mule-maven-plugin to perform the deployment to CloudHub.
All the parameters used in the plugin are injected as command line parameters in the buildSpec file.

The `<server>demo.anypoint.credentials</server>` points to the maven-settings.xml file, where a server has been defined with credentials for accessing CloudHub.

The `anypoint.platform.client_id` & `anypoint.platform.client_secret` properties are passed to the MuleSoft Application to communicate with API Gateway. They are not related to the deployment process.

```xml
<plugin>
    <groupId>org.mule.tools.maven</groupId>
    <artifactId>mule-maven-plugin</artifactId>
    <version>${mule.maven.plugin.version}</version>
    <extensions>true</extensions>
    <configuration>
        <classifier>mule-application</classifier>
        <cloudHubDeployment>
            <uri>https://anypoint.mulesoft.com</uri>
            <muleVersion>${app.runtime}</muleVersion>
            <server>demo.anypoint.credentials</server>
            <applicationName>${project.artifactId}-app</applicationName>
            <environment>${anypoint.platform.environment}</environment>
            <workerType>${anypoint.platform.workertype}</workerType>
            <workers>${anypoint.platform.workers}</workers>
            <region>${anypoint.platform.region}</region>
            <properties>
                <anypoint.platform.client_id>${anypoint.platform.client_id}</anypoint.platform.client_id>
                <anypoint.platform.client_secret>${anypoint.platform.client_secret}</anypoint.platform.client_secret>
            </properties>
        </cloudHubDeployment>
        <inclusions>
                <inclusion>
                    <groupId>org.mule.modules</groupId>
                    <artifactId>demo-custom-connector</artifactId>
                </inclusion>
            </inclusions>
    </configuration>
</plugin>

```

# Summary

So was it worth it? Yes. The use case we have is such that we make changes to the actual demo MuleSoft application maybe once or twice a year. Hosting a Jenkins server somewhere costs money and requires effort to keep it secure. One could host the Jenkins server in any hosting service and start it only when needed, but still would need to take care of the security updates etc. By using services like CodeBuild and CodePipeline, we set us free from those maintenance tasks and only pay for the resources we use during the build and the possible storage costs. So it's a perfect match for our use case.

Setting up services in AWS is simple, but there are some things that are not that simple. Let's take security settings as an example. IAM (AWS Identity and Access Management) is the key to making the AWS services work together. IAM can be difficult to understand in the beginning and getting everything to work might not always be simple. So if you are already working with AWS services, using AWS Developer Tools makes perfect sense. 

If you host your code in GitHub or GitLab they offer similar capabilities and it might be easier to setup the CI/CD pipeline there.

Thank you for reading!