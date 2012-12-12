---
layout: post
title: "Solita Code Tasting 2012: Raspberry Pi"
author: n1ko
excerpt: Last week we had the pleasure of hosting two open Coding Dojos for 30 enthusiastic programmers. The theme was Raspberry Pi and creating your own web server that could serve our demanding challenger.
---

### The theme ###

We had been planning to host an open Coding Dojo for some time, but we had
difficulties coming up with an interesting theme.
Some ideas circled around things like HTML5 and JavaScript (both of which had
been themes in our internal coding dojos).
But then it hit us! There's this new tasty thingie called
[Raspberry Pi](http://www.raspberrypi.org/), which is gaining interest within
[Solita](http://www.solita.fi) as well as worldwide.

[![rpi](/img/codetasting/small/rpi.jpg)](/img/codetasting/rpi.jpg)

[Raspberry Pi](http://www.raspberrypi.org/) (or just RPi) is basically an ARM-based minicomputer.
The newest revision has a 700Mhz ARM11 CPU with 512M of RAM. The device is about the size of a
small fist and uses an SDHC card for mass storage. It's pretty much the perfect device for tinkering
and testing, especially since it also has plenty of GPIO pins.

### tasting.solita.fi ###

The event's name was coined a day before our PR material was sent for printing, on a Saturday evening.
I was sitting in a bus, trying not to throw up after a boat trip with some of my co-workers, when
[Anna](http://github.com/annaragh) nicely reminded me about the deadline for the material.
After some pretty awful brainstorming, we came up with the name, and luckily it was a pretty decent one.

[![tasting_form](/img/codetasting/small/tasting_form.png)](/img/codetasting/tasting_form.png)

After that, it was just a matter of finishing up the application form on
[tasting.solita.fi](http://https://github.com/solita/codetasting-form) and trying to get it to people's attention.

Luckily, we got tons of good applications and were able to hand-pick the participants.
Some very promising guys and gals were left behind, sorry!

### Helsinki edition ###

The first of the two identical events was hosted at our Helsinki office. Even though we had the whole day to prepare for our guests, we still somehow managed to blow our schedule. The final touches were made while the participants were arriving.

[![steve_asiakkaat](/img/codetasting/small/steve_asiakkaat.jpg)](/img/codetasting/steve_asiakkaat.jpg)

Anyway, back to the programme. We kept the propaganda light since we were anxious to get started with the real stuff. You can see [Ari](http://github.com/aautio) presenting our customers in the picture above in our very nice movie theater called Steve, named after Steve Jobs.

[![esko_esittelee](/img/codetasting/small/esko_esittelee.jpg)](/img/codetasting/esko_esittelee.jpg)

After the official brainwashing session, we toured the participants around our office and arrived at our break room Heikki (named after our founder Heikki Halme).

[![rpi_pornoa](/img/codetasting/small/rpi_pornoa.jpg)](/img/codetasting/rpi_pornoa.jpg)

[Esko](http://github.org/orfjackal) started off by explaining how the [rpi-challenger](http://github.com/solita/rpi-challenger) worked and what the participants' challenge would be.

You can read more about [rpi-challenger](http://github.com/solita/rpi-challenger) and the challenge in [Esko's post](/2012/12/11/codetasting-code-behind-the-event.html).

### Coding in Helsinki ###

[![koodestelua](/img/codetasting/small/koodestelua.jpg)](/img/codetasting/koodestelua.jpg)

After the challenge was given and people started working, I was really anxious to see how the challenge would work out. Would it be enough of a challenge for an evening? Or perhaps it would be too difficult for the students? We used Git as our revision control system, and the participants had a little bit of trouble with Git at first, but after they got their repositories up & running, everything started to run really smoothly.

[![koodestelua2](/img/codetasting/small/koodestelua2.jpg)](/img/codetasting/koodestelua2.jpg)

The challenge allowed the participants to choose their technology. Since the participants only had a short amount of time to build a web server, a language like [Python](http://www.python.org/) was a logical choice, and all teams except one chose Python. And the team that didn't pick Python went with [Node.js](http://nodejs.org/), which is also extremely well-suited for a task like this. Even though the majority wrote their servers in [Python](http://www.python.org/) we saw plenty of different approaches to tackling the tasks. Different libraries were used and it was fun to see how differently people were solving the tasks.

[![tulokset2](/img/codetasting/small/tulokset2.jpg)](/img/codetasting/tulokset2.jpg)

Since the [rpi-challenger](http://github.com/solita/rpi-challenger) was giving out points for each minute based on their success we were able to show live stats during the event. Just like in any good sport event, the competition was even.

[![tulokset1](/img/codetasting/small/tulokset1.jpg)](/img/codetasting/tulokset1.jpg)

The winning team was able to gather 488 points, an awesome score! They were also the only team writing unit tests for their implementation. Coincidence? Probably not.

[![palkintojen_jako](/img/codetasting/small/palkintojen_jako.jpg)](/img/codetasting/palkintojen_jako.jpg)

Here is [Anna](http://github.com/annara) giving out prizes to the winning pair. Good job guys!

After giving out the prizes and wrapping up our main program for the evening, we had very enjoyable chats with some of the participants. Hopefully we will see your applications in our recruitment inbox too ;)

### Tampere edition ###

The Tampere version of this event was hosted the very next evening (5th of December). In our Helsinki event we hosted 14 people, but since the Tampere event was a bit more popular, we decided to pick 16 people. There were just too many good applicants!

[![tre_koodestelu](/img/codetasting/small/tre_koodestelu.jpg)](/img/codetasting/tre_koodestelu.jpg)

The program was pretty much the same as in Helsinki; light propaganda, tour around the offices, ferocious programming, beer, pizza, beer and getting to know each other.

[![tre_koodestelu2](/img/codetasting/small/tre_koodestelu2.jpg)](/img/codetasting/tre_koodestelu2.jpg)

The big difference between the Tampere and Helsinki events was that we saw a bigger diversity between the technologies chosen and applied. This is probably explained by the fact that TUT uses C++ in their courses rather than Python, which is used at Aalto university. Some teams went with Node.js, others with Python, and one team even went with Java.

Just like the night before, we started up slowly with some Git trouble, but after everybody got their repositories going and managed to get their web server running, things started to pick up. The teams were even more even in Tampere than in Helsinki, and the top two teams were fighting for the prize till the last half an hour.

### See you next year? ###

We had great fun hosting these events, and hopefully the participants enjoyed them too. We are looking forward to hosting some more, so stay tuned!

P.S. And to those of you who didn't get picked this time, remember to watch this space and apply again! We had to leave some very good people out because of the large number of applications. Also, we're sorry about the limited space that we gave you to tell us about yourself. It clearly wasn't enough for some of you. Sorry about that again :(
