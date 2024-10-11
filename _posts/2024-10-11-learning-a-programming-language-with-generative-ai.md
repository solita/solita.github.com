---
layout: post
title: Learning a programming language with generative AI
author: andandersson
excerpt: >
  Experiences from learning a programming language with generative AI.
tags:
 - Generative AI
 - C#
 - DOTNET
---

# Background

Generative artificial intelligence, or GenAI, is one of the biggest hypes in the software industry. With the introduction of applications like ChatGPT, AI-algorithms can produce text, generate images, and even motion pictures and music. Due to the trends, there have been many discussions how GenAI may affect software development. How can it be utilized, for example, for coding, learning new tools and frameworks, code reviewing? 

![A genAI-created picture of a robot coding](/img/2024-10-11-learning-a-programming-language-with-generative-ai/coding-robot.png)

In Solita's GenAI-twin project, we wanted to find out these things. For the period of March-September 2024, we started to develop a full stack application in C# with .NET and React with the help of GenAI. In that way, we were able to get a picture of how GenAI can affect software development.

As a part of the journey, we also wanted to find out how GenAI can be utilized for learning a new programming language or framework. Myself as a junior developer, I did not have any prior knowledge of neither C# nor .NET and was assigned with the task to learn them.

Even though there are several GenAI-tools for coding, I decided to use ChatGPT since the purpose was to learn, rather than to just develop. GenAI-tools for coding, like Cursor or Codeium, are used for giving suggestions for code rather than explaining concepts and theory.
With ChatGPT, I could ask questions about the code as well as the theory behind C# and .NET.

# The first application

My first task was to make a very simple full stack application for the purpose of learning the basics of C# and .NET. The method I used was to tell ChatGPT small tasks at a time, that I wanted to implement. For example, my very first comment was “I am a software developer that don't know anything about neither C# or .net, and I want to learn both by creating a simple application”. The process started, and ChatGPT suggested that I could create an online shop, which I did. I used the same chat window during the whole process, and step by step I asked questions about implementing different features as well as error handling. When needed, I asked ChatGPT to help me one small task at a time with the implementation. 

![A genAI-created picture of a robot coding](/img/2024-10-11-learning-a-programming-language-with-generative-ai/chatwindow.png)

In general, the results were okay. A working application was created almost completely with the use of GenAI. At some points I had to search certain things on the web, but ChatGPT made most of the work. The quality of the code varied, although mostly it worked. Some methods were not the most effective possible, naming conventions were not followed, and other minor issues. 

# The Twin project application

After finishing the first application, I continued to develop and learn with the actual application of the project. I implemented one of the user stories from the backlog. The purpose was to implement a data model, or in other words create database schemas and their required logic on the backend. The method was still learning by doing. I created database entities as well as controllers, services, repositories, and migration scripts in .NET.  As this task was much bigger than the previous one, ChatGPT started to hallucinate and make several errors. At this point, I decided to have multiple chats open with chatGPT to keep the problems separate. In the end I had one for the timeline of the user story, one for error handling, and one for coding with .NET.

Now and then it generated not working and incoherent code. Because of that I could not rely solely on ChatGPT but also had to read documentation and search the web for certain subjects.

In the end, however, the user story was implemented as it was supposed to be, although the implementation might not have been the best possible.

# The learning experience

Now and then, talking with ChatGPT might feel like having a conversation with a real person. Something that has come to my mind more than once is the Turing test. For a recap, it states that a machine can be seen as intelligent as a human, if it can engage in a conversation without being detected as a machine. I would say that the test might now be considered as succeeded. ChatGPT can engage in a conversation by answering questions. The answers are usually grammatically correct and remind of human generated text. And like when asking questions from a real person, the answers are not always true. The risk with a succeeding Turing test is that one might have the illusion of conversing with a human but forget that humans make mistakes. On the other hand, as it is not asking any own questions, a discussion with ChatGPT may not be a conversation in the traditional form. 

![The turing test](/img/2024-10-11-learning-a-programming-language-with-generative-ai/turing-test.png)

# How to learn with GenAI

Myself, I used a 'learning by doing' approach. There are, however, many ways one can learn with GenAI. Another way to learn a new programming language could be to step by step letting ChatGPT talk about the language in question, including its syntax, variables, typing, data structures, and so on. I, however, would not find this approach useful as there are already online documentation and books for most programming languages that can be used in the traditional way, which are also reliable. Regardless of the way, there are some practices that are good to take into consideration:

- ChatGPT is probably the best option for learning. AI-tools for coding do not explain and tell theory and concepts as well as ChatGPT
- If using ChatGPT, it is preferable to use the paid version and create a customized agent. That will be trained to focus as much as possible on the subject in question.
- Fact check, fact check, fact check! GenAI is not all knowing and will make mistakes!
- Do not over rely on GenAI. When the learning seems to be going well, there is always the risk that one will trust it too much. Too much trust might cause you to forget to fact check. It might also cause passivity and decreased learning, as GenAI is doing most of the job.
- If using ChatGPT, do not use the same chat window for too long. As ChatGPT is iterating over previous answers in the conversation, it will sooner or later start hallucinating.

# Conclusion
 
GenAI can be seen as a learning assistant or tutor. It is by no means an oracle or a guru. Just like a real tutor, it can make mistakes, and is even likely to do so. The information and answers it gives are gathered from the internet without any guarantees of fact checking or correctness. My tasks succeeded in the sense that I learned the basics of .NET and C#. In my opinion, using ChatGPT for learning a new programming language or framework might be beneficial when having the option of learning by doing. It may also be useful if one needs an explanation of a certain topic, as it is answering questions. One should, however, always consider the possibilities of flaws and hallucinations, and remember to not over rely on GenAI. It will certainly not replace traditional learning.
