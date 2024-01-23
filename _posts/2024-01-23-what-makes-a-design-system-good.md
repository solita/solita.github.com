---
layout: post
title: What makes a design system good?
author: harrilappalainen
excerpt: >
   A frontend developer's view on the most important aspects of a design system that provides value to its users.
tags:
 - Design System
 - Web development
 - Accessibility
---

![Concept image of designing](/img/2024-what-makes-a-design-system-good/ds.jpg)
 
A design system is a collection of guidelines, assets, and components to develop web services and native applications. They improve the performance of developers and designers as the basic building blocks and complex solutions are thought out and built for them, allowing them to focus on solving problems for their end users instead of spending time figuring out the user experience on a date picker for example and getting the user interface pixel perfect. I had the pleasure of working on <a href="https://hds.hel.fi/" target="_blank">Helsinki Design System</a>, also known as HDS and hot dog (hodari in Finnish), an open-source design system for the many web projects of the city of Helsinki. 

HDS is quite well known and respected among open-source design systems, and an award for Best Design System in the 2023 Grand One competition serves as proof of that. Design systems are especially helpful for big organizations as they supply a unified look and user experience across all their services. The HDS team consists of a product owner, a couple of designers, and a few frontend developers, some of whom rotate from a developer group that maintains and develops all the projects in the city of Helsinki. I find full-time team members valuable in gaining an in-depth understanding of the complexities of the design system, while the rotating members spread knowledge and usage of HDS components, all the while obtaining valuable insight into how the components work and what could be done better.

In this blog post I, as a frontend developer, will give my opinion on what I consider are the most important aspects of a robust design system that offers value to its users.
 
## Documentation
 
Documentation is the first place the users will flock to when they are interested in or about to use a design system. The best place for docs is a dedicated website, in my opinion, made with a framework that is easy to use and not a hassle, allowing the creators to focus on content, and not worry about the technical side of things. Good examples of frameworks are Gatsby and Next.js, which allow one to include the design system’s components in the markdown.  First off, the home page or the navigation bar should offer links to the most important parts of the design system. To figure out what are the important aspects, we need to understand the different roles of the target audience. Developers implement the components, so they need information about the components and how to get started. Designers want to look at the designs, guidelines, and patterns on how to approach different use cases such as form validation. Product owners are interested in why they should use the design system and how it would improve their product’s development on a day-to-day basis. Documentation is a benefit for the team behind the design system as well as it helps newcomers to get familiar with it. When we have figured out the needs of the users, all we need to do is provide them with quick paths to satisfaction.  A good example of a documentation site is <a href="https://hds.hel.fi/" target="_blank">hds.hel.fi</a> which received positive feedback for being clear and informative. People especially liked components docs because of live code editors which allow users to test the components in a quick and easy fashion.
 
 
I find that components are the ‘meat’ of a design system, so their behavior and specifications should be explained in depth. <a href="https://storybook.js.org/" target="_blank">Storybook</a> is a great tool for displaying isolated components and demonstrating all their possible use cases. With Storybook the users can browse the component’s properties, fiddle with them in a live demo, and read the component docs if they wish to add those there as well. Stories work well with visual regression testing too, e.g. <a href="https://www.chromatic.com/" target="_blank">Chromatic</a> or <a href="https://loki.js.org/" target="_blank">Loki</a>. Speaking of testing…
 
## Testing
 
Automated tests should be a no-brainer for any self-respecting design system. Visual regression tests are great for noticing any unwanted changes in the user interface, but their drawback is that the reference images are static. A component can have many states, such as a dropdown that can be closed and opened. Visual test of a closed dropdown may pass with flying colors, but it can’t know if something has gone haywire in the opened state.
 
Unit tests should not be forgotten either. Not only do they give the design system developers peace of mind that everything is working correctly and users won’t get any sudden hiccups, but they also serve as documentation for them on how the components are supposed to work which is especially helpful with complex components.
 
It’s a sound policy to run tests automatically when there’s an activity in version control, e.g., HDS has it so that whenever a pull request is made or it receives a new commit, the tests are run. Tests were also when merging a feature branch to the main or development branch and in version release workflow. You can’t run tests too often.

![People working together](/img/2024-what-makes-a-design-system-good/together.jpg)

## Together
 
When I was working on a new component for HDS and I was faced with a tricky problem, such as what would be the most intuitive way to use the component or simply naming issues, I found that the best results came when other developers and designers were involved in the decision making. This gives several benefits; the solution is considered from multiple perspectives, component knowledge isn’t behind a single person and the pull review process is sped up as others have already given improvement ideas. I liked to involve others by chatting in Slack but more complex problems with new features and components could be tested and discussed in early draft pull requests. That way the discussions of the why’s and hows are chronicled in case a future developer becomes interested.
 
The team should have shared working practices that they have all agreed upon together and committed to following. Practices serve several purposes. Team members don’t need to stop and think about how to do mundane things when they have a clear model and process for them. Common practices can also ensure that the quality stays up and the system doesn’t deteriorate if the team has some sort of maintenance model. For example, at HDS the Git repository had automated checks for outdated dependencies with security issues with a tool called <a href="https://github.com/dependabot" target="_blank">Dependabot</a> that creates a pull request where the packages are updated automatically. 
 
Assistance can also come from the users of the design system. Bug reports, feature requests, and even contributions are a great help to the team. It’s important to note however that the bar to do all those should be low and all the steps in the process should be well documented, so people bother to do them at all. Speaking of users, it’s important to keep lines of communication open with them. That means keeping them informed about the roadmap and upcoming breaking changes, and maybe introducing a dedicated chat channel for questions and support. HDS had users presenting questions, feature requests, and bug reports in Slack almost daily and they expressed their gratitude for knowing the approximate time frame for upcoming breaking changes so that they could plan their workload accordingly. HDS also informed users about new releases in Slack and had regularly scheduled demonstrations about new components or not-so-well-known features.
 
## Accessibility
 
Design systems are in an ideal position to improve the state of accessibility on the web. Designing and developing components to be accessible can be arduous work when you must consider things such as the color palette and screen readers, so having all of that taken care of out of the box is a huge time saver. I think web developers have a growing responsibility to make sure that all users are equally able to use the provided services, and in the public sector, it is required by law. For example, HDS promises to deliver <a href="https://www.w3.org/TR/WCAG22/" target="_blank">WCAG</a> level AA of accessibility and that is accomplished by working together with accessibility experts. An accessible design system broadens the number of users it can reach and therefore suits more projects.
 
 
## Closing statement
 
My philosophy on design system development is always thinking about the users’ needs and that is reflected in the segments of this post. It was the first thing I learned when I started working on HDS. I had all these wonderful new development ideas and improvements that would be fun to do, but I was brought back to the ground with a simple question “Does somebody want this?” Components should always meet a need and solve a problem. They should also be intuitive or at least easy for the developers to implement, and practical or even fun for the end users to interact with. A happy user makes happy developers.
