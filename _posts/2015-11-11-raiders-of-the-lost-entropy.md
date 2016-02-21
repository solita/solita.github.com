---
layout: post
title: Raiders of the lost entropy
author: lokori
excerpt: When entropy runs low, things are amiss. What, why and how to rectify the situation.
tags:
- entropy
- randomness
- random number
- PRNG
- rngd
- Haveged
- DevOps
---

*Entropy* in this context is essentially randomness. A source of entropy is a magic fountain which
pours forth a stream of random bits. This is intentionally a practical definition, not related to science and physics. When a modern
computer runs out of entropy things stop working and fail in a mysterious way. Why does this happen in our 
cloud based virtual servers and what can one do about it?

## Why do we need entropy?

We want certain things to be practically *unpredictable* in software systems. All cryptographic keys need to be generated safely, 
so that no one can predict the next generated key or deduce previous keys by working backwards from the last generated keys. The same applies to other domains,
for example, it would be awkward if one could deduce the next card from the deck in a poker game simply by looking on the cards dealt.
This has actually happened, see [Poker exploit tale from 1999](https://www.cigital.com/papers/download/developer_gambling.php). 

Any [pseudorandom number generator (PRNG)](https://en.wikipedia.org/wiki/Pseudorandom_number_generator) solution is essentially deterministic based on the initial seed number and algorithm
and therefore the whole sequence can be deduced by looking at a small part of the generated 
"random" number sequence. This is prevented by mixing random bits (entropy) to the sequence so that
the next number in the sequence is not a direct result of the previous. Even a small number
of entropy makes the stream essentially unpredictable (assuming the attacker does not see or 
control the contents of the entropy source).

As computer systems are somewhat deterministic by design, getting entropy means accessing
a source of randomness not directly linked to the current state of the system. Common sources
are I/O based: keystrokes, mouse movements, network events and such. This works fine on a
typical workstation or laptop. 

![Indiana](/img/raiders-of-the-lost-entropy/indiana_jones.png)

## Server side is different

Entropy can be drained quickly on a back-end server. Many keys are required for various events all the time.
Oracle JDBC driver needs some random bits for opening a database connection. HTTPS connections to 
web server require SSL handshake, which consumes some random bits. And so on. 

Usually there is no direct user I/O like keystrokes or mouse events, which means the server 
needs more entropy than a typical workstation, but actually has fewer random bits available. 

## How big a problem is this?

When entropy runs low, reading  from `/dev/random` blocks until entropy is generated. It's designed
to block infinitely. This means opening a connection to Oracle database can take arbitrarily long
as it happens to consume some entropy. No error message appears in a log as this works as designed. 

All sort of unpredictable and strange things can happen if entropy runs low. One important symptom that low entropy
is the cause of weird problems is that when you log in with SSH to investigate, things suddenly work fine. 
Some entropy is generated when a client logs in with SSH and this releases the waiting processes, at least temporarily. Further, when a human
interacts using remote shell, more entropy becomes available and everything is normal for a while. 

## Rise of the virtual machines

The rise of the virtual machines and various hypervisor technologies such as [Docker](https://www.docker.com/) has 
made this a major concern. I was unaware of the whole thing when I started programming server 
backend with Java years ago as the software used to run in a real physical computer. Entropy was just 
a curious theoretical concept in the university lecture materials.

Virtual machines do not have a physical interface, like keyboard or mouse. The same physical machine
can run many virtual servers so even if the physical server does have some small entropy available,
does the virtual server get much? VM's are hidden behind firewalls and routers so no arbitrary
packets arrive from the vast internet. The storage devices are not physical and can be quite
deterministic.

Many systems now have small embedded microservices each running in their own servers which further
reduces the randomness of execution. No human ever logs in with SSH. Unnecessary daemon processes
are not running these days.

The result of these developments is that the entropy easily runs low in a virtual machine. 

## Generating entropy

There are some known and researched ways to generate entropy if I/O events are not suitable. Such as:

1. [Hardware based random number generators](https://en.wikipedia.org/wiki/Hardware_random_number_generator). Sample some noise from radio waves, radioactive decay or noise from a digital camera photo cell. Simple A/D  converter + a sensor and plenty of entropy is available. Costs less than 50 eur to make since you don't require NSA-proof entropy (if you did, you wouldn't be reading this). Some PC chipsets have a built-in HW generator which can be utilized with [rng-tools](https://www.gnu.org/software/hurd/user/tlecarrour/rng-tools.html).

2. Randomness of timing. Linux has [Haveged](http://www.issihosts.com/haveged/), which works by generating randomness from the reasonably
random small differences in timing of system interrupts. See [HAVEGE algorithm](http://www.irisa.fr/caps/projects/hipsor/) for detailed explanation. 
Another interesting trick is to sample clock drift of system clocks, called [Dakarand](http://dankaminsky.com/2012/08/15/dakarand/). The 
computers are deterministic, but modern computers never operate from a single hardware timer clock in a perfectly deterministic way. 
([Original IBM PC actually did just that](https://news.ycombinator.com/item?id=2729571), nice engineering trick there.)

3. Get some from the internet. There are servers which supply supposedly random bits, for example [NIST Randomness Beacon](http://www.nist.gov/itl/csd/ct/nist_beacon.cfm).

4. You could also sample entropy by sending various packets around and measure their roundtrip times, but
this is I/O based method. Essentially not much different from sampling keyboard or mouse movement timings.

There are limitations on each of these

1. HW based devices can't be directly added to virtual machines. You can add the HW 
device to the host machine and then somehow make it visible to virtual machines, but to do this
you need more than root access to virtual server.

2. [Haveged](http://www.issihosts.com/haveged/) does work. The Dakarand trick is dead simple and works even removed from the HW, in Jàvascript! See [POC||GTFO issue 1](https://www.alchemistowl.org/pocorgtfo/) for further information. It does not generate bits very fast though and is CPU intensive.

3. Many systems do not have access to internet. The backend is secured behind a firewall for a
good reason. Also availability may be compromised if you require some third party service to operate.

4. Same thing here. 

## Generating entropy in real life

You might think that major server hosting companies have the HW generator set up for their server
farms. This would be logical and common sense, but unfortunately it is not so. You might not even
get them to do this, even if you are willing to pay 20x the cost of the device. 

So, we encountered precisely this situation some time ago yet again. This time entropy was 
running out mostly because of HTTPS protocol. The SSL handshake consumes entropy, which then
grinds everything to a halt. 

## Beware of voodoo tricks

You could get some entropy from [PRNG](https://en.wikipedia.org/wiki/Pseudorandom_number_generator). This is what `/dev/urandom` does if entropy runs low. 
So the common wisdom of internet is to do some linux magic and sample entropy from `/dev/urandom`
and push it to `/dev/random` with [rngd](http://linux.die.net/man/8/rngd).

This internet "wisdom" works, after a fashion:

```
  rngd -r /dev/urandom -o /dev/random -t 1
```

But it's not real magic, just a cheap trick of a conjurer. Reading from `/dev/urandom` in this
manner will consume all entropy. Then `/dev/urandom` makes up a bunch of bits, which look 
random, and puts the result to `/dev/random`. Entropy appears from thin air. 

However, `rngd` is intended to sample real entropy from a hardware source, not fake entropy from `/dev/urandom`. It's the linux "driver" for solution 1 mentioned earlier.
This magic trick can stretch the  threshold where things stop working, but a deterministic algorithm does not really generate
any randomness.  Using it in this manner is very clever, but not safe.

In a real world setting it worked for a while, but soon this happened:

```
  Aug 24 14:29:10 xxgsovt23l rngd: failed fips test
  Aug 24 14:29:10 xxgsovt23l rngd: too many FIPS failures, disabling entropy source
  Aug 24 14:29:10 xxgsovt23l rngd: No entropy sources working, exiting rngd
```

[FIPS test](https://en.wikipedia.org/wiki/FIPS_140-2) is a mathematical test to ensure that random looking bits are actually 
random. The test failed because real random bits didn't turn up in the system and rngd was just recycling its own pseudorandom bits. By design, rngd quits when
this happens.

## Ugly Java trick

You can "patch" Java systems. JVM parameter can be used to change the source of SecureRandom
from `/dev/random` to `/dev/urandom`. This affects everything running in the JVM which uses 
[SecureRandom](http://docs.oracle.com/javase/7/docs/api/java/security/SecureRandom.html). In our case, SSL handshake came from Tomcat and database connections are handled
by JDBC. This still drains entropy, but JVM actions no longer block. 

This is still quick&dirty fix, not a long term solution I would recommend. 
`SecureRandom` is not very secure if it reads bits which we know would fail the FIPS test. Depending
on the situation this may not be a real concern, but this is definitely not a "best practice".


## A checklist 

* When things seem to halt or performance degrades mysteriously, check entropy levels. 
* Make sure server monitoring includes entropy level. Very important in addition to 
 traditional CPU, disk, memory etc. Remember that manual checking with a remote shell
 will add some entropy while you do it.
* Ensure that your virtual servers have access to real source of entropy. Ask your vendor and demand they install rngd + HW device.
* Beware that your development environment may behave differently than the production environment.
* Try to understand some theoretical background.
* Check the practical side. Which operations consume entropy? Which produce entropy?
* Do you really need Secure Random? What is your real security threat?