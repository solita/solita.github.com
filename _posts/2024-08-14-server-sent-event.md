---
layout: post
title: Server-Sent Events (SSE)
author: shamsss
excerpt: A light-weight introduction to Server-Sent Events (SSE), how it compares to WebSocket, and a simple example demonstrating SSE with Node.js and Express.
tags:
 - Server-Sent Events
 - Server
 - WebSocket
 - Node.js
 - Real-time Communication
---
Server Sent Events or SSE is a “server push” styled real-time communication protocol between a server and a client. It was introduced way back in 2005, became part of HTML5 in 2014 and currently it is supported by all major web browser like - Chrome, Firefox, Safari, etc.  In a way, SSE resembles a lot of WebSocket, but there are some fundamental differences. In this article, I want to go into the difference between WebSocket and SSE, use cases and good-to-knows of SSE, and finally a short example demonstrating Server Sent Events. 

### Server-Sent Events vs WebSocket

While both SSE and WebSocket are used for 'real-time' communication, one of the fundamental differences lies in directionality. WebSocket allows for both the client and server to send data between each other bidirectionally, whereas SSE as one can infer from the name only allows the server to send data to the client, hence unidirectional. WebSocket can transfer either binary data or unicode text, but SSE is only limited to text which has its own mime type (`text/event-stream`). Also the underlying technology for each of these are also different. SSE uses the HTTP protocol (supports both HTTP/1.1 and HTTP/2) and WebSocket, on the hand, uses its own WebSocket protocol. This makes the set up for SSE simpler than WebSocket with less overhead and blends in well with any other regular HTTP endpoints. Furthermore, SSE inherits standard HTTP security features including Same-Origin Policy enforcement by browsers, whereas WebSocket uses its own protocol which doesn't inherently restrict origins, requiring careful server-side implementation to prevent potential cross-origin attacks.

### Use Cases and Good-to-Knows
Based on the discussion up to now, a conclusion can be drawn that SSE is best suited in cases where realtime communication between a client and server is necessary but the client does not need to send any information back the server itself. For example, the state of a process running on the server that the client needs to be aware but has no need to send any data back simultaneously can be a good case for the use of SSE. Both the server and the client can also terminate the request at any time and termination can be handled accordingly. In implementing SSE, the client subscribes to the stream using the [EventSource](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) Web API.  The data sent over follows the [Event stream format](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#event_stream_format). This will make more sense after the demo. Finally, it is worth noting that, SSE allows for automatic reconnection, which allows the client to retry connecting to the server in case the connection is disrupted in a exponential backoff manner and if connection is reestablished, server can resume sending from the last sent event, resulting in no loss of events. This is thanks to EventSource keeping track of event IDs and on a successful reconnection sending the last event ID. The number of retry attempts can be modified at the start. 

### Demo

Now it’s time for the demonstration. Let’s start with our client. Here’s a simple `index.html` file with the JavaScript that uses the EventSource API and its `onMessage`  method to handle messaging with the HTTP server:

**Client:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SSE Client</title>
</head>
<body>
    <h1>Server-Sent Events Demo</h1>
    <div id="events"></div>

    <script>
        const eventsDiv = document.getElementById('events');
        const eventSource = new EventSource('/events');

        eventSource.onmessage = function(event) {
            const newElement = document.createElement('p');
            newElement.textContent = `${event.data} (Event ID: ${event.lastEventId})`;
            eventsDiv.appendChild(newElement);
        };
    </script>
</body>
</html>
```

Implementing the server side logic for SSE is possible in most common server side programming languages and frameworks. For now, I will demonstrate with a Node.js and Express framework. Let’s see the code in `server.js` file: 

**Server:**

```jsx
const express = require('express');
const app = express();
const path = require('path');

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.get('/events', (req, res) => {
  res.writeHead(200, {
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive'
  });

  let id = 0;
  const intervalId = setInterval(() => {
    res.write(`event: message\n`);
    res.write(`id: ${id}\n`);
    res.write(`data: Server time: ${new Date().toLocaleString()}\n\n`);
    id++;
  }, 2000);

  req.on('close', () => {
    clearInterval(intervalId);
  });
});

const PORT = 8080;
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
```

Assuming the `index.html` file is available at the same level, it is being served at the root. If the node dependency is available, running `node server.js` should start the server on [`localhost:8080`](http://localhost:8080) and you should be able to see message being received on the client side in every `2s` interval. Like so:

![image.png](/img/2024-server-sent-events/image.png)

As you can see, it takes very little effort implement SSE on the server side, essentially just setting necessary headers, sending the data, and handling termination if needed.  

I understand this a rather simple and somewhat contrived example, but the idea was to give a gentle introduction to SSE to the readers. Perhaps, now you will consider SSE if you need one-directional real time communication from your server with your browser client. Thanks for reading!