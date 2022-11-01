---
layout: post
title: Testing primer - lessons to learn from Solita development academy exercises
author: hjhamala
excerpt: >
  
tags:
  - testing
  - career development
  - coding
---

The Solita developer [academy](https://www.solita.fi/en/academy/) is a way to kickstart a career in software development. Applying for the academy fall 2022 required to make [a pre-assignemt](https://github.com/solita/dev-academy-2022-fall-exercise). The assignment was based on the Helsinki Capital area city bike journey statistics. We received many great exercises.  

One surprising thing was that there were few or no tests in many applications. Pre-assignment mentioned tests quite clearly. After going through the exercises I found some of the exercises mentioned that an applicant had found difficult to make meaningful tests. 
 
I think that as professional developers we may have forgotten that writing good and useful tests have not been an easy thing to learn - not for me at least. Therefore I present a quick primer based on Solita's fall assignment and how it could be tested. The blog post is mainly aimed at beginner developers. 

## Why do we test?
First, we should think about the reason why we even bother to write tests. The next three reasons rise to my mind
* Tests are quality control. Tests tell us that the things we are developing do the right things - the right way.
* Tests help find out regressions. Changing the code like refactoring is easier and less nervous when we have confidence that the software works after the changes.
* Tests are part of the documentation. In many cases, tests can be used to find out how libraries/APIs are expected to be used.

## How we test

Classically tests are split into three main types of tests.
![paste](/img/testing-primer/Testing_Pyramid.svg)
(source: Abbe98, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons)
* Unit tests test software modules in isolation from each other. 
* Integration tests are used to find out that components/modules work together
* E2E tests test the whole application - for a web application this could mean testing the application flow with an automated browser

The test types are typically visualized as a testing pyramid where unit tests are at the bottom. The size of the area tells us also how many tests should we have from the different types.

For small applications - like Solita assignment - it may be quite hard to make a clear difference between integration and unit especially if the application is not split into clear components. The term unit may also cause some confusion. Typically in the object-oriented programming unit is a class. In other paradigms, it may be as simple as a simple function.   


## Testing approach
One good approach to testing is through the requirements. The pre-assignment contained the next requirements
* The journey and the station data should be parsed, validated, and persisted, short trips should be parsed out
* The journey list should be paginated
* For each journey show departure and return stations, covered distance in kilometers and duration in minutes
* Top 5 return and departure stations from a station

## Testing the datasets

The journeys are in the dataset in the next format
Departure time, arrival time, departure station id, departure station name, target station id, target station name, length of the trip in meters, Duration (sec.)

2021-05-01T00:00:11,2021-05-01T00:04:34,138,Arabiankatu,138,Arabiankatu,1057,259

The datatypes after parsing are: 
DateTime in ISO format: Departure time, arrival time
Integer: departure station id, target station id, Duration (sec.)
String:  departure station name, target station name

I would start the testing by creating a simple validation function

validateJourney(csvLine: string) => boolean 

Then I would make bad scenario tests 
* It should reject a journey where departure time is not a parseable DateTime (and the same for an arrival time)
* It should reject a journey where arrival happens before departure
* It should reject if a departure station id is not a positive integer (and the same with arrival and length of the trip)
* It should accept a valid trip
* It should reject a trip that is less than 10 seconds (this came from the pre-assignment)

The same approach could be used for the station data where the addition coordinates should be validated to be valid geographic coordinates.

## Testing the persistence layer (internal API)
Next, I would consider testing some functional requirements like a paginated journey list. In very simple applications the database queries may be implemented inside the routes but a more clean option would be to create some sort of internal API for the application. Using the application's API guides us toward testable and modular code with clear APIs.

Whether internal API is implemented or not then first the tester should decide whether the test would test against the actual database or not. In the era of easy Docker, I would prefer using the real database in many cases. The second consideration should be how the DB should be prepopulated for the tests.

The options could be:
* Making a docker image that has a database for the testing with a prepopulated situation
* Pre-populating the database with raw SQL inserts
* Using the API of the application to prepopulate the database.

The first two options are quite similar and easy to make. The problem with the second option is that it may easily break if the database schema has been changed. 

I prefer to use the API for setting up the persistence layer for tests. The API hides database internals from the tests so changing the internal data model should not break the tests. Or if it will break the tests then the API is broken and should be fixed.

Likewise, if the service API contains any mutating operations like adding a trip to a database that should not be tested by making a raw SQL query against the database. The test for mutation should add a trip via API and then retrieve it via API. 

## Testing API validation

One layer to test should be validating inputs from the UI layer. If a server has a route for getting information about a single station then tests could be written out for:
* It should return 404 for trying to retrieve the nonexisting station
* It should return 400 if the station identifier is syntactically invalid - if numbers are used then giving a string should return this error
* It should return 200 and the station info for a valid call.

If some sort of dependency injection or mocking can be used then the service call inside the router could be mocked to return syntactically valid data. One option is to populate the persistence using the internal layer via internal API. 

## Testing UI
Last some thoughts about testing the UI. There exist few options. First E2E tests could be made with [Cypress](https://www.cypress.io/), [Selenium](https://www.selenium.dev/), [Playwright](https://playwright.dev/), or other browser automation software. These kinds of tests need somehow handle the persistence pre-population where one option is to use the UI to add data and then use that same UI to read. Unfortunately, E2E tests are very easy to break simply by changing the UI. They are also the slowest type of tests.

Another option is to test the UI in isolation. [React testing library](https://testing-library.com/docs/react-testing-library/intro/) is a good choice for React users. Other frameworks have their testing libraries, so there is no excuse not to test. With [Mock Service Worker](https://mswjs.io/) it is possible to make quite fast UI tests with mocked backend.  

Whether Cypress or any other library is used, it is very preferred to make tests use the UI by finding elements - like buttons - via roles not via data-id or something else hard coded that would make the test fail if the button does not have the required role. Another advantage of using the roles is that the UI is more accessible for screen readers for visually impaired people.

## Structuring the code to make it easier to test
Some advice may be given on how the code can be made easier to test. One thing is to separate the code that does side effects from the code that does not. Side effectless code that output is fully based on its inputs is idempotent. That means that tests with the same input run always with similar results. If the results of the function are based somehow on the time then the time can be given as a parameter instead of determining the time inside of the function.

Another thing is the structure of the code. Especially if the tests are not written before the code, it is important to structure the code to show clear logic. This makes it much easier to write test scenarios for the code. 

## Epilogue
Hopefully, this blog post has given some advice on how applications could be tested. Writing tests can be sometimes tedious thing to do. I find tests also many times very fun to do. I can design an interface for an API by simply writing tests. If using the API from the tests is hard - maybe the API is truly hard to use. 


