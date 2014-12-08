---
layout: post
title: Why infographs have an edge?
author: pvto
excerpt: I explain 3+1 aspects that make interactive infographs superior to traditional document based reporting.
---

[Information visualisation](http://en.wikipedia.org/wiki/Information_visualization) as meaning graphing, plotting and projection of data, is familiar to everybody.  *Infographic* then is a term coined for graphs with combined textual information, possibly embodying some motion and interaction.  This post introduces 3+1 aspects that make interactive infographs superior to traditional document based [reporting](http://en.wikipedia.org/wiki/List_of_reporting_software), from the coder's perspective, unexclusive.

![info](/img/infographs-with-d3js/spat-scal.png)

Interactive infographs were first demonstrated by big news agents like [N.Y.Times](http://www.nytimes.com/), and they have flourished on subjects as diverse as [presidential campaign funding](http://data-informed.com/data-visualization-following-the-money-in-the-presidential-campaign/), [fashion](http://www.nytimes.com/newsgraphics/2013/09/13/fashion-week-editors-picks/), and [bioscience](http://circos.ca/intro/data_visualization/).  Their interactive aspects were powered by [client side](http://en.wikipedia.org/wiki/Client_side) Javascript visualisation libraries like [d3.js](http://d3js.org/).

If you are in a hurry, do skip directly to [Three new aspects of infographing](#three-aspects).

##Introduction: Draw to grasp

    1 2 3
    4 5 6

What does this data mean?  Graphs and charts assist in such questions.  They help in the [interpretation](http://en.wikipedia.org/wiki/Scientific_modeling), modeling, [validation](http://en.wikipedia.org/wiki/Data_validation), pruning, [mining](http://en.wikipedia.org/wiki/Data_mining), enhancing, and communication of data.

The implications of a set of data are painful to grasp from any textual representation.  You will get reactions like the following, regardless of data size.

![Big data oh the probs](/img/infographs-with-d3js/big-data-oh-the-problems.jpg)  

Now when looking at a graph we employ our visual faculties with their sophisticated heuristics to extract information from the world.  Visual understanding may operate on a horizontal level, too.  A visual impression within the visual memory will help memory to hold.

![bars info](/img/infographs-with-d3js/bars-info.png)

These are characteristics of all visualisations, shared by interactive infographs and their static predecessors alike.  The brain may err by seeing [trends](http://en.wikipedia.org/wiki/Trend_estimation) where there are none and by doing overinterpretation, but visuals will nevertheless aid and guide other more formal [methods](http://en.wikipedia.org/wiki/Statistics).  In the area of monitoring, a graphical (well understood) representation shows its absolute strength.

## Three new aspects of infographing
<a name="three-aspects"/>

[Mikhail Bakhtin](http://en.wikipedia.org/wiki/Mikhail_Bakhtin) believed that the use of language is inherently dialogical.  Bakhtin suggests that this may be an aspect of life itself, and while looking at systems theory, chaos, and [game theory](http://en.wikipedia.org/wiki/Game_semantics), we get different kinds of mathematical support for this idea.

Anyway, visual interaction added to a graph would enhance it in three ways.  Firstly, interaction is likely to increase reading time spent with the graph.  Secondly, it assists towards the memorisation of information.  And thirdly, interaction could prod towards [hypothesis formation and validation](http://en.wikipedia.org/wiki/Scientific_process) by the reader/user, thus solidifying the communicative aspects of graphs.  [A good online example](http://www.theguardian.com/world/interactive/2013/apr/30/violence-guns-best-selling-video-games) shows how violence is used within top 50 computer games of 2012, allowing reader to quickly dig into questions of interest.

### 1. More time with the graph

Interaction will create interest in the average user, and interest will lead to time investment.

![exposure-focus](/img/infographs-with-d3js/RR.png)

The designer should keep in mind that too many features will distract rather than communicate.The possibility to link image features should foster sharing.

There may be a tradeoff however between graph interaction time and time spent reading the rest of the page.

### 2. Memorisation

View time is a commonly measured web user statistic.  Researchers ([1][ref1], [2][ref2]) suggest that time of exposure is related to the degree of correctness of memories, as well as to the ability to recall specific memories after different periods of time.

![exposure-focus](/img/infographs-with-d3js/RF.png)

### 3. Learning through interaction

We find [suggestions](http://www.ted.com/talks/alison_gopnik_what_do_babies_think) that the human learning processes operate on much the same principles as the [scientific method](http://en.wikipedia.org/wiki/Scientific_method), that is, by hypothesis-formation, trial and error, reinforcement of successful behavior, and by banishment by counterexample.

[Hypothesis-formation](http://en.wikipedia.org/wiki/Scientific_method#Hypothesis_development) operates by [query](http://en.wikipedia.org/wiki/Query_(complexity)), and to do, we need a view on the target domain.  That an interactive graph provides.

Representation is never value neutral.  Representational ethics dictates that one should inform their reader of any shortages and discrepancies of the data in question.

![bar noise](/img/infographs-with-d3js/bar-noise.png)

##+1. Make it fast

From the [engineer](http://en.wikipedia.org/wiki/Engineer)'s perspective, latency may not be all, but low latencies and short wait times are actually indispensable.

As graphing goes, the relevant question is how to show a graph and pass minimal data over the connection so that the reader still gets the information they need.

![arrows right](/img/infographs-with-d3js/arrows-flow.png)

Preprocessing an image on the server side may often be the right thing to do.  Nevertheless if the amount of data to pass is smaller in bytes than that of the generated image, selection would favor client side graphing with no exception.

Where online graphing is needed, there are d3js based frameworks available that help make use of accumalated online data ([1][ref4], [2][ref5], [3][ref3]).  [D3js](https://github.com/mbostock/d3/wiki) itself supports merging.

![note](/img/note.png)

The shift from static to dynamic graphing has been a change for the better and more solid, both in terms of reinforced information sharing, from the human perspective, and of reduced data transfer, from the technical perspective.

We do these things at [Solita](http://www.solita.fi/).

[ref1]: http://dl.acm.org/citation.cfm?id=1993584
[ref2]: http://www.google.fi/books?hl=fi&lr=&id=m8qMjPF1NYAC&oi=fnd&
[ref3]: https://github.com/mlarocca/Dynamic-Charts
[ref4]: http://square.github.io/cubism/
[ref5]: http://jondot.github.io/graphene/
