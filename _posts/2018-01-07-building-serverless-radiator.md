---
layout: post
title: Building a serverless radiator for fun and benefit with Clojure, Python and AWS 
author: hjhamala
excerpt: Monitoring software development pipeline statuses, environment alarms and metrics are an essential part of a modern software development process in a cloud environment. In this post I show a simple way to monitor different accounts with a serverless radiator. 
tags:
- AWS
- Clojure
- Serverless 
---

***There exists many commercial products for monitoring development pipelines and deployments. What could be more fun than make your own?***

**Modern** software development environment is most likely composed of multiple pipelines. There can be pipelines for build artifacts, infrastructure building etc. It is vital to notice fast when the builds fail. Monitoring only the pipelines is not necessary enough. Also deployments should be monitored for noticing potential problems in performance etc. 

One project might have different accounts for development, testing/integration and production. This means that monitoring simply one account is not even closely enough. For example in my current project at Solita, we have 3 different accounts which have 7 pipelines, over 60 CloudWatch alarms and some exposed metrics from deployments.

One good solution is to have a radiator which shows development status:

![Alarm!](/img/building-serverless-radiator/complete-radiator.png)

Because making your own is interesting and fun I chose to make my own radiator. For cost optimization I chose serverless approach with AWS [Lambdas](https://aws.amazon.com/lambda/). Lets start our journey from how to expose pipelines, alarms and metrics from AWS accounts.

## Exposing environment statuses from AWS accounts

AWS [CodePipeline](https://aws.amazon.com/codepipeline/) is an AWS software product for building, testing and installing software to the AWS environment. It integrates very nicely with AWS [CloudFormation](https://aws.amazon.com/cloudformation/) and is a pay only what you use product. There is no need to provision EC2 virtual machines for builds - AWS will provision them for you.

One can get statuses from CodePipeline by using AWS CLI or AWS SDK which is available for many different languages. AWS [CloudWatch](https://aws.amazon.com/cloudwatch/) alarms and metrics are also accessible via CLI and SDK. 

One way to extract data would be to make an AWS user to every account, generate a access key id and a secret key and poll end points directly from the radiator software. A variant of this would be to make a AWS role and configure cross account permissions to switch to that role. 

Third way which I chose is to make a Lambda function which exposes statuses in one JSON data response. That way it is possible to get all necessary data from one endpoint. The endpoint should be protected with an api key which is supported quite nicely in the Amazon [API Gateway](https://aws.amazon.com/api-gateway/). The radiator should poll the endpoints and generate a view of the account status.

AWS Lambda environment currently supports Node.js, Java, C# and Python languages. For an endpoint exposer I chose Python which have excellent [Boto 3](https://boto3.readthedocs.io/en/latest/) SDK for accessing AWS.

First I started from what I want as a result. The result should be JSON response with different keys for alarms, pipelines and metrics. 

```json
{
    "alarms": [
        {
            "AlarmName": "product-name-service-500",
            "StateValue": "OK"
        }
    ],
    "pipelines": [
        {
            "name": "ProjectInfraBuildPipeline",
            "currentStatus": "Succeeded"
        }
    ],
    "metrics": [
        {
            "name": "RDS CPU Utilization",
            "statistics": "Average",
            "unit": "Percent",
            "result": 7.004
        }
    ]
}
```

The main handler is therefore quite simple. There is no need to use any parameters because we return always all the pipelines and alarms.   

```python
def status(event, context):
    result = {
        "alarms":get_alarms(),
        "pipelines" : get_pipelines(),
        "metrics" : get_metrics()}
    return {"body": json.dumps(result)}
```

Getting pipeline statuses and alarms is quite straightforward. The alarms can be fetched with one API call. Pipelines need to be first fetched and then current statuses can be checked one by one. For the radiator I also formatted the result a little bit.

Metrics cannot be fetched with one call because AWS has tons of different kind metrics available. Currently I make a Python data structure which describes what kind of metric I want to expose. The next code example gets average RDS CPU utilization of last 10 minutes.

```python
metrics= [{'name': 'RDS CPU Utilization',
            'request': {'Namespace':'AWS/RDS',
                         'MetricName':'CPUUtilization',
                         'StartTime': datetime.utcnow() - timedelta(minutes=10),
                         'EndTime': datetime.now() ,
                         'Period': 600,
                         'Statistics':['Average'],
                         'Unit':'Percent'},
            'statistics': 'Average',
            'unit': 'Percent'}]
```            

Lambda can be installed by hand via AWS Console but automatized installing is much more preferable. Fortunately [Serverless Framework](https://serverless.com/) supports also deploying Python code. 

With Serverless installing the Radiator Exposer is easy. Just run ``serverless deploy``. Serverless  runs for a while and returns a new endpoint and an api key necessary for authentication. 

The Radiator exposer is a free software which can be downloaded from [https://github.com/hjhamala/radiator-exposer](https://github.com/hjhamala/radiator-exposer).


## Building a radiator

Getting information from an account is not enough. There should be some fancy and visual way to show it. This can be made also via serverless approach. 

For the radiator I chose to make Clojure Lambda which polls endpoints and generates plain old html response with automatic refresh. Because AWS Lambda supports Java is Clojure therefore supported. For generating necessary Java classes I used [Lambada](https://github.com/uswitch/lambada) library. The radiator should be run also locally so I wrote also a simple web server for local usage.

### Generating HTML

Generating HTML is easy with Clojure using [Hiccup](https://github.com/weavejester/hiccup) library. Hiccup syntax is also very readable way to make HTML. The main function of the radiator is quite simple.

```clojure
(defn generate
  []
  (hiccup/html
    [:html
     [:head
      [:meta {:charset    "UTF-8"
              :http-equiv "refresh" :content "10"}]
      [:meta {:http-equiv "Cache-Control" :content= "no-store"}]
      [:title config/title]
      styles]
     [:body
      page-header
      (content)]]))
```
One limitation of the serverless approach is that all data for rendering the page should be returned in one response or be linked to outside resources. Lambda is not a web server so there is no way to serve static resources like CSS files. One could of course use S3 or another approach for static files.

### Mix some styles and images

Instead of linking to CSS files I chose to embed necessary CSS in HTML response. For this I used [Garden](https://github.com/noprompt/garden) library which makes CSS generation quite similar like using Hiccup.

The next code snippet shows part of the CSS for the radiator.

```clojure
(def styles
  [:style
    (css [:body {:margin  "0px"
                 :padding "0px"}])
    (css [:h1 {:font-family    "proxima-nova,sans-serif"
               :text-transform "uppercase"
               :margin         "0px"
               :font-size      "18px"}])])
```

The Radiator needs of course some fancy images to visually show when something has gone wrong - alert icons etc. Because HTML images are simply links one can link images from anywhere in Internet. GitHub version of the radiator have preconfigured links to Tango Desktop icons which work quite nicely. The images can be changed via configuration.

### Configuring endpoints

The configuration of the endpoints is done with a simple data structure.

```clojure
(def projects
  [{:name             "example account"
    :aws              {:uri     "https://uri-to.com/api-gateway"
                       :api-key "secret-api-key"}
    }])
```

### Supporting different CI providers

The Radiator should of course support also another CI providers like [GitLab](https://about.gitlab.com/). To make this easier I made a generic data structure for pipelines, alarms and metrics. The radiator should therefore first fetch data from endpoints, after that transform them to generic format which is then rendered to Radiator view.

The generic data structure is defined as Clojure Spec as next with example:

```clojure
(s/def ::name string?)
(s/def ::pipeline-status #{:success :in-progress :failed :unknown})
(s/def ::pipeline (s/keys :req-un [::name ::pipeline-status]))
(s/def ::alarm-status #{:ok :alarm})
(s/def ::alarm (s/keys :req-un [::name ::alarm-status]))
(s/def ::metric (s/keys :req-un [::name ::metric-value]))

;; Pipeline example
{:name "InfraBuild"
:pipeline-status :in-progress}

;; Alarm example
{:name "Service-500-alarm"
:alarm-status :ok}

;; Metric example
{:name "RDS avg. CPU"
:metric-value 1.3}
```

Supporting the GitLab is done simply fetching pipeline data via REST api and after that transforming a pipeline status to generic format.

```clojure
(defn- transform-pipeline
  [{:keys [status name]}]
  (condp = status
    "success"  {:name name :pipeline-status :success}
    "failed"   {:name name :pipeline-status :failed}
    "running"  {:name name :pipeline-status :in-progress}
    "pending"  {:name name :pipeline-status :in-progress}
    "canceled" {:name name :pipeline-status :success}
    "skipped"  {:name name :pipeline-status :success}
    {:name name :pipeline-status :unknown}))
```

### Adding visual hints

The radiator should show at a glance what is going on in accounts. In default there is no need to list different pipelines or alarms - only show the number of pipelines etc. so we can be sure that the exposer is working correctly.

![All OK](/img/building-serverless-radiator/all-ok.png)

When the pipeline is running the account name is changed to yellow and the running pipeline is shown:

![Pipeline running](/img/building-serverless-radiator/pipeline-running.png)

Unfortunately there is situations where all gone bad and it should be visually made clear by using red color:

![Alarm!](/img/building-serverless-radiator/alarm.png)


###  Installing radiator

The radiator is also installed by using Serverless framework. The framework has support for Java but for easier deployment I made a [Clojure serverless plugin](https://www.npmjs.com/package/serverless-clj-plugin) for better Clojure support. Using the plugin the installation is done simply by running  ``serverless deploy``. The radiator endpoint should of course be protected but instead of API Gateway - token string can be set in the configuration file radiator.config.

## Conclusion 

Serverless radiator is usable now for my needs at Solita. It should be pretty straightforward to add support for different cloud providers like Azure or Google Cloud. Both of these should have alternatives for AWS Lambdas and a way to expose necessary information. 

The radiator is now done to support only fixed sized displays. Maybe in the future I will make an responsive UI so the radiator can be easily shown in mobile devices. Instead of linking to external images one could simply embed necessary images as inline SVG elements.  

Downloads:
- [Radiator](https://github.com/hjhamala/lambda-radiator)
- [Radiator exposer](https://github.com/hjhamala/radiator-exposer)