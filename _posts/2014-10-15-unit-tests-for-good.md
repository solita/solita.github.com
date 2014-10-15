---
layout: post
title: Unit tests, for good
author: pvto
excerpt: In an opening keynote to Reaktor dev day 2014, Erik Meijer declared unit tests a general waste of time.  Mr. Meijer's routine use of overstatement offers a really nice target for nitpicking.
---

In an opening keynote to [Reaktor dev day 2014](http://reaktordevday.fi/2014/), [Erik Meijer](http://reaktor.fi/blog/erik-meijer-software-eating-world/) declared unit tests a general waste of time.  Mr. Meijer's routine use of overstatement offers a really nice target for nitpicking.

According to Erik Meijer, developers should dream and drink code. It is eating the world away.  "TDD is for pussies", Meijer hustled while urging us to take risks, not unlike recent ideas of [intrapreneurship](http://en.wikipedia.org/wiki/Intrapreneurship), and to resort to production time testing like [Netflix does](http://techblog.netflix.com/2012/07/chaos-monkey-released-into-wild.html).

Sounds quite refreshing!  Yet eating and drinking are poor metaphors for code. 

![idea](/img/unit-tests-for-good/idea-2.png)

With *waste*, Mr. Meijer refers to a [much misunderstood Kanban concept](http://leanandkanban.wordpress.com/2011/03/22/lean-is-about-eliminating-waste-right/).  He did not make absolutely clear, in short, in what way a regression test is waste over longer periods of time.

During the off hours, a colleague asked Mr. Meijer about TDD, but he refrained from pointing out which he would mean, [test-driven design or test-driven development](http://www.drdobbs.com/architecture-and-design/test-driven-design/240168102), or did he even mean *unit testing*, in a more generous manner.

Erik Meijer seems to be suggesting that perfected hackers get it right at the first time, since they live their lives within code, and afterwards they will never forget either.

Perhaps to compensate, he insisted on the importance of [a closed feedback loop](https://www.google.com/search?q=programming+feedback+loop&tbm=isch) during a project run.

A unit test yields no feedback loop, of course!  (Sarcasm fully intended.)  Suffice it to say that a large part of code today is written in environments for which there is no REPL for instant feedback.

Whatever Mr. Meijer represents, he stands in stark contrast to a [top-down](http://en.wikipedia.org/wiki/Top-down_and_bottom-up_design) [waterfall](https://www.google.com/search?tbm=isch&q=waterfall+model&cad=h) development strategy (whatever that is).  Within this frame of idealisation, methodological everyday choices do not matter much, nor do failures.  Days and nights do not exist, only pizza does.  Resources, including personal resources, are approximated to infinity.

![cowboy](/img/unit-tests-for-good/mario_cowboy.jpg)
*Image by [david_a_l](https://www.flickr.com/photos/david_a_lea/3247217194/)*

It is cordial, of course, from a person to attack shortsighted belief in methodology, be it *TDD* or *agile* or *scrum*.  Like Erik Meijer aptly pointed out, the software business needs to grow up.  Developing a healthy *criticality* just might be a part of that process.

Ideally, we could do without interfering methodologies like TDD.  If you really learn to code effectively, to proceed systematically, and do that with blinding speed, your "code wins the argument", like Mr. Meijer cited.  And who says you couldn't win a billion people audience for your coding feats?

For an average coder, it is statistically infeasible to claim such a future.  Everybody must, willing or not, deal with the romantic hacker myth that suggests everything for the elect.

![thrash](/img/unit-tests-for-good/trash-line-2.png)

Getting more to the point, it is true that writing a dozen preparatory tests won't bring anybody nearer to anything novel, and in that way TDD and even unit tests may be a bit of a burden.  Prelude tests won't build your service either.  From that narrow vista, tests are a waste of time.  

Let's play a simile game.

Imagine a surgeon who gets the idea that only time matters.  Away with old-fashioned clinical hygiene!  Away with keeping up with professional literature!  Those only hinder from the only thing that matters – hours with the scalpel!

In his mad scientist way, our type may or might not reach to some invaluable medical knowledge.  Most likely he would go to jail before his first term was over.  I'm skipping his patients' destiny out of abstract mercy.

![idea](/img/unit-tests-for-good/threads.png)

As everybody knows, there are situations that urge for as thoroughly dependable code as possible.  Being a ninny and writing a unit test seems such a smart and straightforward thing to do in that kind of situation...

And growing up does mean dependability too.  Perhaps we should say, rather than dubbing them as waste, that unit tests are a necessary evil.