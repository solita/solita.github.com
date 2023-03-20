---
layout: post
title: GitHub Copilot - let AI write your code?
author: arto
excerpt: >
  Using tools to increase effectiveness has been a long-standing trend in the software development community. Latest wave comes in form of GPT-3, OpenAI, and ultimately GitHub Copilot. Let's try to answer the question: Can AI write your code?
tags:
 - Software development
 - AI
 - GPT-3
 - OpenAI
 - GitHub Copilot
---

_One day soon, AI will be writing the code. I, for one, welcome our new robot overlords._

![Copilot helping with Markdown](/img/github-copilot/copilot_helping_with_markdown_3.png)
*Copilot is writing this blog text for me*

## What is GitHub Copilot?

Right now it's an intellisense-kind of tool you can get in popular IDEs. Whereas traditional code suggestion plugins typically detect patterns in your code and suggest code snippets, GitHub Copilot is reading your code and trying to understand your context, comments, and method names, and then synthesizing code suggestions. Raw material for the suggestions comes from GitHub public repositories. But it's not just a copy-paste snippet.

You might have seen GPT-3 based code generation demos before. Copilot is powered by OpenAI Codex, which is a new AI system, more capable than GPT-3. It's currently available as a technical preview, on request. It's expected that later on it will be released as a commercial offering, open for everyone.

My interest in this tool comes from always wanting to improve efficiency and learning, so I applied for technical preview, and got accepted, and have now used this for a few weeks for various personal projects.

## What can GitHub Copilot do for you?

Well, quite a lot. Once you have installed the plugin and the Copilot has been enabled for you, you can start writing code, and you will start receiving code suggestions. You can ignore them and keep on coding as usual, or press the TAB key to accept the suggestions. You can also press Ctrl+Enter to get up to 10 different suggestions for the problem.

Copilot is using the code you have written as a hint for the code suggestions. If you started writing a function, you'll get nice suggestions for the function, based on the name and parameters. If you started defining a variable, you get suggestions on how to populate it. You can also write comments, to explain in English what you want to accomplish.

Let's see how Copilot could help you implement a simple temperature system conversion function. Using Python, you can start by defining a function. Once you start writing the function name, you get the suggestion for implementation (in gray). You can accept it by pressing the TAB key.

![GitHub Copilot generating Celsius to Fahrenheit function](/img/github-copilot/copilot_celsius_to_fahrenheit_cropped.gif)
*Copilot is creating Celsius to Fahrenheit function based on function name*

What if you did not like that suggestion, but would like to see more ideas? Well, you can press Ctrl+Enter to see more suggestions. Let's do that.

![More suggestions for Celsius to Fahrenheit function](/img/github-copilot/celsius_to_fahrenheit_suggestions.png)
*Copilot is giving me 9 more options for the implementation*

How about those pesky unit tests? Can we generate a good base for a unit test? Let's write a comment and see if we get a suggestion.

![GitHub Copilot generating a Test for Celsius to Fahrenheit function](/img/github-copilot/copilot_generate_test_from_comment_cropped.gif)
*Copilot is creating a test for my function*

Of course, the final question is: Can it handle coding challenges typically used in the work interviews? I grabbed a random task from a google search and put it in the comments. Then I pressed Ctrl+Enter for suggestions.

![Nailing the work inteview challenges?](/img/github-copilot/copilot_interview_questions.png)
*Copilot is implementing answer to work interview challenge*

Oops! I suppose we best ask to turn off the Copilot for the interview challenges. :smiley:

## Where Copilot will fail you

The current version of Copilot is mainly getting its hints from the code you write. If you provide nicely structured code, short well-named functions, it works quite intelligently. If you provide huge blobs of code, badly named things, obscure or impossible comments, you will get quite weird suggestions. In other words, feed Copilot garbage, and you get garbage back.

