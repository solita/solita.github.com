---
layout: post
title: Observations on GitHub Copilot Agent Mode in Daily Development
author: ilkkajo
excerpt: >
  Subjective observations on GitHub Copilot’s agent mode: faster coding, shifting workload to definition, review, and testing, and reflections on quality and ownership.
tags:
  - Software Development
  - GitHub Copilot
  - Agent Mode
  - Productivity
  - Code Review
  - AI in Development
  - Developer Experience
---

These are my subjective observations on how GitHub Copilot’s agent mode has affected our daily development work. The purpose is not to argue for or against the tool, but to document concrete experiences in a project setting.  

An important background detail is that the same people have been working with the same client and the same codebase both before and after the introduction of AI-assisted development. We also received explicit approval to use AI tools in implementation work. This provides a rare opportunity to observe changes in practice under otherwise stable conditions.  

To make sense of these observations, I will first outline how our workflow looked before agent mode.  

## Development Flow Before Agent Mode  

Our team followed a straightforward model for planning and implementing new functionality. Each feature was estimated with story points (1, 2, 3, 5, 8, 12), reflecting difficulty and effort without translating directly into time. This estimation happened in refinement sessions with all developers present. The refinement included high-level discussions, without going too deep into details.  

Once a feature was ready, implementation followed the normal cycle: coding, review, testing, and eventually release. Nearly all code was reviewed by at least one other developer, followed by automated tests and client validation before production. This baseline process forms the backdrop for how agent mode has affected our work.  

Before agent mode, I mainly used GitHub Copilot via the chat/ask mode in Visual Studio and VS Code. Around early spring, the quality of suggestions improved to the point where they were frequently a useful starting point rather than something to discard. From then on, I found myself asking Copilot for help more often than searching Google, which I rarely used anymore for coding-related lookups.  

I cannot say which update caused the change, but the difference was clear. Before that, Copilot often lacked context and its suggestions were irrelevant. In a non-work project late last year, I even became frustrated when trying to fix Copilot’s own broken output. At one point, it felt like I couldn’t code myself anymore.  

Alongside Copilot, I have also consistently used ChatGPT Enterprise, though only for higher-level guidance. Since I cannot share client code with it, my questions there have focused on general topics such as SQL queries, Elasticsearch n-gram matching, or migration away from xBehave.  

## Prompting and Scope  

With agent mode in daily use, a few patterns in how I frame the work became clear.  

In my case, backend coding happens in Visual Studio and frontend coding in VS Code. Although technically I could work across the entire stack from a single environment, I keep the environments separate. This also means I never ask the agent to make cross-stack changes in one go.  

One clear pattern emerged: what works in coding also works with the agent. Breaking tasks down into smaller pieces keeps changes manageable. As a rule of thumb, I now try to ask the agent to implement about one commit’s worth of work at a time. Along with that, I continue to give context in the form of code examples that illustrate how I want the new feature or fix to be structured.  

Previously, I often let the agent finish its work while I planned the next task, only to realize later that my prompt lacked important details. Now, I try to interrupt earlier if I see the agent heading in the wrong direction and provide additional context. This approach keeps changes smaller and more aligned with the project’s practices.  

