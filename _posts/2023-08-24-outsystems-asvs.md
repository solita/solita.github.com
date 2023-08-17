---
layout: post
title: MSc Thesis presentation - Low-Code and OWASP ASVS
author: Hubmara
excerpt: >
  OutSystems compliance with ASVS (OWASP Application Security Verification Standard)
tags:
 - Low-code
 - OutSystems
 - Security
 - ASVS
---

This post comprises two parts: an introduction, giving the Solita context by Martti Ala-Rantala, and the presentation of the thesis, by Sami Spets. For the published thesis, see [4].

## Introduction

Technology solutions categorized as low-code are not one and the same. Their use cases and the needs they serve are quite different. Solita is working with two low-code development platforms: Power Platform and OutSystems. This post focuses on the latter. 	

We have been investing in OutSystems technology since 2019, we are a partner, we have a sizeable pool of developers and several OutSystems projects under our collective belt. We have learned a lot about the realities and benefits of OutSystems development beyond the hype. We will share more insights on the topic in future blog posts.

An OutSystems developer writes logic and content that glues together prefabricated black box components, and boilerplate code is created automatically for, e.g., handling repeating tasks and security issues. The runtime platform also handles many tasks. This means that we must trust OutSystems’ security measures. OutSystems is committed to security and heavily invests in it.

We are working on a large-scale project for a customer with exceedingly strict security requirements, including OWASP ASVS Level 2 compliance. ASVS stands for Application Security Verification Standard [1].

OutSystems had no material regarding ASVS compliance, and trawling the Internet didn't pull any useful material either. Therefore we decided to propose the topic for an MSc thesis project. Sami Spets of University of Turku accepted the challenge and wrote a thesis titled *Application Security Verification Standard Analysis of Low Code Development Platform*.

Emilia Pitkänen, a security expert at Solita, says:

>“The results of the thesis were used as supportive material and finally as proof of ASVS Level 2 compliance in the project. The categorization developed by Sami was used as a baseline for creating secure development guidelines and instructions on how to utilize OutSystems' security features most effectively. The remaining requirements were specific to OutSystems, so they were verified with OutSystems. 

> The combination of OutSystems' answers, development guidelines, and Sami's thesis provided verified compliance level for the customer."

We want to thank Sami for the good work he did with the challenging topic!

## Thesis Research Process

The literature review conducted as the first step of the thesis work revealed that there is scarce research on low-code platforms and their security. Therefore, a novel method for assessing ASVS compliance was developed. Two decision trees were created, one for each of the two ASVS levels. See Figures 1 and 2 below.

![Figure 1](ASVSLevel1.png)

Figure 1

![Figure 2](ASVSLevel2.png)

Figure 2

Level 1 defines the minimum requirements for all applications. The decision tree has five outcomes, corresponding to compliance levels (CLs) from 1 to 4. A requirement is considered unfulfilled if it is classified as CL3 or CL4. There is also an outcome called Developer Action (DA). It is an edge case for handful of requirements, mostly related to GDPR. It indicates that the requirement is not applicable to OutSystems and is the developer’s responsibility.

Level 2 contains more requirements that require the developer’s action. It specifies the minimum security level for a business application, which is the focus of the thesis. Some requirements are implemented by the organization that uses OutSystems, but are not related to OutSystems. To accommodate the differences to Level 1 requirements, a slightly modified decision tree was used. The results show the responsibilites or relevance to both OutSystems and Developer, separated by a slash. For example, "Yes/DA" means that OutSystems supports the requiremend but also developer action is needed. Only "No/DA" indicates failure.

ASVS also has level 3 for critical infrastructure, but that was beyond the scope of the thesis.

## Thesis Research Results

The results show that OutSystems is mostly compliant with ASVS Levels 1 and 2. Out of the 129 Level 1 requirements, only 24 failed, with 15 in the “Validation, sanitization, and encoding” category. The high number of unfulfilled requirements does not imply poor security. They are related to business logic and coding practices.

For the other failed Level 1 requirements, suitable and unofficially trusted ready-made modules were found. OutSystems could make them trusted modules to meet the related requirements.

Level 2 has 126 requirements, of which only seven were unfulfilled. Four of these requirements could be resolved by making an unofficially trusted module trusted and one module needs some improvement. The remaining two unfulfilled requirements need an external system to fulfill them.

Most of the issues in Level 2 belong to the “Authentication” category. The main issue there is the absence of 2-Factor Authentication. Making the suggested modules officially trusted would also address most of the unfulfilled requirements in ASVS Level 2. However, two requirements related to key vaults need a custom solution from the developer. The last unfulfilled requirement in Level 2 concerns the number of iterations used in PBKDF2 algorithm. ASVS recommends using at least 100 000 iterations, but OutSystems uses less in their CryptoAPI. This should be easy for them to fix.

The direct impact of the results can be seen in how Solita will use OutSystems in future projects. Solita can directly reference the results in procurements and in software development.


## Developments After Submitting the Thesis

1.	At the time of writing, OutSystems had no AD nor TFA authentication for IT users (those in various software development roles). This has now been fixed: a beta solution for using AD authentication for IT users became available in August 2022.
2.	Low-code version of OWASP 10 has been published, see [2].
3.	OutSystems has also written about how OutSystems helps in addressing OWASP 10 vulnerablities, see [3].

## References

[1] [https://owasp.org/www-project-application-security-verification-standard/](https://owasp.org/www-project-application-security-verification-standard/)

[2] [(https://owasp.org/www-project-top-10-low-code-no-code-security-risks/](https://owasp.org/www-project-top-10-low-code-no-code-security-risks/)

[3] [https://success.outsystems.com/support/security/develop_secure_outsystems_apps/how_outsystems_helps_you_address_owasp_top_10/](https://success.outsystems.com/support/security/develop_secure_outsystems_apps/how_outsystems_helps_you_address_owasp_top_10/) 

[4] [https://www.utupub.fi/bitstream/handle/10024/173528/Spets_Sami_DI.pdf](https://www.utupub.fi/bitstream/handle/10024/173528/Spets_Sami_DI.pdf).

