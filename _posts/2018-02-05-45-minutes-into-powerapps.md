---
layout: post
title: 45 minutes into Microsoft PowerApps
author: tomila
excerpt: Extremely quick look into Microsoft PowerApps and how to use it to create enterprise apps
tags:
- Microsoft
- Microsoft Power Apps
- Mobile
---

## Premise and Promise

Microsoft's PowerApps boasts a noble promise of streamlining development of enterprise mobile applications. They have a long and notorious history of being, would I say, less than optimal presentations of their fullblown big brothers in desktop and laptop. PowerApps was published back in October 2016, but for some reason it went under my (and apparently many others') radar for over a year. With PowerApps, Microsoft empowers organisations to customise their app needs with no or very little coding effort. Sounds alluring, but let’s see.

First impression upon visiting https://powerapps.microsoft.com/ is that this is serious business. Screenshots of an app presenting hydraulic pump CAD-images accompanied with touch screen signed contracts immediately tease with the idea of extending PowerApps distribution beyond your own organisation. A trial period of 14 days is offered free of charge, no strings attached. After that it can be added as complementary service to your current Office 365 / Dynamics 365 plan with per user per month price. Note that in Some Office 365 plans it’s already included so you may just find yourself in luck with that one. Without going further into details of the pricing model I’d say this model may not be optimal for larger organisations if company’s Office or Dynamics plan does not readily include PowerApps.

## Hands on

Enough with that already, let’s actually do something. First things first, you need an organisational Microsoft account to unleash the power of PowerApps. After you have one set up, head to the [App Store](https://itunes.apple.com/app/id1047318566) or [Play Store](https://play.google.com/store/apps/details?id=com.microsoft.msapps&hl=en) and install PowerApps from Microsoft. The login process needs a bit of patience as clearly we are working in web view environment. Don’t expect to see fingerprint authentication let alone Face ID. After your login succeeds and necessary checkboxes are ticked you’ll be watching at the list of your organisation's shared apps. Probably not much to see here, yet.

Next, head down to https://web.powerapps.com/home on your favourite browser. On the Home screen you’ll be presented with a selection of ordinary business app cases from which to choose, or you can start from blank, if you feel adventurous. Going Indiana Jones is way out of this scribble's scope, so we’ll settle with Contacts example. Clicking the “Add” button presents you with a permissions dialog from which you need to permit PowerApps to read data from your organisation’s Office 365 Outlook. Obviously it needs to fetch data from somewhere right? I assume Microsoft already has this information covered anyways, so it shouldn’t be an issue to allow access. Also making a Contacts app for an organisation without actually having organisation’s people on the app is a bit of a let down from end-users’ perspective. Right, so we grant access to the app by signing in, again, to our personal account. After that, hit Make this app. And guess what, that is pretty much it. You now have a fully functional Contacts app, connected to your organisation's Office 365 data, ready to be shared. Template app of course needs to be customised UI-wise, but search logic, navigation etc. are there 100% ready to run. Nice.

![](/img/powerapps/contacts-app-editor.png)

Fiddling around with UI styles and nuances is quite a similar experience with all the other IDE’s we are accustomed to. Changing colors, fonts, borders, the usual stuff is straightforward, but adding images and media needs a bit more imagination. Hit File -> Media -> Images. Then Browse your media files to upload them to service. After the upload, you’ll see your files on the list and can give them a name or label if you will. From thereof you can use them as image elements' source by that label. Same goes for video and audio content as well.

## Technical bits

In Apple ecosystem's context PowerApps is an odd bird to say the least. Apple is notoriously jealous about what they allow to happen under their roof. Given the not-so-distant history of Microsoft's mobile endeavors it's not surprising to see them go to full lengths at utilising the potential of more successful platforms, namely Android and iOS. And who can blame them? It's exactly the right thing to do from business perspective. The only problem here is that they're not the ones holding all the cards in these turfs, so they need to adjust to the rules of others. Android ecosystem is pretty slack, though Google has started to tighten the reins with Oreo too. Apple on the other hand _may_ some day pull the plug from this type of approach even though likes of [AppGyver](https://www.appgyver.fi) have been successful with similar business model. 

Microsoft is not too keen on disclosing the details of how PowerApps are run on a device, but looking at the UX it's obvious that we're being served web content in a shell of a native app. Native as in React Native maybe, because even though they don't say it out loud PowerApps Dashboard's Analytics-tab yields unmistakeable clues on what is going on under the hood.

![](/img/powerapps/powerapps-dashboard.png)

There's no official word available on this though and by no means is this to say React Native is inherently bad, or even that Microsoft's approach is wrong. It's just something to keep in mind if you're planning on making PowerApps an integral part of your business processes.

## Going public - In organisational context

After tweaks and rebranding efforts it’s time to publish. Hit File -> Save and you’ll be one click away from gentle scrutiny of your first app by your colleagues.  First time around it’ll ask for who can do what with your app. Options are Edit or View. Going back to start page of PowerApps and hitting "Apps" will give you a list of the apps available for you. At this point the App has magically transferred into your mobile device's PowerApps app too. From list selecting “…” -> Settings presents you with App’s global settings. From where you can edit various things about the app, but interesting bits are the Share and Versions tabs. From Share you’ll be able to control access permissions to your app. From versions you control which version of the app is currently published for the audience. 

There’s also an Export package button which allows you download the app package. App package is pretty much a save file meant be uploaded back to PowerApps, or maybe edit offline. Important part is that this app package has nothing to do with an actual mobile app in traditional context.

## Final thoughts

Was that it? Pretty much yes. PowerApps presents you with the ability to connect enterprise data sources, create an UI to present the data and manage access to apps within your organisation. And it does all that in a simple and intuitive way. Obviously I merely scratched the surface here and deep down there you may actually find yourself writing an actual line of code, in JavaScript, what else? After all, in extremely oversimplified definition, PowerApps is, by the looks of it, a React Native container for components and connectors. Should you use it for enterprise apps then? Absolutely, if you are willing to live in Microsoft (and some 3rd party services) ecosystem, and you have rather simple tasks to solve, or you are willing to invest time in creating custom API's to connect to. 

PowerApps offers great opportunity to take down the load of actually running an organisation. I’d be hesitant in selling these solutions to customers at least until they fully understand implications and limitations presented by this type of approach. As a side note for what it's worth, it took me twice as long to write this post than to have the Contacts app up and running and shared to a selection of colleagues for testing.

Next up is Google's [App Maker](https://gsuite.google.com/campaigns/index__appmakereap.html), which is similar product offering from the big G. App Maker is currently available as part of an Early Adopter Program for G Suite Business customers.