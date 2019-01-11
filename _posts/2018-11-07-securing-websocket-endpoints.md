---
layout: post
title: Securing WebSocket Endpoints Against Cross-Site Attacks
author: eerohe
excerpt: WS, CSRF, XSS, SOP, CORS, CSP… WTF?
tags:
- WebSocket
- Security
---

Trying to find accurate information on how to properly secure a WebSocket endpoint from Cross-Site Request Forgery (CSRF) or Cross-Site Scripting (XSS) attacks is surprisingly difficult. Some of the information out there is incomplete, misleading, or just plain wrong.

In this article, I’ll attempt to provide a concise summary of what works and what doesn’t. I’ll try to make it an article I wish I’d have had available back when I first started researching this topic.

To achieve that, I’ll begin by giving a high-level introduction on some common CSRF and XSS mitigation strategies and explain how they relate to WebSockets.

**Disclaimer**: I am *not* a security professional. Don’t take what I write here as gospel. If you spot any mistakes or outright falsehoods, please let me know.

## Same Origin Policy

The [Same Origin Policy] (SOP)[^1] is a security mechanism built into modern web browsers. It stops scripts on one web page from accessing data on another web page.

For instance, if you open foo.com in your browser, SOP prevents JavaScript on that page from loading resources on bar.com or anywhere else.

You can try it out yourself:

