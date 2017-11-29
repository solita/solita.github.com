---
layout: post
title: Kubernetes support, serverless Aurora, DeepLens camera and many more interesting releases in re:Invent 2017 on Wednesday
author: kimmokantojarvi 
excerpt: During Wednesday morning keynote Andy Jassy hit us once again with so many new announcements and service releases. I will try to summarize some of the key points in this post.  
tags:
- AWS
- re:Invent
---

My previous post about the releases on Monday and Tuesday can be read [here](/2017/11/28/AWS-reInvent-first-announcements.html). 

## About the keynote setup
As expected the setup for the keynote show was stunning. DJ playing music, houseband on the stage and house full of people. Most of the time we were hosted by Andy Jassy, but he also brought some customers on the stage to share their experiences. In this post I will only cover key points about new services released today by Andy.

![Reinvent](/img/aws/reinvent_2017_3.jpeg)



### Compute
Container services have been very important focus area in our customer cases during the last years. It is not really a suprise that AWS is also investing heavily into container services. Today we witnessed 2 major releases. 

[Fargate](https://aws.amazon.com/blogs/aws/aws-fargate/) is totally new service that will basically be like serverless containers. Fargate fits very well between the use cases of Lambda which is suitable for very short living tasks and traditional container services where one needs to take care of reserving enough capacity. I'm sure we will be seeing Fargate in use in our customer cases in the future. 

[EKS aka ECS for Kubernetes](https://aws.amazon.com/blogs/aws/amazon-elastic-container-service-for-kubernetes/) is good news for those organisations that have invested heavily into Kubernetes. I believe many have found the limits of ECS constraining and are more than happy to try out EKS instead. 

One of the smaller but interesting release was the [support of routing traffic to different Lambda function versions](https://aws.amazon.com/blogs/aws/amazon-elastic-container-service-for-kubernetes/) based on pre-assigned weights. Mitigating the risk of Lambda function updates will now be easier. 

### Databases
Oh boy what they had reserved for us in the database services. Hard to even decided where to start. First of all the [release of serverless Aurora](https://aws.amazon.com/blogs/aws/in-the-works-amazon-aurora-serverless/) is just amazing. This is definitely the way databases should be heading allowing much greater flexibility and scaling in the future. At the moment it is still a bit unclear how well the scaling will work in real-life scenarios, but based on Amazon blog post it should be blazing fast meaning that scaling up new computing capacity would happen just in 5 seconds. Let's see what the reality will be. 

The releas of [Multi-Master Aurora](http://www.businesswire.com/news/home/20171129006077/en/AWS-Announces-New-Capabilities-Amazon-Aurora-Amazon) is probably more important for those organisations having mission-critical applications connected to Aurora, because the new service will increase the high availability greatly. This is still in Preview and will be released later in 2018. 

Typically the setup and running GraphQL databases has been just too much work. Amazon is once again making our lives easier by [releasing GraphQL as a fully-managed service called Neptune](https://aws.amazon.com/about-aws/whats-new/2017/11/amazon-neptune-fast-reliable-graph-database-built-for-the-cloud/). Neptune supports in the first phase Apache TinkerPop Gremlin and RDF/SPARQL. At the moment is only available as preview in US East.  

DynamoDB was also boosted with additional features. [The release of global tables](https://aws.amazon.com/blogs/aws/new-for-amazon-dynamodb-global-tables-and-on-demand-backup/) is aimed for organisations running multi-region applications where latency could potentially be an issue. Global tables remove the need to sync data between regions and thus provides fast local read and write performance. In addition to the global tables DynamoDB has now also [backup functionality](https://aws.amazon.com/blogs/aws/new-for-amazon-dynamodb-global-tables-and-on-demand-backup/). This will help organisations to meet the regulatory needs and requirements for long-term archiving. Backups can also be used to restore DynamoDB tables, which might sometimes be handy if some specific data has been deleted or lost.


### Machine Learning

<img src="https://d1.awsstatic.com/DeepCamAssets/front.47ed64d4ea219977066e2c3721d61869461d5658.jpg" alt="DeepLens camera" style="width: 250px;"/>

Like for database services a lot of new releases were revealed in machine learning service area. One of my personal favorite is [the release of SageMaker](https://aws.amazon.com/blogs/aws/sagemaker/) service which is managed machine learning service. It has been obvious that creating good ML solutions has been very difficult and it has been typically based on very complex application setup. With the release of SageMaker AWS has set the target of making creating machine learning solutions easier for developers. SageMaker has pre-defined notebooks to start with and it comes with 10 most common machine learning algorithms and pre-configured with Tensorflow and MXNet. One of the nice features of SageMaker is that developers can use just some of the components of SageMaker instead of using only SageMaker for machine learning. For example you can deploy the model through some other solution. 

Another cool service exposed today is [the Rekognition Video](https://aws.amazon.com/blogs/aws/launch-welcoming-amazon-rekognition-video-service/). It can be used to identify people, objects and many other things from the video whether it is live-stream or batch. There are many uses case for Rekognition already for example in home automation and security. When the home owner is arriving from work to home system would recognise the license plate and automatically set all settings in home for returning mode. 


One of the weirdest releases was in my opinion [the DeepLens](https://aws.amazon.com/blogs/aws/deeplens/) which is a combination of web camera and AI software packaged in one bundle. In the example it was used to identify LP shown to the camera and mood of the presenter based on the facial expression. It is a bit difficult tell yet whether it will be a real production-ready product or more of entry level tool for organisations to get going with Rekognition Video service. 

Typically NLP solutions are based on a lot of custom code and custom training material. With the release of [Amazon Comprehend](https://aws.amazon.com/blogs/aws/amazon-comprehend-continuously-trained-natural-language-processing/) once again the work of developers will be made easier. Unfortunately Comprehend will in the beginning support only English and Spanish texts. 

[Amazon Translate](https://aws.amazon.com/blogs/aws/introducing-amazon-translate-real-time-text-language-translation/) is basically a service like Google Translate. With the help of deep learning Translate service can be used to translate texts from and to English to Arabic, Simplified Chinese, French, German, Spanish, and Portuguese. The best part of the Translate is that it can be connected directly to other AWS services such as Polly, S3, Lex, Lambda and ElasticSearch.

[Amazon Transcribe](https://aws.amazon.com/blogs/aws/amazon-transcribe-scalable-and-accurate-automatic-speech-recognition/) is a new service to translate speech to text based on audio files stored in S3. The cool thing is that Transcribe can be connected to Translate and that's how English speech can be translated into German text for example. 





### Analytics
The launch of [Kinesis Video Streams](https://aws.amazon.com/blogs/aws/amazon-kinesis-video-streams-serverless-video-ingestion-and-storage-for-vision-enabled-apps/) was a bit suprise to me at least. To be honest after initial confusion I felt really excited. Real-time analytics of the video streams allows so many new business opportunities for our customers. I can immediately come up with many solutions, which could be utilized in manufacturing and other process industries. Imagine just how easy it will be to improve quality control and other typical manufacturing processes. This is definitely a topic I need to cover more deeply later on.

### IoT
As expected AWS IoT platform received many enhancements. One of the anticipated improvements is [the release of new device management solution](https://aws.amazon.com/blogs/aws/aws-iot-device-management/). Finally there are better search and grouping functionalities for devices and even remote management including firmware updates to devices. Traditionally you have had to create your own setup utilizing S3 and other services. 

[IoT Analytics](https://aws.amazon.com/blogs/aws/aws-iot-device-management/) will ease up the work needed previously to analyse the IoT data. It seems that the IoT Analytics is designed in similar manner as Kinetics Analytics. In the beginning it seems that there are not that many options available how the messages are analyzed. It seems that you can select some attributes from the incoming messages and play around those attributes with simple calculations. 

A bit surprisingly AWS released new [operating system for microcontrollers called Amazon FreeRTOS](https://aws.amazon.com/blogs/aws/aws-iot-device-management/). It is based on open source solution FreeRTOS and is basically extending it with secure cloud connectivity capabilities. Really interesting to see how this will be used in the industry.

[Greengrass ML](https://aws.amazon.com/about-aws/whats-new/2017/11/aws-greengrass-adds-feature-for-machine-learning-inference/) allows deploying machine learning algorithms on the edge increasing the processing power closer to the devices. It will make the devices act more intelligent and also decrease the messaging volumes between edge and cloud.  


### Storage
An addition to existing S3 query capabilities AWS launched today [Glacier and S3 Select services](https://aws.amazon.com/blogs/aws/s3-glacier-select/). What they allow is programmatic access to only for subset of objects in S3 or Glacier. This way less objects are searched and less traffic is generated between S3 and other services. Data can be searched using just standard SQL as a query language. An example use case is to query data from S3 in Python program using Boto library.

![S3Select](https://d2908q01vomqb2.cloudfront.net/da4b9237bacccdf19c0760cab7aec4a8359010b0/2017/11/28/s3_select.png)

### Summary
All the new releases will be listed also in [Amazon website](https://aws.amazon.com/new/reinvent/)

