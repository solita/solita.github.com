---
layout: post
title: Staying un-pwned with HTTP Security Headers
author: massimo
excerpt: >
  Your fancy front-end framework won't print unescaped HTML. But what if it does after the next update? To protect your app, you need security layers. Like an onion, each layer means more tears for the attacker. HTTP security headers form one of these layers. Here are the essential security headers for every non-trivial site.
tags:
- infosec
- software security
- devsecops
---

Defense in depth as defined by Wikipedia is a:
> concept in which multiple layers of security controls (defense) are placed throughout an information technology (IT) system

## Onion in eye

![onion](/img/http-security-headers/onion.jpg)

The purpose of the aforementioned security controls is to provide defense against attacks in a layered fashion. If one security control fails, there is another deeper in the stack. This deters the attacker and gives the defender more time to contain the threat before the next control is breached. Like when an onion is peeled, every layer brings more tears.

## Already fscked? :|

The harsh reality of web applications is that they are complex beasts. Even if your code isn't buggy, maybe someone else's is? Maybe you are shipping that code inadvertently by using a vulnerable library? Or a web server that is [insecure by default?](https://blog.trendmicro.com/trendlabs-security-intelligence/busting-ghostcat-an-analysis-of-the-apache-tomcat-vulnerability-cve-2020-1938-and-cnvd-2020-10487/)

Sooner or later you will forget to patch something and then it's just a matter of time until you are pwned.

Wait a minute. You just remembered that security thing you were supposed to do but an urgent customer request made you put it off in the back of your brain.

There are many ways to stay un-pwned and if you are reading this post, it's up to you to implement them.

Yes, you.

![what me](/img/http-security-headers/whatme.jpg)

When thinking in a layered fashion, what protection do you have against XSS?

There is your fancy WAF (Web application firewall), it'll block anything malicious! What if there was a way to circumvent it? Well, your fancy front-end framework won't ever print unscaped HTML! But what if it does after the next update? There's always a what if.

A cheap and easy way to implement another layer of security is to use HTTP security headers.

## Enough, where's the ~~beef~~ tofu

![tapping](/img/http-security-headers/tapping.gif)

This is not a comprehensive list of all security headers. These are the bare minimum every non-trivial site should use.

### Content Security Policy (CSP)

[CSP](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP) is a powerful if a bit unwieldy header that protects you against XSS. The power comes from the means to restrict what types of resources can be loaded and from where. The unwieldiness comes from the trouble of creating a secure but working policy for a complex site. 

Example: allow loading content (images, media, scripts) only from the same origin
```
Content-Security-Policy: default-src 'self'
```
Example: allow images from anywhere, media from your site's subdomains, scripts from a particular subdomain of your site
```
Content-Security-Policy: default-src 'self'; img-src *; media-src *.mysite.com; script-src scripts.mysite.com
```

To ease the process of commissioning a CSP, it can at first be deployed in report-only mode. Reports can also be [sent to a custom URL.](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP#Enabling_reporting)
```
Content-Security-Policy-Report-Only: policy
```

[Laboratory](https://addons.mozilla.org/en-US/firefox/addon/laboratory-by-mozilla/) is an awesome plugin for Firefox that helps you to generate a CSP policy by analyzing your requests.

Side note: after the introduction of CSP, the previous header responsible for XSS protection, *X-XSS-Protection* has [become](https://groups.google.com/a/chromium.org/forum/#!msg/blink-dev/TuYw-EZhO9g/blGViehIAwAJ) [obsolete](https://blogs.windows.com/windowsexperience/2018/07/25/announcing-windows-10-insider-preview-build-17723-and-build-18204/).

### HTTP Strict Transport Security (HSTS)

When you visit a site that redirects from HTTP to HTTPS, for a brief moment you are vulnerable. An attacker on the same network (e.g. coffee shop WiFi) can intercept your request and redirect it to their own site. This is known as a man-in-the-middle attack (MITM).

The [HSTS header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security) prevents the browser from ever loading a non-encrypted version of a site. There is, however, a catch.

The HSTS header can only be sent via HTTPS. When connecting to a site for the very first time, the connection is unencrypted before the first redirect to HTTPS. After that, the browser will force HTTPS for every request. This will last for the duration specified in the header's max-age value (recommendation is one year). The max-age value is refreshed after each request if the HSTS header is present.

So I can still get pwned? Yes, always. But most browsers nowadays use a [preload list](https://hstspreload.org/) which is a list of sites that support HSTS. Your browser will automatically use HTTPS when connecting to these sites.

HSTS example, note that includeSubDomains can kill any subdomains not using HTTPS!
```
Strict-Transport-Security: max-age=31536000;
```

### X-Frame-Options

Nice app you have there. Shame if someone used it to PWN.

Picture this. You've built an app that has a button that does stuff. Important stuff. Someone notices your app can be embedded to their own site so they mask the button with an irresistible "You've won the Internet!" banner. A user clicks the banner but the click goes through to the important button. With your signed-in credentials. Uh-oh.

All of this hassle could've been prevented with a [single header.](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options)

For more examples, check out the [full spec.](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy)
```
X-Frame-Options: deny
X-Frame-Options: sameorigin
```

## Go forth and do some good

![go forth](/img/http-security-headers/goforth.jpg)

Also, consider implementing:
- Referrer-Policy: prevents your URLs leaking to other sites
- X-Content-Type-Options: prevents your browser from doing stupid file type guesswork
- Feature-Policy: lock down browser APIs such as camera or microphone from being used by other sites you embed

I recommend the [Mozilla Developer Network docs on HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP). It's comprehensive, easy to understand and has lots of great examples.