1. Open [google.com](https://www.google.com).
2. Open your browser’s developer console.
3. Type in this JavaScript snippet:

```javascript
// Make an XMLHttpRequest on solita.fi
fetch('www.solita.fi').then(
  // Print the response into the console
  (response) => console.log(response)
);
```

You’ll get an error that looks something like this:

>Cross-Origin Request Blocked: The Same Origin Policy disallows reading the remote resource at www.solita.fi/. (Reason: CORS request did not succeed).

WebSockets, however, are not subject to Same Origin Policy. That means that if you have foo.com open in your browser, it will let you connect to a WebSocket endpoint at bar.com/ws. Open [google.com](https://www.google.com) again and type this into your browser's developer console:

```javascript
var ws = new WebSocket("wss://echo.websocket.org");
ws.onmessage = (event) => console.log(event.data);

// Wait for a couple of seconds for the WebSocket connection to open.
ws.send("Hello, world!");
```

The text `Hello, world!` should appear in your console.

This means that unless you take extra steps to protect it, your WebSocket endpoint is vulnerable to CSRF attacks.

Here’s an example of how an attacker could exploit the lack of SOP enforcement on WebSocket connections:

1. The attacker uses social engineering to lure you onto their nefarious web page at evil.com.
2. The attacker hopes you’re currently logged in to foo.com with the same browser that you used to open evil.com.
3. evil.com opens a WebSocket connection to foo.com/ws and steals your data.

The way browsers work is that if you're already logged in to foo.com and a script makes an [XMLHttpRequest] on that domain, the browser sends your session cookies for foo.com with that request — even if the script makes the request from somewhere else than foo.com.

So, if you’re already logged in to foo.com with the same browser that you’re using to visit evil.com, the browser sends your session cookies for foo.com together with request evil.com makes on the WebSocket endpoint at foo.com/ws, allowing the attacker to bypass authentication for your site.

Next, I’ll go over some of the recommendations I’ve come across for protecting your WebSocket endpoint against CSRF attacks like this and comment on their effectiveness.

## Cross-Site Request Forgery

Some sources advocate securing your WebSocket endpoint with an anti-CSRF token. For example, in [Cross-Site WebSocket Hijacking (CSWSH)](https://www.christian-schneider.net/CrossSiteWebSocketHijacking.html), Christian Schneider writes:

>Use session-individual random tokens (like CSRF-Tokens) on the handshake request and verify them on the server.

The [WebSocket handshake request] is an HTTP GET request on your WebSocket endpoint. For example, let’s say the address of your WebSocket endpoint is foo.com/ws. To open a CSRF-proof WebSocket connection, you’d make an HTTP GET request that looks something like this:

```
GET /ws HTTP/1.1
Host: foo.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13
X-CSRF-Token: U1e7Zk8mxu9HWVAQQFIVGkR5n0bVE59pq+LYwwbl7YPTrGaF3FySb0hexZhxWlg+LT+DAtBiVvbg32x3
```

The bit we'll focus on here is the `X-CSRF-Token` header. It tells the server that the handshake request originates from a source that’s allowed to connect to the WebSocket endpoint. The server compares this token with its own, and if they match, the server sends the client a handshake response, accepting the connection request.

Anti-CSRF tokens are effective against CSRF attacks. However, it might not be immediately clear how to safely deliver the token to the user of your WebSocket endpoint.

Providing it in the handshake response isn’t useful. At that point, the WebSocket connection is already open and there’s nothing left for the token to secure.

Here are two options for delivering the token to your users:

1. Embed the token into one of the HTML pages of your web application.
2. Create a REST endpoint where your client can fetch the token.

    For example, create an endpoint at foo.com/csrf that responds to an HTTP GET request with the anti-CSRF token.

Imagine once more that you get lured onto evil.com. It tries to connect to your WebSocket endpoint at foo.com/ws. SOP doesn’t apply, so the browser allows it, and since you’re already logged in to foo.com, it sends your session cookies, too.

However, evil.com can’t make an XMLHttpRequest to fetch the anti-CSRF token from the HTML page or the REST endpoint at foo.com because SOP prevents it. Even if the anti-CSRF token is in the session cookie, the attacker can’t read the value of the cookie and put it where the server expects it to be. This makes anti-CSRF tokens effective against CSRF attacks.

Note, though, that all of the above only applies when browsers adhere to SOP. There is a mechanism called [Cross-Origin Resource Sharing](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) (CORS) that allows you to relax Same Origin Policy. It allows you to set HTTP headers that allow scripts on other web pages to load resources on your web page.

Therefore, whether you deliver the anti-CSRF token embedded into a HTML page or via a separate GET request, you must make sure that your site does not use CORS headers that allow cross-origin requests to those resources. Otherwise evil.com will be able to retrieve your anti-CSRF token and use it to connect to your WebSocket endpoint.

There’s much more to be said about CSRF attacks and anti-CSRF tokens. To get a more complete picture, see [OWASP’s Cross-Site Request Forgery Prevention Cheat Sheet][CSRF Cheat Sheet].

## The Origin Header

An alternative to using an anti-CSRF token is to use the [`Origin` HTTP header][Origin]. Every request that browsers make on one web page that target another web page include the `Origin` header. As per its name, it contains the *origin* of the request. The origin comprises the scheme, hostname, and port of the source of the request.

For example, if a browser makes a request from evil.com:8080/bar to foo.com/ws, `Origin` looks like this:

```
GET foo.com/ws HTTP/1.1
…
Origin: evil.com:8080/bar
```

To use `Origin` as an anti-CSRF mechanism, you can check whether the value of `Origin` matches one of the whitelisted origins in your request handler on the server. If it doesn’t, the server must disallow the request.

There appears to be some confusion on whether an attacker can simply spoof `Origin` to conduct a CSRF attack. For example, a [Heroku article on WebSocket security](https://devcenter.heroku.com/articles/websocket-security#origin-header) says this about the `Origin` header:

>However, remember that the Origin header is essentially advisory: non-browser clients can easily set the Origin header to any value, and thus “pretend” to be a browser.

It’s true that non-browser clients (such as cURL) can “pretend to be a browser” insofar as they can spoof the `Origin` (and any other) headers. `Origin` is nonetheless a valid anti-CSRF mechanism. Remember how CSRF attacks can bypass authentication: if you’re already logged in to foo.com in your browser, the browser bundles your session cookies with all XMLHttpRequests, regardless of where they originate.

A non-browser client, however, cannot access the session cookies stored in your browser. Even if the attacker spoofs `Origin`, their request will be denied because they’re not authenticated.

Conversely, browsers control the `Origin` header. An attacker cannot set the value of `Origin` with JavaScript such that the value they set actually reaches your web server.

Using `Origin` can be a simpler way to prevent CSRF requests. There’s a downside to checking `Origin`, however: if you run many instances of the same website or your site is accessible via multiple different addresses, you’ll have to configure the `Origin` check to account for all of those addresses.

## Content Security Policy

[Content Security Policy] (CSP) is a mechanism for preventing Cross-Site Scripting (XSS) attacks. Essentially, CSP allows you to set rules that say:

>While you're on this web page, you're only allowed to load scripts and styles from this set of sources.

There are two ways to use CSP:

- Set the `Content-Security-Policy` header in your HTTP response
- Use the CSP `meta` element in your HTML

Some sources advocate using CSP to secure your WebSocket endpoints. For example, [WebSockets - An Introduction](https://gist.github.com/subudeepak/9897212#websockets---an-introduction)[^2] says that setting `Content-Security-Policy` to `connect-src ‘self’` “prevents webSockets [sic] requests from any place but the current server.”.

This is not true, however. CSP does *not* prevent evil.com from loading anything at all on foo.com. It works the other way around: it inhibits foo.com/ws from loading anything on other web pages, if you tell it to.

With regard to WebSockets, the only type of attack CSP can prevent is one where an attacker manages to inject JavaScript into foo.com that tries to open a WebSocket connection to a server the attacker controls.

Therefore, while certainly a valuable security mechanism, CSP is not effective against CSRF attacks.

For more information on CSP, see [Content Security Policy on MDN][Content Security Policy].

## Conclusions

To secure your WebSocket endpoint against CSRF attacks, consider these options:

1. Use an anti-CSRF token.
2. Check the `Origin` header of every WebSocket handshake request.
3. Both.

If you use an anti-CSRF token, deliver it to your users such that cross-origin browser scripts cannot acccess it: either embed it into your HTML page or allow users to fetch it with a separate GET request. In both cases, make sure your CORS headers disallow requests to that resource.

While using a Content Security Policy on your site is effective against XSS attacks, it does nothing to prevent someone from connecting to your WebSocket endpoint. It is therefore not a valid anti-CSRF strategy.

As an alternative to WebSockets, you could consider [Server-Sent Events][SSE] (SSE). Unlike WebSockets, they use the HTTP protocol, and are therefore subject to SOP just like regular XMLHttpRequests.

*Thanks to Timo Mihaljov for his insights on CSRF and CSP.*

[SSE]: https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events
[CSRF Cheat Sheet]: https://www.owasp.org/index.php/Cross-Site_Request_Forgery_(CSRF)_Prevention_Cheat_Sheet
[Content Security Policy]: https://developers.google.com/web/fundamentals/security/csp/
[Origin]: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Origin
[Same Origin Policy]: https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy
[WebSocket handshake request]: https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API/Writing_WebSocket_servers#The_WebSocket_Handshake
[XMLHttpRequest]: https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest

[^1]: Many sources mix up Cross-Origin Resource Sharing (CORS) with Same-Origin Policy (SOP). Often, when you see people talking about CORS, they actually mean SOP. CORS is a method for lifting some or all of the restrictions that SOP imposes.
[^2]: I’m mentioning this source because it appears second in my Google search results for “WebSocket security”.
