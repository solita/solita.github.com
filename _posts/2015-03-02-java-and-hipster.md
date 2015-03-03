---
layout: post
title: Java and Hipster
author: juuso
excerpt: First experiences as a new employee of Solita... and some Java Hipsterism
---

New employees of Solita get a thorough introduction to the company, and as a part of that coders get to implement a little exercise application to familiarize themselves with a typical modern web application stack. Programmers do the exercise themselves but asking for help and discussing architectural decisions with each other and with more senior employees is highly encouraged. Of the three of us who started at the same day, me and Arto were going to be very involved in Java development which meant that we would be using a Spring based stack. Arto by the way already wrote [a great wrap up of his first experiences at Solita](http://dev.solita.fi/2015/02/16/microservices.html). The third guy got a chance to delve into the world of Clojure. Lucky him?

I will give a few glimpses at code of the parts that I found interesting. The coding exercise was quite simple so most of the glimpses are excerpts or modifications of existing solutions that were originally written by someone else. Our Java stack for the exercise was based on Spring and we were encouraged to try [Spring Boot](http://projects.spring.io/spring-boot/) which makes Spring web applications stand-alone by embedding Tomcat, Jetty or Undertow into a .jar file which means that getting your app up and running is quick and comfy and cushioned, and ponies. Of course you Node.js and Rails hipsters have always had this... I have a few years of experience on Spring but I had not tried Spring Boot before, which really excited me.

The front end would be written with [AngularJS](https://angularjs.org), which many believe is the most productive front end framework at the moment. Some cool guys told me that they like [Facebook's REACT](http://facebook.github.io/react/) better, and because they are so hipster, they wrap it with some [ClojureScript](https://github.com/clojure/clojurescript) goodness with [Om](https://github.com/omcljs/om). I wish I was that hip too! Luckily our senior guru Arto told me not to worry. He had heard that there actually was a Hipster stack for Java developers. I googled Java and Hipster and there it was: ["JHipster - A hipster stack for Java developers. Yeoman + Maven + Spring + AngularJS in one handy generator"](https://jhipster.github.io/). That would be my stack of choice.

## Scaffolding the app

JHipster is a [Yeoman](http://yeoman.io) generator. It scaffolds beautiful modern single page AngularJS web applications running on and served by a Spring backend. Installation is done via Node Package Manager:

<code>
npm install -g generator-jhipster
</code>

After the installation, to get the application generated, I just had to execute:

<code>
yo jhipster
</code>

I answered a bunch of questions about what's my preference for different layers of the stack: Java version? (8, of course), Authentication mechanism?, Development database?, Production database?, Hibernate 2nd level cache?, clustered HTTP sessions?, WebSockets?, Maven Or Gradle? Grunt or Gulp? Compass for CSS?

After that a few times

<code>
yo jhipster:entity
</code>

and there I had my Java Hipster application scaffolded.

## Booting up the Spring.

I had a CRUD application skeleton and Maven was well preconfigured by JHipster so I simply executed:

<code>
mvn spring-boot:run
</code>

And now I had a running Java Hipster application.

![Java Hipster](/img/java-and-hipster/hipapp.png)

The generated backend seemed to follow a typical layout of a Spring MVC application. The configuration of the application was done using the programmatic configuration http://docs.spring.io/spring/docs/3.0.x/spring-framework-reference/html/beans.html#beans-java instead of the previously more common XML configuration which I was more familiar with. Other notable addition to what I had used and seen previously was the use of the new Java 8 Optional in controllers:

{% highlight java %}
@RequestMapping(value = "/departments/{id}/employees",
        method = RequestMethod.GET,
        produces = ResourceMediaType.JSON_UTF8)
public ResponseEntity<List<Employee>> getEmployees(@PathVariable Long id) {
    log.debug("REST request to get Employees by Department id: {}", id);
    return Optional.ofNullable(employeeService.getEmployeesByDepartmentId(id))
            .map(department -> new ResponseEntity<>(
                    department, HttpStatus.OK))
            .orElse(new ResponseEntity<>(HttpStatus.NOT_FOUND));
}
{% endhighlight %}

Because the backend was simplistic, I decided to try out something new and extended my JPA repositories with [Querydsl](http://www.querydsl.com/) [PredicateExecutors]( http://www.petrikainulainen.net/programming/spring-framework/spring-data-jpa-tutorial-part-five-querydsl/). The predicates were simple to implement:

{% highlight java %}
public static Predicate municipalityNameIsLike(final String searchTerm) {
        QMunicipality municipality = QMunicipality.municipality;
        return municipality.name.startsWithIgnoreCase(searchTerm);
    }
{% endhighlight %}

This is what my queries looked like after implementing Querydsl predicates:

{% highlight java %}
municipalityRepository.findAll(municipalityNameIsLike(searchTerm));
{% endhighlight %}

I also wrote a BDD style test harness during the implementation of the backend.

## The Front

The UI was written in AngularJS. I had gazed at it before but it was a long time ago and I had to start learning from scratch. I found [this course at thinkster.io](https://thinkster.io/a-better-way-to-learn-angularjs/) to be of great value. Taming the asynchronousnes, promises, modules, injectors, dependency injections, filters, scopes, directives, services, controllers etc. took a while but I managed to add new functionality and modify the generated functionality to fit my needs quite easily. Having a JHipster generated, an opinionated, project structure helped me a lot by giving me clear advice on best practices.

## Asynchronous testing

Testing the UI was a different experience from what I expected it would be. Of course I have been writing tests before but I had never written asynchronous tests for asynchronous AngularJS. I used typical Karma + Jasmine combo for unit tests as it was already set up by JHipster. Injecting the dependencies into tests was really straightforward with Angular's toolset. Things got hard when I was trying to isolate the test functions to test only the functionality that the tested methods were responsible for. I guess it gets easier over time.

I typically write acceptance tests using the awesome keyword driven [Robot Framework](http://robotframework.org). I did a quick research on how it would work with AngularJS and ended up into a conclusion that I'd better try another solution. Asynchronous nature of a single page AngularJS application would have required me to add a Lot of implicit waits into the tests which would in a long run, either slow the testing speeds dramatically or lead to unreliable tests due to too short timeouts. I ended up using the now default AngularJS end to end testing framework [Protractor](http://angular.github.io/protractor). Protractor makes it possible to write asynchronous tests in a synchronous style. It also provides AngularJS specific functionality to ease the pain of AngularJS acceptance testing. There is, for example, a function waitForAngular that should allow me to get rid of all the implicit waits. Also writing both the application and the tests in JavaScript sounded beneficial.

There were a couple of quirks that I encountered that the plain `browser.waitForAngular()` could not fix. Also Arto had noticed that there seemed to be cases where `waitForAngular` was not enough. I ended up writing a small utility module to overcome the problems. After calling `waitForAngular`, I also sometimes had to wait until some elements were present and displayed by the browser. I ended up writing my own waitFor function.

```javascript
module.exports.waitFor = function (locator) {
    browser.waitForAngular();
    browser.wait(function () {
        return browser.isElementPresent(locator) && element(locator).isDisplayed();
    });
};

```

I replaced all my `browser.waitForAngular()` calls with my custom `utils.waitFor(by.id('anExcellentButton'))` to make sure that I would not usually have to care about the type of waiting I was supposed to do.

Another typical utility function I implemented was selecting an item from a select menu. I found an existing broken listing for an old version of Protractor from Stack Overflow and modified it work on current version of Protractor.

```javascript
module.exports.selectDropdownbyNum = function (element, optionNum) {
    if (optionNum) {
        element.all(by.tagName('option'))
            .then(function (options) {
                options[optionNum].click();
            });
    }
};

utils.selectDropdownbyNum(element(by.id('departmentSelect')), 2);
```

Besides using my own utils module, I took an advantage of [a nice set of additional matchers for Jasmine](https://github.com/JamieMason/Jasmine-Matchers).

## Wrapping up

What I really liked about JHipster was that it provided quite a complete project skeleton with most of the build automation preconfigured. Only the acceptance testing had to be set up manually. Deciding if it is a good thing to have a preconfigured and opinionated environment when you are starting a new technology is matter of everyone's own opinion. Some people prefer bottom-up learning while other prefer top-down learning.

Overall the simple introductory programming exercise felt like the right way to start working at Solita. I got a few non-stressful weeks to get know the company and the technologies before starting to work at a real customer project. What also felt good was that no technology choice was strictly set in the exercise. I got a feeling that Solita trusts my decisions.
