---
layout: post
title: "Understanding MCP: Connecting Language Models to the Real World"
author: janne.tuhkanen
excerpt: >
  In this blog we go through how the Model Context Protocol (MCP) is transforming the way we build AI applications by standardizing how language models interact with data sources and tools.
tags:
  - AI
  - MCP
  - Language Models
  - Architecture
---

I've been working with Solitaire MCP plugin servers since last autumn. It's been a privilege to work with such an interesting technology, which could really be the first versions of a standardized framework for how we make queries to data sources. Reasoning models are useful, when a search logic needs to be more than pattern matching and profiled data. In addition, we can enable actions like Reservations and Orders directly within the same interface. By leveraging reasoning models, we can create a much smoother and more capable user experience. 

I'm not your everyday LinkedIn AI Bro; I'm usually the skeptic in the room. But what I want to discuss in this blog is something I genuinely believe is part of the future.

## Introduction: What is MCP?

If you've been working with large language models (LLMs) lately, you've probably noticed a recurring challenge: how do you give these powerful AI systems access to your data, tools, and services in a reliable and standardized way? Every integration seems to require custom code, special handling, and maintenance overhead. Prompting with ChatGPT might require hand-picking documents that you add as attachment for enhanced context everytime you open a new conversation.

Enter the **Model Context Protocol (MCP)** an open protocol that standardizes how applications provide context to LLMs. Think of it as a universal adapter that allows language models to connect to any data source, API, or tool through a common interface. 

MCP was developed by Anthropic and released as an open standard, designed to solve the fragmentation problem in AI integrations. Instead of building custom integrations for every data source you want to connect to your LLM, MCP provides a unified way for applications to expose their capabilities to AI systems.

## The Simple Formula: LM + Data Source = MCP Application

At its core, MCP follows a following concept:

- **Language Model (LM)**: The reasoning part that understands and generates text, like Claude, GPT-4, or any other LLM
- **MCP Server**: A standardized interface that exposes data, tools, or capabilities to the language model
- **MCP Client**: The application that orchestrates communication between the LM and MCP servers

The magic happens when you connect these pieces. The MCP server wraps your data source (database, API, file system, etc.) and exposes it through a standardized protocol. The language model can then interact with this data naturally, asking questions, retrieving information, or performing actions – all through a uniform interface. The MCP Server exposes tools to the Client LM, including detailed descriptions that help the model reason about which tool to call based on the user's prompt. 

Instead of writing custom integration code for each data source, you write one MCP server, and any MCP-compatible client can use it. This dramatically reduces complexity and increases reusability.

## Real-World Applications: What Can You Build?

The possibilities with MCP are extensive. Here are some compelling use cases:

### **Knowledge Base Integration**
Connect your LLM to internal documentation, wikis, or knowledge bases. Employees can ask natural language questions and get answers grounded in your organization's specific information. Solitaire forexample.

### **Flight Information System** *(Our Example)*
In this blog post, we'll explore a practical example: a flight information system. We'll create an MCP server that provides access to flight data; departures, arrivals, cost, gate information. This demonstrates how MCP can transform static data into an interactive, queryable service that responds to natural language.

### **Multi-Source Intelligence**
The real power emerges when you connect multiple plugin-like MCP servers simultaneously. Imagine an assistant that can query your calendar, read/create tickets from your favorite project management tool, and update documentation, all in a single conversation, providing synthesized insights across systems.

## Implementation: Building an MCP Server

Let's walk through building a practical MCP server in Python. We'll create a flight information system that exposes flight data to language models.

### Setting Up the Environment

Before we dive into the example, you need to have Docker installed and some kind of LM implementation that supports MCP Server connections. I'm using [LM Studio](https://lmstudio.ai/) but you can choose to use whatever tool you wish. 

