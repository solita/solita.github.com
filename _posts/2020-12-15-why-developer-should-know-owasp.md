---
layout: post
title: Why a developer should know OWASP?
author: riikkanen
excerpt: OWASP stands for Open Web Application Security Project. Why should I be interested in OWASP as a developer? If I'm not a hacker or cybersecurity specialist, and we don't even handle any sensitive information in our project, can I just skip the OWASP? Well, the answer is "nope".
tags: 
- security
- developers
---

[OWASP](https://owasp.org/) stands for Open Web Application Security Project. Why should I be interested in OWASP as a developer? If I'm not a hacker or cybersecurity specialist, and we don't even handle any sensitive information in our project, can I just skip the OWASP? Well, the answer is "nope".

# Different projects, different requirements

If you think about a big patient information system used in hospitals, it is obvious that information security must be concerned in every phase of building such a system: in planning, implementation, and testing. The system contains sensitive data, e.g., social security numbers, and personal medical reports. In addition to the valuable content, the system might interest hackers because it most likely has integrations to other critical information systems. The patient information system must have restricted access, strong authentication, audit logging, and whatnot. You might rightfully presume that the project team includes also hard-boiled information security professionals.

![Information security](/img/why-owasp/hacker-1944688_640.jpg)

How about a web store? It differs from a patient information system because it's by default available to everyone. However, also the web store contains information that must be protected: the customer information, accounts, credit card information, purchase history, and so on. It would also be nice if the purchase event is secure and reliable. If one thinks about big web stores like Amazon, one can predict that information security is tightly entwined in building the whole system. On the contrary, we cannot be so sure about smaller web stores. Are the building blocks of the store widely used and acknowledged or has someone coded, for example, authentication by themselves?

Finally, let's think about implementing a simple feedback form to an existing website. Well, implementing a simple feedback form sounds quite an easy and straightforward task and it might look like we don't need to consider information security at all. However, a simple feedback form can provide a way for a hacker to harm other parts of the system, for example, by using an SQL injection. The form can also tempt spam bots, either filling your database (and site) with numerous falsy feedbacks or misusing the form to relay email spam messages to others. Furthermore, if we collect the usernames, phone numbers, and hometown, it quickly becomes a person registry, where the data must be protected. In such cases, the developers need to familiarize also with [GDPR](https://gdpr-info.eu/) (General Data Protection Regulation).

# All software projects are also information security projects

As we can see, information security must be considered in software projects of any size. Also, information security is something you can't just add to the top of the software afterwards. It must be taken into account from the beginning, already in the planning phase. The baseline of information security should be something you can just rely on. Just as you expect to get the software of good quality, you should get secure software.

Of course, there are software projects where the baseline of the information security must be higher, and achieving that level costs more money. However, I like to think that implementing basic things in securely does not increase costs. If you decide to do, for example, SQL queries in a way where SQL injection is impossible from the beginning, it takes as much time as making them less securely. The costs increase only if you first make them less securely, and then in a more secure way afterwards.

![Bobby Tables we call him](/img/why-owasp/exploits_of_a_mom.png)

*Bobby Tables we call him, a classic from [https://xkcd.com/327/](https://xkcd.com/327/)*

In a software project, the possible risks must be examined carefully, and sufficient security level needs to be decided. If the information system is going to be used in a restricted network by a certain number of users, you might not need the same amount of security as in open banking systems. However, it is a decision which needs to be done knowingly. 

# Where the information security comes from?

The information security in a project comes from people. Depending on the project there might be some security specialists but all the people involved in the project need to be aware of security issues.

One security aspect is the practises used in the project. Do people behave securely? When working on a project, you can't tell everyone about it, at least not on a detailed level. You must not keep your passwords on post-its, you should always use good passwords, perhaps utilize a password manager, and enable multi-factor authentication whenever it's possible. Do not push sensitive data, such as database passwords, to version control. Use a VPN instead of unprotected WLANs. Recognize if the risk is bearable before pasting project-specific things into third-party services, like Pastebin, XML validator or some language translator. After all that, the other aspect is being aware of different security threats which exist in a digital environment. 

![Passwords on post-its](/img/why-owasp/passwords.jpg)

The developers are basically problem solvers. We need to solve a problem which is given to us. Sometimes the problem is easy and simple to solve. However, just solving the problem might not be enough. For example, a testing specialist might find a bug from the implementation in seconds. They have a different point of view and typically try all the nasty corner cases. Does this work with empty input? Or with negative numbers? If the developers are experienced, they have been already taken care of all those corner cases. Also, hackers have a different point of view. They are used to finding vulnerabilities from the software. To be able to secure the software, also the developers must be aware of the possible threats. 

# This is where OWASP comes in

The developers should be aware of the threats, but how. One way is to familiarize with the [OWASP](https://owasp.org/) material. OWASP stands for Open Web Application Security Project, and it has produced a significant amount of material of most common information security vulnerabilities and published on the internet. There are several detailed examples and also a web store for trying vulnerabilities in action by yourself. If you are aware of [OWASP Top 10](https://owasp.org/www-project-top-ten/) vulnerabilities, understand those and know how to prevent them from happening, the software you're building is already quite secure. Besides OWASP there are also other lists or sources, for example, CWE (Common Weakness Enumeration) provides [the top 25 most dangerous software weaknesses](https://cwe.mitre.org/top25/archive/2020/2020_cwe_top25.html).

Of course, you don't have to have all the knowledge by yourself. The main point is to recognize that there might be some spots in your software where the information security issues should be thought more carefully. You can collect information by yourself, ask teammates or an information security specialist. The implementations concerning high-risk spots should at least be reviewed by someone with more experience on security issues. Developing your competence in information security helps to notice the possible pitfalls.

Test automation can also be utilized here. There are several commercial and open-source vulnerability scanning tools available. These tools can be integrated into the CI/CD pipeline and with the help of those, you can actively monitor the information security level of your software. The vulnerability scanners point out the places where some hardening is needed. Also, the tools can be used to list outdated and vulnerable third-party libraries used in the project, so they can be updated to more secure versions if available.

# Tighten your foil hats

Being an information security oriented developer requires a suspicious mind. Never trust anyone is good advice for a software developer. Always assume that the user might have something bad in mind. Don't trust any data coming directly from a user.

![Onions have layers](/img/why-owasp/layers.jpg)

Information security is about layers. Do not trust only validation on the user interface, validate data also on the server level. It is quite usual that a quite harmful looking vulnerability is enough for a hacker to provide a backdoor to the system. When in the system, it is easier to find more vulnerabilities and dig deeper. Onions have layers, [ogres have layers](https://www.youtube.com/watch?v=-FtCTW2rVFM) and also information security should have layers to protect the valuable system and its contents.

Tighten your foil hats, fellows, and read your OWASP!


Pointers to more detailed information:

- [OWASP](https://owasp.org/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Juice Shop for trying out](https://owasp.org/www-project-juice-shop/)
- [CWE Top 25 Most Dangerous Software Weaknesses](https://cwe.mitre.org/top25/archive/2020/2020_cwe_top25.html)
- [GDPR (General Data Protection Regulation)](https://gdpr-info.eu/)

*This blog post was inspired by the speech I gave about developers and OWASP in Solita's Dev Meetup in Lahti in March 2019.*
