---
layout: post
title: Communication in library design, a user's perpective
author: pvto
excerpt: Everyone has encountered a software library that is hard to use.  From the designer's perspective, the user can always be educated a bit more, but sometimes user training misses the point.
---

Everyone has encountered a software library that is hard to use.  From the designer's perspective, the user can always be educated a bit more, but sometimes user training misses the point. This post touches on some problems in library documentation.  We can insist on simple things that require no major effort on the part of a library designer, but could beautifully facilitate usage and user satisfaction.  Examples in this post, unhip as they are, spring from the Java ecosystem.  We use established libraries mainly for the reason that they are not likely to receive any damage from our reference.

##Good library design principles (from a library user's perpective)

From a user's perspective, a valuable software library can be recognized from various traits.  Here are some:

  * it does a thing extremely well
  * it communicates its logic and constraints very clearly
  * it enables rather than restricts its user
  * it is simple and clean
  * it does a thing extremely well rather than doing many assorted things (there are exceptions, of course, to this rule!)
  * it prefers instruction over hiding of features
  * it is as little intrusive as possible
  * it is kept small
  * it is suspicious of external dependencies

There is little novelty in what these items tell about good design.  Against this positive underpinning, we bring on some general traits of badness.

##Bad library design principles (from the user's perspective, again)

A bad software library should, generally speaking (to be bad):

  * be unclear or fuzzy about its scope of operation/services
  * integrate many external forces, ultimately aiming to bewilder its user over and over again
  * trade flexibility and predictability for ease of use (in other words, it should facilitate library-centered, vulnerable and disabling practices)

##A small case in badness

Let's say we wanted to generate a one-page PDF document that contained some text from a third party feed and an image.  The [Apache PDFBox web site](http://pdfbox.apache.org/) tells that said library can be used for PDF generation, and a small unit test class confirms.  However, we find out that a dash '–' from the feed stands out as 'þÿ' on our printed page.  It turns out that there is no simple solution within the library to this problem, and UTF-8 characters remain unprintable.  We could interprete '–' as '-', but there will be other characters.

Please feel free to study the [PDF 1.7 Reference](http://www.adobe.com/content/dam/Adobe/en/devnet/acrobat/pdfs/pdf_reference_1-7.pdf) and the [PDFBox implementation](http://svn.apache.org/repos/asf/pdfbox/trunk/).

The problem, in the end, is not wholly in Apache PDFBox code, which belongs to an OS project.  We could contribute to it if we wish.  Rather, cited documentation seems a bit misleading, because *it does not communicate the library's one basal restriction*.

##Listing mysterious properties of software libraries

(What remains hard to understand):

  * A lib's web site (tutorial or doc) may *communicate goals* but not the fleshly essence of the library.  Is this not like constructing a time bomb and giving it to a friend for safekeeping?  But instead of stating ['Create a PDF from scratch'](http://pdfbox.apache.org/), PDFBox documentation could say something like this: 'Create a PDF (with a TypeA font) from scratch'.  A little piece of technical jargon would alleviate a lot where brevity requires!  *There is abstract structural support of encodings in the PDFBox codebase, but it is not fully realised.*
  * Sometimes it is *hard to tell* what exactly a library will do.  Its usage pattern may be so complex that understanding it requires formidable knowledge.  On the other hand, information on its typical usage may be available, but then library operation is hard to understand.  Which, by implication, means that the library is too complex to communicate.  All this means that using the library is inherently unpredictable!  Then there will be unwished for side effects for the user.  All this may be a flaw in communication, or simply sham.  In the case of [Hibernate](http://hibernate.org/) there certainly are multifaceted assets for the user, but there also are many pitfall-patterns.  [Martin Fowler](http://martinfowler.com/bliki/OrmHate.html) gives a balanced view on the issue.  Now what if Hibernate *documented in bold letters* that it will act unpredictably in such-and-such case?
  * A lib is intentionally or unintentionally building undocumented constraints. This is probably more like generic a problem, of human nature, than a peculiar design problem:  of diligence and delusion, of being unclear about one's aims.  From an ecological point of view, a general rule of thumb goes:  the more you run a routine, the silmplier it should be.  [Jorma Rissanen's](http://en.wikipedia.org/wiki/Jorma_Rissanen) [minimum description length principle](http://en.wikipedia.org/wiki/Minimum_description_length), roughly interpreted, states that the description of a set of data that is shortest is the best.  We could apply this to the relationship between a library and its documentation: the shorter the documentation the better.  But if the library incorporates a plethora of constraints as a kind of net of safety checks within its code, they will be very hard to document, and, in the end, they make the library unpredictable to its user.  On the other hand, such checks are perfectly valid, if they ensure watertightly that the library does as indicated.
  * A lib comes with *lots of dependencies*.  In a typical scenario, after including such a beast, you find that you must track down multiple library version resolution conflicts, even change your code to satisfy the hassle.  But there is a clean solution to all this, and it is *no dependencies*.  We can refer to any pure API library, [jdbc](http://docs.oracle.com/javase/8/docs/technotes/guides/jdbc/), almost any part of the [Java standard library](http://docs.oracle.com/javase/8/docs/).  One good counterexample, too, is [Apache camel](https://camel.apache.org/).  Things that do real work don't generally require many external dependencies.

These examples could carry on for some time, and everyone can make up some more.  One essential thing, to summarise, is that what a library is is not only its software code but also all the promises it makes.  The less it makes promises and the better it fulfills them, the happier its user will be.

##A bitter ending note on mysteries

I sometimes (not always) wonder if a two page instruction sheet on hacking with the language standard library would serve one better than a 100000 codeline library that ultimately fails you in simple things, makes your life dreary in the process, and is dead within three years from now.

