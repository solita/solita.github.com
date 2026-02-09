---
layout: post
title: "Python in 2026: Popular As Ever, Avoided in Production"
author: solita-jonte
excerpt: >
  Python runs everything from LEGO to NASA missions — yet most enterprises still hesitate to bet their core systems on it. This post digs into that paradox: how Python became the world's most popular language, why it's still seen as too risky for serious production, and what changes within once you treat it as a friend instead of an enemy.
tags:
  - python in production
  - python performance
  - enterprise software development
  - software architecture
  - backend development
  - dynamic typing
  - performance optimization
  - programming languages
  - software engineering best practices
---
I'm biased toward Python for many reasons. I'm also one of the few who've watched my own Python scripts place *$1.5M* worth of asset orders in my personal brokerage account — but that's a story for another time. The
point is: I trust Python with systems where mistakes are expensive.

In this post, I'll explain how Python became the world's most popular programming language, yet is often sidelined in enterprise production. Why? And should it be?

![Popularity vs. Production](/img/2026-02-python-pop-prod/balancing-scale.jpg)

## Popularity
Python became the world's most popular language in [2021](https://www.tiobe.com/tiobe-index/), when it left the last two languages (C and Java) in the dust. Thanks to its ease of use and lower friction, it became the
primary choice in [academia](https://dl.acm.org/doi/pdf/10.1145/3626252.3630761) as well as for quick hacks. [Harvard](https://harvardonline.harvard.edu/course/cs50s-introduction-programming-python),
[MIT](https://iblnews.org/story/mits-intro-to-cs-using-python-on-edx-reaches-1-2-million-enrollments),
[Princeton](https://collegeparentcentral.com/princeton/online-courses/introduction-to-computer-science-and-programming-using-python/2127148731),
and even [my local uni](https://www.chalmers.se/utbildning/dina-studier/hitta-kurs-och-programplaner/kursplaner/TDA548/) now use Python for their introductory courses. At Google and Amazon, it's a first-class language,
and the other cloud providers (Microsoft, IBM, Oracle, etc.) fully support it for serverless and their other APIs.

For many students and professionals — myself included — the low barrier to entry and high productivity, without any safety net, is love at first sight. I *really* enjoy writing Python code: I'm able to focus on the
problem at hand, and can ignore all formalism. And the freedom! Oh boy, the freedom.

For ML and AI tasks, Python is the default language. TensorFlow, PyTorch, Pandas, and scikit-learn all effectively require you to jump through hoops to use anything else.

But what *exactly* made it a giant in the first place? It's trivial; just answer this: how many languages do you know of that can open a browser tab for every HTML file in some subdirectory, only using the standard
library and a couple of lines of code?

```python3
import pathlib, webbrowser

for htmlfile in pathlib.Path(".").rglob("*.html"):
    webbrowser.open(htmlfile.absolute().as_uri())
```

Some will say that's compact and convoluted. I say brief and beautiful! But let's not get bogged down by aesthetics here. No main function. No error checking. No type checking. Just. Make. It. Happen.

Quite the opposite of what an [Architecture Astronaut](https://en.wikipedia.org/wiki/Architecture_astronaut) would come up with: this has nothing to add, nothing to subtract, and if you understand those two lines of
code, you know everything there is. No interfaces, no objects to orient, no errors to handle, no types to take care of, no main to declare. A noob who sees it can understand it — it's almost English. And this
simplicity, of course, not only applies to browsers and files. For _All The Things_, Python makes it easier.

![Rise up](/img/2026-02-python-pop-prod/up-up-up-up-up-uu-uupp.jpg)

And let's not forget the feeling. I can script _anything_ in a few lines; that's addictive!

## To Use or Not To Use
When building desktop and mobile apps, Python is not where sane people tend to look. Performance is equally off-brand. Even when it comes to web dev, Python still suffers from a bad rep (arguably due to the horrific
standard library web server implementation). There have however, been stellar industry-standard web frameworks for [16 years](https://flask-dev.readthedocs.io/en/latest/changelog.html#version-0-1). Assuming you've
created the app in a couple of lines, this is how easy it is to serve an HTML page:

```python3
@app.route("/")
def index():
    return '<a href="https://tinyurl.com/iamdeveloper">Goodnight!</a>'
```

My two code examples here are not outliers; Python is generally extremely concise and productive, including for web dev.

What's more, many performance problems are [fixable](https://numba.pydata.org/). I'm one of the few who should know, as I've written an online 3D [game](https://store.steampowered.com/app/3462870/Landslip/) with
physics, skinning, and terrain generation. In Python. From scratch. Able to reach [500 FPS](https://www.youtube.com/watch?v=oLDnQELxKsM) on my old junk PC. (That's a whole 'nother blog post.) As you see, the performance
ceiling isn't where many think.

In regards to type information, error handling, and hygiene, most risks can be mitigated with a [linter](https://github.com/astral-sh/ruff) and a [static type checker](https://github.com/microsoft/pyright) (pre-commit
time).

If Python _can_ do all these things — and easily too — why is nobody using it for enterprise production?

## When its strengths become its weaknesses
Python is made for scripting, and it's super easy to get started. But if you are used to letting the IDE take care of most problems at the time of writing code, there's a real risk of runtime problems unless guardrails
are put in place. And frankly, most humans are lazy. Good programmers more than most. So while it's easy to fix, those that don't know, don't know — and don't want to know. An
[old study](https://arxiv.org/pdf/1409.0252) from 2015 shows Python to be one of the most concise languages, but also one of the most error-prone. The quick-hack qualities that propelled its popularity also make it easy
to misuse at scale, which in turn fuels enterprise distrust.

When it comes to data scientists, analysts, and researchers, they aim for experimentation and insights. Their incentives have nothing to do with long-term maintainability for large teams. So we can't take their advice on
what to code our enterprise systems in.

[Half](https://survey.stackoverflow.co/2023/#most-popular-technologies-language-prof) of professional developers (have to?) *use* Python, but it seems highly disliked by those who don't take it to heart. Looking at my
own employer, only [6% prefer Python](https://dev.solita.fi/2024/12/03/developer-survey-2024.html) over other languages. From talking to developers, I believe that the main reason for the dislike is that people feel
it's "like Java but error-prone and slow." To which the response should be: [if my grandmother had wheels, she would have been a bike](https://www.youtube.com/watch?v=A-RfHC91Ewc).

![Grandmother is a bike](/img/2026-02-python-pop-prod/bicycle-grandma.jpg)

But of course, there is a kernel of truth to that. On the other hand, nobody avoids knives because "that's what Jack the Ripper used." I say: better to learn how to use a knife, and use it with caution. And I realize
that no amount of preaching is going to move the needle even one bit. Which also tells me that you, dear choir, who've made it this far are part of the few Chosen Ones.

## Causality vs. Python: 1–0
We all know Python is used by everyone and their Uber driver. [NASA](https://www.python.org/about/success/usa/) uses it, [banks](https://www.fullstackpython.com/companies-using-python.html) use it,
[Reddit](https://github.com/reddit?language=python)'s built on it. Everyone from [Netflix to Pfizer](https://www.superprof.co.uk/blog/what-companies-use-python/) uses it for orchestration and analysis. But. And there's a
big but. The enterprise adoption has to do with the arrow of time. Let me explain.

Nobody who's deciding on a language for their platform:

1. Spends years learning Python,
1. Discovers how productive it is,
1. Learns about static type checkers,
1. Learns how to fix performance bottlenecks,
1. Builds confidence that it can work in enterprise production,
1. And then goes back in time to pick Python as their foundation.

By the time you've climbed that ladder of understanding, the choices have already been made. Python is the chicken, and nobody's the egg.

Many people realize Python is highly productive, but very few know it can be highly performant. Most people get off the ladder way before they see that Python can be suitable for production.

Even MSc graduates who've used Python a lot for experimentation in small teams have no prior experience in working in large corporations with enterprise solutions. And surely they've all made abominable programming
mistakes during their years in college, so they'd be the first to admit that Python is too permissive for its own good. And a lab exercise in computer science is a far cry from a 100-person development department where
everyone is trying to churn out features.

For the staggering few remaining proponents, there's one more hurdle: they hear that YouTube, Instagram, and Dropbox rewrote parts of their stack in other languages for performance. Counterfactual reasoning is hard.
Would YouTube have been written by 2 people in a small office above a pizzeria if it weren't for Python? Who knows.

So the enterprise reasoning goes "better safe than sorry." And truth be told, that might be the right way to go.

## Final words on enlightenment
But if you're the type of company that dares to think different — if you've gone all the way up that ladder, eaten the egg, and reversed the arrow of time — then, just like a Buddhist monk, you'll have focused your ass
off for years, just to realize when you pop out at the top of enlightenment, that it was all _so easy_ all along.

And then, just like the monk, you're in for a _really_ good time. Aesthetically and productively. And more than ever, you'll be able to focus on the big picture, not on the code.

But _definitely_ don't take my word for it. Love is blind, you know.

_Disclaimer: The content, ideas, and the way they're expressed in this blog post are entirely my own. However, Solita FunctionAI was utilized for grammar, spelling, and stylistic review, and ChatGPT was used for
visualizations._
