---
layout: post
title: Please write a README
author: jgke
excerpt: >
  Every time you skip writing a README, a puppy dies.
tags:
 - Software development
---

How many times have you opened up a project and seen a README like this?

````
example-project$ cat README.md
# example-project

$
````

Next, you have to find out what the repo is about and how to get it to start,
and soon you've used up two hours of your time on something you could have read
in 30 seconds. The problem gets even worse if you have to ask colleagues about
any of those, as now you're using up multiple people's time where a couple of
lines of text would have been enough.

This also applies if you've created the repo yourself! If you leave a project
dormant for a few months, you *will* forget how you can boot your software...
with the exception that you now have zero people to ask. Would it have been
nice if you had spent the few minutes of your life back when it was just a few
minutes?

Having to endure the lack of basic documentation reduces the output you create,
reducing the effectiveness of you as a cog in the machine. This will cause
dynamic effects to permeate through the economy, reducing the total amount of
money people have available to upkeep their pets, and...

![A small dog looking at the camera](/img/please-write-a-readme/dog.jpg)

Every time you create a project with a lacking README file, a puppy dies.

## What if you walk into a project with a bad README?

Fix it. It takes literally 5 minutes for you to fix the mistakes of the
previous person. At the same time, you get to set up the project on your
computer and verify that you understand what the project does.

## What should be the bare minimum for a README?

- what is the project about
- initial setup instructions
- how to run the project
- how to test the project
- how deployment works

Bonus points if you can also include how to use the software.

## Example README

Please copy this to your project if you're feeling uninspired.

````markdown
# Project Name Here

A project for frobicating widgets using Frobicator. The project is running at
https://example.com

## Local development

Dependencies: Java 21, Node 24, Docker

Starting backend:

```
docker-compose up
cd backend
./gradlew bootRun
```

Starting frontend

```
cd frontend
npm install
npm run dev
```

## Running tests

Backend:
```
./gradlew test
```

Frontend (ensure backend is running):
```
npm run test
```

Format frontend:
```
npx prettier --write .
```

## Deploying:

The code merged to `main` will be automatically deployed to the test
environment at test.example.com and deployed to production at example.com by
approving the deployment.
````

## See also

- [makeareadme.com](https://www.makeareadme.com/)
- [readme-templates.com](https://www.readme-templates.com/)

Dog photo taken by [@miaandersonphotography](https://unsplash.com/@miaandersonphotography)
