---
layout: post
title: Mastering AWS Kinesis Data Streams, Part 2
author: anahitpo
excerpt: >
  By now we have gone in quite some details when it comes to writing your dat to a Kinesis stream. How about making use of that data, aka reading it from a stream?
tags:
- AWS
- Data streaming
- Lambda
- Serverless
- Best practices
---

DO NOT MERGE YET!!! :)


This is the second part of the post about AWS _Kinesis Data Streams_. Part 1 is [here](https://dev.solita.fi/2020/05/28/kinesis-streams-part-1.html).


# Reading from a Stream

So, you have successfully written your valuable data to the stream, using all the tips from the Part 1 (link). What's next?

## All these consumers
As with writing to a stream, there are a bunch of ways to read data from a stream. But first, let’s make a short detour.

**TODO**: img of detour

Kinesis family has two more extremely useful services for working with streaming data:
- _Kinesis Data Firehose_, which is meant to load data to a destination with plenty of them to chose from (think _S3_, _Redshift_, even HTTP endpoints), and
- _Kinesis Data Analytics_, which can run queries on your streaming data in near real-time. 

I won't be going into details of those services here, each of them deserves a blogpost (or two 😉). I will just say that both, _Kinesis Firehose_ and _Kinesis Data Analytics_ can be used as stream consumers, providing you with out of the box possibilities to analyse the data being streamed, as well as to deliver your data to a destination of your choice. 

One of the main superpowers of _Kinesis Streams_ though is that you can attach **custom data consumers** to it to process and handle data in any way you prefer, in near real-time. There are once again plenty of options to choose from.

If u are inclined to do so, you can use an [EMR cluster as your custom consumer](https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-kinesis.html). Or, as with writing to the stream, there are a lot of third-party tools that integrate with _Kinesis Streams_. Think of possibilities like Databricks and Apache Spark integration (which actually uses KCL under the hood), among others.

On a perhaps more familiar side of things, you can have your own consumer application reading from the stream. For that purposes you can once again use either AWS SDK or _Kinesis Consumer Library (KCL)_, which is the counterpart of the _[already familiar KPL](https://dev.solita.fi/2020/05/28/kinesis-streams-part-1.html)_ and which I’ll be mentioning briefly.

And finally, you can use AWS Lambda as you stream consumer, which gives you all the scalability and resilience that comes with it. You might have already guessed that that’s exactly what I’ll be focusing on in this post.

But first, let’s lay out some ground for it.


## Consuming the stream, two ways

As with writing to a stream, when reading from it you should be aware that Kinesis stream is composed of shards (link to part1) and each shard in your stream comes with a limited throughput: you can write **1 MB or 1 000 records** of data per second, while on the way out, each shard provides up to **2 MB** of data per second. So, in theory, you can consume the stream **twice** as fast as you can write to it.


### Shared throughput

But not only that. This also means that you can actually have **at least two different consumers** reading from a same Kinesis Stream at all times. A thing to note here is that by default, the 2 MBs are **shared** between all the consumers you attach to the stream. So, if you would want to have more than recommended two to three consumers, you may face a situation when the data is being written to the stream faster than it can be read. This, in turn, may lead to some of the data expiring (aka being deleted from the stream) before any of the consumers get a chance to read it. You can think of it as a sink that u pour water into: if u do it faster than it can be drained, it ends up overflowing and u get water all over your floor. 

**TODO**: image with two lambdas

**TODO**: image of an overflowing bathtub? 🙂 

To add more gravity to the situation, both, direct integration with _Kinesis Data Analytics_ and _Kinesis Firehose_, use this shared throughput of 2MB when acting as stream consumers. So you are supposed to add just one custom consumer to the stream if you are using any of those direct integrations.

But wait: what if you r feeling greedy and want even more ways to consume your data from a single stream? Fex. you may have a firehose writing data to S3, a _Kinesis Analytics_ application doing some real-time data aggregations and then you also have a lambda function for custom processing.

**TODO**: image with firehose, analytics and lambda

As we established, If all of the consumers are sharing the throughput of 2MB, they might start lagging behind the stream and you may end up loosing your data. But worry not! There is one more way to consume your stream and it’s called **enhanced fan-out**.

**TODO**: Standard iterator


### Enhanced Fan-out

Instead of sharing  the throughput of 2MB per second per shard with other consumers, enhanced fan-out is an “elite” way to read from the stream, where each custom consumer will have its own dedicated throughput of up to 2MB per second per shard. In fact, as of today, you can have up to 20 (link) such “elite” consumers attached to as single stream! 

Though the direct integrations with EMR, Firehose or Analytics can only used the shared throughput, the great news is, you can use the enhanced fan-out with your custom consumers. With consumer application using KCL, you can simply configure it to use the [enhanced fan-out](https://docs.aws.amazon.com/streams/latest/dev/enhanced-consumers.html). With both, custom consumers using AWS SDK and AWS Lambda, you need to create a so-called **enhanced stream consumer** first. I know, naming becomes confusing here, but bear with me..

You can think of an enhanced consumer for lambda (and SDK) applications just as of an isolated connection to your stream, sort of a private highway of yours.

**TODO**: image?

All it takes to create an enhanced consumer that Lambda or SDK applications can use is a simple API call. Though apparently there's no way to register an enhanced consumer through the console (if you find one, let me know!), in addition to the API call, you can use e.g. CloudFormation, SAM or  AWS CLI for that:

```aws kinesis register-stream-consumer --consumer-name my_highway --stream-arn arn:aws:kinesis:<region>:<account_id>:stream/the-best-stream```

After that the consumer will be visible in the AWS console and you can delete it from there later, if you want to.

**TODO**: screenshot of a stream consumer in console

But it’s not just the dedicated throughput that you r getting with the enhanced fan-out. Together with it comes even less read propagation latency, aka the time between when the data is written to the stream and when it is ready to be consumed. This is in part due to the dedicated throughput “highway" each consumer gets, and in part to the fact that enhanced fan-out uses HTTP2 instead of HTTP, allowing to have persistent connections and to push records to the client, instead of clients polling for them. On average, you will have records available to read 70ms after you wrote them to the stream, vs 200ms in case of the shared throughput consumers, that actually slows down with each additional consumer.

By now, you might be thinking, why would anyone event use the standard shared throughput? Well, you might have guessed the answer. While the standard shared throughput consumers read the data for free, you will have to pay for having all the perks of the enhanced fan-out. You will [pay for both](https://aws.amazon.com/kinesis/data-streams/pricing/), the amount of data consumed, as well as for the number of consumers per shard. So, your highway actually ended up being a toll road..



## Few words on KCL

Before we finally move to the lambda functions consuming kinesis streams, let’s have a word about the _Kinesis Consumer Library_, or _KCL_ for short.

Just like KPL, the _[Kinesis Producer Library](https://dev.solita.fi/2020/05/28/kinesis-streams-part-1.html#Few%20words%20on%20KPL)_, KCL adds another layer of abstraction over _Kinesis_ API calls and is meant for reading data from the stream, not managing the stream itself. While the situation with supported languages is a bit better than with KPL, where you only have one option of Java, if you want to use other languages for your application, you still need a separate Java-based daemon running in the background at all times.

An interesting detail that should be taken into the consideration when using the KCL is that it use a DynamoDb table to keep track of the shards and to "know" where in the stream to read from at any given moment. The _DynamoDb_ table is created automatically when starting up your KCL application and it has a throughput of [10 reads and writes per second](https://docs.aws.amazon.com/streams/latest/dev/shared-throughput-kcl-consumers.html). Naturally, you will be charged for that table.

There is also another gocha here: if you add more shards to your stream (with the autoscaling solution you build, or by hand, to accommodate the increased amount of data), you are running a high risk of exceeding DynamoDb table's throughput. This might take you by surprise while u didn't even create any tables in the first place! Once you know it's there, you can add more capacity to the table when that happens, either by hand (through console or API calls), or you could have a lambda function, which is triggered by re-sharding and adding the capacity "automatically”.



# Lambda

Let’s finally talk about lambda!

When using a Lambda function as a stream consumer, **Lambda service** takes care of a lot of heavylifting on your behalf and behind the scene. It will fex. keep track of all the open shards in the stream and of where exactyl in the stream and each given shard are you reading from at any given time (remember that, unlike fex. SQS, a kinesis stream retains your data even after it has been read, so consumer needs know which records to read next). It will also handle errors and retries, and here, once again, you need to pay close attention and know exactly what's happening.


## The magic of ESM

First, let’s look a bit deeper into how lambda actually works with _Kinesis Streams_. Right from the start, we need to make a clear distinction between the lambda **service** and a lambda **function**. While lambda function is what you mostly deal with, the actual function instance being invoked, Lambda service is what does all the magic behind the scene and makes it so powerful. An essential and often overlooked part of the lambda service is the **event source mapping**, or the **[ESM](https://docs.aws.amazon.com/lambda/latest/dg/invocation-eventsourcemapping.html)**. 

When attaching a lambda function to a stream, you are actually attaching an event source mapping and pointing your lambda function to it. The ESM will read batches of records from the stream and invoke you lambda function for you. In scenarios when there is no ESM involved and the lambda is triggered directly (fex. with an _SNS_ or _CW_ triggers), there can be **no batching**. So, ESM is your invisible magical ingredient that is behind all that we are going to discuss next.

**TODO**: my own image of the ESM


### Batches and windows

As discussed before, each shard in a Kinesis stream can be thought of as a separate queue, each with its own throughput limits. So, it shouldn’t come as a surprise that when you want to consume your stream with a lambda function, each shard will be processed separately. There will be **separate concurrent lambda invocations** that will each read from a dedicated shard. So, by default, you will have as many concurrent lambda invocations reading from your stream as you have shards.

![kinesis](/img/kinesis/kinesis.png){: .img.centered }

With the help of the ESM, each invocation of your lambda function gets a batch of records from a single shard. You can choose what sizes of batches you want to process, specifying the **batch size** (from **1 to 10 000** records per batch) and how often do you want to process them, specifying the **batch window** (from **1 sec and up to 5 min**).

The event source mapping will diligently collect records from a specific shard to a batch until one of the three things happen:
- your desired batch size is achieved
- your desired time window has passed or
- the batch gets so big that it reaches Lambda’s own universal **payload limit of 6MB**
After that it will **synchronously** invoke your lambda function with the batch it has collected.

Here’s what the input of a single lambda function may look like:

**TODO**: screenshot of the event?

If you have a relatively low throughput stream, it makes sense to use a larger batch window than the default 1 second, while the time will probably not be enough to collect the entire batch and you will trigger your lambda function more often than it’s needed.


### Error Handling

Event source mapping also takes care of handling possible errors related to retrieving batches from the stream itself behind the scene. But what happens if an error happens while processing the batch of records in the lambda function itself?

By default, lambda will try to process the batch until it succeeds or until the data in the batch expires. As we have learned (link to part 1), by default the data in a Kinesis stream expires in 24 hours, so in a worst case scenario, lambda will be retrying the “bad” batch for 24 hours, causing extensive number of fruitless lambda invocations, until the data finally expires and is removed from the stream. You end up losing an entire batch of valuable data, even if there was just one “bad” record causing the problem.

But bad things don’t stop there, quite the contrary.

The thing is, while lambda keeps retrying that one unfortunate batch from a shard, no other batches are being read from that shard. This, of course, is a reasonable thing to do while otherwise _Kinesis_ wouldn’t be able to guarantee ordering of records within a shard. However, it means that because of just one “bad” record, your entire shard is now stuck, while the rest of the shards in your stream go on with their lives. That’s why that “bad” record is often referred to as a **poison pill**.

![this_is_fine](/img/kinesis/this_is_fine.jpg){: .img.centered }


In our scenario, in 24 hours the poison pill finally leaves the shard, together with other records that were unfortunate enough to end up in the same batch. But at that moment when lambda can finally start taking in new batches, the shard can be filled with records that were written to the stream around the same time. This, in turn, means that they expire around the same time that the already discarded batch. So u may end up in a situation, when lambda just doesn’t have enough time to catch with the shard and records will just keep on falling off the edge of the stream, so to speak (remember our overflowing sink analogy?). And though we started off with just one bad record which cannot be processed, we ended up losing a lot of valid and valuable data. All this because of not having **proper error handling**.


The good news is, there are several ways to mitigate these kind of situations. First and foremost, you should decide how to proceed with those “bad” records. After that you could implement proper error handling in your lambda function not to let the entire function to fail because of of some “bad" records in a batch. Or, you could use the possibilities that are provided for you out of the box by the Lambda service and the ESM:
- set the maximum number of **retry attempts** (max 10 000)
- set the maximum **age of the record** that will be retried, to ignore older ones (from 1 minute up to 7 days)
- tell lambda to recursively **split** the “bad” batch and try to process the halves separately (also called bisecting), and finally
- set an **on-failure destination** (_SQS_ or _SNS_) for the records that cannot be processed after all the retries. Lambda will not send to the destination the failed records themselves, but the metadata that includes the positions of the records in the stream. In that way you can retrieve the records from the stream at any time later, as long as they don’t expire.

One thing to note here is that you can not use lambda’s own DLQ, because it can only be used with **asynchronous** lambda invocations. Instead you need to configure the on-failure destination and other error handling settings for the event source mapping you are using.


### Parallelization Factor

What if you have a high throughput stream and your lambda just can’t keep up with the amount of data that comes in? Because there is a separate lambda invocation associated with each shard, one way to increase the processing speed is by adding more shards to the stream. Each new shard comes with one more lambda to process the data. However, as we know, each shard will cost you money. Resharding is also an operation that takes time and has its own [limits](https://docs.aws.amazon.com/kinesis/latest/APIReference/API_UpdateShardCount.html).

Instead of adding more shards to your stream, you can actually add **more lambda functions** to read from each shard. This is called **parallelisation factor** and you can have up to 10 concurrent lambda executions per each shard in your stream.

![stream_parallelization](/img/kinesis/kinesis_parllelization.png){: .img.centered }

When you write data to the stream, it is distributed between the existing shards based on the partition key. This guarantees ordering of records within a single shard. Similarly, when using a parallelisation factor, batches the event source mapping receives from each shard are once again split based on the partition key into smaller batches and distributed between “parallelized” shards. So, you can have up to 10 such sub-shards each with its own lambda function attached to it. Because you parallelise the processing for each shard, this time the ordering will be guaranteed on the level of **individual partition keys**, not the entire shard.

**TODO**: img


It’s also worth mentioning, that to fully utilise all the parallel lambdas, you must have enough distinct partition keys in each shard.

[Here](https://aws.amazon.com/blogs/compute/new-aws-lambda-scaling-controls-for-kinesis-and-dynamodb-event-sources/) is an excellent article about how the parallelisation factor actually works with _Kinesis Streams_.


## Shared throughput vs enhanced fan-out

As described before, when you want to consume a Kinesis Stream with a Lambda function, you can choose to either use the free shared throughput of 2MB with somewhat slower (though still quite impressive) read propagation, or the payed enhanced fan-out with a dedicated 2MB bandwidth and an even more impressive and steady read propagation. Let’s compare how lambda service behaves in both these scenarios.

When you have a lambda event source mapping pointing at your stream, it either **polls** the records from each shard for you using the `getRecords` API at a base rate of one call per second per shard (_shared throughput_), or the events are **pushed** to it through a dedicated long-lived HTTP2 connection (_enhanced fan-out_). After that it all looks the same for you lambda function, it just gets invoked with a batch of records and doesn’t car how that batch got there.

Let’s take a closer look at the shared throughput model, also known as the standard iterator.

**TODO**: own version of this


Though the getRecords API calls r hidden behind the magical ESM, there are some important [limits](https://docs.aws.amazon.com/streams/latest/dev/service-sizes-and-limits.html) to be aware of. You can have at most **5 `getRecords` calls** within one second and each call can return at most **10 000 records** or **10 MB** from your stream. It's worth noting that the getRecords call can actually return 5 times more data than the **2MB** shard limit would permit, but as a result, all the subsequent calls within the next 5 seconds will fail.

All these means, that while technically there’s not limit to how many lambda functions you can attach to a single stream while using the standard iterator, in reality the 2MB throughput limit means that you might start getting behind your stream if u have more than 2 consumers, and the 5 `getRecords` call limit means, that you can have at most 5 consumers before they start to get throttled. In both cases you may start seeing _ReadProvisionedThroughputExceeded_ in your CW metrics. Though event source mapping will take care of retries behind the scenes  when this happens, this will slow down the stream processing even further and will be reflected in the _IteratorAge_ metrics.

So, one way or another, if you need to have more than 2-3 applications reading from your stream, enhanced fan-out is the way to go. This will give you up to 20 lambdas with a dedicated throughput. Moreover, you can use both enhanced fan-out and shared throughput for the same stream, which adds another 2-3 lambdas that share the bandwidth. Of course, all the consumers don’t have to be lambdas, you can also mix and match different types of consumers.


## Lambda concurrency limit

Word of caution:
One last, but by far not the least thing to note about lambda, and this one is once again about the limits (because let’s face it, there r always limits 🙂). Concurrent lambda executions is a [limited resource](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html). By default, you can only have up to 1 000 concurrent lambda executions in the same region. And though it’s a soft limit that you can increase, there still is going to be a limit. And once that limit is reached, all the new lambda executions in the same account will be throttled.

In case of lambda function as a stream consumer, there might be up to 10 times as many concurrent lambda executions as you have shards in the stream with just one consumer application. Imagine having a stream with 100 shards and a parallelisation factor of 10, and you will have 1 000 lambda executions polling your stream at all times. This means that some of your business critical lambda functions might stop working because your stream consumer takes up all of the lambda "budget" for the account/region.



# Conclusions

TODO

----

TODO

Done! yahoo!
