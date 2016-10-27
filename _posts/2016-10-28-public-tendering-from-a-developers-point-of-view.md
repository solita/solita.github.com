---
layout: post
title: Public tendering, from a developer's point of view
author: pkalliok
---

This essay is about a topic that has been beaten to death already: how
to make public tenderings of IT services, or software development.
There certainly is no lack of writings about how you can conduct a
procurement, what to do and especially what _not_ to do.  Here's my
teaser: it's hopeless.  However well you prepare, whatever you will set
as the criteria, there's always the possibility that your chosen IT
supplier will not get the job done, and then you only have bad options.

It is no guarantee of quality if the subcontractor is expensive.  It
only tells that they are preparing for a lot extra work, or big profit
margins.  It's almost on the contrary, but a cheap subcontractor _might_
just have totally misunderstood the scope of what you're buying, or is
otherwise delirious about their own abilities.  It might help that you
stick with a subcontractor that has a good track record, but then there
is the risk that you're actually sticking with a total douchebag
supplier out of fear of change.  It's hard to assess the ability of your
subcontractors when it's about IT.

Why is it so hard to procure IT stuff with public tenderings?  Because
programs and digital services are very different from most other things
you buy.  First of all, at the time of procuring, it is often very
ill-defined what the expected "product" is.  When you buy socks, it's
easy to switch to a new product, because they are drop-in replacements
for each other.  The closest equivalent you have in IT, is programs that
implement exactly the same (probably standardised) interface, such as
different LDAP servers.  But for most of those standardised interfaces,
open source products already exist, so most of the time it makes no
sense to use money when you can get a better implementation for free.

But it doesn't end there.  For most stuff you buy, you can readily
access their worth by using them.  The defects and problems of IT
products become apparent very slowly and only through extensive use of
the software/service.  Unless your IT subcontractor is making deliberate
effort to ensure that they are building something that actually helps
you, they will be long gone by the time you have gathered enough
experience to know what you should be asking for.  

Combine this with the fact that in addition to an "outer" quality (what
it looks like and whether it is easy to use), IT products also have an
"inner" quality: how often it will crash, do you ever lose data, how
difficult the product is to update, how difficult further development
will be, how hard it is to integrate with other systems.  Still combine
this with the fact that these are systems that often hold data that is
critical to the business or organisation, and it is far from trivial to
transfer this data to other systems.  And as if that wasn't enough,
these are also systems tied to the very working of your internal
processes, and your employees will specialise in the particular systems
they have to use, however bad and counterproductive they might be.

Put together, all this means that you have no way of ensuring that you
will get something useful for your money, _but_ you will still be tied
to that system for quite a while.  As I said, it is hopeless.

What will then happen, if it is hopeless?  With your tender, you will
get what you will get.  You can't really ensure that it will be
something useful, but there _are_ some ways to ensure that it will be
useless.  For instance, too long a feedback cycle (too much planning and
too little trying things out) will almost always bring you something
that will prove useless, or a lot less useful than what you hoped for.
A policy that prevents automation is also very bad for productivity and
software quality - for instance, hand-written installation instructions
to server administrators.  Trying to procure before you have a clear
understanding of what the system will at least do is also a sure way to
disaster.  Even if you have a great IT subcontractor and they're doing
their best, they have almost no way of succeeding in these situations.

One approach is to avoid buying IT "solutions", but instead to buy
brilliant people that will build those solutions _and_ find what you
actually need solutions for.  Employing these people was the traditional
way, but consultants will also do.  However, if you are buying these
people to do your IT for you, you probably don't have much idea whether
they are doing it well - because assessment of IT work is a very
challenging skill in itself, and usually requires good IT skills.

Another approach is just to absolutely trust whichever IT subcontractor
you choose, and give them as much information as possible so that they
can help you.  Then, if they are smart and benevolent, they will
probably be able to help you.  I know that my colleagues try their best,
but I still can't promise they will always succeed.  We also try to tell
our customers if they're asking impossible or insensible things, and
sadly, neither can I promise that we'll always succeed in that.

One approach that I haven't seen used, but which should prove
interesting, is to implement the same system in maybe two or three
unrelated projects.  That way, it's easier to see the strengths and
shortcomings of these different implementations.  It might sound
expensive, but because this multiplicity works as one kind of quality
control, you can let go of supplier quality criteria (such as years in
business etc).  This should drive the price down a lot.
