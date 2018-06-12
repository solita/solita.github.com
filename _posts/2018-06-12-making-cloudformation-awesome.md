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

[CloudFormation](https://aws.amazon.com/cloudformation/) is a cloud provisioning tool by AWS for AWS for declaratively describing your AWS resources. CloudFormation is hard, complex, inconsistent and badly documented piece of software to say the least, but by following couple of easy guidelines you can really make it shine and provide cloud resources like a pro.

![CloudFormation like a pro](/img/cloudformation-awesome.jpg)

Even though this post assumes basic knowledge of CloudFormation, here's quick definitions of some of the terms used in this text.

**Stack**

Stack is a atomic collection of resources in CloudFormation. Stack update or creation can success only and only if all the resources within stack success. Failure in updating stack rollbacks the previous state.

**Stack Export/Import**

Each stack can Export and Import values. Exports are effectively key/value store, to which other stacks can refer to. For instance, your stack might export `MyAppRole.Arn`, with key `MyAppRole` value being something like `arn:aws:iam::123456789012:role/MyAppRole` to which other stacks can refer to using `!Import MyAppRole`.

**Stack Parameters**

Stacks can be parametrised, which is really powerful feature for spinning multiple environments from same templates.

## The Principles

Here's my principles I follow with CloudFormation. And trust me, your truly has crafted some pretty hefty CloudFormation based systems 😉

### 1. Large is Good

You might be tempted to divide your application stack into small logical pieces. And I don't blame you for this - programmers and ops people are generally really good in structuring things from small pieces. But with CloudFormation, this is just not practical. For instance, you could have horseloads of small stacks, such as:

* `acme-iam-stack.yml`
* `acme-network-stack.yml`
* `acme-security-groups-stack.yml`
* `acme-messaging-stack.yml`
* `acme-computing-stack.yml`
* `acme-load-balancing-stack.yml`
* `acme-persistence-stack.yml`

But this brings really tough problem to the table: stacks have dependencies to each others and you really need to maintain correct creation and deletion order for your microstacks. This can bring up huge problems in updating your system.

If resources don't change, CloudFormation is generally really fast in updating stack. Well, at least acceptably fast in updating stack. This is not a optimisation issue. This is a dependency issue.

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

You be the judge. Of course, making one stack with lots of resources equal huge file. With CloudFormation, you should be ready to compromise bit on file sizes. Of course, you should order and name your resources nicely in your template files, and keep them under version control (duh!).

CloudFormation has [hard resource limits](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cloudformation-limits.html). Each stack can contain 200 resources, and when you're coming close to that, it's good time to think about splitting the stack to smaller pieces. At that stage, your system is probably anyway so complex that you have done it anyway already.

Good test for you is to try to spin up your system to a new AWS account or to a different region. Can you make it in 15 minutes? Or does it take more than a day? If you can make it quickly, I bet you have small amount of stacks or a really good graph in your head of the dependencies between the stacks.

There are cases, when having multiple stacks is a pretty good idea. And this brings us to our next principle.

### 2. Be Careful with the Dependencies

When you need more than one stack, you really need to start to think about *dependencies*. Usually CloudFormation stacks do not live in isolation, but instead they refer to resources created by separate stack. Concrete example would be for instance multiple microservices in single ECS/FARGATE cluster behind one single [ALB](https://aws.amazon.com/elasticloadbalancing/).

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
    acme-products-service.yml (ECS Service and Task definitions, Imports necessary stuff)
acme-orders-api
    acme-orders-service.yml (ECS Service and Task definitions, Imports necessary stuff)
acme-customers-api
    acme-customers-service.yml (ECS Service and Task definitions, Imports necessary stuff)    
```

Using shared ALB like this requires some additional tweaks, i.e sharing routing priority numbers between services, but that is an implementation detail. Rule of the thumb is that you should have just the right amount of stacks and dependency graph must be unidirectional. So kids! Remember not to use `!Import` in the infra stack! 😘

It's super important to understand in which stack you should add your resource in multi-stack scenario, because you can really easily make circular dependencies between stacks. Think for instance if you have separate stacks for [CloudFront](https://aws.amazon.com/cloudfront/) and [S3 buckets](https://aws.amazon.com/s3/). Your CloudFront stack needs to know S3 bucket domains and your S3 bucket policy is S3 stack needs to know CloudFront [Origin Access Identity](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html). There you have a circular dependency and you probably spend loadsa time debugging and possibly even suffer some downtime when stuff hits the fan.

But the good news is that when you just bake both CloudFront and S3 stuff into same stack - it just works.

Bottom line is that, when having multiple stacks, you should be really careful when selecting a stack for your new resource. It's a good idea to have well maintained visualisation of the stacks and exports/imports. Don't be afraid to make a loose coupling between resources when needed! It's totally ok to just copy resource references directly as a parameters to other stacks instead of exporting and importing them. Exporting is a really powerful tool and it makes really hard coupling between the stacks.

What about the different environments then?

### 3. Parametrise Right Things Instead of All Things

CloudFormation supports parameters for stacks which can be given as a JSON file or directly to AWS CLI. This is nice, because I would hate to maintain `acme-app-dev.yml` and `acme-app-prod.yml`, both thousands of lines long.

My CloudFormation parametrisation principle is really easy to follow:

1. Parametrise attributes that actually are different in your environments
2. Don't parametrise things that you think can eventually change in your environments
3. When thing changes which is not parametrised, see if it is different per environment. If it is different, add it as a parameter, and if not, leave it to the template.

And this brings us to our last principle.

### 4. Do Just the Right Thing with CloudFormation

**Usual question with CloudFormation:**

> Should I do **everything** with CloudFormation or do some stuff from the console?

**Answer:**

> Do **99%** with CloudFormation.

Stuff I usually leave outside of CloudFormation:

**Route53 Hosted Zones**

I create hosted zones manually. This is primarily because usually domains are registered outside of Route53 and generated NS records are just given to registrar which points records to Route53. I feel more safe for some reason when this is done manually.

But I sure do add DNS records to hosted zones with CloudFormation.

```
AcmeProductsALBRecord:
    Type: AWS::Route53::RecordSet
    Properties:
        AliasTarget:
            DNSName: !GetAtt LoadBalancer.DNSName
            HostedZoneId: "Z32O12XQLNTSW2" # Ireland hosted zone id for ALB
        Comment: "Acme products ALB record"
        HostedZoneId: !Ref AcmeProductsHostedZoneId # This is from manually created Route53 hosted zone!!!
        Name: !Ref AcmeProductsDNSName
        Type: "A"
```

**Simple Certificate Manager SSL Certificates**

These require validation steps, so I have just created these by hand and copied Certificate ARN to CloudFormation templates/parameters. If you have a good workflow for automating this, feel free to drop a comment down below!

**SES Production Configuration**

SES contains validation steps as well, so this is also something I have always done outside of CloudFormation.

## Serverless

What about those cool kids spinning up cost efficient lambdas while sipping soya-latte? AWS actually recommends, that when you do http services with lambdas, you're way better of using something like [serverless](https://serverless.com/), instead of using CloudFormation for lambdas and API Gateway. Serverless does this for you and it does it pretty good.

But what you can do, is that you can bake in some bare CloudFormation resources to your serverless app!

Here's my example of serveless app with raw CloudFormation resources baked in: [https://github.com/juhofriman/serverless-rocket-example](https://github.com/juhofriman/serverless-rocket-example).

The weirdest thing is that YAML serverless.yml is not CloudFormation YAML but it is transformed to JSON.

Spend some time debugging how those Refs work in serverless.yml 😂

But that's another story.
