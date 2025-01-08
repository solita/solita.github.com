---
layout: post
title: Edge computing, some ways to make it happen
author: msasurinen
excerpt: >
  Running workloads on the edge is a tricky business. You need to solve problems regarding device authentication, reliable deployments, monitoring and messaging. Luckily there are tools to help with these things, actually there are a lot of tools to help you. In this blog post I go over some of them. I have stuck with services from AWS and Azure, mainly because these can be used for a quite broad set of use
  cases (they are not specific for a certain automation system or domain for that matter) but also, many companies already have some operations in of these, so they sit nicely to their technological landscape. 
 
tags:
 - Edge computing
 - IoT
 - Intelligent Devices 
---
# Getting things connected 
In the last blog I introduced the concept of edge computing and outlined its benefits. In this blog post I want to go over the some of the enabling technologies, focusing on how your trusted cloud providers could help us in this matter.

Getting the devices connected to our cloud environment is usually the first step in integrating the edge into our system, or atleast its often a neccessary step. For this function the go to Azure resource is **Azure IoT Hub**. 
IoT Hub is a managed service that handles messaging and device management. Incoming messages can be enriched with metadata and relayed to other Azure services quite easily. 
It also gives your devices an identity in your cloud, it includes a device identity registry where you create identities for your IoT devices. Authentication is done via SAS tokens or X.509 certificates, with the latter being more secure but requiring the device to securely store the private key. 
Once provisioned, devices can send and receive messages. In this context cloud-to-device (C2D) messages are called direct methods, which are synchronous calls to methods defined on the device, say setting a temperature threshold.
IoT Hub also provides a device twin, which is a JSON document with metadata (like last connection timestamp), desired properties, and reported properties. 
This acts as another way to set device parameters like the aforementioned temperature thresholds. The device will receive updates when the twin changes, and it can report back values that are then accessible from the IoT hub. For a code example, check out the [IoT Hub documentation.](https://learn.microsoft.com/en-us/azure/iot-hub/iot-hub-devguide-device-twins)  

These same features can be found from **AWS IoT Core** as Device Shadows and IoT jobs.

IoT Hub and IoT Core offer strong connectivity features, but they don’t provide much control over the workloads running on devices. That’s where services like **Azure IoT Edge** come in. 
It is an extension of sorts of IoT Hub. IoT Edge contains two docker containers that you set up locally. 
The first container, **edgeAgent**, monitors the local workloads and automatically downloads and launches the correct version if the deployment manifest (a JSON file in Azure) is changed. The second container, **edgeHub**, handles all communication, acting as a message broker between custom IoT edge modules, the device, the cloud, and even other edge devices (this is called the gateway pattern).
A useful feature of the edgeHub is that it allows for message retention —it can store messages locally when offline, and when the device reconnects, it sends all missed D2C messages to IoT Hub, which is a very nice out-of-the-box feature.
With this system you can run almost anything on the edge, within the limits of your hardware that is. There are ready made marketplace modules like Stream Analytics and OPC UA clients as well as modules for Azure AI services. You can also deploy custom workloads by adding some IoT edge-specific code to your app and containerizing it. 
Below is a reference architecture for running a data collection and analysis solution on the edge, for more info check this guide: [Data Storage Edge.](https://learn.microsoft.com/en-us/azure/architecture/solution-ideas/articles/data-storage-edge)
![Data storage and analysis at the edge](/img/2024-edge-computing/iot_edge.png)
*Data storage and analysis at the edge, https://learn.microsoft.com/en-us/azure/architecture/solution-ideas/articles/data-storage-edge
 
Again, AWS has a quite similar product called **AWS IoT Greengrass**. 

While IoT Edge and Greengrass are both excellent products, a word of caution. At least for IoT Edge these benefits come with the cost of a rather mediocre dev experience. Do you remember the “IoT edge-specific code” that I mentioned earlier? Yeah, that makes the application dependent on the edge runtime. Also, your CD pipelines need to do the deployments via the IoT hub and that opens another can of worms. 
You can get around these things, and Microsoft even provides an edge runtime simulator for vsCode, so you do have the possibility to run the system locally, but the system is still very much tied to IoT Hub and the edge runtime. 
I don’t have personal experience with Greengrass, perhaps it's all rainbows and sunshine with that, or maybe not. 

# What about a very big thing? 
The solutions introduced until now are dealing with devices. They can be big machines - IoT Edge was used for modernizing a forest machine at Ponsse, but still, it is a quite small system. So, what to do if you want to connect an entire factory? For this purpose, we have **Azure IoT Operations**, or AIO for short. 
This is a brand-new product that reached General availability in the last week of November 2024. 
AIO is a solution that provides robust messaging capabilities via an MQTT broker, data pipelines called dataFlows, and integrations to cloud services like Event Grid and Fabric. The whole thing is designed to be run on an Arc-enabled cluster, which makes the edge devices and services really part of your IT landscape. 
Below you see the architecture overview of the system. The devices are connected with connectors to the MQTT broker which then relays the messages to the dataflows and from there, the messages swim upstream to the cloud. As said, AIO has not been GA for that long, so real-life experiences with working with this platform are rather spars. We have at least one dev in Solita who made a POC with this while it was in preview. He described the experience as “not terrible” so there might be some potential. 

At least to my knowledge, AWS does not have any similar solution currently available.

![Architecture overview of AIO](/img/2024-edge-computing/iot_edge.png)
*Architecture overview of AIO, https://learn.microsoft.com/en-us/azure/iot-operations/overview-iot-operations

As a side note, both AWS and Azure have hardware as a service products called Outposts and Edge Stack, I'm not going to cover these in this post, but these services are designed for hybrid could scenarios.

These are some of the tools that you can use to connect your devices to the cloud as well as for edge computing. There are lots and lots of others out there, like Crosser. Crosser is a low code tool that lets you build data flows in a web portal and deploy them on locally running nodes, which you can then monitor and even debug remotely. 
Major PLC manufacturers also have their own solutions and the market is full of different kinds of platforms for different use cases. But I think this blog is quite long already, so I’m going to wrap things up here. 

# Conclusion
This post started with the need to connect devices to the cloud, which can be done using services like AWS IoT Core and Azure IoT Hub. These platforms allow secure data ingestion from a plethora of IoT devices simultaneously and support C2D messaging as well as some remote management. 
Next, we looked at enhancing messaging and integrating edge devices more tightly with the cloud by managing and monitoring workloads remotely with IoT Edge and Greengrass.
The final step in this imaginary ladder of complexity and scale is Azure IoT Operations (AIO). Not every use case is a case for Kubernetes, but when you have a factory-sized thing that you want to integrate with the cloud, this might be a valid approach, time will tell. 

Lastly, I want to highlight one thing. Moving computing to the edge will make **everything** a bit harder, not impossible but harder. For example, deployments and monitoring of your software require a bit more effort. Backing up or updating a db that sits on the edge – again not as straightforward compared to some db running as a managed service in your favourite cloud. Also, if you move some computing to a device, you will create a new run environment. So, machine A1 might have a set of configuration files, sw component versions, and physical properties that affect the system, and machines A2 to ZXW100 have their own combinations of these. This increases the complexity of the whole operation quite a bit.

If you made this far, thanks for reading. I hope you learned something!