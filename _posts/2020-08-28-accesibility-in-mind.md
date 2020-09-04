---
layout: post
title: How designing with accessibility in mind benefits your web app
author: jalef
excerpt: >
  Accessibility is a requirement for plenty of projects nowdays - especially the ones developed for the public sector. But why implement accessibility only when asked, istead of starting designing and developing with accessibility in mind? 
tags:
 - accessibility
 - frontend
 - UI/UX
---

The W3C has published the Web Content Accessibility Guidelines (WCAG) [document](https://www.w3.org/WAI/standards-guidelines/wcag/) in an effort to make the Web more accessible to people with disabilities. Our disabled fellow netizens may be a minority demographic, but the WCAG is relevant and useful to all Web Designers and Developers. In fact, the only fault in the document is its stated purpose, which might mislead you into thinking it won't help improve your flashy web app. Nothing could be farther from the truth! Let's examine why.

![Accessibility in mind](/img/accessibility-in-mind/a11y.jpg)
*Accessibility often abbreviated to A11y — as in "a" then 11 characters then "y"*

## 1. It improves UX across the board

If learning what the WCAG acronym stands for makes you think the guidelines don't apply to modern, feature-rich interfaces, prepare to be surprised! The WCAG compiles common-sense approaches to providing functionality which match the cognitive patterns of all humans, not just the disabled. For example, consider guideline [1.4.1 -Use of Color](https://www.w3.org/WAI/WCAG21/quickref/?showtechniques=132%2C211%2C311%2C325%2C131#use-of-color), which forbids using color as:

*[...] the only visual means of conveying information, indicating an action, prompting a response, or distinguishing a visual element.*

Following the WCAG here benefits your UI. On a general engineering level, eliminating the single point of failure (i.e. color as an information channel) yields a more robust design. In recent years, we had an opportunity to observe this when public awareness was raised about the effect of blue light on eye health. Apps which followed the guideline were better prepared to implement dark-mode / night-theme and were usable on a red-shifted monitor.

For another example, consider guideline [2.4.7 - Focus Visible](https://www.w3.org/WAI/WCAG21/quickref/?showtechniques=132%2C211%2C311%2C325%2C131#focus-visible). It prescribes:

*Any keyboard-operable user interface has a mode of operation where the keyboard focus indicator is visible.*

Removing the keyboard-related parts, we are left with a piece of sound design advice fit for any situation:

*Make the focus indicator visible.*

Be it via touchscreen taps or mouse clicks, all users move from one part of an interface to the next. A visual cue to where they last interacted with helps them scan the surrounding elements with confidence, making the UI more effective. Such cues also help with switching to a whole different task and then back again, making the UI more usable.

## 2. It improves maintainability

Developers care about maintainability because they wish their designs to be ready for change. A tried and true practice for achieving maintainability is separation of concerns. In the world of front-end development, the main concerns to separate are content and presentation. On occasion, it is unclear where one ends and the other begins. It is there that WCAG helps draw the line. The most fundamental guideline [1.1 - Text Alternatives](https://www.w3.org/WAI/WCAG21/quickref/?showtechniques=132%2C211%2C311%2C325%2C131#text-alternatives) mandates:

*All non-text content that is presented to the user has a text alternative that serves the equivalent purpose [...].*

This forces the developer to ponder the content / presentation question. In the case of images, this translates to a decision on whether to use an  [`<img>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/Img) tag or a [`background-image`](https://developer.mozilla.org/en-US/docs/Web/CSS/background-image) CSS attribute, making the value of the guideline all the more evident.

![Accessibility puzzle](/img/accessibility-in-mind/puzzle.jpg)

## 3. It improves robustness

Web apps today are called upon to achieve [Web Scale](https://en.wikipedia.org/wiki/Scalability). The preeminent architecture for achieving this is Microservices. Microservices however, require that developers adapt the way they put their apps together. The most radical change comes in handling failure states. The Microservices way of doing things is to expect that services might be unavailable and carry on nevertheless. This mindset change is aided by guideline [1.1 - Text Alternatives](https://www.w3.org/WAI/WCAG21/quickref/?showtechniques=132%2C211%2C311%2C325%2C131#text-alternatives) (see above). The UI of a modern Microservices-powered web app ought to gracefully fall back to a textual representation when fetching assets fails.

## 4. It improves content quality

Navigating your UI with a screen reader is an eye-opening experience which no front-end developer should spare themselves. The screen reader makes unnecessary repetition painfully obvious.

Lack of clarity in the titles and the labels also sticks out. Uncovering lack of clarity in these crucial pieces of text is of tremendous importance because two pitfalls await the unawary designer: First, the full visual experience often compensates for lack of clarity with context. Danger lurks here because this supporting context might change or even go away. Secondly, the designer is too close to their creation, too close to the business concepts and too involved in the development process to identify lack of clarity. The "fresh eyes" a designer needs to view their UI with is just what a screen reader provides.

Screen Readers help weed out weaknesses in navigation, too. Listening to your document flow might make your rethink the order in which you present your content. At the very least, it's a useful tool for testing your assumptions about content layout undistracted.

## 5. It makes your app adjustable to user’s preferences and needs

Providing a value for the [`lang`](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes#attr-lang) attribute on the `<html>` element is optional. However, WCAG [3.1.1 - Language of Page](https://www.w3.org/TR/WCAG21/#language-of-page) marks it as required. The integrated translation feature on the Google Chrome browser requires lang to be properly set. Modern web apps target a global audience and Google Chrome owns majority market share. Therefore, it makes great business sense to follow this guideline. At the end of the day, it is a testament to how the WACG may serve as a best-practices document for web development.
Furthermore, WCAG provides rules about content visibility (for instance [1.4.4 - Resize text:](https://www.w3.org/TR/WCAG21/#resize-text) *“text can be resized without assistive technology up to 200 percent without loss of content or functionality”* and [1.4.10 - Reflow](https://www.w3.org/TR/WCAG21/#reflow), which sets a screen limit for scrolling in two dimensions). Following these guidelines provides advanced UX experience for users who do not really need accessibility, but they choose to zoom the app through browser settings or work on a small window or on a mobile device.

## 6. It future-proofs

Following the WCAG may benefit your web app in unexpected ways. Guideline [1.3.1 - Info and Relationships](https://www.w3.org/WAI/WCAG21/quickref/?showtechniques=132%2C211%2C311%2C325%2C131#info-and-relationships) suggests techniques G115 (Using semantic elements to mark up structure) and H49 (Using semantic markup to mark emphasized or special text). Why prefer `<header>`, `<section>` and `<article>` over good old `<div>` and `<span>`? There may not be a compelling reason today, but chances are there will be one tomorrow! Advancements in AI and SEO technology indicate that web crawlers will be able to reason about web content some day. Semantic HTML is standardized and supported by all browsers so why not prepare for the future today?

## 7. It eliminates whole classes of UI bugs

WCAG recommends semantic markup (see above), which helps clear up content for the developer. By imbuing HTML containers with meaning, the developer reduces cognitive load, which is known to be a major source of bugs.
The benefits don't end with content-related bugs, though. Semantic markup is good medicine against *divitis* (i.e. overuse of `<div>` elements). The default CSS attributes of the various semantically-rich elements eliminate `block / inline` misconfiguration bugs – a major symptom of divitis.

## 8. It improves efficiency

Admittedly, efficiency should be at the top of the UX considerations list. Take for example productivity apps. These thrive on providing users with means of building "muscle memory" on the keyboard. Consequently, ease of use for each action is evaluated on a basis of number, complexity and intuitiveness of keystrokes required. These are all covered under rule [2.1 - Keyboard Accessible](https://www.w3.org/WAI/WCAG21/quickref/?showtechniques=132%2C211%2C311%2C325%2C131#keyboard-accessible). For builders of productivity apps, guideline 2.1 serves as a handy checklist.

## Conclusion
The WCAG document is a great foundation and inspiration for improving web apps. Web Designers and Developers need only extract the generic, common-sense parts from the guidelines. Sometimes, this extraction requires intuition or knowledge specific to the app. Most of the time though, it is a straightforward process. So, waste no time and find out what makes sense for your app today!


