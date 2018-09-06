---
layout: post
title: Fullstack shared typed API with TypeScript
author: jgke
excerpt: >
  TypeScript makes it possible to share type information between frontend and
  backend. Here's how to use it to ensure consistent API calls between the
  frontend and backend.
tags:
 - TypeScript
 - Full stack
---

Did you get a yet another error due to the JavaScript frontend slipping an
unnoticed ``undefined`` to a request or passing a string instead of a number,
which causes requests to fail without a clear reason? Or even worse, succeed in
a weird way? Maybe you changed the API on the server side but forgot to update
the client? Consider sharing the API as a single type between the
frontend and the backend. This blog post explains the process on how to build a
shared API using fullstack TypeScript. As a bonus, you also get runtime type
checks!

## Sketching out an API

Let's make a simple API:
- ``GET /customers``: fetch a list of customers
- ``POST /customers``: create a new customer
- ``GET /search?id=123&name=foobar``: search a customer by id/name

As we're building a JSON-based API, every request and return value has to be an
object. We can handle this transparently by defining the format for responses:

```ts
export interface ApiResponse<Res> {
    message: Res;
}
```

All HTTP requests look roughly like functions ``(queryParameters, body) =>
returnvalue`` (for GETs, this means (queryParameters, {}) => returnValue``).
This means that we can model the API with the following type:

```ts
type Customer = {
    id: number,
    name: string
}
type ApiMap = {
    customers: {
        GET: () => Promise<Customer[]>,
        POST: (customerName: string) => Promise<Customer>
    },
    search: {
        GET: (query: {id?: number, name?: string}) => Promise<Customer[]>
    }
}
```

On the client side, the ApiMap type can be used to define a object:


```ts
function fetchAny(url: string, queryParams?: any,
                  method?: string, body?: any): Promise<any> {
    let address = new URL(url);
    Object.keys(queryParams || {})
        .forEach(key => address.searchParams.append(key, queryParams[key]));
    return fetch(address.toString(), {method, body})
        .then(response => response.json()
            .then((responseBody: any) => new Promise<Res>(resolve =>
                resolve(responseBody.message))));
}

const api: ApiMap = {
    customers: {
        GET: () => fetchAny('/customers'),
        POST: (customerName: string) => fetchAny('/customers', {}, 'POST', customerName)
    },
    search: {
        GET: (params: {id: number?, name: string?}) => fetchAny('/search', params, 'PUT')
    }
};

// ...

api.customers.GET().then(val => /* ... */ val)
```

The client side implementation can now be used as if the API was just an object
with methods. Server side needs a bit more work, since we have to tie the api
to implementations:

```ts
const customers: Customer[] = [];
let id: number = 1;

const api: ApiMap = {
    customers: {
        GET: () => new Promise(resolve => resolve(customers)),
        POST: (customerName: string) => {
            let newCustomer = {name: customerName, id: id++};
            customers.push(newCustomer);
            return new Promise(resolve => resolve(newCustomer));
        }
    },
    search: {
        GET: (params: {id?: number, name?: string}) => {
            let filteredCustomers = customers
                .filter(customer => !params.id || customer.id == params.id)
                .filter(customer => !params.name || customer.name == params.name);
            return new Promise(resolve => resolve(filteredCustomers))
        }
    }
};

// ...

const app = express();
app.get("/customers", (req, res) => {
    api.customers.GET().then(msg => {
        res.send({message: msg});
    });
});
app.post("/customers", (req, res) => {
    api.customers.POST(req.body.message).then(msg => {
        res.send({message: msg});
    });
});
app.get("/search", (req, res) => {
    api.search.GET(req.query).then(msg => {
        res.send({message: msg});
    });
});
```

If the client tries to call the API with the wrong parameter...

```ts
api.customers.POST(123);
```

... the compiler notices this:

```
error TS2345: Argument of type '123' is not assignable to parameter of type 'string'.
```

However, we have a problem. The implementations are not completely type checked
to match the API! In fact, there is a small typo in the client side
implementation - can you spot it? In addition, there's a lot of duplicated code
we'd like to avoid. The approach seems to be a good one, but the actual
implementation needs some work.

Instead of being a type, what if the API was a value? Then we could
automatically generate code for client fetches and server binds by iterating
over the API. Turns out, we can, and we also get to maintain type safety.

