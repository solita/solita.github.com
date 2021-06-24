---
layout: post
title: Type Phantoms and Safe APIs
author: mpajunen
excerpt: >
    Writing both frontend and backend of a web application in TypeScript allows using common model
    type definitions in both. Let's explore one technique to make the API calls type-safe as well.
tags:
    - Api
    - TypeScript
---

Using a typed language like TypeScript for the frontend of a web application can already be a great
boon. When using a backend service also written in TypeScript, it's easy to share some model types.
What about making the API boundary between the frontend and the backend type-safe? There are several
ways to do that as well.

## Approaches to API type safety

One way to create a type-safe API is to generate code from metadata. If you have API documentation
in OpenAPI or similar format, there are libraries that can generate corresponding types. Depending
on the use case, some custom code might be needed as well. Tools like
Apollo [rely on code generation](https://github.com/apollographql/apollo-tooling#code-generation)
for type safety.

An interesting approach is to first create runtime representations of the types in TypeScript. Types
in TS are compile-time only but can be derived from the runtime code. This code can be used to
validate data at the edges of the type system. [io-ts](https://gcanti.github.io/io-ts/) uses this
approach.

Libraries like [tRPC](https://trpc.io/) derive the API types from the server implementation. This
avoids writing separate models entirely and can integrate well with validation code.

My colleague
Jaakko [also blogged about typed APIs](https://dev.solita.fi/2018/09/06/fullstack-typed-api-with-typescript.html)
earlier. Using type casts can enable some powerful features, such as runtime type checks.

TypeScript has evolved a lot, and in this post we'll examine a types first approach. The main
advantage is a clean API endpoint model, that can use all type system features. This model can be
manipulated with type logic to create helpers and utilities as needed. It's not without downsides
though: All validation logic will have to be written separately, since there are no runtime
representations. Generating API documentation may require extra effort as well.

Choosing the right approach depends on the problem: Is the API external, or only for internal use?
How important is API documentation? What kind of validation logic is needed? Are you starting a
greenfield project or expanding existing functionality?

We'll start with an example that can be adapted to any typical REST API. This means using a normal
route structure, some path parameters, and common HTTP methods. After a basic example, we'll explore
expanding the functionality to cover real-world use cases and ponder a bit how all this could be
simpler or even more useful.

Complete source code, including a working example
application, [is available on GitHub](https://github.com/mpajunen/rest-type-map).

## Designing an API model

As an example, let's create a simple API for spaceships. The ships have features like `name`
and `size`. We'll give them numeric `id` values as well:

```typescript
type ShipSize = 'small' | 'medium' | 'large' | 'huge'

type ShipFeatures = {
  name: string
  size: ShipSize
}

type Ship = { id: number } & ShipFeatures
```

We'll implement some basic operations to fetch, add and update ships:

```
GET  /ships
POST /ships
PUT  /ships/:id
```

These operations have a specific return type. Adding a ship requires a body parameter, and editing
requires a path parameter as well. We could think of these as asynchronous functions. Combining
these functions in a single object gives us the basic API client structure:

```typescript
type ShipClient = {
  getShips: () => Promise<Ship[]>
  addShip: (params: {}, features: ShipFeatures) => Promise<Ship>
  editShip: (params: { id: number }, features: ShipFeatures) => Promise<Ship>
}
```

Using the exact same API for the server has a couple of issues:

1. We might want to pass more parameters to the server handlers.
2. Any `number` values in path parameters will be converted to `string` values.

Most server-side libraries already use a request object we can use to access parameters. We can
adapt our functions to use that style and convert any numbers. In our example the server model would
look like this:

```typescript
type ShipServer = {
  getShips: () => Promise<Ship[]>
  addShip: (request: { body: ShipFeatures }) => Promise<Ship>
  // The id parameter is going to be a string here:
  editShip: (request: { params: { id: string }, body: ShipFeatures }) => Promise<Ship>
}
```

We'll define the basic form of these operations as plain object types to make building the API
easier. This enables type manipulation
using [mapped types](https://www.typescriptlang.org/docs/handbook/2/mapped-types.html).

```typescript
// common/Model.ts

type ShipHandlers = {
  getShips: {
    // Declaring undefined properties helps with type inference:
    path: undefined
    body: undefined
    result: Ship[]
  }
  addShip: {
    path: undefined
    body: ShipFeatures
    result: Ship
  }
  editShip: {
    path: { id: number }
    body: ShipFeatures
    result: Ship
  }
}
```

Using this common `ShipHandlers` type to implement both client and server handlers would already
give some type safety. We can improve on that by combining the parameter and return types with the
route information.

The routes also need a runtime representation, so declaring only the types won't work. Instead,
we'll declare an object with keys that match the `ShipHandlers` type. The values will include the
HTTP method and path pattern. The route types can then be combined with the handler types:

```typescript
// common/Model.ts

// Declare routes as a readonly object:
const routes = {
  getShips: { method: 'get', pattern: '/ships' },
  addShip: { method: 'post', pattern: '/ships' },
  editShip: { method: 'put', pattern: '/ships/:id' },
} as const

// The route properties are now string literals:
type ShipApi = ShipHandlers & typeof routes

// Now for example ShipApi['editShip'] has the following type:
type EditShip = {
  path: { id: number }
  body: ShipFeatures
  result: Ship
  method: 'put'
  pattern: '/ships/:id'
}
```

Using the declared `routes` and `ShipApi` we can create a type-safe API.

## Building the client and server APIs

In addition to the defined API type, we'll need some common utilities to build the client and
server. Creating and using the API should be straightforward:

```typescript
// client/api.ts

const api = Client.createHandlers(httpClient, shipRoutes)


// client/ShipList.ts

async function getShips() { // component / data service / thunk / hook
  const ships = await api.getShips()
  /* ... */
}


// server/index.ts

const handlers: Server.Handlers<ShipApi> = {
  getShips: async () => {
    return db.ships.getAll()
  },
  /* ... */
}

Server.addHandlers(router, shipRoutes, handlers)
```

Here we have used a few utility functions and types. We'll define those next. The types get more
complex, and we'll need techniques like mapped types
and [conditional types](https://www.typescriptlang.org/docs/handbook/2/conditional-types.html). Some
common type definitions first:

```typescript
// lib/Common.ts

type HttpMethod = 'delete' | 'get' | 'patch' | 'post' | 'put'

type MaybeObject = object | undefined

type Call<PathParams extends MaybeObject, Body extends MaybeObject, Result> = {
  path: PathParams
  body: Body
  result: Result
}

type RouteBase<Pattern extends string, Method extends HttpMethod> = {
  pattern: Pattern
  method: Method
}

type EndpointBase<
  PathParams extends MaybeObject,
  Body extends MaybeObject,
  Result,
  Pattern extends string,
  Method extends HttpMethod,
> = Call<PathParams, Body, Result> & RouteBase<Pattern, Method>

export type Endpoint<T = any> =
  T extends EndpointBase<infer PathParams, infer Body, infer Result, infer Pattern, infer Method>
    ? EndpointBase<PathParams, Body, Result, Pattern, Method>
    : never

export type Route<T> =
  T extends EndpointBase<infer PathParams, infer Body, infer Result, infer Pattern, infer Method>
    ? RouteBase<Pattern, Method>
    : never

export type Endpoints<T = any> = { [K in keyof T]: Endpoint<T[K]> }

export type Routes<T> = { [K in keyof T]: Route<T[K]> }
```

The generic types here match the `ShipApi` and `routes` from the example API. While we already had
exact types for the API, the utility functions will only use these generic types. These types can
also be used for sanity checks:

```typescript
const shipRoutes: Routes<ShipApi> = routes
```

Here `shipRoutes` and `routes` have the same type, but if we had mistyped an HTTP method in the
route definition, this assignment would cause a type error. We couldn't enforce that restriction in
the original definition, since we need the exact literal types from `as const`.

The `Endpoint` type may seem redundant, but it basically condenses five separate type parameters to
one. This keeps the utility function code cleaner.

Meanwhile, values of the `Route` type only use the `Path` and `Method` type parameters, but the type
requires that all the endpoint parameters are available. These _phantom_ parameters form a contract:
Given a specific route, a utility function can only return an API endpoint with matching parameter
and return types.

### Client utilities

We can now build the utility functions. For the client we'll create a handler function for each
route. This function takes the endpoint parameters, makes a request and returns the response data.
Then we'll combine these functions in a single object:

```typescript
// lib/Client.ts

export type Handlers<T extends Endpoints> = { [K in keyof T]: Handler<T[K]> }
export type Handler<EP extends Endpoint> =
  (params: EP['path'], body: EP['body']) => Promise<EP['result']>

/** Create client API from routes */
export function createHandlers<T extends Endpoints>(
  client: HttpClient,
  routes: Routes<T>,
): Handlers<T> {
  function createHandler<EP extends T[keyof T]>({ method, pattern }: Route<EP>) {
    const handler: Handler<EP> = (params, data) => {
      const url = getUrl(pattern, params)

      return client.request<EP['result']>({ data, method, url }).then(r => r.data)
    }

    return handler
  }

  // Can't infer that all handlers are created:
  const handlers = {} as Handlers<T>
  for (const name in routes) {
    handlers[name] = createHandler(routes[name])
  }

  return handlers
}

/** Create request URL from path parameters */
const getUrl = (path: string, params?: object): string =>
  Object.entries(params ?? {}).reduce(
    (current, [name, value]) => current.replace(`:${name}`, encodeURIComponent(value)),
    path,
  )

/** HTTP client helper type, rough match to Axios API */
type HttpClient = {
  request: <Data>(config: HttpConfig) => Promise<{ data: Data }>
}
type HttpConfig = { data?: object, method: HttpMethod, url: string }
```

We need to cheat a bit here and use a type
cast. [Object iteration is tricky](https://effectivetypescript.com/2020/05/26/iterate-objects/) in
TypeScript, and the type system can't infer that every handler has really been created.

The utility function uses a custom `HttpClient` type that matches [Axios](https://axios-http.com/)
API. Using Axios, creating the API object would look something like this:

```typescript
const api = Client.createHandlers(axios.create({ baseURL: '/api' }), shipRoutes)
```

### Server utilities

While the client-side implementation is somewhat complex, it behaves pretty much the same way
regardless of what library makes the requests. The routing and request handling in server-side
frameworks and libraries varies a lot more. We'll use [Express](https://expressjs.com/) in the
example; some changes would be needed for other libraries.

The server-side utilities take handler functions and the route definitions, and bind those to a
router object:

```typescript
// lib/Server.ts

export type Handlers<T extends Endpoints> = { [K in keyof T]: Handler<T[K]> }
export type Handler<EP extends Endpoint> = (params: Params<EP>) => Promise<EP['result']>

type Params<EP extends Endpoint> = {
  path: Stringify<EP['path']>
  body: EP['body']
}
type Stringify<T> = { [K in keyof T]: T[K] extends string ? T[K] : string }

export function addHandlers<T extends Endpoints>(
  router: Router,
  routes: Routes<T>,
  handlers: Handlers<T>,
): void {
  for (const name in routes) {
    const { method, pattern } = routes[name]

    router[method](pattern, createHandler(handlers[name]))
  }
}

const createHandler = <EP extends Endpoint>(handler: Handler<EP>): RouteHandler<EP> =>
  async (req, res) => {
    res.send(await handler({ path: req.params, body: req.body }))
  }

// Server / router helper types, rough match to Express API

type Router = Record<HttpMethod, (path: string, handler: RouteHandler<any>) => void>
type RouteHandler<EP extends Endpoint> =
  (req: Request<EP['path'], EP['body']>, res: Response<EP['result']>) => void

type Request<PathParams, Body> = {
  body: Body
  params: Stringify<PathParams>
}
type Response<Result> = {
  send(content: Result): Response<Result>
}
```

Adding routes to an Express application would look like this:

```typescript
const router = express.Router()

Server.addHandlers(router, shipRoutes, handlers)

express().use('/api', router)
```

That's it! A type-safe API applying generic, reusable utilities. Changes to the API model will be
immediately reflected in both client and server code. Any incompatibility will cause a compilation
error, and for example a new endpoint would be available in the client without additional glue code.

There are still a lot of improvements we could make.

## Extending the basics

This basic version lacks a lot of functionality we would like in a real-world application. It
doesn't support query parameters, there's no error handling, and even with strict types you'd need
validation.

Some of this functionality could be included in the handler functions, but we can also implement it
in the common utilities. That means we'll only have to implement it once. We can also rely on the
types to make sure that all requests are validated, for example.

### Removing client extra parameters

The basic client handler always needs two parameters. For example, you'd have to
use `api.getShips(undefined, undefined)` to fetch ships. This can be remedied with a more complex,
conditional `Handler` type, and a type cast:

```typescript
// lib/Client.ts

type Handler<EP extends Endpoint> =
  EP['body'] extends object
    ? HandlerFull<EP>
    : EP['path'] extends object
    ? HandlerPath<EP>
    : HandlerNone<EP>
type HandlerFull<EP extends Endpoint> =
  (params: EP['path'], body: EP['body']) => Promise<EP['result']>
type HandlerPath<EP extends Endpoint> = (params: EP['path']) => Promise<EP['result']>
type HandlerNone<EP extends Endpoint> = () => Promise<EP['result']>
```

Now it's possible to call `api.getShips()`, but an extra `undefined` is still required when there is
a body parameter, but no path parameters: `api.addShip(undefined, features)`.

### Adding query parameters

Adding query parameters would be straightforward: just add a `query` property to the common `Call`
type. Quite a few of the utilities would need changes though, and the new property would need to be
added to all endpoint declarations.

With query parameters added, using a single parameter object for the client might be more ergonomic:

```typescript
api.getShips()
api.addShip({ body: features })
api.searchShips({ query: { name: 'tie fighter' } })
```

### Implementing error handling

The basic example doesn't deal with _any_ errors. In a real application both the server and the
client need some error handling.

If a server handler throws an exception on failure, we can use the exception to produce an error
response:

```typescript
// lib/Server.ts

const createHandler = <EP extends Endpoint>(handler: Handler<EP>): RouteHandler<EP> =>
  async (req, res) => {
    try {
      const result = await handler({ path: req.params, body: req.body })

      res.send(result)
    } catch (error) {
      res.sendStatus(500)
    }
  }
```

This can be expanded to check error types and produce different status codes based on that. An error
object library like [boom](https://hapi.dev/module/boom/) could be useful as well.

An interesting alternative is to use more functional style, and a `Result` / `Either` type.
Languages like [F#](https://docs.microsoft.com/en-us/dotnet/fsharp/language-reference/results),
[Haskell](https://hackage.haskell.org/package/base/docs/Data-Either.html)
and [Rust](https://doc.rust-lang.org/std/result/enum.Result.html) use them extensively.

Result types
are [extremely useful in TypeScript](https://imhoff.blog/posts/using-results-in-typescript)
as well, and a bare-bones implementation is easy:

```typescript
export type Result<Success, Failure> =
  { ok: true; value: Success } | { ok: false; error: Failure }
```

One way to use them on the server-side would be to expand the `Handler` type:

```typescript
// lib/Server.ts

export type Handler<EP extends Endpoint> =
  (params: Params<EP>) => Promise<Result<EP['result'], string>>

const createHandler = <EP extends Endpoint>(handler: Handler<EP>): RouteHandler<EP> =>
  async (req, res) => {
    const result = await handler({ path: req.params, body: req.body })

    if (result.ok) {
      res.send(result.value)
    } else {
      res.status(500).send(result.error)
    }
  }
```

This example uses a plain `string` as the error type. The error type could also be some structured
error, or even depend on the result type.

Of course, the backend code could throw exceptions regardless, so still catching those as well would
be useful.

Result types are even more useful in client code, where it's easy to forget to handle an error case.
If the API client always returns a `Result` value, the error handling code needs to be made
explicit, and there's no way to miss an exception. Using a `Result` type on the client-side works
similarly to the server code:

```typescript
// lib/Client.ts

export type Handler<EP extends Endpoint> =
  (params: EP['path'], body: EP['body']) => Promise<Result<EP['result'], string>>

/* ... */
  function createHandler<EP extends T[keyof T]>({ method, pattern }: Route<EP>) {
    const handler: Handler<EP> = (params, data) => {
      const url = getUrl(pattern, params)

      return client.request<EP['result']>({ data, method, url })
        .then(r => ({ ok: true, value: r.data }))
        .catch(e => ({ ok: false, error: e?.response ?? 'Request failed' }))
    }

    return handler
  }

/* ... */
```

### Validating requests

While strict types can guarantee that the request content is correct to a high degree, there's still
need for validation. Perhaps some requests don't use the utilities, and malicious requests are
always possible.

We can use the existing type definitions to make sure that all requests pass through validation.
Assuming we already have some validation functions, we can combine those with the API model. The
utility types guarantee that there must be a correctly typed validation function for every endpoint:

```typescript
// server/validation.ts

type Validator<T> = (value: unknown) => value is T

declare const validateFeatures: Validator<ShipFeatures> // Implementation skipped here

type BodyValidators<T extends Endpoints> = { [K in keyof T]: Validator<T[K]['body']> }

export const bodyValidators: BodyValidators<ShipApi> = {
  getShips: body => body === undefined,
  addShip: validateFeatures,
  editShip: validateFeatures,
}
```

Now we can use this validator object in the server handler, expanding the original version:

```typescript
// lib/Server.ts

const createHandler = <EP extends Endpoint>(
  handler: Handler<EP>,
  bodyValidator: Validator<EP['body']>,
): RouteHandler<EP> =>
  async (req, res) => {
    if (!bodyValidator(req.body)) {
      res.sendStatus(400)
    } else {
      res.send(await handler({ path: req.params, body: req.body }))
    }
  }
```

Path parameters can use the same kind of validation. With the validation utilities in place, any
changes to the API will also have to be reflected in the validation code.

Usually, we'd also like meaningful error messages. In that case using `Result` with the `Validator`
works well:

```typescript
type Validator<T> = (value: unknown) => Result<T, ErrorMessages<T>>
```

### Passing added context to handlers

Often the server handler needs more data, not just the request parameters. If this data depends on
the request, we need to initialize it before calling the handler. This may involve middleware to
modify the request object. In that case, the server-side `Params` type would need changes. Another
way is to pass a separate `context` object to the handlers:

```typescript
// lib/Server.ts

type Context = { /* ... */ }

declare function createContext(req: Request): Context

export type Handler<EP extends Endpoint> =
  (params: Params<EP>, context: Context) => Promise<EP['result']>

const createHandler = <EP extends Endpoint>(handler: Handler<EP>): RouteHandler<EP> =>
  async (req, res) => {
    const context = createContext(req)

    res.send(await handler({ path: req.params, body: req.body }, context))
  }
```

If the *type* of `Context` also depends on the endpoint, the utilities would need changes as well.

## Further improvements

That's quite a few changes and tweaks already! Turns out it's not easy to write glue code and
utilities that would be usable out of the box. Project requirements and techniques vary, and the
glue code needs adjustments as well.

We've not even touched on many common API features that may be needed:

- How is authentication handled? What about authorization?
- What about specific request and response headers?
- How to make multiple separate APIs type safe?
- Can we make route handling even more safe, for example with path uniqueness checks?

Some of these are straightforward using techniques we already explored. That means even more changes
to the common utilities though. Could we develop the core functionality further to make it more
generic and support various kinds of API structures?

### Adapting to different API structures

Using custom adapters would help with some of these issues. The generic utilities are less useful
then, but the request and response conversions can be customized. The client-side implementation
could look like this:

```typescript
// lib/Client.ts

type MakeRequest<EP extends Endpoint = Endpoint> =
  (params: Omit<EP, 'result'>) => Promise<EP['result']>

export function createHandlers<T extends Endpoints>(
  makeRequest: MakeRequest,
  routes: Routes<T>,
): Handlers<T> {
  /* ... */
}
```

Now the common utility functions don't know the details of how to make requests, and those details
can be tweaked freely. Some features still need type changes. For example, using the `Result` type
means changing the `MakeRequest` type as well.

The server implementation could use the same principles to extract library logic and enable
customization.

### Simplifying types

Making things simpler can make them easier to use as well. The utility types are quite complex, and
perhaps some could even be removed entirely? It's easy to make some types simpler, but type
inference can suffer, and the error messages could become more cryptic.

It's also possible to derive all the API model types from the server-side implementation. Then
separate types wouldn't have to be written at all. However, this could make the API model less
understandable, and some error messages incomprehensible.

Despite these challenges, there's probably a lot that could be improved, without adverse effects on
readability.

### Stop being so RESTful?

If you are just writing function calls, do you need separate body, path and query parameters? Are
the different HTTP methods useful?

If it's an external API, sticking to typical REST conventions will be more familiar to the API
users. For an internal API, the API structure may not matter that much when it's abstracted away.
Ditching different parameter types would already make utilities simpler. Perhaps only GET and POST
requests are needed? Maybe route paths are unnecessary too, and the function name could be passed as
a parameter instead?

GraphQL for example [serves data this way](https://graphql.org/learn/serving-over-http/). However,
sticking with some REST conventions may be a better fit for a project, and custom utilities allow
flexibility.

When using common utilities for the API, it's easy to experiment with changes like this. Just
modifying the utilities will change how all endpoints work. Validating and testing that an
experiment works doesn't require a lot of changes.

## Verdict: Definitely recommended

What benefits does a type-safe API give us?

A good data model can make many errors outright impossible. Shared, common types are a single source
of truth for how the data should look. A straightforward API model enables more use cases, such as
required validation.

When some functionality changes, the types can tell what other parts of the code should change as
well. While it would be ideal to place all related code in one location, that's not always feasible.
API changes are a common example: Placing all related frontend and backend code in the same file
isn't possible in most cases. In this situation the contract of types is the next best thing: We'll
get a compiler error for any incompatible changes. Similarly, if we forget something when
implementing a new feature or endpoint, the compiler will remind us.

Implementing a type-safe API means some extra work to start with, but the benefits come up quickly.
The contracts are useful even for an API with only a few endpoints. Part of the benefit is due to
separating the technical issue of making requests from the data model and the actions.

There's little reason not to make your API type-safe. Depending on the implementation technologies,
solutions such as code generation may be necessary. For full stack TypeScript applications, a types
first approach works well.
