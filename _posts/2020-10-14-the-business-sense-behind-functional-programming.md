---
layout: post
title: The Business Sense Behind Functional Programming
author: jalef
excerpt: >
  Functional Programming has risen in popularity among developers, but non-technical people still consider it to be too scientific. In this article we try to present the advantages of Functional Programming in a non-technical approach and explain why it makes sense businesswise.
tags:
 - Functional programming
---

The Functional Programming (FP) paradigm has been enjoying a resurgence in developer circles for more than five years now. Its advocates however have faced difficulty making the case for FP when management sits across the table. Usually, the typical FP advocacy piece drowns the business advantages of FP in technical terms, and the audience tunes out. In this article, we strive to avoid this pitfall and ground the case for FP in the real world of profitability and risk.

We at Solita at positioned well to make the necessary distinctions: We boast great experience in FP, we count FP among our software best practices and we advocate for FP to our customers.

![Functional Programming for Business](/img/the-business-sense-behind-functional-programming/functional-programming.jpg)

## Quality

If your business offers a software product or service, you care about quality. The connection between quality and your bottom line needs no explanation. Let's proceed then to the connection between the quality of a software product and an FP codebase. It's a fact of life that code is faulty. All but the most rigorously written code contains faults and the number of faults per line of code is, on average, constant[^1]. The conclusion: more code, more faults. The FP solution to a problem is not only less code[^2] compared to the typical alternatives but also less fault-prone on a per-line-of-code basis[^3]. We may safely state: FP, higher quality.

## Time To Market

Managers of most software products treat time-to-market (TTM) as priority #1. The time developers need to complete a feature is the primary driver behind TTM. Moreover, the effort required to tackle a software project scales superlinearly, i.e. if project A is twice the size of project B, it requires more than twice the code[^4]. With less code to write for features and less code to test them, it is safe to state: FP, reduced TTM.

## Strategy

Shrewd folks in the software business know that technology evolves very rapidly. They also know that being competitive is directly correlated to how well the business can keep up with these changes. One change that is here to stay is that getting better performance by buying faster processors is a thing of the past[^5]. Steve Jobs, at the time, believed that the industry lacks the skills to address this crisis:

>*“The way the processor industry is going is to add more and more cores, but nobody knows how to program those things. I mean, two, yeah; four, not really; eight, forget it.”* [^6]

These statements are a bit technical though, so let's break them down. If you serve customers with a digital product, you are faced with a hard limit on how many customers you can serve per second. Any business which seeks to grow must have a strategy for pushing this limit upwards. Today, there is only one way to push that limit: *write the software such that it scales*. Such software though, is difficult to write in non-FP languages. The reason is that they encourage the sharing of computation state, an difficult thing to get right on a distributed system. By forbidding the sharing of state and by providing tools for mutating state explicitly, the FP paradigm has proven[^7] [^8] [^9] to be a much better fit for scalable software. It is, therefore, safe to state: FP, improved long-term growth.

## Human factor

In the software world, managers bemoan the difficulty of hiring FP developers. This difficulty is an undeniable fact. The keen manager however, also recognizes that this difficulty is just another trade-off. Let's take a closer look at the stakes: FP developers are aware of the comparative scarcity of FP jobs. FP developers are perfectly capable of delivering OO software. The typical FP developer *foregoes safe, abundant, high-paying OO jobs* so that they may develop in their favorite paradigm. Any manager who considers FP may therefore expect to run a highly motivated and highly performing team. Hardly the kind which the drive-by headhunter will cripple during the most critical phase of development. You are safe to infer: FP, tight and loyal team.

## Myth-busting

FP adoption has been hindered by a number of misconceptions. Let's set the record straight!

### There are no libraries!
It depends on the language and the runtime. The most popular FP languages today run on the JVM and feature seamless Java interoperability. In other words: you may use any existing Java library you wish with them.

### I don't trust the runtime!
If the runtime is a concern, you have a wide selection of languages to choose from which are designed for battle-tested runtimes. Scala and Clojure run on the JVM, F# runs on the .NET CLR, Erlang and Elixir run on BEAM. All of these have proven their worth in production under extreme workloads[^10] [^11] [^12] and are actively maintained by large, reliable corporations.

