This post is inspired by a discussion at work about the meaning of the word **expressiveness** as it relates to software development. It got me thinking and reading a lot.

The [original post](https://www.tuomistolari.net/blog/2024/10/14/abstraction-alienation) can be found here.

# Made up realities

In our quest to understand and simplify the world, we often rely on **models** — whether they are mathematical frameworks, physical simulations, linguistic systems, or even programming languages. Models are pretty much all we have.


These models serve to break down complex systems into something more manageable. However, the **act of abstraction has a penalty**: we increasingly deal with problems that have nothing to do with the reality they represent.

# The map is not the territory

The phrase "the map is not the territory” or “the word is not the thing” coined by Alfred Korzybski, is a perfect metaphor for this phenomenon. A map is a simplified model of a complex landscape, and while it can be incredibly useful for navigation, it inevitably leaves out details. More importantly, it may introduce **distortions** — what I’d like to coin as **modelspace problems** — that only exist because of the simplification. In the real world, a mountain might be traversable, but on a map with insufficient detail, it might appear impassable or even nonexistent.

This is exactly the kind of issue we encounter when working with any abstraction.

# The word is not the thing

Language itself can be seen as a model of reality. Words are abstractions—simplified representations of the complex objects, concepts, or experiences they refer to. As such, language is in no way excluded from having modelspace problems.

A classic example: Different languages divide the spectrum of colors in different ways. Some languages have fewer words for colors, which seems to influence how speakers actually perceive and categorize colors. This isn’t a problem with the nature of color itself but a problem with the linguistic model used to describe it.

Similarly, **vagueness and ambiguity** are linguistic modelspace problems. A word like "bank" can refer to both a financial institution and the side of a river. This ambiguity can lead to confusion or misunderstandings, but the problem exists only in the linguistic model, not in the physical world where these two "banks" are easily distinguished.

Another example from linguistics is the **Sapir-Whorf Hypothesis**, which suggests that the structure of a language influences how its speakers perceive the world. If a language lacks a word for a particular concept, speakers may find it more difficult to conceptualize or express that idea. The problem of limited conceptualization arises not because the concept doesn’t exist in reality, but because our languages imprison our thinking.

# The vector is not a triangle

In programming, we deal with models exclusively. Every programming language is a model designed to abstract the complexities of machine operations and make problem-solving more intuitive for developers. These abstractions introduce **modelspace problems**. For instance, programming languages that offer high-level abstractions, such as garbage collection, simplify memory management, but can create new issues like performance bottlenecks or memory leaks that don’t exist in languages with manual memory control. Therefore, optimizing the language becomes the problem we solve for.

Similarly, paradigms like object-oriented programming (OOP) or functional programming come with their own abstractions and assumptions about how problems should be structured and viewed. As a result, they introduce complexities, such as inheritance issues in OOP or immutability overhead in functional programming.

Just like in other fields, it is absolutely common to see a sort of **hyperreality** emerge in programming. **The abstraction becomes more important than the task it was designed to solve.**

Programmers end up focusing more on improving the structure or elegance of the code (the form) than on the real-world problem the software is meant to address. The model takes on a life of its own, displacing and multiplying the original problem it was supposed to solve.

# Alienation

I feel that many problems exist solely because of how far we’ve abstracted. As humans, we are all stuck inside models and every day they become more abstract: from money, to literature, to social issues. **The ability to distinguish what is objective reality and what is emerging from the models is almost impossible.**

A huge piece of the issue is that we all tend to fall in love with the models themselves - their convenience and ability to sweep inconvenience from our eyes. We love them to the point of preferring to have money in our bank account rather than experiencing something with that money.

Why do I write about this problem? Because I think every one of us faces this problem and I believe that in abstract fields the alienation we end up feeling stems from the above problems.

So I ask myself: “How does what I’m doing actually help?” When I make a fire, it is apparent. When I try to figure out why some cloud service sometimes isn’t able to connect, then it is less apparent.

As we become more involved in the world of ever deeper abstract models, it causes a sense of detachment from the real world and of the objective reality around us.

In fact, I see no end in how far you can drift into solving problems that only exist in model space. You may even lose sight of what you are trying to solve. As an architect, I suffer from this immensely, as the problems I deal with day to day exist entirely in model spaces.

Ultimately, I hope that after reading this you’ll have a word and a concept you can use to point to and recognize the paradox that we live in and are all imprisoned by.

And maybe we should consider abstracting less.

More on this topic:

[Linguistic relativity](https://en.wikipedia.org/wiki/Linguistic_relativity)

[Gestell](https://en.wikipedia.org/wiki/Gestell)

[Navigating the Hyperreal: A Journey Through Jean Baudrillard's Simulacra and Simulation](https://medium.com/@thecuriousphilosopher/navigating-the-hyperreal-a-journey-through-jean-baudrillards-simulacra-and-simulation-ea30bad3fa69)

[Twin paradox](https://en.wikipedia.org/wiki/Twin_paradox)

[Uncertainty principle](https://en.wikipedia.org/wiki/Uncertainty_principle)

[Gödel's incompleteness theorems](https://en.wikipedia.org/wiki/G%C3%B6del%27s_incompleteness_theorems)

[Video on related topics](https://www.youtube.com/watch?v=sA30Ap3Uh4A)

[The eleventh word](https://www.theparisreview.org/blog/2020/10/05/the-eleventh-word/)
