---
layout: post
title: How to stay sane with Robot Framework
author: tuomoturunen
excerpt: >
  Robot framework with Selenium offers a wide toolbox to work on with
  browser UI tests. With simple patterns and architechture, writing and 
  maintaining UI tests is not a big deal as it used to be.
tags:
 - Robot Framework
 - Test automation
 - Selenium
---

How to stay sane with web application test automation with the Robot Framework 

Intro
-----
My first experience in Selenium was in university approx 15 years ago and it was an optional part of a bigger assignment. Wasn’t surprised that only a few people managed to complete it. Back in the days, writing browser UI tests were more and less black magic: keywords were high level yet translating low-level technical requirements into selenium keywords had a steep learning curve. After plus ten years of professional software development, I had a Deja Vu moment where there was an optional assignment and it involved Selenium with a twist of Robot Framework. 

Compared to my previous experience with browser UI testing, the documentation and usage were much more userfriendly, and getting started didn’t include frustrating and complex setup. Over four months there were hard times when not everything worked as I thought yet with some trial and error I managed to achieve project goals without sacrificing too much of my sanity. Like always in software engineering, the winning receipt was to find common patterns and general solutions for 80% of requirements and avoid using duct tape solutions.

When designing UI tests, test fragility is the key thing to keep in mind. When the UI changes, how many things I have to change in my code? How can I uniquely click objects when app has dynamic content and in a shared environment? Simple patterns lead to simpler solutions that are more maintainable and easier to comprehend when the project is transferred to another person and hopefully this blog post gives you an idea or two how to leave a solid project for the other person to continue.


Getting started
---------------
I don’t know if it is the Google and Youtube algorithms or lack of my research skills, but I simply couldn’t find anything more advanced than how to click a button or input a text. Since there are tens of youtube videos and blog posts about basic features, we're gonna skip those and enter into the realm of basic architecture and timing. If you’re not yet familiar with the Robot Framework, I suggest you read a tutorial or two about basic functions and concepts. 

Building architecture
---------------------
Keeping code nice and tidy is the way to success in the long run. If you’re not planning to maintain the codebase by yourself for the next six years, putting some effort into the architecture will reduce the risk of cold glances during coffee breaks. 

On the highest level, we have two boxes: test cases/scenarios and the page model. Page model models the structure of the application and works as an interface for actual tests. You can think of it as a class or module hierarchy in software development where entities encapsulate implementation. Then composing tests is only a matter of calling these modules with parameters and life is beautiful.  In the Robot Framework, we separate these two by having them in separate directories, files, and inside robot-files the page models consist of task keywords and tests test keywords (more on that later). 


Writing everything in a single test is fast and simple, and even preferable in some cases, yet eventually, you start to duplicate code which leaves you a bigger and bigger codebase to maintain. Not to mention how difficult it is to have different tests and test parameters in different environments.    
Let’s take a generic e-commerce site as an example. I’m not a big fan of writing documentation so I prefer to have a self-explanatory structure and codebase, so my page model could look something like this:

<use graphics maybe?>
* Navigation
    * top-menu.robot
        * goto products
        * goto brands
        * goto activities
        * do search
        * login 
        * goto basket
    * side-bar.robot
        * open category (products, brands…) tree
        * open sub-category tree
        * open sub-category as a page
* Ordering
    * basket.robot
        * remove product
        * change product quantity 
        * add promotion code
        * proceed to checkout
    * checkout.robot
        * input shipping details
        * select shipping method 
        * input payment details
* Products
    * product-search-result.robot
        * select search result by (parameter, ordinal or so)
        * filter results 
    * product-details.robot
        * select the description tab
        * select the specification tab
        * select reviews tab
        * add to basket
        * leave a review

In my experience, the granularity of the page model depends on the size of the application and the requirements of your tests. With small applications and happy days test cases, you can bundle more into the same robot file and keep the interface small, yet if you want to test your UI thoroughly you need to have a more refined interface for the test cases. My advice is to have a simple page model and refactor it along the way. With more experience of modeling and the application itself, the need for refactoring lessens.

