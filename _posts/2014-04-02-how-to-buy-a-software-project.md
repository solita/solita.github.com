---
layout: post
title: How to buy a Software Project
author: empperi
excerpt: We are doing agile projects but at the same time we aren't. The reason to this is in the way software projects are bought.
---

Today most of the software projects done out there use agile methods. We have sprints, product backlogs, kanban boards and so forth. Today's customers require use of agile methods in the projects which is a good thing. Waterfall has been proved to be a wrong way to do things time and a time again.

However there is a problem. The way most of the projects are bought do not support agile methods in the least and in fact they force to something wierd which isn't quite waterfall and it isn't quite agile either. In the best case scenarios these projects end up feeling like agile and in the worst case they are very very far away from agile projects. I'll first describe this model which is used so commonly in the tendering process and then go forth to the suggested model which would truly support agile methods.

## The way it is now

When the customer recognizes a need for some software system which it needs to buy from an outside organization they start to gather requirement specifications. In some cases the customer creates these specifications themselves and in other cases they start a separate tendering process for finding a parter which will help them in creating this document. In this document they will gather all the requirements they can think of which might be important for the future system and it is used as a baseline for the future tendering process for the actual system. After the requirements specification has been made a significant amount of money and time is spent since creating a comprehensive requirements specification is not a small task - most likely tens of thousands of euros is spent and in some cases hundreds of thousands or even millions.

Next the customer starts a tendering process for the actual system. They send the created requirements specification along with more accurate rules for participating in the tendering for all participant organizations. How these organizations are found depends on the case, but in some cases anyone can participate and in others the customer chooses the participants from a pre-selected list.

The rules included in the tendering vary, but they usually contain at least the following:

* The vendor shall provide a comprehensive list of the development team which will implement the product along with the CVs and project history of all of them
* The product must be delivered within a certain time frame
* Failing to deliver the product in an agreed time frame and/or budget will lead to penalties such as loss of income for the vendor
* The project must be done by using agile methods, preferably Scrum

Now all the organizations wishing to participate in the tendering dig in to the requirements specifications and start making estimates of how long it would take to create such a system as described in the document. All of the participants know that their rivals will try to outbid them and so they all try to get the price as low as they can go. In many cases they go lower than they think is realistic because that's the only way they can truly compete.

Of course the vendor is chosen by other factors too than just mere price. The experience of the team is an important factor as is also the promised delivery date.

After the customer receives the bids they (usually) choose the lowest one but in some cases the quality factors may allow the second lowest bid to win. After this contracts are made and the project is started.

## What's wrong with this?

The described process drives off the road (and badly) right in the beginning: when the customer starts a project to create a requirements specification. There's nothing wrong about requirements but this is a wrong way and time to do those. In the perfect world this would be just the right way to do it but in reality there is no one who can create a requirements specification so detailed and without conflicts in requirements that it could be used as it is in the actual development. And even if it could be made there is no human who could interpret it fully and create a reliable estimate. There is a name for this kind of perfect requirements specification without discrepancies which can be interpreted always the same way: a computer program.

So the vendors are given a lacking requirements specification which is full of discrepancies and they are expected to give work estimates based on those requirements and then commit to those estimates. Sounds like a bad deal, huh? The situation is made worse by competition which forces the estimates unnaturally low thus ending with unrealistic estimates which will end up hurting both the vendor and the client.

And if we are truly honest this whole requirements spefication made beforehand sounds awfully lot like waterfall model. And we all know it is a bad choice.

## Well wiseguy, what's the better way then?

Before we dig in to my proposal let's talk little about agile methods.

When doing an agile project there are few basic principles to follow:

* Do not plan too much ahead - situation may and will change and too detailed features too far away in the future will end up being wasted effort
* Ensure that developers will always have enough well defined features so that they never need to stop making progress
* Embrace change, change is a good thing
* Always prioritize features

What this essentially means is that you *should* create detailed requirements but just *not too early*. This is due to the fact that the closer you are to the actual development of that feature the better you understand the application itself and the domain behind it. This also encourages to drop unneeded features. It is a good thing to have even wild features in the product backlog - just don't define them in a detailed matter until you are quite certain they should be implemented at all.

Does this sound a bit different from the traditional way of creating a requirements specification? How do you fit this model in with requirements specification? The answer is simply: you don't.

The way this is done traditionally is to gather all of these wild feature requests, try to define them accurately which *will* fail, dump them into the requirements specification document and then bind the vendor to deliver them via contract. It doesn't matter if these features are actually reasonable or even needed.

So my proposal is very simple: **do not write a requirements specification document.**

## Holy smokes, what are you taking?

For the beforehand said reasons agile projects and requirements specification document just don't fit together. This is even more so because it is not the actual development team who is writing that document. So we are also missing an opportunity to learn the business domain well. This has to be done though, so it is done at least once for nothing - no one needs the requirements specification document, they need a functioning software.