## Make the object out of you... er, the API

Let's think for a moment. What do we actually want? We want for
``customers.GET`` to be a function ``() => Promise<Customer[]>`` that is
located in ``api.customers.GET``. Let's make helper function ``zero<T>(returns:
T): (T) => Promise<T>`` which, when called with ``zero<Customer[]>([{id: 0,
name: ''}])``, returns something which has the type ``() =>
Promise<Customer>``.

```ts
function zero<R>(returns: R) {
    return undefined as any as () => Promise<R>;
}
```
...and do the same for ``one()``, which, when called with ``one<string,
Customer>('', {id: 0, name: ''})``, returns something which has the type ``(p:
string) => Promise<Customer>``.

```ts
function one<T, R>() {
    return undefined as any as (takes: T) => Promise<R>;
}
```

Using the new syntax introduced in TypeScript 3.0, we can combine these
functions into one, and also provide a version, which takes two parameters:

```ts
// the first any? here is body type, the second is query parameters
function fun<T, TS extends [any?, any?]>(returns: T, ...takes: TS) {
    return undefined as any as (...t: TS) => Promise<T>;
}
```

Let's also create helpers for string, number, object and array in the similar
fashion:

```ts
const str = undefined as any as string;
const num = undefined as any as string;

function optional<T>(param: T): T | undefined {
    return undefined as any;
}

function obj<T extends object>(param: T): T {
    return undefined as any;
}

function arr<T>(param: T): T[] {
    return undefined as any;
}
```

We can now write the API in a more terse syntax:

```ts
const customer = obj({id: num, name: str})
type Customer = typeof customer;
const partialCustomer = obj({id: optional(num), name: optional(str)})
const apiObject = {
    customers: {
        GET: fun(arr(customer)),
        POST: fun(str, customer)
    },
    search: {
        GET: fun(partialCustomer, arr(customer))
    },
}
type ApiMap = typeof apiObject;
```

## Automatically generating client and server code

For the client, we can wrap each of the requests with ``fetch()``, so the
client code can just call the method with ``clientApi.path.METHOD(body)`` and be done
with it. For the server, we can bind the API to eg. Express.

```ts
import {ApiMap, apiObject, ApiResponse, ApiResponseValue} from './api';

const baseAddress = 'http://localhost:3000';

function apiCall<QueryParams, Body, Res>(path: string, queryParams: QueryParams,
                                         method: string, body: Body): Promise<Res> {
    const address = new URL(`${baseAddress}/${path}`);
    Object.keys(queryParams || {})
        .forEach(key => address.searchParams.append(key, queryParams[key]));

    return fetch(address.toString(), {body: body && JSON.stringify({message: body}),
                                      method,
                                      headers: { 'Content-Type': 'application/json'}})
        .then(val => val.json())
        .then((message: ApiResponse<Res>) =>
            new Promise<Res>(resolve => resolve(message.message)));
}

// tslint:disable:no-any

/* Wrap the argument object so that path.method.fn makes requests to the server */
function wrapApi(api: any): ApiMap {
    const wrapped: any = {};

    Object.keys(api).forEach((path: string) => {
        wrapped[path] = {};
        Object.keys(api[path]).forEach((method: string) => {
            if (method === 'GET') {
                wrapped[path] = (queryParams: any) =>
                    apiCall(prefix.join('/'), queryParams, method, undefined);
            } else {
                wrapped[path] = (body: any, queryParams: any = {}) =>
                    apiCall(prefix.join('/'), queryParams, method, body);
            }
        }
    });

    return wrapped;
}

// This can be used like clientApi.path.METHOD(params).then(...)
// It is also type safe!
export const clientApi = wrapApi(apiObject);
```

Then for the server:

