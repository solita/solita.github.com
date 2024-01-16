---
layout: post
title: OWASP top ten 2021 explained with non-technical examples, </br>Part 2
author: petteri.poyhtari
excerpt: >
   How could we make the most typical risks of web applications aware of all project personnel, to improve the quality of the entire web infrastructure? Part 2 blog post about OWASP top 10 with physical world analogies.
tags:
 - DevSecOps
 - InfoSec
 - OWASP
 - Quality
 - Security
 - Software security
 - Web development
---

## What is this blog about?

This is the second part of our [OWASP top 10](https://owasp.org/Top10/) explanation with non-technical examples. In [part 1](https://dev.solita.fi/2024/01/09/owasp-top10-with-abstract-examples-part-1.html) I lead into the subject why understanding the most common risks for non-technical persons is also important and explained risks from one to three. Let's continue with risks four to ten.

## 4 Insecure Design

Applications can be designed with care and safety in mind from the beginning or with the fastest possible return of investment in mind. Unfortunately, the latter mostly means that information security gives way to "more important features". [Insecure design](https://owasp.org/Top10/A04_2021-Insecure_Design/) means that security is not built in, but is added afterwards when the product is ready enough. This fails in most cases and is more expensive. Since it is more expensive to do, it is either hardly done or not done at all. For example, application layers or the network can be considered in the design. Fixing these later is expensive.

![Insecure design](/img/2024-01-owasp-top-10/4_insecure_design_3.jpg)

What if in our scenario the business owners were busy building a restaurant building. The sales window could be implemented so that the computer is at such an angle that the customer can see the screen along with other sensitive information. Another good example would be that the hatch locking mechanism is too complicated to use. As a result, employees just keep it open because they are lazy.

### The fix

Try to enable Secure Software Development Lifecycle. It means that security has moved to the left in the software development life cycle. When starting a project, think about the risks considering the project and the product. What laws and conditions must be taken into account. Test and raise issues on time, etc. Read more about SSDLC in [Joona's thorough blog post](https://dev.solita.fi/2020/04/08/secure-software-development-lifecycle.html).

In our example, business owners should know how to run a business in this kind of restaurant. They should have designed the facilities before there was brick on top of brick. Otherwise, the drive-thru does not work as a drive-thru and business stalls.

## 5 Security Misconfiguration

Most of the [security misconfigurations](https://owasp.org/Top10/A05_2021-Security_Misconfiguration/) are done by accident, but deliberately weakening protections, such as closing a firewall or leaving unnecessary network ports open, are also done on purpose. Forgetting to close unnecessary features or APIs, leaking dangerous information in error messages, using default credentials and not segmenting the network are also good examples of security mistakes.

One configuration error is when an employee forgets to lock the restaurant door when leaving the building at night. Anyone walking by could get in just by trying the handle. Or perhaps a better example is that a temporary hole has been made next to the door during the restaurant renovation. When the renovation was done, they forgot to close it. Also, what if the customer could shout orders directly to the kitchen, completely bypassing the cashier.

### The fix

As technology develops, we have more and more things to configure. Forgetting to set something up correctly is a common human error. For this reason, we should also use automated tests to detect these security configuration errors. We should also try to do things right from the start. Opening the firewall just because it's the fastest way to get things done is tempting, but the wrong move. Using default passwords in systems should also be made impossible.

If customers could shout orders directly to the kitchen while doing business, things could get messy pretty quickly. The checkout should be built in such a way that bypassing the correct user interface, the cashier, is not possible. Also, the kitchen staff must only take orders from a certain route, through the restaurant workers.

## 6 Vulnerable and Outdated Components

[Outdated components and tools](https://owasp.org/Top10/A06_2021-Vulnerable_and_Outdated_Components/) are a growing threat. Defects and information security holes are found in products at an accelerating rate these days. Products are increasingly built from various components, the safety of which we cannot fully guarantee. This leads to the difficult situation of having to keep track of what we have and what the states of those components are.

What if the lock on the restaurant door in our example was the best that money could buy in the 19th century. The company that made the lock still exists and has improved its lock systems several times in recent years. The door can be used, it looks like it's locked, but it's not. It keeps cats and toddlers away, but not much else. Another good example would be that the restaurant uses kitchen utensils that have been withdrawn because they are dangerous.

![Outdated components](/img/2024-01-owasp-top-10/6_outdated_2.jpg)

### The fix

We live in a constantly changing world, and people often make mistakes. This means we can no longer fire and forget our products. Although our product should be bulletproof, maybe some library we use is not. One solution is to monitor product and library updates and update them whenever possible. Getting rid of unused libraries and functionalities also helps a lot. It is also good practice to automate this task as part of the release pipeline. Read more of autometed security testing from [Antti's blog post](https://dev.solita.fi/2017/11/08/automated-security-testing.html).

The restaurant should somehow try to automate the maintenance procedures. They should have a list of the tools they use and some kind of communication channel to the manufacturer so that information about the tools gets to the restaurant. The inspection of locks and other equipment should also be done regularly using a checklist.

## 7 Identification and Authentication Failures

[Authentication problems](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/) revolve very strongly around the fact that a user does not have the right to do the actions that they do. Whether it happened by accident or on purpose. This could happen when the system mixes user IDs or sessions, gives too many rights to some users or fails to remove rights when needed. Also allowing brute forcing will usually lead to unauthenticated actions.

Imagine if one customer places an order, picks it up, drives away and the next customer can buy at the expense of the previous customer. It would also be problematic if one customer could repeatedly ask the cashier about the companies that have an account in the restaurant in order to get their own purchases to a company's account. If drive through customer orders are mixed, we are talking about identification failures. The mixing of purchase transactions would also be worrisome.

### The fix

In order to improve the quality of software, a secure software development life cycle should be used. Especially the test automation part in this case. Users should not be able to perform actions for which they are not authorized.

The drive through restaurant in our example should improve the process so that customers' orders are not mixed up. Authentication methods should also be used to place the order with the right customer. Cashiers should also be trained against customers who try to trick someone else into paying for their order.

## 8 Software and Data Integrity Failures

[Integrity failures](https://owasp.org/Top10/A08_2021-Software_and_Data_Integrity_Failures/) mean that we cannot fully trust the data, library or software we have. Has someone changed the resource we're loading or the libraries we're using? What about our own source code? Is the data intact and not manipulated somehow? Have our secrets been revealed to users, perhaps through serialization errors?

Let's imagine that the order process works internally with pieces of paper. If the kitchen doesn't pay attention to the origin of the order papers, someone can slip the order under the kitchen door and write on the order that the food should be delivered through the back door, no questions asked. Another breach of integrity would be if the cashier blurted out all the restaurant's secrets to the customer, whether they asked or not.

### The fix

We should somehow try to raise the trust factor of our data and libraries. We could scan the products we use for common vulnerabilities and fix them when patches are available. We should also enforce digital signatures to ensure that updated information and code are only installed from trusted sources.

In our example, shaking up the cash register and kitchen staff would be in place. They shouldn't rely on random order notes in the kitchen. especially if they are found in suspicious places like the floor. Also, the cashier should not leak or overflow information to a random customer, but stick strictly to taking orders.


## 9 Security Logging and Monitoring Failures

When we don't have a complete view of what is happening in our application, then we have a [logging and monitoring risk](https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/) at hand. Without good logging and monitoring, we use our software more or less blindly. How do we find out about unauthorized access or that our software is down due to a traffic spike? It's also pointless to produce errors that no one can use or understand.

Let's assume that our restaurant would not properly monitor what is happening. They do not have cameras in the driving lane and the purchase transaction is monitored only with the minimum amount required by law. The restaurant would have great difficulty in monitoring which products are sold and developing its business accordingly. There would also be a lack of communication. For example, if the kitchen makes a mistake and prepares the wrong product, the cashier just shouts "ERROR" without saying what went wrong.

### The fix

When we use our services and applications, we should have a good view of how they work and who uses them with what rights. Tracking should be used to provide insight into the status of our services. Is it healthy, struggling or down. Logging can be also used to detect strange anomalies and suspicious user actions.

![Logging and monitoring](/img/2024-01-owasp-top-10/9_logging.jpg)

Surveillance cameras should be added to the driving lane to detect vandalism and abuse. Purchase transactions should also be recorded at a level that enables the daily business to be run. Not just to the level required by law. The cash register should also increase communication with the kitchen so that possible errors are understood and corrective measures are implemented.

## 10 Server-Side Request Forgery

[Server-side request forgery](https://owasp.org/Top10/A10_2021-Server-Side_Request_Forgery_%28SSRF%29/) (SSRF) occurs when the server fails to validate the user-supplied URL to an external resource. A bad request can go to some third-party service or local file system with extended permissions.

Assume that the customer could somehow change the behavior of the kitchen staff when making a regular order. If the kitchen staff blindly follows the order, they could be told to pick up the ordered steak from the more expensive restaurant next door. The steak is then paid for cheaper and the restaurant loses money. It would also be bad if a customer in the driving lane directs the payment request to the next customer in line and speeds away.

### The fix

The server must sanitize all input, perhaps use whitelists for secure connections, should not send raw responses to clients (may contain something useful to attacker), and use firewall rules to prevent unintended connections. This should give us better control over what the user is doing.

In our example scenario, the restaurant's kitchen staff must confirm the request made to the kitchen. If a steak was requested from the restaurant next door, the request should set off alarm bells in the heads of the kitchen staff. Regarding the redirection of the payment request. The cashier does not have to accept the current customer's comment "the next customer in line pays".

## Conclusion

Thank you for reading this blog post. The topic is important and will never go away. Although technical fixes themselves are a practical way to raise the level of information security, the best fix right now is to improve the information security culture of organizations. This ultimately leads to improved security at all levels.

If we understand the most common risks of web applications and projects overall, we have a better chance of fixing them in time. Fixing them in time also means saving money. Once the risks mentioned above are minimized, we can focus more [on other growing problems](https://yle.fi/a/74-20065352) such as phishing.

Phishing is a huge problem, and it keeps getting worse because of new large language model tools. Did you know that [there has been 1265% increase of malicious phishing emails](https://www.cnbc.com/2023/11/28/ai-like-chatgpt-is-creating-huge-increase-in-malicious-phishing-email.html) since fourth quarter of 2022? Phishing is still a good attack vector, because it is so effective. 

Don't cut corners. Neglecting data security will hit harder later. Someone may think that the damage caused by a breach can be avoided only by paying the fines received for it. However, it is worth remembering that a data breach can affect more than just the company’s business. For example, in [Vastaamo's data breach](https://en.wikipedia.org/wiki/Vastaamo_data_breach), customers' really sensitive data became public knowledge, and people lost trust in information systems, perhaps forever.