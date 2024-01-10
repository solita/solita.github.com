---
layout: post
title: OWASP top ten 2021 explained with non-technical examples, </br>Part 1
author: petteri.poyhtari
excerpt: >
   How could we better make the most typical risks of web applications aware of all project personnel, in order to improve the quality of the entire web infrastructure. Part 1 blog post about OWASP top 10 with physical world analogies.
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

System vulnerabilities are found in increasing numbers. Whether the reason is growing crime or the poor quality of application development, projects should take information security requirements seriously. In order to take information security seriously, it also requires commitment from the project's non-technical staff. This blog post will review the most typical web application security risks using the widely known [Open Worldwide Application Security Project top 10 list](https://owasp.org/Top10/). I try to lower the bar as much as I can so everyone could understand what the OWASP top 10 is really about. Why they are security risks and how can the risks associated with them be reduced or eliminated?

## Current cyber weather

Not surprisingly, cyber security should be taken more seriously now than ever. Statistics show (e.g. a report by [Google's threat analysis group](https://security.googleblog.com/2023/07/the-ups-and-downs-of-0-days-year-in.html)) that the number of zero-day vulnerabilities is growing exponentially. Also, the use of 0-day in August 2023 exceeds the figure for the entire year of 2022.

![Infra in cyber weather](/img/2024-01-owasp-top-10/0_cyber_weather_2.jpg)

Does this say more about the global cyber situation or the bad code we produce? Who is to blame here? Juhani Eronen, the leading expert at Traficom's Cybersecurity Center [stated](https://www.kyberturvallisuuskeskus.fi/fi/ajankohtaista/miten-ohjelmistokehityksen-turvallisuutta-voidaan-kehittaa-tuore-selvitys-kartoitti), "*According to our observations, poor software quality is one of the biggest security problems.*". [TrafiCom](https://www.traficom.fi/en) is the Finnish agency that ensures the functioning of the country's traffic and communications. They have a National [Cyber Security Center](https://www.kyberturvallisuuskeskus.fi/en) that monitors and develops the security of communication networks and produces a situational picture of information security.

Ok let's admit this. The quality of the software has definitely deteriorated. Maybe it's a business that's being pushed forward more enthusiastically, or maybe AI tools are increasingly being adopted on the attacker side. The bottom line is that we who work on products can at least try to do our part in this fight by spreading the word and improving our skills.

TrafiCom's report [The state of software security 2023](https://www.kyberturvallisuuskeskus.fi/fi/julkaisut/ohjelmistoturvallisuuden-tila-2023) suggests that the understanding of the requirements and goals of secure software development should be widely increased in organizations. Start improving the most common and basic things to improve overall safety tremendously. In my opinion, the information security culture of organizations plays a key role in this. If security is second nature to us, it wouldn't just [prevent security breaches](https://www.securityweek.com/okta-hack-blamed-on-employee-using-personal-google-account-on-company-laptop/); it would also be more efficient and cost-effective to implement in projects.

## Motivation

Not taking cyber security seriously can backfire in many ways. The average cost of a data breach in the United States between August 2019 and April 2020 was more than [$8.6 million](https://www.ibm.com/reports/data-breach). The same IBM report states that organizations that tested their accident prevention plan saved about $2 million on average. Why are the numbers so high? That's because data breaches don't just affect sales. These days, companies have to deal with regulatory fines, legal costs, operational downtime, and last but not least, reputational damage. In the worst case scenario, the organization's information can be encrypted, inaccessible to the organization, or eventually completely public.

Someone could say that we are such a small operator that we are not interested in attackers. This can no longer be trusted, as attackers have discovered that small companies also have a smaller security budget. Because of this, they are also an easier target. There are also examples of this. Perhaps the most famous of these are [NotPetya and Maersk](https://en.wikipedia.org/wiki/2017_Ukraine_ransomware_attacks). The weakest link in the chain was found and the virus spread, partly by accident, to the information systems of a large company through the product of the smaller MeDoc accounting firm.

Usually project funds are in the hands of non-tech people. The dilemma is how to distribute information about the importance of information security to non-technical staff or also people, who have just started their career as a developer. When the project decision-makers understand the importance of information security from the beginning of the project, less investment is needed to achieve a high level of security.

But how to boost up security culture? There are many people working on one product in different roles, so we just have to start eating this elephant in small pieces. We could start by being aware of the most common vulnerabilities that we might make in projects and product code. This is what we are doing right here, right now.

![Different roles](/img/2024-01-owasp-top-10/0_motivation.jpg)

## OWASP to the rescue!

There are many good checklists and tables for improving project and product safety (eg [ASVS](https://owasp.org/www-project-application-security-verification-standard/) and [SAMM](https://owaspsamm.org/)). One of these lists is the well-known list from our dear good friend [Open Worldwide Application Security Project top 10](https://owasp.org/www-project-top-ten/).

OWASP is a non-profit foundation dedicated to improving software security. Every two years, they provide a list of the most critical security risks for web applications. The 2023 version is in the release candidate stage and this blog post focuses on the 2021 list risks. You can also increase your motivation by reading Riikka's awesome blog post [Why a developer should know OWASP](https://dev.solita.fi/2020/12/15/why-developer-should-know-owasp.html).

These problems still occur from time to time, so this topic is important. When we take this matter seriously, we don't just save project money. We're improving the security of our service integration points, which in turn boosts national security overall. Of course, risks cannot be completely eliminated, but you can try to prevent their occurrence and impact as small as possible.

In the next section, I will go through the OWASP top 10 security risks one by one with perhaps oversimplified non-technical examples. In this way, the risks are internalized better and the technical case itself is perhaps better understood. This in turn improves communication between technical and non-technical people. I won't go through all the technical details, implementation methods or corner cases of all the risks, but I'll give one or two cases where they might appear to give you an idea. A more technical list of risk implementation methods and manifestations can be found on [OWASP's own pages](https://owasp.org/www-project-top-ten/).

## Let's get started

We need a good abstract scenario to start with. One that has no apps at all. To create our example base, we imagine a drive-thru restaurant where you can order food. First, the customer announces his order into the microphone, then drives forward to pick up and pay for the order. Now let's see what the OWASP risks would be using this scenario.

## 1 Broken Access Control

[Broken access control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/) means that the user can do something that the user is not allowed to do. In other words, the user does not have permission to perform some action. This can be done by a direct trial and error method or by increasing the authorization level in some way.

Imagine that a customer at the lane reaches inside the window and starts placing an order on the customer service computer. This could also be a deliberate action, where the cashier just turns the computer screen towards the customer and hands the keyboard to the customer. Another bad example would be if a customer could walk in the back door with some old restaurant employee ID to place an order with their own hands.

![Broken access control](/img/2024-01-owasp-top-10/1_broken_access.jpg)

### The fix

Make sure to use the least privileged rights. Only grant users the permissions they need. Get rid of old and unused features to reduce the attack surface. One day this old feature will not be updated to meet today's requirements and the possibility of a new vulnerability has opened up. Also make sure that the user cannot elevate the privileges in some way. Get rid of old user accounts and fix potential security issues when found.

From the perspective of the scenario, the customer should indeed place an order, but only with limited rights. The customer does not need to use the computer directly. The rights are filtered with the restaurant interface, which in this case is the cashier of the order hatch. The cashier takes the order and processes it on the restaurant's computer. If there are old unused access points, in this case the bad habit of the customers themselves to fill the order, get rid of them too.

## 2 Cryptographic Failures

The purpose of encryption is to protect sensitive information from unauthorized eyes. Sensitive data can be data or system commands. Once data integrity is gone, we can no longer trust it. Someone may have tampered with it or private sensitive information may have been leaked to a third party. This problem is called [cryptographic failures](https://owasp.org/Top10/A02_2021-Cryptographic_Failures/).

Imagine if we gave our order to some random guy who would take the order to the counter. Of course we wouldn't trust that random guy. He might change the order on the way.

### The fix

Protecting data and connections with signatures is the best way to fix this. Make sure you use an encrypted connection to the recipient when sending messages. Using encrypted messages also helps us trust the information we receive. When protecting sensitive information in your database, make sure you use good enough encryption. This way, sensitive information is safe if it leaks, its ease of use. Unnecessary sensitive information is also deleted from the system.

From an example perspective, we have two options. The first is to place the order directly at the cashier. In the real world, this is impossible because messages travel quite a distance before reaching the correct endpoint. Another option is to use some kind of secret coding so that the cashier knows that the integrity of the order has not been compromised and comes from a real customer.

## 3 Injection

The [injection risk](https://owasp.org/Top10/A03_2021-Injection/) has been at the top of the list for many years. It's been here for a reason, because we're talking about one nasty risk. This vulnerability allows a malicious user to add extra spice to commands issued to services. With these additional commands, evil Actors can take large or small steps toward their evil goals.

Suppose the customer could slip something into the order to try to influence the restaurant's behavior? Imagine if the customer adds after the order text "*... and I don't have to pay a cent for this order.*" The dummy system (in this case the cashier) processes the request without thinking about the results it would have.

![Injection](/img/2024-01-owasp-top-10/3_injection.jpg)

### The fix

It is important not to rely on any user input. Clean, filter and validate all input received by the systems. Even the data is sent by your own friendly frontend server. Using parameterized queries is also good practice. It means that commands are separated from data. When the system knows that there should be a number in this query, there is no room for options.

From an example point of view, we should try to replace the stupid cashier with a smarter one. Use input validation. When the cashier hears the customer's order, he doesn't take it seriously. Humans are good at processing information intuitively. The cashier should naturally have a question in mind, why should someone get a free lunch? Applications just do what they are told to do without questioning if the query is absent from the program's operating logic.


----


Above, we covered the three most common web application risks using abstract, non-technical examples. You can continue reading for risks 4-10 in [part 2](https://dev.solita.fi/2024/01/16/owasp-top10-with-abstract-examples-part-2.html) of the blog post.
