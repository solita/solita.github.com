---
layout: post
title: Prompt Engineering 101
author: solita-markump
excerpt: "Starter Guide to Prompt Engineering: How to Get Good Results"
tags:
  - AI
  - Generative AI
  - GitHub Copilot
  - Software Development
  - Best Practices
  - Productivity
  - AI in Development
---

Let's be honest. Those who have embraced AI as part of their daily development work have noticed significant improvements in both speed and *quality* (yes, we are *not* talking about vibe coding). So the question is no longer "Is AI useful for coding?" but rather "How do I get the most out of it?"

Why do some developers see tremendous benefits while others end up with spaghetti code and hallucinations? I took on a challenge at the end of last year to only work by prompting, in order to learn the ins and outs of AI-assisted development.

In this post, I'll share the key lessons from that journey, and hopefully inspire you to give it (another) try.

## So What's the Problem?

**Bad prompt:**
> My app hangs when users log in but only sometimes and I've tried everything, can you fix it?

A common mistake when starting out is selecting the wrong problem for AI to solve. I made this mistake myself and have observed many others doing the same. The workflow typically goes something like this:
1. There's an issue to fix.
2. You try the obvious solution (and it doesn't work).
3. You go deeper, read more code, debug, and exhaust all your own resources.
4. You finally ask the AI for help.

You *might* get a useful hint, but more often than not, the results miss the mark entirely. So you dismiss the AI and go back to debugging by hand.

**Better prompt:**
> I'm debugging a login issue where the app sometimes hangs.
> 
> Look at `Services/AuthService.cs`, `Controllers/AuthController.cs` and `Middleware/JwtMiddleware.cs` to understand the login flow.
> 
> Look at `Repositories/UserRepository.cs` to see how we fetch the user from db.
> 
> Here is our logic in the cache layer: `Services/TokenCacheService.cs`
> 
> Analyze the flow and give me suggestions where the issue might be.

When I set the prompting challenge for myself, I quickly realized that using AI effectively requires a mental shift away from thinking of it as an "all-knowing entity" or a sparring partner. Instead, *you need to guide the AI like you would instruct a junior developer*. Once you are skilled enough in prompting, you can treat it more like a peer at the same level as you. Once I started giving the agent simple and clear tasks, I found it performed remarkably well!

Here's the thing: **if you don't know how something should be done, the AI doesn't know either.**

AI is fundamentally a guessing machine. Without clear guidance, it will confidently guess and keep guessing. The quality of your output is directly tied to the clarity of your instructions.

## Context Is Everything

The key to effective prompting is understanding how AI context works. While the model is trained on vast amounts of data from across the internet, the context provided in your current chat session carries significantly more weight. I initially assumed that since JavaScript dominates AI training data, the model would perform poorly with other languages. This assumption was incorrect. Once you grasp how context influences output, you can achieve excellent results regardless of programming language or tech stack.

Here is another example:

**Bad prompt:**
> Create a new API endpoint for user profiles.

This prompt would likely result in unexpected changes across your codebase and generic code based on common conventions from training data.

**Better prompt:**
> Create a new API endpoint for fetching user profiles. 
> 
> Look at `Controllers/ProductController.cs` for reference on how we structure our endpoints and routing attributes. 
> 
> Look at `ClientApp/src/views/UserProfile.tsx` and see what placeholders we are using to deduce what fields should be returned. 
> 
> Follow the same patterns for error handling and response formatting.

The second prompt is more effective because it provides the AI with concrete reference points from your actual codebase. Instead of leaving the AI to guess your project's conventions, you're explicitly pointing it to existing implementations. The AI can now read those files, understand your patterns for routing, controller structure, and error handling, and produce code that fits seamlessly into your project. 

But what if I told you that even the bad prompt can yield excellent results? Enter Planning mode.

## Just Use Planning Mode

I'm a huge advocate of Planning mode. In Agent mode, Copilot immediately starts executing, and often in the wrong direction.

Planning mode, on the other hand, forces the AI to stop, think, and *explore the codebase* first. It creates a step-by-step plan of what it *intends* to do and asks for clarifying questions. This simple change makes a massive difference. You can catch misunderstandings early, redirect the approach, or refine your requirements before any code is written. And most importantly, it automatically loads exactly the files and references it needs into context so it can complete the task without going off the rails.

Let's see how the same "bad prompt" can outperform our carefully crafted "better prompt" when used with Planning mode.

**You:**
> Create a new API endpoint for user profiles.

**Planning Agent:**
> I'll help you create a new API endpoint for user profiles. Let me first understand your project structure and conventions.
>
> **Gathering context...**
> - Reading `Controllers/` to understand your controller patterns and routing attributes
> - Reading `Models/User.cs` to understand the User entity
> - Reading `Services/` to see how business logic is structured
> - Reading `ClientApp/src/views/UserProfile.tsx` to see what fields the frontend expects
>
> **⚠️ I noticed something:**
> Some of your GET endpoints use `IDistributedCache` with a 5-minute TTL. Since user profiles are read frequently but rarely updated, I'll apply the same caching strategy here.
>
> **Here's my plan:**
> 1. Create `Controllers/UserController.cs` following the pattern in `ProductController.cs`
> 2. Add route `/api/users/{id}` using `[Route]` and `[HttpGet]` attributes
> 3. Create `DTOs/UserProfileDto.cs` with fields: `Id`, `Name`, `Email`, `Avatar`, `CreatedAt` (based on `UserProfile.tsx` usage)
> 4. Implement Redis caching with 5-minute TTL using `IDistributedCache`, same as `ProductController.cs`
> 5. Use the same `ApiResponse<T>` wrapper and error handling as other controllers
> 6. Add input validation using FluentValidation
>
> **Questions before I proceed:**
> - Should this endpoint require authentication?
> - Can users view other users' profiles? If so, should we use a separate DTO that omits sensitive fields like email?
>
> Does this plan look correct?

Now we are cooking! You can see exactly what the agent intends to do before it writes a single line of code. You can answer its questions, refine the plan, and polish it until it's exactly right. In my experience, the agent often catches details I overlooked (like the caching pattern example above), which would have caused inconsistencies later.

Here's the magic of context. Once the agent has explored your codebase and built a plan, you don't need to start from scratch for related tasks. The relevant files are already loaded, and the agent remembers what it just did. Your next prompts can be much simpler:

**You:**
> Update the UI to call the new endpoint and replace the placeholders with real data.

**You:**
> Add unit tests for the new endpoint. Look at `ProductControllerTests.cs` for reference.

*Notice that we still point the agent to the right reference file when needed.*

**You:**
> Actually the CreatedAt timestamp is not needed. Remove it from the response dto and from the UI.

**You:**
> When the user id does not exist we hit 404 but in this case we want to redirect to the front page. Look at `ProductPage.tsx` for example.

*"What about the hard stuff like race conditions, complex state machines, and security edge cases?"*

Well... you're not there yet. Start by automating the easy tasks you already know how to solve. AI performs best when you can clearly describe the outcome. If you know you need to extract logic into a service and refactor 10 files to use it, let the AI do that and save time. You probably would've made a copy-paste error anyway, or left a misleading comment in.

But once you've built that foundation, the complex problems are exactly where good prompting shines. The AI struggles when you're vague, but if you can enumerate the edge cases, describe the state transitions, or specify the security requirements, it handles them remarkably well. Complexity isn't the enemy. *Unclear* complexity is. AI can solve any complex task, but the challenge is breaking it down into clear, actionable steps. Ask yourself: how would you delegate this task to a junior developer?

## Prompting Is a Skill

Once you get the hang of it, this is what "coding" looks like for me now. It's going back and forth with the AI to refine the plan until it's right. I get to focus on the big picture and how the pieces fit together. In the end, I design better features, improve the codebase through refactoring, and save time because the code writing is automated.

But getting here wasn't instant. At first, I felt like an idiot when nothing worked. After my initial attempts, I caught myself thinking "I can code faster by hand than fixing the AI's mistakes." It took about two weeks to break even with manual coding, and another few weeks before the new approach finally clicked.

Prompting is a skill just like any other. You have to accept a small ego hit and feel dumb for a bit to make progress. The hardest part is getting started **and keeping going.** You don't yet know how to talk to the agent. Your prompts will fail. You'll redo things. A lot. But with each mistake, you learn what works and what doesn't.

**The point comes eventually when you realize you've done a day's worth of work in minutes without the AI making a single mistake.** After that, there's no going back.

## How Not to Get Overwhelmed

The world of agentic coding is evolving way too fast for anyone to stay on top of everything. New concepts emerge constantly: [MCP (Model Context Protocol)](https://modelcontextprotocol.io/introduction) lets agents connect to databases, APIs, and external tools. [Agent Skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills) give Copilot specialized capabilities for specific tasks. Multi-agent orchestrators like [Gas Town](https://github.com/steveyegge/gastown) let you coordinate 20-30 Claude Code agents working in parallel with persistent work tracking. And [custom agents](https://code.visualstudio.com/docs/copilot/customization/custom-agents) let you create specialized assistants tailored to your workflow.

It can feel overwhelming. If I changed my workflow every time a new tool came up, I wouldn't get any work done. And it all boils down to context management: these features are just different ways to feed better instructions to the model.

My advice is to tune out the noise. First focus on mastering the fundamentals: understanding context, writing clear prompts, and using Planning mode. Once you've nailed those, the advanced features will make much more sense.

## Getting Started

This is what you need to get going:

1. Get a GitHub Copilot license from [IT Services](https://it.services.solita.fi/support/catalog/items/134)
2. Install the [GitHub Copilot Chat](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat) extension in VS Code
3. Log in with your Solita GitHub account

That's it. You should now have the Copilot chat panel on the right side of VS Code. You can switch between Agent and Plan modes using the dropdown, and choose which model to use. In my opinion, the best coding model right now is **Claude Opus 4.5.**

## Conclusion
AI-assisted development isn't magic, and it's not going to replace you. It's a tool that enables you to focus on solving the actual problem and helps you save time by automating the coding part.

Start with Planning mode. Just talk to the agent. Break big problems into smaller ones together with the agent. Accept that there's a learning curve and your performance takes a hit in the beginning. And when it finally clicks, the bottleneck moves from typing to thinking.