Test structure and composition follows a natural pattern where a directory contains test scenarios (robot files) and files steps to go through a scenario. 

* /products/find-products-tests.robot
    * Find a product by query
        * top-menu.robot - search
        * product-searchresults.robot - select product
        * Assert the product page
    * Find a product by query and filtering
        * top-menu.robot - search
        * product-searchresult.robot - filter result (by brand etc)
        * Assert the page contains certain products
* /products/product-details-tests.robot
    * Write a review
        * top-menu.robot - login
        * top-menu.robot - perform search
        * product-searchresults.robot - select product
        * product-details.robot - select review tab
        * product-details.robot - leave a review
        * Assert the reviews tab
* /orders/ordering-tests.robot
    * Change product quantity
        * top-menu.robot - perform search 
        * product-search-results.robot - select product
        * product-details.robot - add to basket
        * top-menu.robot - goto basket
        * basket.robot - change product quantity
        * Assert changes
    * Checkout the basket
        * top-menu.robot - perform search 
        * product-searchresults.robot - select product
        * product-details.robot - add to basket
        * top-menu.robot - goto basket
        * basket.robot - proceed to checkout
        * checkout.robot - input shipping details
        * checkout.robot - input payment details
        * ...

As we can see, our example has a natural language that is both easily comprehensible and verifiable. Non-technical people should be able to read each test step and verify that they follow test requirements. Technical details such as how to press buttons, input text, and select checkboxes and radio buttons are encapsulated in the page model. 

If you’re about to have a vast amount of tests you eventually end up having repeating same step patterns like in our brief example going to a specific product page or adding a product to the basket. Depending on your personal and project preferences you can write convenience tasks to boost productivity. However, this will force you to perform the steps, in the same way, each time and it lowers test coverage at that part. There’s no right and wrong way as long as you know the consequences and balancing between granularity, coverage, productivity and maintainability is an ongoing struggle.  

Page model + test case example
------------------------------
Like I previously mentioned, both the page model and test cases are plain robot files where the page models consist of keywords and tests consist of test cases. Let’s see how the login should work in write a review test

top-menu.robot:
```Python
*** Settings ***
Resource ../PageModelCommon.robot

*** Keywords ***
Login
    [Arguments] ${username} ${password}
    Input text id=username  ${username}
    Input text id=password  ${password}
    Click element id=login



```
product-details-tests.robot:
```Python
*** Settings ***
Resource    ../PageModel/Navigation/top-menu.robot
Resource    ../PageModel/Product/product-searchresult.robot
Resource    ../PageModel/Product/product-details.robot

*** Variables ***
${user}     test-user
${passwd}   password123
${product_name} product-x   

*** Test Cases ***
Write review
    top-menu.login  ${user}    ${passwd}
    top-menu.Perform search    ${product_name}
    product-searchresults.Select product   ${product_name}
    product-details.Select review tab
    product-details.Leave review
```



Timing actions and avoiding caveats 
-----------------------------------
First of all, there’s no single solution on how to check if the page is fully loaded or not. Especially if you’re working with a single-page app. The Robot framework performs actions synchronously as fast as it can without any default waiting or so. This is problematic since depending on network speed, latency, and used browser it takes unknown time to load the page to the point where the next action can be performed. If you try to press a button that is not yet rendered or the dom tree is not refreshed, the Robot framework can not perform actions and the test will fail. 

You can set default delay between actions by using keyword *Set Selenium Speed*, which is very convenient when debugging or following tests, yet it prolongs test duration. If you set the delay 500-1000ms and your test scenario consists of 60-120 actions, you end up adding 30-120 seconds of unnecessary delays. Using keyword *Sleep* is also highly not recommended since it sometimes makes the selenium driver unstable or you end up waiting for too long and again your test runs start to get longer and longer. 

So how do we overcome this problem without sacrificing time and performance? The solution is quite simple: we perform actions when the desired elements are available. With implicit waiting, we minimize wasting time and make our tests robust and less fragile.