But how on earth can we find the best vendor for our project if we don't do a requirements specification? How can we know when our project will finish if there's no requirements to evaluate and estimate? And don't even start to talk about the mismatch with budgets?

No one has unlimited amount of money in their disposal. Projects cannot cost more money than what the customer has available. But the fact is, that **you cannot make something cheaper by wishing it cheaper**. If you want something to be cheaper then you need to cut down on features or make them more simple. And you cannot do this before you've got the whole picture regarding that feature.

Let's say you have 500 000 euros at your disposal for creating a custom made ERP system. You know roughly what you're going to need in order for the project to be successful. You also know when it has to be ready. What you do not know is what you're going to get in that time with that amount of money. And the cruel fact is that **no one does**.

The way you should approach budgets in agile projects is to do a rough estimate in the very beginning of the project with team if this is going to be doable at all. Is 500 000 euros enough to deliver a functioning system with enough features to be useful? If the answer you **together** come up with is *yes* then you start the project. And it continues as long as one of the following things happen:

* Customer runs out of money and nothing "good enough" has been delivered. This is the worst case scenario.
* Customer runs out of money but what has been delivered so far is "good enough". There are still a lot of features sitting in the product backlog but the most important features are there and the software is usable. In this case the project is a success. Rest of the features in the backlog might actually be features which are best left out anyway - they might just be in the way in the actual product. It all depends.
* Deadline is reached and there is no point in doing anything anymore. This is very rarely the case, since usually these projects continue on after the deadline. Potential market windows might be missed which would equal to project failing.
* All the necessary features have been implemented and the customer says "ok, this is enough". This is the best case scenario. Project finishes before the deadline and with less money spent than what was budgeted. Yes, this actually happens in some agile projects.

I want to emphasize that the last situation can happen before the deadline has been reached or before the budget has been spent.

When working like this we are accepting the fact that we really do not know what we are going to end up with in the end. This is always the truth in software projects. Trying to guess everything too early will just end up in pain and misery.

## And about the tendering and finding the vendor?

After all this ranting I'm finally closing in on my proposal on how to actually buy a successfull software project. Since everybody likes checklists let's provide one:

1. First define **roughly** what you are going to need. An ERP system? A web store? A client registry? A 3d modelling software? Mars lander control software?
2. Next define your budget. How much money do you have at your disposal to do this? Does it sound reasonable to you that you might actually get this kind of software with that money? If not, stop here and forget it. If yes, then go ahead and proceed to next step.
3. Start a tendering process for finding a **proper team** to implement your software. Concentrate on finding the most skillfull team with least amount of money (how much a working hour costs). Provide your rough description of the system to be implemented. This might be maybe one A4 paper full of text, no more.
4. Choose top-3 of the vendors who participated in the tendering
5. Make all of these three vendors to implement a simple prototype of your system. **Pay for this work by their hourly cost**. You may provide a limit for either the money or hours available in implementing this prototype. This prototyping phase may take anything from two weeks to one month but no more. Less than two weeks and it is doubtful you'll get anything useful out the teams. More than a month and you're starting to pay for too detailed features for the two losing vendors.
6. Evaluate the prototypes by their quality, usability, how quickly the team delivered, how much it actually cost and so forth. Which prototype just "feels best"?
7. Choose the best candidate
8. Start the actual project in an agile manner

You might be suprised about few things if you proceed like this. First, you may find out that a team with a higher hourly cost ended up providing a higher quality prototype with less money than the cheaper teams. Or vice versa. Second you'll find out just how different these three prototypes will be. When teams are given free hands they might suprise you with ideas you never even thought about. Thirdly you might be suprised just how much the best team was able to deliver in such a short time period.

It is ok to pay for the failed prototypes too since they have provided you with important information. Some of the losing prototypes might contain good ideas which can be implemented later or show definetly bad approaches.

Also when you do tendering like this you can be sure you're going to get the team you were presented with. If you demand a project team months before the actual project starts then there are no guarantees that even one of those people you were promised can be actually delivered. No one can just keep a guy on hold for months "just in case we win this tendering". But two weeks? That's bearable especially since you **pay** for the prototypes even if the vendor loses.

The key here is to proceed quickly with the tendering. The whole process from start to finish should take no more than two months. This allows faster time to market and more certainity regarding the team available.

Also make sure in contract that you can always stop the project when you feel like it. When doing scrum this possibility comes after every sprint - two to four weeks. If the team fails you, just stop the project and kick the team out before more money is spent. If the team delivers then keep them as long as you can. Good developers are hard to find.

## Conclusion

So don't buy projects. Buy teams. Don't try to guess the future in detail. Keep the future vague and concentrate on what's important right now. Future cannot be guessed in any kind of certainity and trying to do so will just end up with false security. Successful software projects are grown like gardens, not built like buildings. They evolve during the process.