---
layout: post
title: Generating test data with Burp suite
author: lokori
excerpt: While Burp suite is fundamentally a tool for penetration testers and security researchers, it has other uses too. A developer could use it to neatly generate a bunch of test data for example.
tags:
- Burp
- hacking
- software security
- testing
- test data
---


## The usual story with the test data

It's not enough to test a system with one or two manually generated data points if the real usage will be in order of millions rows in the database. At the same time, it's usually not feasible to maintain a full copy of the production database for all daily development and test needs. Many developers have created various "test data generator" suites that can generate a bunch of entries to the system, but the data is made to look like it came from actual usage and doesn't contain malicious and weird inputs.

What if you don't have the generator and don't want to bother writing one just now?

The "nice" generator can also give a false sense of security. How do you know everything works correctly with weird inputs if you never test it? 

![Cunning cat](/img/burp-test-data/kisuli.png)

## Enter Burp Suite

[Burp Suite](https://portswigger.net/burp) is the de facto tool for professional security testers and security researchers to attack web applications. It contains a lot of functionality and is constantly expanding. I will only touch some functionality in this article, relevant to purposes of generating test data.

[OWASP ZAP](https://www.owasp.org/index.php/OWASP_Zed_Attack_Proxy_Project) is a nice free open source tool, which could be used in a similar fashion. 

## First, let's create one entry manually

I created a single entry manually from the browser and Burp captured the traffic. After that the request can be sent for further processing to one of the Burp's "tools", like Repeater, Attacker or Intruder. Repeater is rather boring as we would need to edit the request manually so we'll skip that here.

## Intruder attack!

After that it's simple to send the request to Burp's *Intruder* which is a tool to create multiple attacks against the same endpoint and customize the attack. The user can select which parameters or HTTP headers to test and what kind of encoders and value generators are used. 

First we need to select which part of the request we want to attack. In this case I have marked the name fields as the targets.

![Burp intruder payload](/img/burp-test-data/intruder-payload.png)

Next, I can select the value generator. In this case, for simplicity, I have chosen to generate numbers 1..10 but there are many other possibilities. You could even attach [Radamsa](https://github.com/aoh/radamsa) to fuzz inputs.

![Burp intruder options](/img/burp-test-data/intruder-options.png)

Finally, let's attack and in a matter of seconds we have a lot of data in our database.

![Burp intruder running](/img/burp-test-data/intruder-attack.png)

If you want to generate test data that is painful to handle, you could use nice input lists through the Intruder, like this [Big List of Naughty Strings](https://github.com/minimaxir/big-list-of-naughty-strings/blob/master/blns.txt). Something from [SecLists](https://github.com/danielmiessler/SecLists) might also reveal what the developer missed in input validation.


## Does this make any sense?

This is far from perfect in the sense that the data is not realistic. This can't compete with a custom made test data generator, but it's significantly bigger effort to write that test generator. And if you want to create actually malicious inputs, how do you do that with your custom tool? Download [SecLists](https://github.com/danielmiessler/SecLists) and bolt them in? Maybe, but that's even more work when you could just take Burp and press a few buttons.

And you can even automate all of this. Then you don't even need to press buttons, just run it in the CI pipeline.

## Enough talk. Attack!

![Burp intruder payload](/img/burp-test-data/attack.jpg)

Burp has another nice tool in this regard, the *Attacker*. It's basically a web app scanner, similar to [Nessus](https://www.tenable.com/products/nessus/nessus-professional), [Acunetix](https://www.acunetix.com/web-vulnerability-scanner/), ZAP and the like. It tries to enter various malicious inputs to the fields in the request and based on the server's responses it might find some actual security flaws. But assuming the backend server is not actually vulnerable and doesn't crash when faced with such hostile requests, this can be used to generate some rather interesting data entries in the database.

If there is a second order problem with the system, the scanner may not be able to detect it. For example, a stored [XSS](https://en.wikipedia.org/wiki/Cross-site_scripting) where the XSS is triggered in some other page not directly related to the store endpoint, might go unnoticed. Same thing for second order SQL injections. But if a human browses the application after the attack has run it's course, such issues can be very visible. 

You could also see all kinds of encoding issues and trouble with assumptions about field lengths and so on, which may not be security flaws, but you would want to fix them anyway because they are bugs in the system. This is something security testers rarely think about because they are not rewarded if they report mundane ordinary bugs to the developers, but if you are a developer you can understand the value in this.

So, I launched an attack towards the same endpoint and here are some of the results. Behold, what a jolly bunch of awesome people I now have in my local database!

![Generated persons](/img/burp-test-data/generated-persons.png)

I can pretty much guarantee that your puny test data generator won't generate a person with a handy name like this:
```IVAN IVANOVITSX|ping -n 21 127.0.0.1||`ping -c 21 127.0.0.1` #' |ping -n 21 127.0.0.1||`ping -c 21 127.0.0.1` #\" |ping -n 21 127.0.0.1```


## Why should we care about messieur ```IVAN <scRIpT>alert(42)//``` ?

Because he's awesome and he has now mastered omnipresence. He's everywhere. The notorious ```IVAN <scRIpT>alert(42)//``` will come to visit you one day so better be certain that everything works. Even if no one tries to hack you, sooner or later someone will throw something extremely weird into your API. Don't think you are fine because you are using some hocus pocus encoder library or parser. Test it!

The good news is that This is a low hanging fruit. You don't need to be a hard core hacker to do what I described here. Any developer could do this with a few hours of practice with the tools. It's much easier to detect the easy bugs and potential security flaws than to actually exploit them succesfully.