```ts
function dropFirstParameter(fn: any): any {
    return (...args: any[]) => fn(...args.splice(1));
}

function hostApi(app: express.Express, api: ApiMap, checkers: any): void {
    const methods: any = {
        GET: app.get.bind(app),
        POST: app.post.bind(app),
        PUT: app.put.bind(app)
    };
    Object.keys(api).forEach((path: any) => {
        Object.keys(api[path]).forEach((method: string) => {
            const path = '/' + path;
            methods[method](path, (req: any, res: any) => {
                const body = req.body.message;
                const queryParameters = req.query;

                let handler: any;
                if (key === 'GET') {
                    // GETs don't have a body, so drop it from the list
                    handler = dropFirstParameter((api as any)[key]);
                } else {
                    handler = (api as any)[key];
                }

                handler(body, queryParameters)
                    .then((value: any) => {
                        res.status(200);
                        res.send(JSON.stringify({message: value}));
                    })
                    .catch(() => {
                        res.status(HTTPStatus.InternalServerError);
                        res.send('Internal server error');
                    });
            });
        }
    });
}

export function initRoutes(app: express.Express) {
    hostApi(
        app,
        {
            customers: {
                GET: getCustomers,
                POST: addCustomer
            },
            search: {
                GET: searchCustomers
            }
        },
        apiObject);
}
```

The type checking still works:

```ts
apiMap.customers.POST(0);
```

```text
Argument of type '0' is not assignable to parameter of type 'string'.
```

It also works on the server side, although the error messages are somewhat harder to read:

```text
 error TS2345: Argument of type '{ customers: { GET: () => Promise<{ id: string; name: string; }[]>; POST: (p: number) => Promise<{ id: string; name: string; }>; }; search: { GET: (p: { id?: number; name?: string; }) => Promise<{ id: string; name: string; }[]>; }; }' is not assignable to parameter of type '{ customers: { GET: () => Promise<{ id: string; name: string; }[]>; POST: (t_0: string) => Promise<{ id: string; name: string; }>; }; search: { GET: (t_0: any, t_1: { id: string; name: string; }) => Promise<{ id: string; name: string; }[]>; }; }'.
  Types of property 'customers' are incompatible.
    Type '{ GET: () => Promise<{ id: string; name: string; }[]>; POST: (p: number) => Promise<{ id: string; name: string; }>; }' is not assignable to type '{ GET: () => Promise<{ id: string; name: string; }[]>; POST: (t_0: string) => Promise<{ id: string; name: string; }>; }'.
      Types of property 'POST' are incompatible.
        Type '(p: number) => Promise<{ id: string; name: string; }>' is not assignable to type '(t_0: string) => Promise<{ id: string; name: string; }>'.
          Types of parameters 'p' and 't_0' are incompatible.
            Type 'string' is not assignable to type 'number'.
```

## Runtime checking

JavaScript is a dynamically typed language, and TypeScript only gives
compile-time warnings. Since our API is an object, could we add runtime checks
without modifying the API?

Let's start by changing the helper functions slightly:

```ts
const num = ((p: any) => typeof p === 'number') as any as number;
const str = ((p: any) => typeof p === 'string') as any as string;

function fun<T, TS extends [any?, any?]>(returns: T, ...takes: TS) {
    return (((...t: TS) => takes.every((validator, i) => (validator as any)(t[i])))
            as any as (...t: TS) => Promise<T>);
}

function optional<T>(param: T): T | undefined {
    return ((t?: T) => (t === undefined) || (param as any)(t)) as any as (T | undefined);
}

function arr<T>(param: T): T[] {
    return ((p: T[]) => (p.every(t => (param as any)(t)))) as any as T[];
}

function obj<T extends object>(p: T): T {
    return ((inner: T) =>
            Object.keys(p).every(
                (checkme: string) =>
                    (p as any)[checkme]((inner as any)[checkme]))
    ) as any as T;
}
```

Instead of returning ``undefined``, these now return functions which check
whether the argument is the alleged type. For example, ``str`` is a function,
which returns true if the argument is a string. At the same time, the function
is of type ``string`` (instead of ``string => boolean``) so it can be used in
the API definition.

Now, when we rewrite the server function...

```ts
const handler = apiImplementation[path][method];
const checker = api[path][method] as any;
if(!checker(req.body)) {
    res.status(400);
    res.send('Bad request');
} else {
    // passed initial validation
    const response: Promise<any> = handler(req.body);
    // ...
}

```
... we get serverside runtime type checking for free!

## Further work

This is a relatively simple example, and doesn't implement any way to specify
things like headers.  The API could allow nested paths, for example
`/foo/bar/baz` using``{foo: {bar: {baz: ...}}}``. Error responses could also be
modeled to be type safe.

[Check out a complete project!](https://github.com/jgke/typescript-react-express-starter/)
The example project using this as a framework supports nested routes.
