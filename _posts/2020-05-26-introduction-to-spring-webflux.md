---
layout: post
title: Introduction to Spring WebFlux
author: perttihu
excerpt: >
  Spring Framework 5.0 introduced a new reactive web stack Spring WebFlux in addition to Spring MVC. In this post I'll give a brief introduction to Spring WebFlux and talk about how to choose between the two stacks.
tags:
 - Java
 - Spring
 - WebFlux
 - Project Reactor
 - reactive
---

## What is Spring WebFlux?

Traditionally Spring Framework web applications have been written with Spring Web MVC, which was a purpose-built web framework for Java Servlet API and Servlet containers, and has been part of the Spring Framework since the very beginning. Spring Framework 5.0, release in September 2017, introduced a non-blocking reactive-stack web framework called [Spring WebFlux](https://docs.spring.io/spring/docs/5.3.0-SNAPSHOT/spring-framework-reference/web-reactive.html#spring-webflux).

There were two major reasons for a new web framework. First, there was a need for a non-blocking implementation to handle concurrency with less threads (i.e. using fewer hardware resources). And then there were the possibilities of functional programming made possible with Java 8 lambda expressions which allow declarative composition of asynchronous logic.

### Reactive? Non-blocking?

Reactive and non-blocking are terms which are closely related. The term *reactive* means the style of programming where you react to change, be it an incoming network request or a user interaction event such as a mouse click. In a sense, reactive means also *non-blocking*, as you are now reacting to a change instead of waiting something to happen.

Let's consider a case where you send a request to a server. When executing a synchronous call, you are blocking the execution of your current thread until you get response from the server and the call is ready. But as you are blocking you are also implicitly handling back-pressure, which means that you cannot overwhelm the server with your requests. However, when you execute a non-blocking asynchronous call you are not anymore waiting the result. Instead you continue code execution (perhaps doing something else) and react when the result comes available. Problems arise if you send too much requests and overwhelm the destination server. There needs to be a back-pressure mechanism, which means a way for the server to indicate you to please slow down.

[Reactive Streams API](https://www.reactive-streams.org) fulfills this purpose by providing a small spec defining the interaction between asynchronous components with back pressure. As it is too low level API to be practical for applications, there are reactive libraries providing a higher-level functional API to compose asynchronous code. Spring WebFlux chose [Reactor](https://projectreactor.io) as its reactive library.

Reactor has two main types which offer a rich vocabulary of different operators to compose your asynchronous logic. A `Flux` object represents a reactive sequence of 0..N items whereas a `Mono` object represents a sequence of 0..1 items (single value or empty). When programming with Spring WebFlux you'll be playing a lot with Fluxes, Monos and their operators such as map, flatMap and filter.

## Which web framework to use?

There are a number of things to consider when choosing between Spring MVC and WebFlux.

First of all, if your application already uses Spring MVC, there is no need to switch over to WebFlux. Spring MVC is not going away anytime soon, even though its `RestTemplate` is marked as being in maintenance mode. If you have older codebase you'll probably use blocking libraries anyway. However, if your application has HTTP calls to remote services, you could give a try to the reactive `WebClient`, which is Spring WebFlux's alternative to `RestTemplate`. It works fine from Spring MVC as well and you might already see some performance gains depending on your application.

If you are starting to develop a new application, you need to evaluate your use-cases and dependencies. If you need to use blocking APIs, then it's better to stick with Spring MVC.  Examples of popular blocking APIs are persistence APIs such as JPA and JDBC. If you are considering a microservice architecture, you can have a mix of Spring MVC and WebFlux applications. For example, you could isolate your persistence needs to a dedicated microservice built with Spring MVC, and use WebFlux for rest of the microservices. Or, if you like living on the edge, you could evaluate [Spring Data R2DBC](https://spring.io/projects/spring-data-r2dbc) which provides familiar Spring abstractions and repository support for accessing relational databases with reactive non-blocking driver. Under the hood, it uses Reactive Relational Database Connectivity (R2DBC) project libraries and drivers to replace traditional JDBC. So far there are drivers for PostgreSQL, MySQL, Microsoft SQL Server and H2.

Finally, you'll also need to take into account the somewhat steep learning curve with WebFlux. Its functional, declarative, non-blocking programming model is not easy to start with if you have no prior experience with reactive programming. However, as with many other things, it's a matter of taste and after the learning curve I've grown fond of Webflux's functional style.

## My experiences with Spring WebFlux

I've been using Spring WebFlux in my project for over a year. Why did we end up choosing WebFlux and not traditional MVC?
- Our application was going to be built from scratch without burden of legacy code
- Our application mostly consists of HTTP calls to various backend systems, combining and manipulating data to a more user friendly format
- Data storage is mostly done in other backend systems

Regarding the last point, our data storage needs are not very complex nor are they the main functionality of our application. We chose to isolate our data storage functionality to a dedicated microservice written with Spring MVC and traditional blocking JDBC. Other microservices requiring data storage communicate with this microservice over REST API.  With this way we could write other parts with reactive WebFlux, evaluate the maturity of Spring R2DBC as a side track and maybe later migrate the data storage microservice to WebFlux & R2DBC.

There was indeed a learning curve with WebFlux and its functional programming style. It took me couple of weeks to get comfortable with it and start seeing the benefits. For example, when porting functionality from the old codebase to our new application, it was quite easy to see problematic patterns or clear architectural violations in the old codebase, as trying to implement similar functionality with WebFlux was surprisingly hard. It was clear quite quick that if you need to use old codebase as a reference, you only check what you need to do (e.g. which calls are needed to backend systems) but not how to actually do it.

### Tips for some common pitfalls you might encounter

#### Returning an empty value
Sometimes you just need to check something in a function, without returning a value. For example, you might need a function to check if some operation can be made. Your function returns a void value in a success case and throws an exception in an error case:
```
public Foo doSomething() {

  // Get state etc.
  Bar bar = getBar();

  checkOperationXxx(bar);

  return operationXxx(bar); // Returns foo
}

void checkOperationXxx(Bar bar) {
  // Check for access rights, etc.
  if (bar.isOperationXxxAllowed()) {
    return;
  }
  throw new OperationDeniedException();
}
```
You might try to implement this with WebFlux as follows:
```
public Mono<Foo> doSomething() {
  return getBar() // Returns Mono<Bar>
    .map(bar -> checkOperationXxx(bar)
      .onErrorResume(throwable -> { // Handle error })
      .map(aValue -> operationXxx(bar)));
}

Mono<Void> checkOperationXxx(Bar bar) {
  // Check for access rights, etc.
  if (bar.isOperationXxxAllowed()) {
    return Mono.empty();
  }
  return Mono.error(new OperationDeniedException());
}
```
However, when you return an empty value with `Mono.empty()` the result really is an empty value. You can't execute any operation such as map or flatMap to it. Your `operationXxx()` is never executed and you'll spend hours trying to figure out what's wrong.

Your next attempt might be to write the caller function as:
```
public Mono<Foo> doSomething() {
  return getBar() // Returns Mono<Bar>
    .map(bar -> checkOperationXxx(bar)
      .onErrorResume(throwable -> { // Handle error })
      .then(operationXxx(bar)));
}
```
This does work in an success case: `checkOperationXxx()` completes with empty value and then you start executing a new Mono in `then()`-function. However, `operationXxx()` is executed also in an error case! This is not what you want.

In our case we solved the issue by always returning a non-empty value, usually the same value which we pass to the function as a parameter:
```
public Mono<Foo> doSomething() {
  return getBar() // Returns Mono<Bar>
    .map(bar -> checkOperationXxx(bar)
      .onErrorResume(throwable -> { // Handle error })
      .map(b -> operationXxx(b)));
}

Mono<Bar> checkOperationXxx(Bar bar) {
  // Check for access rights, etc.
  if (bar.isOperationXxxAllowed()) {
    return Mono.just(bar);
  }
  return Mono.error(new OperationDeniedException());
}
```

This works as you want - `checkOperationXxx()` does the necessary checks and `operationXxx()` is executed only on a success case.

#### Nothing happens before you subscribe

With reactive code, you describe the steps of the operation, but nothing really gets executed before you call `subscribe()`. This is not that clear in WebFlux context, as Spring executes the `subscribe()` call to your WebFlux flow on your behalf, at least in case of REST Controller. You simply return the reactive result type from REST controller method and Spring will take care of the rest. In any case, it is good to understand.

By the way, if you use WebClient from MVC side and wonder how to get the resulting object out from reactive context, just call `.block()`.

#### Unit testing

For unit testing reactive code I recommend using the official tool, which is the `reactor-test` library. Previously we used either `subscribe()`- or `block()`-approaches, but for some reason they were not always reliable. Better to stick with the recommended way. Reactor test library comes with `StepVerifier` class for unit testing reactive flows. Here's an example:
```
@Test
void testSuccessCase() {
  StepVerifier.create(doSomething())
    .expectNextMatches(f -> f.equals(expectedFoo))
    .verifyComplete();
}

@Test
void testErrorCase() {
  StepVerifier.create(doSomething())
    .expectErrorSatisfies(error -> {
      // Assertions for error
    })
    .verify();
}
```

For testing your reactive REST Controllers you can use Spring `WebTestClient`:
```
@Test
void testGetSomething() {

  webTestClient.get()
    .uri("/something)
    .exchange()
    .expectStatus().isOk()
    .expectBody()
    .jsonPath("$.value").isEqualTo(foo.getValue());
}
```

How about testing your WebClient calls? Let's say you call some backend system to fetch some data and would like to test that functionality. While there's no built-in tool in Spring for such a case, you can use [MockWebServer](https://github.com/square/okhttp/tree/master/mockwebserver) to mock the backend. I believe Spring developers use it too for their testing purposes. Do note that you need to override both `MockWebServer` and `okhttp` library versions, because the versions coming in from Spring Boot dependency management are too old (at least in Spring Boot 2.3.0).

## Conclusion

Spring WebFlux is the new reactive non-blocking alternative to traditional Spring MVC web application framework. With recent releases of Spring Framework and Spring Security, it has almost reached feature parity with Spring MVC. For example OAuth2 functionalities in Spring Security have matching implementations for both web frameworks. Usually the reactive counterpart of an MVC class is pretty straightforward to figure out, e.g. `ReactiveSecurityContextHolder` (WebFlux) vs. `SecurityContextHolder` (MVC). So if you are starting a new Spring-based web application, do give it a try!