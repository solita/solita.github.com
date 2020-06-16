---
layout: post
title: Supporting Open Source Clojure Software Through Clojurists Together
author: juholei
excerpt: Clojurists Together is an organisation dedicated to funding and supporting Clojure open source software. Here's how it works and what our experience as a member has been like.
tags:
- Clojure
- ClojureScript
- open source
---

> Clojurists Together is an organisation run by Clojars, dedicated to funding and supporting open source software, infrastructure, and documentation that is important to the Clojure and ClojureScript community.

[Clojurists Together](https://www.clojuriststogether.org) was started at the tail end of 2017 and has been running now for about two years. Solita was one of the founding company members and has been a member ever since. Clojurists Together works by collecting monthly (or yearly) donations from its individual and company members. These funds are then used to support open source software development on a quarterly basis. Each quarter a few projects are chosen for funding.

The current on-going funding for Q3 of 2019 (August - November) targets four projects: [Shadow CLJS](http://shadow-cljs.org/), [Meander](https://github.com/noprompt/meander), [Calva](https://github.com/BetterThanTomorrow/calva) and [CIDER](https://cider.mx/). Each project gets paid $9,000 over three months. [In their funding announcement posts](https://www.clojuriststogether.org/news/q3-2019-funding-announcement/) Clojurists Together provide detailed explanations of what the projects are and what their developers aim to achieve with the funding they receive. These coupled with monthly updates from the projects ([August update](https://www.clojuriststogether.org/news/august-2019-monthly-update/), [September update](https://www.clojuriststogether.org/news/september-2019-monthly-update/)) make it easy for the members and the wider Clojure community to see and understand what is being funded and how the work is progressing.

In my opinion, Clojurists Together has done a great job selecting the projects to fund. For example, looking at the projects currently being funded, CIDER is a massively important piece of software for clojurists. Even if you aren't using emacs with CIDER, its infrastructure in nREPL, cider-nrepl and orchard provide a better REPL and development environment for clojurists regardless of their editor of choice. This is very well visible in another currently funded project, Calva. Calva aims to provide a first-class Clojure development environment in Visual Studio Code and builds on top of all these infrastructure pieces that are powering CIDER. As Visual Studio Code is an immensely popular editor these days, providing an easy and well-working Clojure environment for it can make Clojure much more accessible to beginners.

Another currently funded project, Shadow CLJS, is quickly becoming the best ClojureScript build tool out there. With current funding round going towards React Native and expo support, coupled with the existing Node.js features and npm support, it is the easiest tool for ClojureScript projects, especially when targeting something else than the browser. This makes it easy and viable to choose ClojureScript in these kinds of projects, adding to the use cases of the language.

Looking back at the previously funded projects, most Clojure developers have probably used at least a couple of them at some point: [clj-http](https://github.com/dakrone/clj-http), [Figwheel](https://figwheel.org), and  [ClojureScript](https://clojurescript.org) itself, to name a few, are fundamental building blocks of many projects and as such deserve to be funded to make their continued support viable. Funding such widely used projects also provides advantages to a large part of the Clojure community. Another funded project to highlight is [cljdoc](https://cljdoc.org), which provides a central place for documentations of Clojure libraries.

Clojurists Together just recently published [results of their membership survey for Q4](https://www.clojuriststogether.org/news/q4-2019-survey-results/). Through this survey the members can give feedback on what kind of projects they would like to see funded in the future and also give feedback on how the program is being run. The results provide some interesting insights, so it's worth checking out even if you are not a member.

Solita has gained a lot through the use of both open source and Clojure. Clojurists Together provides us an easy way to give back to these communities and help the continued support of established tools, as well as helping new shiny things come into life. If you or your company wants to support open source, I can wholeheartedly recommend Clojurists Together as a way to do so.