### I can't reuse!
Whether it's engineering skill or some trusted piece of in-house code, migrating to FP doesn't mean throwing the baby out with the bathwater. You may pick a language that interoperates with the code or skill you want to reuse. Scala and Clojure interoperate with Java. F# interoperates with C#. ClojureScript interoperates with JavaScript and the list goes on.

### It's slow!
In today's world of distributed computing, there is no excuse for complaining about performance without taking parallelism and scalability into account. If you develop performance-sensitive software for single-threaded execution, then FP might not be the right tool for you.

### It's only good for mathematicians and academics!
The many and varied success stories of FP adoption by industry disprove this. Be it networking[^13], messaging services[^14], finance[^15], insurance[^16] or web development[^17], FP languages are proving versatile and capable tools.

## Conclusion
Functional Programming is a tool. A mature, stable and reliable tool with a track record reaching as far back as the '80s. Nevertheless, not more than a tool and therefore only useful when applied to the right problem. From the business perspective, is safe to say that the current era of computing (i.e. distributed in a global scale) presents problems that are a good fit for this tool. Companies who succeed in putting FP teams together are on their way to building high-quality software and ensuring their long-term viability.

[^1]: Steve McConnell (2004). Code Complete: A Practical Handbook of Software Construction, Second Edition. Microsoft Press. p. 521. ISBN 978-0735619678.
[^2]: Baishakhi Ray, Daryl Posnett, Vladimir Filkov, Premkumar Devanbu (Novermber 2014). [A large scale study of programming languages and code quality in GitHub](https://dl.acm.org/doi/10.1145/2635868.2635922). FSE 2014: Proceedings of the 22nd ACM SIGSOFT International Symposium on Foundations of Software Engineering.
[^3]: Sebastian Nanz, Carlo A. Furia (August 2014). [A Comparative Study of Programming Languages in Rosetta Code](https://arxiv.org/abs/1409.0252). Proceedings of the 37th International Conference on Software Engineering (ICSE'15), pages 778-788. IEEE.
[^4]: Steve McConnell (2006). Estimation: Demystifying the Black Art (Developer Best Practices). Microsoft Press. p. 56. 978-0735605350.
[^5]: Herb Sutter (March 30, 2005).The Free Lunch Is Over: A Fundamental Turn Toward Concurrency in Software. Dr. Dobb's Journal.
[^6]: John Markoff (June 10, 2008). [Apple in Parallel: Turning the PC World Upside Down?](https://bits.blogs.nytimes.com/2008/06/10/apple-in-parallel-turning-the-pc-world-upside-down). New York Times - Business, Innovation, Technology, Society.
[^7]: Joe Armstrong (August, 2014). Programming Erlang, Second Edition - Software for a Concurrent World. The Pragmatic Programmers. p. xiii. ISBN 978-1937785536.
[^8]: Peyton Jones, Andrew Gordon, Sigbjorn Finne (January 1996). Concurrent Haskell. Proceedings of the 23rd ACM Symposium on Principles of Programming Languages.
[^9]: Ricardo Terrell (July 17, 2018). Concurrency in .NET : Modern patterns of concurrent and parallel programming. Manning Publications. p. 23. ISBN 978-1617292996.
[^10]: Raffi Krikorian (August 16, 2013). [New Tweets per second record, and how!](https://blog.twitter.com/engineering/en_us/a/2013/new-tweets-per-second-record-and-how.html). The Twitter Blog.
[^11]: Whatsapp team (January 6, 2012). [1 million is so 2011](https://blog.whatsapp.com/1-million-is-so-2011). The Whatsapp Blog.
[^12]: Yan Cui - Lead Server Engineer at GameSys. [The F# solution offers us an order of magnitude increase in productivity](https://fsharp.org/testimonials/#yan-cui). F# Testimonials.
[^13]: Johan Bevemyr. [How Cisco is using Erlang for intent-based networking](https://codesync.global/media/https-youtu-be-077-xjv6plq/).
[^14]: [Who uses Erlang for product development?](http://erlang.org/faq/introduction.html) Erlang homepage.
[^15]: OCaml Success Stories. [Jane Street](https://ocaml.org/learn/success.html#Jane-Street). OCaml homepage.
[^16]: Grange Insurance. [Grange Insurance parallelized its rating engine to take better advantage of multicore server hardware](https://fsharp.org/testimonials/#grange-insurance-1). F# Testimonials.
[^17]: [Write simple, fast and quality type safe code](https://reasonml.github.io/). ReasonML homepage.