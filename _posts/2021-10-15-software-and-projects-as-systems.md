---
layout: post
title: Software Engineering and everything related - Software and Project as systems
author: tommi.kenakkala
excerpt: Have you ever wondered why a change to software produces unexpected results? Taking a system theory flavored view might help software developers. Read on to find out more!
tags:
  - Software engineering
  - Project management
  - Ways of working
  - System Theory
---

## Foreword

Have you ever wondered why a change to software produces unexpected results?

Software designers build systems.

Taking a system theory flavored view might help. Following highlights may help especially fresh software developers to see the big picture around them in software projects.

Read on to find out more!

## System

[System](https://en.wikipedia.org/wiki/System) is a set of things working together.

- Systems are composed of other systems
  - Examples
    - a bridge
    - the Solar System (it's in the name after all!)
    - software, its operating environment and people operating it
- Software systems are produced by other systems
  - Examples
    - software project
    - team
    - organization

## Change

A change is something which alters the structure or state of a **system**.

A change may take the system a step towards a desired state or away from it.

One can argue that the whole **art of software engineering simply produces changes to systems**.

There are no features, bugs, change requests or whatnot. They are all equally and simply changes to a specific system. The change in the behavior or state of that system in turn affects other systems.

A software engineering change may implement, alter or remove a feature, fix a problem, create or alter documentation and so forth. A change is _any difference_ to previous structure, functionality or state of a deliverable (see ["Project"](#project) section) which is part of the end system.

We are distracted because we tend to value a change more if it has a fancy name. However, a change of "lesser nature" may have just as big of an impact as some "important change".

Changes to the system often have unpredicted consequences because systems quickly grow in complexity past human comprehension.

- For example, let's say an automated procedure composes documentation by reading a readme file. The procedure could run into trouble due to a simple change in the file. This in turn could lead to a problem with the software delivery system because of missing or incorrect documentation or if building the software fails. This way an innocent one-character change to a readme file may lead to problems for future software developers developing the system or to users or IT specialists who would use the documentation.

## The Produced System

![Time machine DeLorean](/img/software-and-project-as-systems/BTTF_DeLorean_Time_Machine-OtoGodfrey.com-JMortonPhoto.com-07.jpg "Time machine DeLorean")
([Image source](#image-sources))

The system produced by software developers, in the form of a service or a product, does not exist in isolation. The technical system lives in symbiosis with

- The human actors interacting with the system
- The environment system is operated in

Human interaction happens, for example, by using the technical system (by users) or by operating the technical system (by IT specialists).

The system which software developers should consider is composed of all those.

This _[holistic](https://en.wikipedia.org/wiki/Holism)_ view inspects software as part of the whole environment instead of in isolation.
If inspected alone without its intended habitat a change to a system may present itself as insignificant.
As part of the whole it may change considerably the functionality of a project delivery or the expectations for a software project.

Reflecting on the previous, software developers should consider the following:

### What are the motivation and goals of each user role?

A key take-away here is users want to spend as little time as possible with the technical system.

Software developers should forget their own interests and peer groups if those like to fiddle with things. That's not normal :)

Software developers may be distracted from this cornerstone because the time of a developer is spent building all those shiny features. Users have their real work to do and there the specific software application is only one smallish step towards their business goal. Users do not want to spend their time learning every this 'n that about a software application.

To recap: changes to the system may have unexpected results if the business goal of each user role is not clear.

### What are the motivation and goals of IT specialists?

What level is their knowledge about the service operated?

What level is their knowledge about the business domain of the service operated?

IT specialists usually do not work full time with a specific product or service. They have a bunch of applications and services which to keep up and running somehow. Each very different and serving different business domains. Often domains which they are only superficially familiar with.

Changes to the system may have unexpected results if the IT operations are not considered. For example, does a change impact following IT operations:

- How application is configured and what is the likelihood of misconfiguration
- Logging procedures and analysis
- Version updating procedures
- Backup procedures
- Rollback procedures
- System health monitoring

and so forth depending on the enterprise.

## The Producing System

![Charlie Chaplin CC BY-SA 2.0](/img/software-and-project-as-systems/charlie-chaplin-modern-times.jpg "Charlie Chapling in a mahine in Modern times")
([Image source](#image-sources))

Systems produced by software developers, or their tool systems, are not the only systems developers are working with. Software developers themselves are part of:

- a project or a service team or several
- a higher-level organization or several

### Project

Project is an endeavor with the following attributes - also known as the project iron triangle:

- Schedule
- Budget
- Goal

An old rule is that not all three should be fixed, but that is a subject for a separate discussion.

A project produces deliveries to meet project goals.

**Deliveries** are groups of specified and approved deliverables which affect people called [stakeholders](#organization-and-stakeholders). One deliverable could be for example a software change, new software component, documentation, configuration and so on. Semantically speaking you could argue that system view changes and project management view deliverables are synonyms. In the other hand, if you prefer, you could differentiate them for example so that: a deliverable is some larger logical entity which brings business value itself and aims to meet a project goal, when a change alone might not yet bring both.

Changes to the system may have unexpected results if the project-system is not considered:

- A project has a very high risk of failing or producing waste if schedule, goals and budget are not clear and agreed by project stakeholders.
- Evaluation and approval of deliveries is difficult if goals are not clear.
- For example
  - Software developers should prioritize work differently when all mandatory goals are already met when compared to e.g. when delivery is only halfway ready.
  - It is a waste to do technical refactoring if the result won't have a long enough lifespan.
  - Software developers not aware of all stakeholders and user roles cannot reliably evaluate the impacts of changes.

The project itself may change during project execution by changing:

- the definition of the project: schedule, goals, monetary budget or personnel budget
- the expected deliverables: goals, approval criteria, operation environment like integration interfaces, hosting or data platforms and so on

### Organization and stakeholders

Implementing a change using some technical approach or another might not always seem very different from a software developer's point of view. Impacts on project stakeholders may, however, be very different. Differences might not be obvious if a developer spends only a short time in a project, if a project is a Proof of Concept (PoC) project or if the project manager is overly protective.

The following describes typical stakeholders for a software project:

- Business representatives
  - Project delivery is typically expected to affect business areas by
    - revenue changes
    - cost changes
  - Business stakeholders who don't collaborate with the project or with each other are one reason for unexpected impacts.
- End users
- IT and operating teams
  - Delivery must fit into the existing IT and software environment when it is deployed. Delivery is typically operated and maintained by a different team than the one creating it.
- User support
  - Corporate or consumer End user support
  - Business-to-business support
- Marketing
  - Internal for corporate users or external for public communications
- Training
  - End user organizations and people may require scheduling additional training or existing training content must be updated.
- Organizational entities
  - For example, the managers responsible for resources
- External or internal collaborators
  - A delivery may be a joint creation by different delivery teams or companies.
- Regulations and legal
  - Delivery may have to comply with national or international regulations. Compliancy could be ensured by collaboration with a domain expert.
  - In some domains delivery may be a pioneering pilot project whose results will affect upcoming domain standards.
- Intellectual Property Rights
  - Is delivery respecting Intellectual Property Rights (IPR) like existing patents and licensing terms?
    - A common software developer challenge is evaluating software licenses of software components and tools.
  - Will any new IPR be created for the delivery or customer organizations?
- Open-source community
  - Project may affect existing open-source projects or create new ones
  - Open-source projects affect software projects, for example if the delivery uses software components which become unreliable or not maintained.

## Final words

The everyday challenge for many software engineers is to remind themselves to take the step back and demand the big picture.

A common pitfall is when a customer or end user comes to the table with a ready solution. It is tempting to take that for granted and trust that "someone" has already asked the "what if" questions.

The presented thoughts are not groundbreaking, but hopefully a good reminder on the world where software engineers send their children...by children meaning here of course the created software.

## Further reading

- [https://en.wikipedia.org/wiki/System](https://en.wikipedia.org/wiki/System)
- [https://en.wikipedia.org/wiki/Systems_theory](https://en.wikipedia.org/wiki/Systems_theory)
- [https://en.wikipedia.org/wiki/Software_system](https://en.wikipedia.org/wiki/Software_system)
- [https://en.wikipedia.org/wiki/Holism](https://en.wikipedia.org/wiki/Holism)

---

## Image sources

- "BTTF DeLorean Time Machine-OtoGodfrey.com-JMortonPhoto.com-07.jpg" by [Oto Godfrey and Justin Morton](https://commons.wikimedia.org/w/index.php?curid=44599363) licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0?ref=ccsearch&atype=rich)
- "Charlie Chaplin" by [twm1340](https://www.flickr.com/photos/89093669@N00/1535417993) licensed under [CC BY-SA 2.0](https://creativecommons.org/licenses/by-sa/2.0/)
