---
layout: post
title: "What I Learned from Porting an Astro HTML Generator to Java with AI"
author: jarzka
excerpt: >
  Switching technologies mid-project used to be a massive undertaking. With AI agents, it's now possible to port an entire codebase to a different language in a fraction of the time — but it still requires careful planning and human oversight.
tags:
  - AI agents
  - porting code
  - Astro
  - Java
---

There have probably been many situations where software development teams have made the "wrong" technology choice but couldn't justify switching because they were already too deep in the swamp. Maybe the chosen technology turned out to be hard to maintain, support got dropped mid-project or the choice was simply a poor fit for the problem — but since it works, rewriting it could not be justified and developers just have to live with their choice.

You might remember from my [earlier blog post](https://dev.solita.fi/2024/12/02/building-static-websites-with-astro.html) that we picked [Astro](https://astro.build/), a Node-based framework, for our static website generator project. Astro was chosen because it felt modern, content-focused, and was easy to pick up for any React developer — just what we needed. While the previous blog post is still relevant and I personally enjoyed using Astro, it ended up being the wrong choice in our project. The main reason was performance: we have strict requirements for site generation speed that Astro just couldn't meet despite multiple optimisation attempts. This created a motivation for us to begin thinking about switching it to something else.

Switching technologies is a significant change that would traditionally require a lot of work. With today's AI agents, however, the change is possible to carry out in significantly less time, leveraging existing code as much as possible. For AI, an existing codebase with good tests is like precisely written documentation of how a system should work. And since AI has proven to be very efficient in generating working systems from text prompts, it can use the existing implementation as a "prompt" for generating a similar system in another technology.

## Why Astro Wasn't For Us

Our practical experience of using Astro for two years revealed that the generation slowness was mainly caused by two factors. First, Astro orchestrates page generation by itself (via `getStaticPaths`) and doesn't really allow fine-grained optimization such as parallel page generation or reading all required data into memory once before generation starts. Second, while splitting HTML code into small Astro components is good for maintainability, we noticed that each additional component slowed the generation.

We also realized that building a static site in our case didn't necessarily require a dedicated HTML framework. Without a framework, we would get full control over orchestration: how data is read, how generation is parallelized, in which order pages are generated and so on. This led us to abandon frameworks altogether and look for a programming language + templating engine combination instead. We evaluated both Java and Go-based solutions by creating test ports that proved their performance benefits. We chose Java because the rest of our system was already built with it. For a templating engine we picked [JTE](https://jte.gg) for its promise of speed and type safety.

## Planning the Porting

I might not have dared to start thinking about AI-assisted code porting without previous experience. Luckily, I had already ported my personal chess game project written in Java over 10 years ago into a web-based version. The porting was a success, so I was fairly convinced that AI had reached a level where even larger project's technology — several tens of thousands of lines — could be reasonably switched. The experience also gave me some intuition about how to approach a port and what to expect.

To begin code porting with AI, you need two things: An LLM (Large Language Model), which is essentially a machine that is used to generate text based on statistics and probabilities, and an AI agent that is able to figure things out on its own by using the LLM. In my case, the tool of choise was **GitHub Copilot** (the VS Code extension with agentic capabilities) and **Claude Opus 4.6** model.

In theory, you have a chance to get a decent result with a simple prompt like: _"Port this project to Java"_. In practice, however, you'll get much better results by providing good context for the process. For example, it was beneficial for us to write an initial plan on how the Astro-specific page orchestration should look in the Java port and provide the idea as a context for the AI. While AI is also pretty good at solving tooling differences on its own and can ask clarifying questions, it still helps if you make important choices early on. This of course requires sufficient understanding on both the source and target technologies.

Once the plan is ready, you can give it to the AI as context in Copilot's planning mode for further analysis. In my case, the AI agent was able to create an execution plan for the order in which things should be ported. For example, domain objects that are used everywhere in the project were clear candidates to port first, since their shape affects the entire codebase.

## Porting Process

One challenge during the porting was that I occasionally noticed things going in the wrong direction mid-process. Fortunately, I was able to guide the agent by providing more details ("steering") while it was creating the port. This turned out to be highly worthwhile: if the AI "forgot" to follow my instructions early on, it didn't follow them later either. Fixing issues as early as possible helped steer the whole process in the right direction.

However, giving steering instructions sometimes caused the agent to stop the porting process entirely after fixing a single issue. I could resume it with a simple _"continue"_ command, but an even better approach turned out to be prefixing my instructions with _"by the way"_, causing the agent to correct its behavior on the fly. This way, I was able to continuously review and guide the AI's work while it was doing its thing.

## Findings After Initial Porting

In our case, the actual code porting took a couple of hours. This covers the time from the first prompt to the point where the new generator code compiled successfully. A couple more hours were spent to ensure all the ported tests were green before actually trying to run the generator.

After AI considered the port _"done"_, I ran it and immediately experienced a multifold speed improvement compared to our original generator! It was a joy to see the first output: the familiar-looking HTML website we had created but this time generated by an entirely different technology.

At this point, it was clear that the new system was functioning, so it was time to start analysing the quality of the code more closely. Diving deeper into the generated code, we found several issues:

- **File and folder mapping was confusing**, meaning that there was no clear A-to-B relationship between the source files / folders and the ported system, which made reviewing much harder. In some cases the difference was justified by the architectural differences, but AI had clearly used its own imagination of how the project should be structured even if the original structuring was quite clear. Thus, I ended up starting the whole porting process from scratch and asked the AI to prefer a one-to-one relationship between files and folders when porting code (with some exceptions).
- **Code duplication.** The original codebase had many shared utilities used across the generator. In the ported code, the AI didn't always understand to reuse these utilities and instead created new inline solutions.
- **Unused code.** The AI created various helper functions that it ended up not using at all. This might have been partly caused by architectural differences between the source and target systems. It caused unnecessary confusion since after the port was done, we ended up reviewing and reasoning code that turned out to be dead.
- **Missing or replaced comments.** Important code comments from the original source were often left out. Even worse, the AI sometimes added its own comments explaining how the ported Java code differs from the original TypeScript. Such comments are pointless since the original Astro project will eventually be removed.
- **Non-idiomatic code.** The ported code was technically functional but not always "Java-like". For example, the AI had ported our manually written number formatting logic directly from TypeScript to Java even if there was built-in support for such formatting directly in Java. AI just didn't dare to take advantage of it.
- **Accidental bug discovery.** Perhaps the most "entertaining" finding was that the porting process revealed bugs in the original implementation! For example, the original generator was creating a few unnecessary pages with empty content. I noticed this when I was arguing with the AI about generation rules that differed from the original. It turned out the AI had independently changed the rules — not something I knew I wanted, but this time it was actually correct!

Despite these problems, the most significant finding was that logical errors were almost nonexistent in the ported generator code: there were only a few and they were easy to fix. It seems that AI is pretty good at porting code between languages and keeping the result functionally equivalent. Also our Astro components, which range from simple to more complex HTML templates, were cleanly converted to JTE code without any major issues.

I'm not sure whether addressing every possible issue in the initial prompt would have produced a perfect result. After all, it's easy to tell an AI not to make mistakes, but since porting a system to another technology is a lengthy process, the AI might not "remember" to follow every instruction at every step. Duplication and dead code can also happen by accident when ported code is being refactored. Thus, I believe the initial port — even if working — should only be treated as a starting point towards the final version.

## Ensuring Code Quality

Ensuring the quality of such a large-scale ported system is challenging. First and foremost, it's important to understand that the quality of the ported code is highly dependent on the quality of the source system itself. For example, if the source system has good test coverage, you are already at a good starting point. Also, code structuring, method naming and general _feeling_ of the quality will be strongly retained in the ported version.

To begin analysing the quality of the ported code, we used static code analysis tools to verify that the ported generator did not break our coding rules. We also used a diffing tool to ensure the new generator produced identical output to the original generator with the same input data (not counting irrelevant details like formatting differences). Luckily, fixing little things here and there also forced me to check whether I could make sense of the AI-ported code as a human developer.

We slowly progressed towards the point in which classic rules-based tools stopped finding issues, diffing showed no change in functionality and I could not find problems by reading the new code. Still, I wasn't confident that there were no more problems to find. So I began thinking...

![Expanding brain meme](/img/what-i-learned-from-porting-code-with-ai/galaxybrain.avif)

Yes: it was time to use AI to analyze its own code! While I do not recommend blindly trusting AI in this process, I believe it can reveal interesting findings that other methods might miss.

While a simple prompt like _"Review this ported code"_ could produce desired results, I found that giving a specific angle for the analysis provided much better results. Here are some of the prompts that provided good results when run multiple times with different agents. Even better results can be obtained by focusing the analysis on a specific part of the ported codebase.

- _"This project was ported from Astro to Java. Can you find duplicates that could use shared helpers?"_
- _"... Can you find unused code or code that is only used in tests?"_
- _"... Can you find functionality that could be implemented more idiomatically in Java?"_
- _"... Can you find security issues in the ported implementation?"_
- _"... Can you find any functional differences between the original and ported implementation that could cause different output?"_
- _"... Can you find places where null handling differs between the original TypeScript and the ported Java, such as unchecked nulls?"_

Despite all the automated code reviewing, I feel that human code review still remains highly necessary. After all, the main purpose of programming languages is not to tell a computer what to do, but to tell _another human_ what a computer should do. Thus, the ported code is not usable if a human cannot understand it.

As mentioned previously, our plan was to import not only the generator code itself, but also its tests. Some tests were written in Playwright which did not need porting at all since we could just run them normally against the new generated output. Still, there were many unit tests originally written in TypeScript for Vitest and now ported to Java that obviously needed human observation. Green tests mean nothing in the end if they do not test the right things. Luckily, AI had been quite clever also when porting test code — most of the needed fixes were related to using common patterns in the test code.

We manually reviewed the ported code and its tests until our feeling was strong enough that the result was merge-ready. When an issue was found, we investigated whether a similar issue was also found elsewhere in the ported codebase (with and without the help of AI) and very often found multiple things to fix. This helped create certainty that most of our findings were fixed throughout the whole ported codebase, not just in a single file.

## Verdict

The main motivation of switching the generator's technology was to gain performance benefits that were simply impossible to get with the old implementation. This goal was clearly reached, so the only question remains: did we manage to create a port that’s just as high-quality as if it had been written from scratch?

As mentioned, there were numerous small problems in the first version of the ported code. The initial port was ready in a single work day, but cleaning, refactoring, testing and reviewing the whole thing took a couple of weeks of work. Despite this, the AI-generated code was still a much better starting point than trying to port everything manually. Of course, it would have been best to implement it this way right from the start, but I'm quite happy with the end result we got by porting the existing code with AI.

## Conclusion

One of the most significant shifts brought by agentic AI is that "wrong" technology choices no longer have to be permanent. What previously meant months of expensive rewriting can now be approached as a structured, AI-assisted process with significantly less time. Choices and their reasoning still matter, but the fear of being locked into a suboptimal stack is considerably smaller than it used to be.

That said, AI-assisted porting is not a single-step operation. Badly written system won't automatically become better if ported to another technology. Also, the initial port will almost certainly contain duplication, dead code, missing documentation, and non-idiomatic patterns. Treating the first working version as a foundation to improve upon is the right mindset. Good upfront context, active steering during the process, and thorough quality assurance afterwards — combining static analysis, diffing, targeted AI review, and human code review — are all necessary ingredients for a good end result.