```Python
Click Element When Visible
    [Arguments]    ${selector}
    Wait Until Element Is Visible    ${selector}    
    Click Element    ${selector}
```

Quite an anti-climax after a long rant of different problems? Kinda, there are still few caveats to overcome.

What selenium sees is the dom tree and it has no clue of its state. Is it ready enough, complete, about to change, or loading? The gap between an asynchronous app and the synchronous Robot framework is deep yet not impossible to overcome but requires some detective work and experimenting. Since most UI frameworks generate lots of clutter into the DOM tree, writing a unique and readable selector might be tricky. 

Since the Robot Framework or Selenium doesn’t know the state of the DOM and there’s a chance that both source and target pages contain the same elements, we have to be sure that we don’t click an element from the source page while we are in the middle of loading the target page.

For example, we have a source page that contains:
a list of products (or a single product if your test assumes so) 
a list item contains a link to the product page
a button containing the text “Add”. 

and the target page contains

a button containing the text “Add”. 

```Python
Click Element When Visible //label[contains(text(), ‘Product-X’]
Click Element When Visible //button[contains(text(), 'Add')]
Do something else in the product page
```

Now, what may or may not happen is that while the browser sends a request to the server, gets a response, and starts to render the new view, the Robot Framework will perform the next action clicks the element in the source page. If adding a product in the product list page takes the user to the basket and the product detail page doesn’t, the browser is on a page where it should not be and the next actions cannot be performed.

You could check that if the URL has changed the browser is in the right place, but that depends on when the UI framework updates the URL, and sometimes it happens asynchronously so we cannot use it reliably. 

Another way is to wait until the footer is loaded, but some browsers tend to render the page in an unpredictable way so that won’t work either. 

The best solution that I could find was writing XPath that finds the desired element inside a unique element since it’s highly unlikely that the source and target page has the same wrapper elements.

To fix our previous flow we write the add to basket actions slightly differently:

```Python
Click Element When Visible //div[contains(h1, ‘Product-X’)]//button[contains(text(), 'Add')]
```

In English: we click a button element that reads “Add” that is inside of a div that has h1 element containing text “Product-X”. 

I tend to write the page model as simply as I could and avoid having complex XPath and CSS selectors. If my first selector is not unique enough or doesn’t work in certain situations, I make them more specific yet always try to keep them as readable as possible. 

When actions are scattered in different robot files, my preferred pattern was that the keyword assumes that the correct page is loading and waits for the target element to be visible. Since the source page does not know what the next action is, it cannot implicitly wait for the target to be loaded even if the action is performed on the same page. Defensive programming and constant checking only hide problems in the action flow (actions are performed in the wrong order or are missing something) and adds unnecessary complexity.


Loading spinners
----------------
Spinners are a great way to signal that the application is not stuck and loading the view and they can be easily used for waiting. Since the Robot Framework does not support events, we have to explicitly wait for the spinner to appear and then disappear. This makes using them costly in places where the spinner rarely ever appears. The preferred way is to not detect them until your test starts to fail because the target element does not appear before timeout. Generic spinner detection may look like this

```Python
Wait Until Element Appears And Disappears
    [Arguments]    ${selector}=    ${timeout}=10s    ${pre-timeout}=5s
    Log    waiting 5s for ${selector} to appear
    Run Keyword And Ignore Error    Wait Until Element Is Visible    ${selector}    ${pre-timeout}
    Log    ${selector} appeared! Waiting ${timeout} to disappear  
    Run Keyword And Ignore Error    Wait Until Element Is Not Visible    ${selector}    ${timeout}
    Log    ${selector} disappeared!
```

Since all Robot keywords are tests we have to ignore errors in case the spinner never appears. 

Afterwords
----------
After a few months with the Robot Framework, I was pleasantly surprised at how less soul-crushing is to develop UI tests. However, I wish the Robot Framework had basic if-else statements or other ways to control the action flow or recover from unexpected events. When you write your tests against multiple different environments, it would be more efficient to have some control flow for special occasions and continuous testing.   




 



    