![Copilot suggestions don't always make much sense](/img/github-copilot/copilot_bad_suggestions_1.png)
*Copilot is being humble about its abilities*

Also, localization may throw some challenges in your way, suggestions might not be compatible with your language system, date formats, currencies, or any number of other local things. Not to say you cannot still use them as inspiration and modify them to work of course.

Copilot will also not so much offer you the best way of doing things - the best it can do is give you 10 ideas on how to do this, based on how well you were able to specify your need. If you're trying to accomplish a very simple thing, a one-liner, it will probably include a good choice among those. But if you try to give it a larger task to accomplish, like how to transform a Dataframe, it's more hit-and-miss.

If you just blindly accept any suggestions and combine them to your solution, your end result will be as if your code was written by an absolute madman.

## Concerns about using GitHub Copilot

There are numerous concerns of course for using advanced tools to generate your code. Let's try to go through some of them here.

### This tool is useless and produces crappy code

Well, based on my experience it can do that, yes. But very often it provides at the very least average code that can be used, not worse as an average day average developer could do. And often it might have almost a brilliant or elegant solution for a problem. I've found out it's worth taking a look at the suggestions. Very rarely all 10 are bad, most often there's at least one good one among them.

As I stated above, yes you can make it produce crappy results, by having crappy code in the file or asking for impossible or too large things in a too unspecified way. The code itself is not as dirty as you might think, but of course, you have to work as a quality gate and think a bit about how to combine the parts.

If you think about this as doing a code review for some code written by an inexperienced developer, things will most of the time work out for you. But if you think about it as a code review for some code written by a professional, you might find that the code is not as clean as you might think - sometimes.

### This tool is too powerful and will take my job

Well, at least today you still cannot request it to write a full application for you. Even if you could, the problem is how to specify what you need. I would argue that specifying what we need in technical terms is the biggest part of software designer work, not writing the code. This tool is a copilot, not the pilot. It still needs someone to specify what is needed, to chop down larger requirements into smaller ones, and also to filter what solutions would actually work and be compatible with the chosen architecture.

So perhaps someday, abstractions will evolve to a higher level. I've been waiting for the day when I can dictate what I want to happen, and get those early POCs and MVPs out faster, so we can get some feedback loops going, without sacrificing quality or architecture. Perhaps in 2031, this is how it is done, and our trade has changed from tapping keyboards in unergonomic positions to specifying what the AI bots should be doing. We'll see. But that day is not today.

### This tool will make developers lazy, undisciplined, and generally just bad

Some people say intellisense tools, and especially Copilot, is a crutch. That is absolutely true. You learn to lean on it, and after a while, you could not imagine working without it. 

Now, I embrace that. I want to have those crutches. Today's world requires results faster every year, within ever-growing complexity. We have already raised the abstraction levels quite a bit and will be doing that more in the years to come. I remember how when C++ came along, many protested and said it's not a real language for real work. Later, the same thing happened with Java, compared to C++. Today, Clojure can be a very very neat high abstraction language, almost a no-code environment with proper libraries. So my point is, as things grow more complex, and we cannot afford to build the systems within decades of work, we need to raise the abstraction level. Whether it's better more expressive languages, better frameworks, and libraries, low code tools, or AI assistants, there's no fighting this. It will happen.

And you know, while I do believe that Assembler coders are not lazy or undisciplined, there are not many of those around anymore. And even fewer coders using punch cards. What a crutch it was to move on not using punch cards anymore!

### This tool is a security risk as it's exposing my own code

Well, this one is a bit concerning. You see, the architecture for this extension/plugin involves sending your code over the network, securely of course, but still to 3rd-party server. As per their FAQ, the private code you're working on will not be used to synthesize solutions for other people. Right now it's supposedly only sending the one file you're working on, and the code is stored securely, processed by mostly automated tools.

![GitHub Copilot Architecture](/img/github-copilot/architecture.png)
*GitHub Copilot Architecture*

But it's still sent out, and stored. It's still processed by automation and may be processed by people as well. So if you're working on a project where code is not public, or are under an NDA, this area will need more clarification, to say the least. I would not say it's an immediate no-go, as this is not the only tool that would send things from your IDE to a third party. But let's say it's definitely a concern and probably not something a developer can decide without consulting the rules. So for now, I'm happy to use this as an experiment, and for personal projects, but for work, I would need to clear its use. I'll drop a few related links at the end of this article.

Additionally, of course, you should never write any secrets within your code. This rule is followed pretty fanatically in our company, but I know it's not followed everywhere, at least not systematically. When trying this tool I sometimes would get suggestions that included API keys, secrets, to access services. Some other people's API keys. So they were probably included and exposed already in GitHub, but now it's pretty much too easy to accidentally see them. So never put your secrets inside your code, not even while testing, take it seriously, whether you use any extra plugins or not. 

### This tool is laundering open-source code for reuse outside license

Another valid concern. Let's say I'm working on an open-source project, with some license. I'm using Copilot to get some suggestions, that originate from GitHub public repositories. Supposedly they are mostly synthesized, unique code for me. But there is still code that comes from licensed open source repositories. Even though it's shuffled, its atoms are still parts under a license, which may be incompatible with my project license. And if I'm working on a commercial non-OS project, it gets even more interesting.

This is certainly pushing the limits a bit here. Let's say if we'd take 100 developers, give them access to open source repositories, then request them to use those code lines to produce new functions and algorithms for a new project with an incompatible license. Would this be okay? Would it be okay if an algorithm does it? It would probably not have been okay in the past. Could it be okay? I don't know. But this is definitely a gray area where some light must be thrown. Is a reshuffled, synthesized code an original art, or just a laundered copy? Depends a bit also on the implementation of that shuffling.

## Conclusion

I think it's been fun trying out GitHub Copilot. I like any advances in productivity, especially any that help me do the boring stuff faster so I can concentrate on the fun stuff, like the value of what we are creating, or ease of use. I've been running this tool for a while now, and it's even offering me suggestions on how to write this blog. At its worst, it's bad and amusing. But at its best, it's almost creepy in the way it's able to anticipate my needs.

Additionally, I am a sucker for learning new things, and for me, the most important feature is not rapid code generation, but it's the interactive feedback loop giving me more ideas and suggestions to try, you know, like a real copilot. Some of them are just bad or even harmful, but some of them can be really good, can be something I haven't thought of. Especially considering that I'm specialized in being a generalist - I use many languages, many contexts, so it's quite obvious I cannot focus on mastering all. A good tool like this can help me remember how to do things, and can sometimes even give some new ideas.

Of course, nothing can replace a real co-pilot, you know, like in pair-programming mode, or even a code review. A human coder who similarly has patterns, approaches, and snippets in their head, and is able to shake things up and make you learn. But many companies are not doing pair programming, nor code reviews, due to various reasons. And even if they do, it can be exhausting and time-consuming, so it's not often done for the full workday. On the other hand, the AI tool here is always available, will never tire, will not judge you (a lot), so there are some benefits to that especially in the new Hybrid/Remote working world.

On the other hand, the concerns I listed above, are still valid and must be addressed. Perhaps the right thing to do is not try to avoid progress and fight back, but instead try to see the shortcomings, risks, and problems, and try to work through them over time. What we see here is the first iteration of more intelligent coding aids, and in the future, I am pretty sure we'll see more of this.

## Links and refs
- [GitHub Copilot](https://copilot.github.com/)
- [GitHub copilot in action - let AI write your code? (Video)](https://youtu.be/wL41Xx2YzD4)
- [GitHub Copilot Telemetry](https://docs.github.com/en/github/copilot/about-github-copilot-telemetry)
- [Terms of GitHub Copilot Telemetry](https://docs.github.com/en/github/copilot/github-copilot-telemetry-terms)
- [GitHub Privacy Statement](https://docs.github.com/en/github/site-policy/github-privacy-statement)
- [Research recitation](https://docs.github.com/en/github/copilot/research-recitation)
