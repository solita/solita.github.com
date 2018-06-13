---
layout: post
title: Making CloudFormation Awesome
author: juhofriman
excerpt: AWS CloudFormation can be your best friend or the worst enemy depending on how you use it. Here's my tips and trick in making CloudFormation to really shine.
tags:
- Cloud
- AWS
- CloudFormation
- DevOps
---

[CloudFormation](https://aws.amazon.com/cloudformation/) is the inhouse cloud provisioning tool of AWS for declaratively describing your cloud resources. CloudFormation is a hard, complex, inconsistent and badly documented piece of software to say the least, but by following couple of easy principles you can really make it shine and provide cloud resources like a pro.

![CloudFormation like a pro](/img/cloudformation-awesome.jpg)

My principles are:

1. Large is Good
2. Be Careful with the Dependencies
3. Parametrise Right Things Instead of All Things
4. Do Just the Right Thing with CloudFormation
5. Protect your Persistent Data

Even though this post assumes basic knowledge of CloudFormation, here's quick definitions of some of the terms used in this text.

**Stack**

Stack is an atomic collection of resources in CloudFormation. Stack update or creation can success only and only if all the resources within the stack success. Failure in updating stack rollbacks the previous state.

**Stack Export/Import**

Each stack can Export and Import values. Exports are effectively key/value store, to which other stacks can refer to. For instance, your stack might export `MyAppRole.Arn`, with key `MyAppRole` value being something like `arn:aws:iam::123456789012:role/MyAppRole` to which other stacks can refer to using `!Import MyAppRole`.

**Stack Parameters**

Stacks can be parametrised, which is really powerful feature for spinning multiple environments from same templates.

## The Principles

### 1. Large is Good

You might be tempted to divide your application stack into small logical pieces. And I don't blame you for this - programmers and ops people are generally really good in structuring things from small pieces. But with CloudFormation, this is just not practical. For instance, you could have horseloads of small stacks, such as:

* `acme-iam-stack.yml`
* `acme-network-stack.yml`
* `acme-security-groups-stack.yml`
* `acme-messaging-stack.yml`
* `acme-computing-stack.yml`
* `acme-load-balancing-stack.yml`
* `acme-persistence-stack.yml`

But this brings a really tough problem to the table: stacks have dependencies to each others and you really need to maintain correct creation and deletion order for your microstacks. This can bring up huge problems in updating your system.

If resources don't change, CloudFormation is generally really fast in updating stack. Well, at least acceptably fast in updating stack. This is not an optimisation issue. This is a dependency issue.

Which is cooler?

```
aws cloudformation create-stack --stack-name acme-app --template-body fileb://acme-app.yml
# Do some work, time passes on, applications die...
aws cloudformation delete-stack --stack-name acme-app
# ...and your resources are deleted
```

**OR**

```
aws cloudformation create-stack --stack-name acme-iam-stack --template-body fileb://acme-iam-stack.yml
aws cloudformation create-stack --stack-name acme-network-stack --template-body fileb://acme-network-stack.yml
aws cloudformation create-stack --stack-name acme-security-groups-stack --template-body fileb://acme-security-groups-stack.yml
...
...
# Do some work, time passes on, applications die...
# ...Weeel, what was the correct stack deletion order?
```

You be the judge. Of course, making one stack with lots of resources equal a huge file. With CloudFormation, you should be ready to compromise on file sizes. Of course, you should order and name your resources nicely in your template files, and keep them under version control (duh!).

CloudFormation has [hard resource limits](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cloudformation-limits.html). Each stack can contain 200 resources, and when you're coming close to that, it's good time to think about splitting the stack to smaller pieces. At that stage, your system is probably anyway so complex that you have done it anyway already.

Good test for you is to try to spin up your system to a new AWS account or to a different region. Can you make it in 15 minutes? Does it take more than a day? If you can make it quickly, I bet you have small amount of stacks or a really good graph in your head of the dependencies between the stacks.

There are cases, when having multiple stacks is a pretty good idea. And this brings us to our next principle.

### 2. Be Careful with the Dependencies

When you need more than one stack, you really need to start to think about *dependencies*. Usually CloudFormation stacks do not live in isolation, but instead they refer to resources created by separate stack. A concrete example would be for instance multiple microservices in single ECS/FARGATE cluster behind one single [ALB](https://aws.amazon.com/elasticloadbalancing/).

Consider an example, in which Acme Corporation has three microservices:

* https://products.acme.com
* https://orders.acme.com
* https://customers.acme.com

All services are kept in separate git repositories (`acme-products-api`, `acme-orders-api` and `acme-customers-api`), but because of the cost optimisation policy, all of these services must be served via single load balancer using host based routing and all docker containers must be deployed in the same ECS cluster.

In a scenario like this, it's a pretty good idea to spin up a new stack `acme-infra` for defining shared resources. So setup would be something similar to this.

```
acme-infra
    acme-infra.yml (vpc, SecurityGroups, ECS cluster + roles, ALB)
acme-products-api
    acme-products-service.yml (ECS definitions, target group, ALB routing rules, Imports necessary stuff)
acme-orders-api
    acme-orders-service.yml (ECS definitions, target group, ALB routing rules, Imports necessary stuff)
acme-customers-api
    acme-customers-service.yml (ECS definitions, target group, ALB routing rules, Imports necessary stuff)    
```

Using shared ALB like this requires some additional tweaks, i.e sharing routing priority numbers between services, but that is an implementation detail. Rule of the thumb is that you should have just the right amount of stacks and dependency graph must be unidirectional. So kids! Remember not to use `!Import` in the infra stack! 😘

It's super important to understand in which stack you should add your new resource in a multi-stack scenario, because you can really easily make circular dependencies between stacks. Think for instance if you have separate stacks for [CloudFront](https://aws.amazon.com/cloudfront/) and [S3 buckets](https://aws.amazon.com/s3/). Your CloudFront stack needs to know S3 bucket domains and your S3 bucket policy is S3 stack needs to know CloudFront [Origin Access Identity](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html). There you have a circular dependency and you probably spend loadsa time debugging and possibly even suffer some downtime when stuff hits the fan.

But the good news is that when you just bake both CloudFront and S3 stuff into the same stack - it just works.

Bottom line is that, when having multiple stacks, you should be really careful when selecting a stack for your new resource. It's a good idea to have well maintained visualisation of the stacks and exports/imports. Don't be afraid to make a loose coupling between resources when needed! It's totally ok to just copy resource references directly as a parameters to other stacks instead of exporting and importing them. Exporting is a really powerful tool and it makes really hard coupling between the stacks. Try to minimise the amount of stacks. Less is more.

What about the different environments then?

### 3. Parametrise Right Things Instead of All Things

CloudFormation supports parameters for stacks which can be given as a JSON file or directly to AWS CLI. This is nice, because I would hate to maintain `acme-app-dev.yml` and `acme-app-prod.yml` - both thousands of lines long.

My CloudFormation parametrisation principle is really easy to follow:

1. Parametrise attributes that actually are different in your environments
2. Don't parametrise things that you think can eventually change in your environments
3. When thing changes which is not parametrised, see if it is different per environment. If it is different, add it as a parameter, and if not, leave it to the template.

And this brings us to our last principle.

### 4. Do Just the Right Thing with CloudFormation

**Usual question with CloudFormation:**

> Should I do **everything** with CloudFormation or do some stuff from the console?

**Answer:**

> Do **80-90%** with CloudFormation.

The stuff I usually leave outside of CloudFormation:

**Route53 Hosted Zones**

I create hosted zones manually. This is primarily because usually domains are registered outside of Route53 and generated NS records are just given to registrar which points records to Route53. I feel more safe for some reason when this is done manually.

But I sure do add DNS records to hosted zones with CloudFormation.

```yaml
AcmeProductsALBRecord:
    Type: AWS::Route53::RecordSet
    Properties:
        AliasTarget:
            DNSName: !GetAtt LoadBalancer.DNSName
            HostedZoneId: "Z32O12XQLNTSW2" # eu-west-1 hosted zone id for ALB
        Comment: "Acme products ALB record"
        HostedZoneId: !Ref AcmeProductsHostedZoneId # This is from manually created Route53 hosted zone!!!
        Name: !Ref AcmeProductsDNSName
        Type: "A"
```

**Simple Certificate Manager SSL Certificates**

Acquiring SSL certificates require validation steps, so I have just created these by hand and copied Certificate ARN to CloudFormation templates/parameters. If you have a good workflow for automating this, feel free to drop a comment down below!

**SES Production Configuration**

Amazon Simple Email Service contains validation steps as well, so this is also something I have always done outside of CloudFormation.

**CI/CD Pipeline User Access Keys**

I create IAM User for pipelines usually in a separate stack. Here's a template you can use:

```yaml
CiPipelineUser:
  Type: "AWS::IAM::User"
  Properties:
    # Pass required Managed Policy ARN:s here
    ManagedPolicyArns:
      - arn:aws:iam::aws:policy/AmazonS3FullAccess
    Policies:
      # Additional policy for CloudFormation
      - PolicyName: "CloudFormation-access"
        PolicyDocument:
          Version: '2012-10-17'
          Statement:
          - Effect: Allow
            Action:
            - "cloudformation:*"
            Resource: "*"
      # Additional policy for SSM parameter access
      - PolicyName: "Parameter-store-access"
        PolicyDocument:
          Version: '2012-10-17'
          Statement:
          - Effect: Allow
            Action:
            - "ssm:GetParameter"
            - "ssm:GetParameters"
            - "ssm:GetParametersByPath"
            - "kms:Decrypt"
            Resource: "*"
```

But access keys for user are created and injected to CI/CD system outside of CloudFormation. This is primarily meant for [Gitlab](https://about.gitlab.com/), [Travis CI](https://travis-ci.org/) and such. If you use an AWS managed CI/CD services like CodePipeline, CodeDeploy and such, case is bit different. Then you would use a IAM Role instead of a IAM User.

Homework for you is to plan automatic rotation for access keys. Managing secrets is out of scope of this post, but I promise to write a follow up post: *Securing your CloudFormation*.

### 5. Protect your Persistent Data

It's really easy to accidentally nuke all the data in RDS with CloudFormation. Just make a change that requires replace to your RDS resource and **BANG**, your data is lost.

Excerpt from [CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html):

> If a DB instance is deleted or replaced during an update, AWS CloudFormation deletes all automated snapshots. However, it retains manual DB snapshots. During an update that requires replacement, you can apply a stack policy to prevent DB instances from being replaced.

You have pretty much two choices:

1. Don't update stacks automatically, but instead make a [CloudFormation change set](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-changesets.html), which gives you a good listing, what CloudFormation will actually do.
2. Use [CloudFormation stack policy](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/protect-stack-resources.html) to protect the resources from accidental deletion.

When making changes to CloudFormation stacks you should always browse through the documentation and see if your modification requires a REPLACE operation for your resource. If it does require replacement, analyse what will happen to all the dependent resources.

## Serverless

What about those cool kids spinning up cost efficient lambdas while sipping soya-latte? AWS actually recommends, that when you do http services with lambdas, you're way better of using something like [serverless](https://serverless.com/), instead of using CloudFormation for lambdas and API Gateway. Serverless does this for you and it does it pretty good.

But what you can do, is that you can bake in some bare CloudFormation resources to your serverless app!

Here's my example of serveless app with raw CloudFormation resources baked in: [https://github.com/juhofriman/serverless-rocket-example](https://github.com/juhofriman/serverless-rocket-example).

The weirdest thing is that YAML serverless.yml Resources block is not CloudFormation YAML, but it is transformed to JSON.

Spend some time debugging how those Refs and Attrs work in serverless.yml 😂

But that's another story.
