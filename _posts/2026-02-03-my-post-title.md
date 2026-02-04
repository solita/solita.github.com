---
layout: post
title: Prompt Engineering 101
author: solita-markump
excerpt: Starter Guide to Prompt Engineering - How to Get Good Results
tags:
  - AI
  - Generative AI
  - GitHub Copilot
  - Software Development
  - Best Practices
  - Productivity
  - AI in Development
---

Let's be honest. Those who have embraced AI as part of their daily development work have noticed significant improvements in both speed and quality. So the question is no longer "Is AI useful for coding?" but rather "How do I get the most out of it?"

Why do some developers see tremendous benefits while others end up with spaghetti code? I took on a challenge at the end of last year to only work by prompting, in order to learn the ins and outs of AI-assisted development. At my current level, I haven't written a single line of code by hand in a couple of months, yet my speed and quality have only improved.

In this blog post, I'll share my personal learnings from this journey and try to extract the most important takeaways in this Prompt Engineering 101 starter guide.

## So What's the Problem?

Most of us (myself included) first encountered AI capabilities through ChatGPT. For a long time, it served as a "Google replacement" and felt like a knowledgeable colleague you could ask for help and ideas. However, I quickly noticed AI's limitations, as I often received hallucinations and outdated information in return. Then came agents and code generation, where the impact of hallucinations and poor code quality actually became a hindrance rather than a benefit.

A common mistake when starting out is asking the AI to solve problems that are too complex. The workflow typically goes something like this:
1. There's an issue to fix
2. You debug manually and try to find the root cause
3. You exhaust all your own resources trying to solve it
4. You finally ask the AI

The result is predictably poor and useless.

When I set the prompting challenge for myself, I quickly realized that using AI effectively requires a mental shift away from thinking of it as an "all-knowing entity." Instead, you need to guide the AI like you would instruct a junior developer, or once you are skilled enough in prompting, a peer at the same level. Once I started giving the agent simpler tasks, I found it performed remarkably well!

This is the most important lesson in prompting: If you don't know how something should be done, the AI doesn't know either. AI is an eager guessing machine, and without clear guidance, it will simply guess, eagerly.

## Context Is Everything

The key to effective prompting is understanding how AI context works. While the model is trained on vast amounts of data from across the internet, the context provided in your current chat session carries significantly more weight. I initially assumed that since JavaScript dominates AI training data, the model would perform poorly with other languages. This assumption was incorrect. Once you grasp how context influences output, you can achieve excellent results regardless of programming language or tech stack.

Let me illustrate this with a practical example.

**Bad prompt:**
> Create a new API endpoint for user profiles.

**Better prompt:**
> Create a new API endpoint for fetching user profiles. 
> Look at `src/controllers/ProductController.ts` and `src/routes/products.ts` for reference on how we structure our endpoints in this project. 
> Look at `src/views/UserProfile.tsx` and see what placeholders we are using to deduce what fields should be returned. 
> Follow the same patterns for error handling and response formatting.

The second prompt is more effective because it provides the AI with concrete reference points from your actual codebase. Instead of leaving the AI to guess your project's conventions, you're explicitly pointing it to existing implementations. The AI can now read those files, understand your patterns for routing, controller structure, and error handling, and produce code that fits seamlessly into your project. The first prompt would likely result in generic code that follows common conventions from its training data, requiring significant refactoring to match your style.

But what if I told you that even the bad prompt can yield excellent results? Enter Planning mode.

## Just Use Planning Mode

I'm a huge advocate of Planning mode. In Agent mode, Copilot immediately starts executing. And since AI is fundamentally a prediction machine, it will confidently keep going even when it's heading in the wrong direction. 

Planning mode, on the other hand, forces the AI to stop, think and explore the codebase first. It creates a step-by-step plan of what it *intends* to do and asks for clarifying questions. This simple change makes a massive difference. You can catch misunderstandings early, redirect the approach, or refine your requirements before any code is written. And most importantly, it automatically loads exactly the files and references it needs into context so it can complete the task with good results without hallusinations.

Let's see how the same "bad prompt" can outperform our carefully crafted "better prompt" when used with Planning mode.

**You:**
> Create a new API endpoint for user profiles.

**Planning Agent:**
> I'll help you create a new API endpoint for user profiles. Let me first understand your project structure and conventions.
>
> **Gathering context...**
> - Reading `src/controllers/` to understand your controller patterns
> - Reading `src/routes/` to see how routes are structured
> - Reading `src/models/User.ts` to understand the User entity
> - Reading `src/views/UserProfile.tsx` to see what fields the frontend expects
>
> **⚠️ I noticed something:**
> `ProductController.ts` uses Redis caching with a 5-minute TTL for GET requests. Since `UserProfile.tsx` fetches this data frequently, I'll apply the same caching strategy to improve performance.
>
> **Here's my plan:**
> 1. Create `src/controllers/UserController.ts` following the pattern in `ProductController.ts`
> 2. Add route `/api/users/:id` in `src/routes/users.ts`
> 3. Return fields: `id`, `name`, `email`, `avatar`, `createdAt` (based on `UserProfile.tsx` usage)
> 4. Implement Redis caching with 5-minute TTL, same as `ProductController.ts`
> 5. Use the same `ApiResponse` wrapper and error handling as other controllers
> 6. Add input validation for the user ID parameter
>
> **Questions before I proceed:**
> - Should this endpoint require authentication?
> - Do you want pagination for listing multiple users?
>
> Does this plan look correct?

Now we are cooking! You can see exactly what the agent intends to do before it writes a single line of code. You can answer its questions, refine the plan, and polish it until it's exactly right. In my experience, the agent often catches details I overlooked (like the caching pattern example above), which would have caused inconsistencies later.

## Prompting is a skill

This is what "coding" looks like in my workflow nowadays: going back and forth with the AI to refine the plan until it's right. I get to focus on the big picture, how the pieces fit together, and in the end I design better features, improve the codebase through refactoring, and save time because the code writing is automated.

But getting here wasn't instant. At first, I felt like an idiot when nothing worked. After my initial attempts, I caught myself thinking "I can code faster by hand than fixing the AI's mistakes." It took about two weeks to break even with manual coding, and another few weeks before the new approach truly clicked.

Prompting is a skill just like coding. And like any new skill, you have to accept a small ego hit to make progress. The hardest part isn't learning new syntax or tools. It's letting go of the urge to dive straight into implementation. You have to trust the process: describe the problem clearly, let the AI explore, refine the plan together, and only then execute. Once you've done a day's worth of work in minutes without the AI making a single mistake, you'll never want to go back.

## How not to get overwhelmed

The world of agentic coding is evolving way too fast for anyone to stay on top of everything. New concepts emerge constantly: [MCP (Model Context Protocol)](https://modelcontextprotocol.io/introduction) lets agents connect to databases, APIs, and external tools. [Agent Skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills) give Copilot specialized capabilities for specific tasks. Multi-agent orchestrators like [Gas Town](https://github.com/steveyegge/gastown) let you coordinate 20-30 Claude Code agents working in parallel with persistent work tracking. And [custom agents](https://code.visualstudio.com/docs/copilot/customization/custom-agents) let you create specialized assistants tailored to your workflow.

It can feel overwhelming. If I changed my workflow every time a new tool came up, I wouldn't get any work done. And here's the thing: all of these features are ultimately just different ways to feed better instructions to the model.

My advice? Don't chase every new feature. Focus on mastering the fundamentals: understanding context, writing clear prompts, and using Planning mode. Once you've nailed those, the advanced features will make much more sense.