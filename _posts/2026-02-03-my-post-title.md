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

The workflow typically went something like this:
1. There's a bug to fix
2. You debug manually and try to find the root cause
3. You exhaust all your own resources trying to solve it
4. You finally ask the AI

The result is predictably poor and useless.

When I set the prompting challenge for myself, I quickly realized that using AI effectively requires a mental shift away from thinking of it as an "all-knowing entity." Instead, you need to guide the AI like you would instruct a junior developer, or once you are skilled enough in prompting, a peer at the same level. Once I started giving the agent simpler tasks, I found it performed remarkably well!

This is the most important lesson in prompting: If you don't know how something should be done, the AI doesn't know either. AI is an eager guessing machine, and without clear guidance, it will simply guess, eagerly.

## Context Is Everything

The key to effective prompting is understanding how AI context works. While the model is trained on vast amounts of data from across the internet, the context provided in your current chat session carries significantly more weight. I initially assumed that since JavaScript dominates AI training data, the model would perform poorly with other languages. This assumption was incorrect. Once you grasp how context influences output, you can achieve excellent results regardless of programming language or tech stack.

Let me illustrate this with a practical example.

**Example: Bad prompt**

```
Create a new API endpoint for user profiles.
```

**Example: Better prompt**

```
Create a new API endpoint for fetching user profiles. 
Look at src/controllers/ProductController.ts and src/routes/products.ts 
for reference on how we structure our endpoints in this project.
Look at src/views/UserProfile.tsx and see what placeholders we are using to deduce what fields should be returned.
Follow the same patterns for error handling and response formatting.
```

The second prompt is more effective because it provides the AI with concrete reference points from your actual codebase. Instead of leaving the AI to guess your project's conventions, you're explicitly pointing it to existing implementations. The AI can now read those files, understand your patterns for routing, controller structure, and error handling, and produce code that fits seamlessly into your project. The first prompt would likely result in generic code that follows common conventions from its training data, requiring significant refactoring to match your style.

Later in this article, I'll show how even the bad example can yield good results by leveraging Planning mode.

## Getting started

What you need:
- Github Copilot license
- Github Copilot extension for the IDE of your choosing
- Put it on Agent



## Konkreettiset 

More content...


- Multiagent setups, skills, frameworks etc etc etc -> just focus on understanding context