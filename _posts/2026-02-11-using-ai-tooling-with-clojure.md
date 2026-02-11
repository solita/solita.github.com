---
layout: post
title: Using Generative AI tooling with Clojure
author: mattiuusitalo
excerpt: >
  With the data oriented design and highly interactive development
  workflows, Clojure can offer interesting characteristics when used
  with Generative AI.
tags:
  - Clojure
  - AI
---

## Clojure is easy to read for humans and AIs

Code written in Clojure is expressive and concise, but is still easy
to reason about. In his ["History of Clojure"](https://dl.acm.org/doi/pdf/10.1145/3386321) paper Rich
Hickey, the original author of Clojure states his motivations for
building a new programming language:

> "Most developers are primarily engaged in making
> systems that acquire, extract, transform, maintain, analyze, transmit and render information—facts
> about the world ... As programs grew large, they required
> increasingly Herculean efforts to change while maintaining all of the presumptions around state
> and relationships, never mind dealing with race conditions as concurrency was increasingly in play.
> And we faced encroaching, and eventually crippling, coupling, and huge codebases, due directly to
> specificity (best-practice encapsulation, abstraction, and parameterization notwithstanding). C++
> builds of over an hour were common."

As a result, Clojure programs are very much focused on dealing with
data and do it safely in concurrent programs. We have by default
immutable data structures, easy to use literal representations of the
most common collection types (lists, vectors, sets and maps) and a very
regular syntax. A typical Clojure program has way less ceremony and
boilerplate, not to mention weird quirks to deal with compared to many
more programming languages such as Java, C#, Typescript or Python

This means that large language models have less to deal with when
reading or writing Clojure code. We have some evidence in Martin
Alderson's article that Clojure is [token efficient](https://martinalderson.com/posts/which-programming-languages-are-most-token-efficient/) compared to most other popular programming languages.

When we author code with generative AI tools, a developer reviewing it has less
code to read, in a easy to reason about format too.

## Clojure MCP boosts Agentic development workflows

The REPL driven workflow speeds up the feedback cycle in normal
development modes. *R*ead *E*val *P*rint *L*oop is a concept in many programming languages in the LISP family such as Common Lisp, Scheme and Clojure. It allows the developer to tap into and evaluate code in a running instance of the application they are developing. With good editor integration, this allows smooth and frictionless testing of the code under development in an interactive workflow.

With the addition of [MCP (Model Context Protocol)](https://modelcontextprotocol.io/introduction)
agents have gained access to a lot of tooling. In May 2025 Bruce
Hauman announced his [Clojure MCP](https://github.com/bhauman/clojure-mcp)
that provides an MCP that provides agents access to the REPL. Now
AI agents such as Claude Code, Copilot CLI and others can reach inside
the application as it is being developed, try code changes live, look
at the internal state of the application and benefit from all of the
interactivity that human developers have when working with the REPL.

It also provides efficient structural editing capabilities to the
agents, making them less error-prone when editing Clojure source
code. Because Clojure code is written as Clojure data structures,
programmatic edits to the source code are a breeze.

We can even hot load dependencies to a running application without
losing the application state! This is a SKILL.md file I have added to
my project to guide agents in harnessing this power:

```
---
name: adding-clojure-dependencies
description: Adds clojure dependencies to the project. Use this when asked to add a dependency to the project
---

To add dependencies to deps.edn do the following:

1. Find the dependency in maven central repo or clojars
2. Identify the latest release version (no RCs unless specified)
3. Add dependency to either main list (for clojure dependencies),
   :test alias (for test dependencies) or :dev alias (for development dependencies). Use the REPL and
   `rewrite-edn` to edit the file
4. Reload dependencies in the REPL using `(clojure.repl.deps/sync-deps)`
```

In my experience, with the Clojure MCP coding agents have a far easier
time troubleshooting and debugging compared to having them just
analyze source code, logs and stacktraces.

As a developer, we can also connect to the same REPL as the coding
agent, making it easy to step in and aid the agent when it gets
stuck. In my workflows, I might look at the code the Agent produced
and test it in the REPL as well, make changes as required and instruct
the agent to read what I did. This gives another collaborative
dimension to standard prompting techniques that are normally
associated with generative AI development.

## Getting AI to speak Clojure

Generating and analyzing code with AI tooling is just one way
to apply AI in software development. As developers, we should
understand the potential for embedding AI functinality at the
application level too. LLMs seem to be good at understanding my
intentions, even if they don't necessarily produce the right
results. One possibility is to take input provided by a human and
enrich it with data so that further processing becomes easier. For the
sake of experiment, let's look at a traditional flow of making a
support request.

The user goes to the portal and their first task is to identify the
correct topic under which this support request belongs to. They
usually have to classify the severity of the issue as well. Then they
describe what problem they have and add their contact
information. With this flow, there's a large chance that the user
misclassified their support request, causing delays in getting the
work in front of the right person, making the user experience poor and
causing frustrations in the people handling the support requests. From
the user's point of view they don't care about which department
picks up the request, so this system is pushing the support
organization's concerns to the end user.

What if we could avoid all that and have the request routed
automatically to the right backlog? Enter OpenAI's [Requests API](https://developers.openai.com/api/reference/resources/responses/methods/create)
which can handle text, image and various file inputs to generate text
or JSON outputs. The *json_schema* response format is interesting in
particular, because we can express the desired result format in a
manner that we can then use to process the response programmatically
down the line.

In Clojure world, we often use [Malli](https://github.com/metosin/malli) to define our data models. We
can use `malli.json-schema` to transform our malli schemas into
json_schema that the endpoint understands, and then use
`malli.transform` to translate the response from json back to Clojure
data.

A [similar idea](https://gist.github.com/ikitommi/e643713719c3620f943ef34086451c69)
has been shown previously by Tommi Reiman, author of Malli.

Note that the choice of model can have a big effect on your output!

```clojure
(require '[malli.json-schema :as mjs])
(require '[malli.core :as m])
(require '[malli.transform :as mt])
(require '[cheshire.core :as json])
(require '[org.httpkit.client :as http])

(defn structured-output
  [api-endpoint-url api-key malli-schema input]
  (let [;; Convert Malli schema to JSON Schema
        json-schema (mjs/transform malli-schema)

        ;; Build request body
        body {:model "gpt-4o" ;; consult your service provider for available models
              :input input
              :text {:format {:type "json_schema"
                              :name "response"
                              :strict true
                              :schema json-schema}}}

        ;; Make HTTP request
        response @(http/post
                   (str api-endpoint-url "/v1/responses")
                   {:headers {"Authorization" (str "Bearer " api-key)
                              "Content-Type" "application/json"}
                    :body (json/generate-string body)})

        ;; Parse response
        parsed-response (json/parse-string (:body response) true)

        ;; Extract structured data from response
        content (-> parsed-response :output first :content first :text)
        parsed-data (json/parse-string content true)

        ;; Decode using Malli transformer
        result (m/decode malli-schema parsed-data (mt/json-transformer))]

    ;; Validate and return
    (when-not (m/validate malli-schema result)
      (throw (ex-info "Response does not match schema"
                      {:schema malli-schema
                       :result result})))
    result))

(structured-output
   (get-base-url)
   (get-api-key)
   [:map
    [:department [:enum :licences :hardware :accounts :maintenance :other]]
    [:severity [:enum :low :medium :critical]]
    [:request :string]
    [:contact-information [:map
                           [:email {:optional true} :string]
                           [:phone {:optional true} :string]
                           [:raw :string]]]]
   "Hi, my laptop diesn't let me login anymore. Can't work. What do? t. Hank PS call me 555-1343 because I can't access email")
; => {:department :hardware,
;     :severity :critical,
;     :request "Laptop doesn't let me login anymore. Can't work.",
;     :contact-information
;     {:raw "Hank, phone: 555-1343, cannot access email",
;      :phone "555-1343"}}
```

One doesn't usually have to use any of the more powerful and expensive models to do this level of work. The older *json_object* response format has some capabilities and supports even lighter models. See [OpenAI's documentation](https://developers.openai.com/api/docs/guides/structured-outputs) for reference.

I think methods like this make it easy to embed LLM enabled functionalities in Clojure applications, giving them capabilities that are normally very hard to implement using traditional methods.

## Further reading

If you're new to agentic development, [Prompt engineering 101](https://dev.solita.fi/2026/02/10/prompt-engineering-101.html) is a great starter for how to get past the first hurdles.