I also find it important to be explicit about what the agent should **not** do. Helpful guidelines for this can be found in [awesome-copilot](https://github.com/github/awesome-copilot), and both Visual Studio and VS Code provide clear instructions for setting custom rules.  

## Perceived Efficiency and Quality  

Subjectively, my efficiency has increased since adopting agent mode. I can deliver features faster and I am more likely to add extra improvements such as broader test coverage.  

At the same time, code quality dipped when I first started using the agent. I asked it to handle tasks that were too big, and it generated excessive code. Despite this, in my subjective experience the features still reached production faster than before.  

One factor behind this perception is what I would describe as a pull effect. Getting results faster creates a positive feeling that encourages me to keep producing more and more quickly. This pull effect partly explains why quality dipped at first: the sense of momentum made it easier to overlook issues in the agent’s output. It is also easy to become blind to certain changes because they look fine at first glance, even though they may hide issues that only become visible with closer inspection.  

A concrete example concerned a new feature in which I used the agent to create seed data for a new entity in the development environment. The code worked fine if the database was already running with all related entities present. However, if the development database was created from scratch, the seed data for the new entity was not inserted, because it had been placed in the code before the entities it depended on. I later noticed the same mistake in a colleague’s code, almost certainly because I had introduced the pattern first with the help of the agent. This showed me how quickly such quality issues can propagate: the code looks correct at first glance, works in some situations, but fails in others that should have been considered from the start.  

A side effect was that code reviews and testing grew in importance. In practice, I shifted responsibility without realizing it: reviewers and testers had to catch issues I had overlooked. We even agreed to mark pull requests with an estimate of how much of the code was produced by the agent, so reviewers could adjust their approach. While this helps, it also adds weight to the reviewer’s role. These pressures also shaped how we approached reviews, which in turn led us to try agent-assisted reviewing.  

## Review with an Agent  

To balance this, our architect experimented with using an agent for code reviews. Results were mixed: the agent identified technical improvements that humans had missed, but also flagged irrelevant stylistic points due to limited context. Most critically, it could not catch functional or business-logic gaps unless explicitly described.  

One example illustrated this clearly. A feature was implemented in the backend and technically everything worked: the code compiled, automated tests passed, and even an agent-assisted review confirmed the solution. On paper, it all looked correct. However, the feature description had not mentioned the required frontend part, and as a result there was no way for the end user to actually access the functionality. 

For a human reader, it was obvious that the feature would need a frontend implementation as well, even if it had not been written down explicitly. In other words, from the perspective of both the implementing agent and the reviewing agent, the task was complete, yet in practice the business requirement remained unmet. This highlighted the risk that incomplete requirements lead agents to produce solutions that look correct but fail to meet business needs.  

## Shifting Workload  

This points to a broader pattern: producing more code faster with agents shifts the workload elsewhere. More features mean more reviews and more testing. While test coverage tends to improve, the final validation still rests with the business owner or the end-user representative. Their role in testing and approval is critical, both for ensuring that the solution meets actual needs and for maintaining shared responsibility.  

In my own experience, this shift also raises questions about where exactly the work moves and how it affects my role in the short term. One clear change is that the importance and workload of feature definition grows. Since code can be produced faster, the backlog must contain more well-prepared items ready to be implemented. In practice, this could mean that feature descriptions evolve into something written primarily with agents in mind. Story point estimation may then need to place less emphasis on coding effort and more on the time required for review and user testing.  

At one point we even experimented with writing tasks so that the agent could take them over directly. For example:  

> “Implement comment deletion in `#ICommentService.cs`, using the existing tag deletion in `#ITagService.cs` as a reference.”  

The idea was that by embedding code references in the description, the agent would have enough context to generate production-ready code with minimal prompting. In practice, however, this added significant overhead to refinement and did not provide benefits that matched the extra effort. Even so, I believe it is important to try out different approaches, since only by experimenting can we learn what actually works in practice.  

While the future may reduce human involvement in reviews, today the practical effect is on how end-user representatives experience the flow of testable work. Up to now, they have been able to rely on a predictable rhythm: after requirements are defined, they can expect functionality to arrive for testing at certain points. With Scrum, this typically happens gradually during a sprint; with a waterfall-style approach, it arrives in larger chunks but still at a roughly known moment. When functionality is delivered faster, the corresponding testable pieces also arrive faster, which may require additional resourcing and effort for user acceptance testing.  

Although my own role has not yet changed significantly, I believe it will evolve more clearly in the near future, at least that is how it feels right now. I can imagine my work moving closer to the customer and the end users, with a stronger emphasis on describing and shaping functionalities from their perspective in addition to implementing them.  

## Conclusion  

The landscape of language models and development tools is changing rapidly. New capabilities are introduced frequently, and both efficiency and quality can shift over relatively short periods of time. This ongoing change affects not only how we code, but also where the effort in the process lands.  

My own experience shows both the benefits and the risks: agents speed up delivery and create a strong pull effect that motivates producing results faster, but at the same time this momentum can reduce careful review and make it easier to overlook problems hidden in seemingly good code. As agents accelerate development, more of the workload moves toward defining functionalities in sufficient detail, reviewing results, and ensuring meaningful testing with end users.  

While the exact impact on my future role is still unfolding, what seems clear is that the balance of effort across the whole development process is changing. Coding itself takes less time, while definition, review, and validation take more. This makes it essential for teams to keep refining and sharing good practices together, so that the productivity gains from agents do not come at the cost of quality or shared ownership.  

One open question is how we preserve a genuine sense of ownership when much of the code is written by a machine. Pride and responsibility for the codebase are critical to quality, yet they may feel more distant when an agent does most of the typing. To truly benefit from these tools, we need clear agreements on how to use them and deliberate practices that keep ownership and accountability within the team. We should be proud of the solutions we build, whether assisted by an agent or another tool, and we must not let responsibility for quality drift away from ourselves. In the end, the quality of our work remains in our hands, even as the tools evolve at a fast pace.  
