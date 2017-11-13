---
layout: post
title: Testing AWS Lambda Functions and S3 with Node.JS
author: atteheino
excerpt: Thoughts of an integration developer on testing AWS Lambdas written with Node.JS.  
tags:
- AWS
- Lambda
- S3
- Testing
- Node.JS
- integration
- Serverless
---

### What's the job?
I needed to write tests for AWS Lambda functions that receive JSON events that need to be persisted to S3. The Lambda gets the events from AWS API Gateway endpoint that is called by another system. Sounds simple right?

So I went ahead and chose [Mocha.js](https://mochajs.org/) as my testing framework as I have worked with it previously. Installed it from NPM as a dev dependency to the project. Next I figured out that I need to mock S3 as I don’t want to have external systems hooked up for my unit tests. I also needed some way to easily test Lambda functions.

So Google, tell me what is the tool for the job:
- [mock-aws-s3](https://www.npmjs.com/package/mock-aws-s3) sounded like the tool for me. This library mocks most common use cases for S3. It also supported the upload method that I was using. Perfect. *** MISTAKE #1 ***
- [lambda-tester](https://www.npmjs.com/package/lambda-tester) sounds good. It simplifies testing lambdas. So  I installed both of these as dev dependencies.

### Let's get it done
Started writing tests. At about the same time (I know I shouldn't multitask) I was also working on the [Serverless](https://serverless.com/) config that I had in the root of the project directory. I had just one package.json that had the Lambda dependencies, test dependencies and Serverless framework dependencies. As I was soon about to find out, this setup of one package.json was bloating my lambda function package size with some totally unneeded libraries. I went ahead and split the project up so that I now have three package.json files and also three node_modules directories:

```
PROJECT ROOT
- serverless.yml
- package.json
- src/
    - package.json
- test/
    - package.json
```

After configuring Serverless to include files only from certain directories I was able to keep my Lambda package size minimal without having to resort into any black magic.

```
package:
  exclude:
    - ./**
  include:
    - src/**
```

### Creating the test

Okay, back to testing. I picked up [Mockery](https://www.npmjs.com/package/mockery) to help me wire up aws-s3-mock to the tests. So I wrote a test where I require Mockery and use the ```mockery.registerSubstitute``` method. The test is really simple:

1. Require sample event from file
2. Feed it to the lambda using lambda-tester
3. Validate that writing to S3 succeeds (mocked) and nothing on the way breaks.

I defined ```mockery.enable()``` and ```mockery.disable()``` into Mocha’s default ```before()``` and ```after()``` functions as suggested in some user post somewhere in the internet.
*** Mistake #2 ***

I placed the before and after method calls to the *global* function scope:

```javascript
'use strict'
const mockery = require('mockery')
const LambdaTester = require( 'lambda-tester' )
const event = require('../lambda_sample_events/lambda_event.json')

before(function() {
  mockery.enable({ useCleanCache: true, warnOnReplace: false,
  warnOnUnregistered: false })
  ...

describe( 'event changes handler', function() {
  ...  

)}
```

### Include environmental values

I have several tests in different files testing different use cases and source files. Each require Mockery and setup it. The test runs, but fails because my lambda environment variables are not present. Okay, So bring in [dotenv](https://www.npmjs.com/package/dotenv) and create the required setup for each use case:

```javascript
require('dotenv').config({path: __dirname + '/.envForProduct'})
```

Run the tests again and the mock is not working as the config object for the S3 is missing update method. So I try to define the Mock object as follows:

```javascript
const S3 = require(‘aws-s3-mock’)
const s3Mock = {
 S3: S3,
Config: { update: function …
```

Run again and it almost works.. Now it’s loading and running the test but failing on the  ```s3.upload(S3_PARAMS).promise()``` promise() function call. The aws-s3-mock upload implementation does not support promises. Oh …

### Getting over the disappointment

Bang my head to the wall for a while and then decide to simplify the test. I decide to separate the uploading to S3 from the rest of the code. So I create a really simple implementation:

```javascript
const sendToS3Imp = function(S3_PARAMS){
 return s3.upload(S3_PARAMS).promise()
}
module.exports = { sendToS3: sendToS3Imp }
```

I tie this to the rest of the function code and create my own S3 mock:

```javascript
const sendToS3Imp = function(S3_PARAMS){
 return Promise.resolve()
}
module.exports = { sendToS3: sendToS3Imp }
```

*** Mistake #1 Solved ***

Summary: I should not have tried to implement a complicated mock for the S3 as I did not need to actually verify anything on the S3 part, but rather test that the rest of the code works as it should. Keep it Simple!

### Refactoring the test

So back to the test. I removed the aws-s3-mock and replaced it with a really simple custom mock for S3:

```javascript
'use strict'
const mockery = require('mockery')
const LambdaTester = require( 'lambda-tester' )
const expect = require('chai').expect
const fileEvent = require('../lambda_sample_events/file_lambda_event.json')
const S3Mock = {
  sendToS3:  function(S3_PARAMS){
      return S3_PARAMS.Body.indexOf("100002")==0 ? Promise.resolve(): Promise.reject(new Error("FAIL"))
  }
}

before(function() {
  mockery.enable({ useCleanCache: true, warnOnReplace: false,
  warnOnUnregistered: false })
  mockery.registerMock('./s3', S3Mock)
})
after(function(){
  mockery.deregisterMock('./s3', S3Mock)
  mockery.disable()
})

describe( 'file Changes handler', function() {   

    it( 'writes to S3 succesfully', function() {
        return LambdaTester( require('../../src/file-changes.js').handler )
            .event( fileEvent )
            .expectResult()
    })
```

I run the test and it’s not loading the mock I’m expecting it to. What the…???

### Day 2

Next day debug the hell out of the test and it just doesn’t make any sense. Finally some gut feeling says to me to move the ```before()``` and ```after()``` inside the test suite. *** Mistake #2 *** solved. So what happened was mocks were being loaded at the same time that the tests were being loaded by Mocha and there can be only one present at a time. So when the tests were being run, the last mock being loaded was used in all the tests no matter what I had configured. After moving the setup and teardown to the correct place, the setup & teardown were being run at the correct time and resulting in having the correct mock loaded at the correct time.

Working example:

```javascript
'use strict'
const mockery = require('mockery')
const LambdaTester = require( 'lambda-tester' )
const expect = require('chai').expect
const fileEvent = require('../lambda_sample_events/file_lambda_event.json')
const S3Mock = {
  sendToS3:  function(S3_PARAMS){
      return S3_PARAMS.Body.indexOf("100002")==0 ? Promise.resolve(): Promise.reject(new Error("FAIL"))
  }
}

describe( 'file Changes handler', function() {   
    before(function() {
      mockery.enable({ useCleanCache: true, warnOnReplace: false,
      warnOnUnregistered: false })
      mockery.registerMock('./s3', S3Mock)
    })
    after(function(){
      mockery.deregisterMock('./s3', S3Mock)
      mockery.disable()
    })

    it( 'writes to S3 succesfully', function() {
        return LambdaTester( require('../../src/file-changes.js').handler )
            .event( fileEvent )
            .expectResult()
    })
```


## Summary:
- Write Lambda function implementations so that they are easy to test.
- Lambda-tester really works and makes testing lambdas simple.
- Know your test suite. (I could have saved a lot of time if I had not misplaced the setup & teardown functions)