Clone [this](https://github.com/JanneTuhkanen/FlightsMCP) repository to your environment. There is a Dockerfile included and a shell script to setup the MCP Server for you.

Now, run run_dockerized.sh and wait until the Docker has finished.

Once Docker is finished setting up. We can connect to our mcp server from our LM settings. For LM Studio, you can setup the connection from top right Program -> Install (on Integrations panel) -> Edit mcp.json.

Add the flights mcp server to the settings like this.
{
  "mcpServers": {
    "flights-mcp-server": {
      "url": "http://127.0.0.1:8000/mcp"
    }
  }
}
Now you should have connection open to the FlightsMCP server.

# Lets get promting

I'm using OpenAI's gpt-oss model. Feel free to select same model for testing our MCP Server.

![Promting](/img/mcp-what-and-how/promt.png)

As you can see, it thinks it should call /flights endpoint since its an available tool for us to use. Click "Proceed" to give LM permission to call this tool.

![Flights being listed](/img/mcp-what-and-how/promt-result.png)

What happens, it gets the full json as a response and reasons with our promt that it needs to filter flights except to Oslo.

## Under the Hood: How MCP Works

Now that we understand what MCP can do, let's explore how it actually works at a technical level.

### Architecture Overview

MCP follows a client-server architecture:

1. **MCP Client**: Typically integrated into an AI application or chat interface. It manages the connection to one or more MCP servers and facilitates communication between the LLM and these servers.

2. **MCP Server**: Exposes capabilities through three main primitives:
   - **Resources**: Data or content that can be read (files, database records, API responses)
   - **Tools**: Functions that can be invoked to perform actions (code)
   - **Prompts**: Pre-configured prompt templates that can be used to guide interactions

3. **Transport Layer**: MCP supports multiple transport mechanisms:
   - **stdio**: Communication through standard input/output (great for local processes)
   - **HTTP with SSE (deprecated)**: Server-Sent Events for remote connections, th
   - **WebSocket**: For bidirectional streaming communication

### JSON-RPC: The Communication Protocol

MCP uses **JSON-RPC 2.0** as its underlying message format. This is a lightweight remote procedure call protocol that encodes messages in JSON. It's simple, language-agnostic, and widely supported.

Here's what a typical MCP interaction looks like:

**1. Client discovers server capabilities:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {
      "name": "example-client",
      "version": "1.0.0"
    }
  }
}
```

**2. Server responds with its capabilities:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "resources": {},
      "tools": {},
      "prompts": {}
    },
    "serverInfo": {
      "name": "flight-info-server",
      "version": "1.0.0"
    }
  }
}
```

**3. Client requests to list available tools:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list"
}
```

**4. Client calls a tool (e.g., search flights):**
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "flights",
    "arguments": {}
  }
}
```

## Closing Thoughts

The Model Context Protocol represents a significant step forward in making AI applications more practical and maintainable. By standardizing how language models connect to data sources and tools, MCP solves a fundamental problem that every AI developer faces: integration complexity.

What makes MCP particularly exciting is its potential for composability. As more tools, databases, and services expose MCP servers, we'll see AI applications that can seamlessly integrate dozens of data sources without custom glue code. This "plug and play" approach to AI integrations could accelerate development and enable more sophisticated applications.

However, MCP is still young. The ecosystem is growing, but many tools and services don't yet have MCP servers. There are also ongoing discussions about best practices, security patterns, and protocol extensions. If you're building AI applications, now is an excellent time to get involved – whether by creating MCP servers for your services, contributing to the specification, or simply experimenting with the possibilities.

### Further exploration

If you're interested in exploring MCP further:

- Check out the [official MCP specification](https://modelcontextprotocol.io/)
- Explore existing MCP servers in the community
- Build your own MCP server for a data source you work with
- Join the conversation about where the protocol should go next

The future of AI applications is connected, contextual, and composable – and MCP is helping to make that future a reality.

---

*Have you built something with MCP? We'd love to hear about your experience. Share your thoughts and projects in the comments below.*
