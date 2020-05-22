---
layout: post
title: ClojureScript web server with Macchiato, Shadow CLJS and Reitit  
author: hjhamala
excerpt: ClojureScript is a valid alternative for backend development besides browser development. In this post I will explain how a simple server is created using Shadow CLJS as a compilation tool, Macchiato as the server software and Reitit as a Ring router. 
tags:
- ClojureScript
- Node.Js
- Macchiato
- Shadow-CLJS
- Reitit
- Web servers
---
[ClojureScript](https://clojurescript.org) is a variant of [Clojure](https://clojure.org) which compiles to JavaScript. 
This makes ClojureScript usable in devices which can run JavaScript such as browsers and backend services with using (Node.js)[https://nodejs.org]. 

Traditionally ClojureScript has been mostly used in browsers and backends have been made with Clojure or with other technologies. 
Pure ClojureScript backend usage has been more rare. Movement towards serverless technologies have although changed the industry.
AWS Lambda and container tecnologies prefer fast starting and short living applications. Node.js is compared to JVM much faster
in the startup and therefore this applies also to ClojureScript vs Clojure comparison. This means that in certain cases
ClojureScript may be a better alternative for backend programming.

One way to create backends in ClojureScript would be to use Express.js or other JavaScript frameworks and program only 
handlers with ClojureScript.There exists fortunately alternative to that which also allows us to use existing Clojure web development tools 
which many times have support also for ClojureScript. Especially this means that we could use existing [Ring](https://github.com/ring-clojure/ring/wiki/Concepts) middlewares 
and routers

Adapting Ring routers and middleware to Node.js web server is not complicated but fortunately [Macchiato project](https://macchiato-framework.github.io/) 
is a ready framework which adapts Node.js internal web server to Ring framework. 

I also want to use Metosin [Reitit](https://github.com/metosin/reitit) which is an excellent router library.  Reitit also 
supports Swagger generation and Clojure Spec based request and response coercion.  Personally I prefer to  
use [Shadow CLJS](https://shadow-cljs.github.io/docs/UsersGuide.html) as a build tool for ClojureScript instead of [Leiningen](https://leiningen.org/). 

Using Macchiato, Reitit and Shadow CLJS needs certain tweaks compared to normal Clojure Ring project which I will next introduce.

As a prerequirement I will assume that Node.js and NPM is installed.

# REPL driven development
This differs a lot depending on what development environment is used so please read Shadow CLJS
[documentation](https://shadow-cljs.github.io/docs/UsersGuide.html#_repl_2.)  for different scenarios. 

One way is to:

```bash
# Start Shadowcljs compilation
npm run watch 
# Connect node to compilation unit
node target/main.js
# Connect the REPL to port which Shadowcljs exposed
# Invoke from the the REPL
(shadow/repl :app)
# Start coding :)
```

# Getting example parts from GitHub repository

I have made a GIT repository (https://github.com/hjhamala/macchiato-example-solita-dev-blog)[https://github.com/hjhamala/macchiato-example-solita-dev-blog] 
containing branches for different parts of the project. If you don´t want to copy the texts then 
you can simply clone the repository and switch to the branches. 

# Installing shadow-cljs
_Branch: 01_minimal_project_

Shadow-cljs is installed via NPM. 
First create `package.json` file with next contents.

````json
{
  "name": "macchiato-shadow-cljs-example",
  "version": "0.1.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "watch": "shadow-cljs watch app",
    "compile": "shadow-cljs compile app",
    "release": "shadow-cljs release app",
    "start_release": "node -e 'require(\"./target/main.js\").server()'"
  },
  "keywords": [],
  "devDependencies": {
    "shadow-cljs": "2.9.8"
  },
  "dependencies": {
  }
}
````

After this run command `npm install` in the same directory.

Shadow CLJS compilation is configured in `shadow-cljs.edn` so create a new file with the next content: 
```clojure
{:source-paths ["src" "test"]
 :dependencies [[com.taoensso/timbre "4.10.0"]]
 :builds {:app {:target :node-library
                :source-map true
                :exports {:server macchiato-test.core/server}
                :output-dir "target"
                :output-to "target/main.js"
                :compiler-options {:optimizations :simple}}}}
```
I added Timbre as a logging library but that part is optional.

Then we create a new ClojureScript file for starting the server `src/macchiato_test/core.cljs':
```clojure
(ns macchiato-test.core
  (:require [taoensso.timbre :refer [info]]))

(defn server []
  (info "Hey I am running now!"))
```

Lets compile the file and run it. This can be done from the REPL as well.

```bash
npm run release
npm run start_release
```

This should print out something like 

`INFO [macchiato-test.core:5] - Hey I am running now!` 

and then exit.

# Making minimal Macchiato server
_Branch:  02_add_minimal_macchiato_

First we need to install Macchiato as dependency by adding the next dependency to `shadow-cljs.edn`:

`[macchiato/core "0.2.16"]`

Change `core.cljs` with next content:

```clojure
(defn handler
  [request callback]
  (callback {:status 200
             :body "Hello Macchiato"}))

(defn server []
  (info "Hey I am running now!")
  (let [host "127.0.0.1"
        port 3000]
    (http/start
      {:handler    handler
       :host       host
       :port       port
       :on-success #(info "macchiato-test started on" host ":" port)})))
```
Then start the server from the REPL by invoking 

```clojure 
(server)
```

And be greeted with many errors... 

Most likely compiler or Node.js will give errors like  'MODULE_NOT_FOUND' not found.
The missing NPM modules are listed in Macchiato core library `project.clj` file. Shadow CLJS does not load them because
it expects NPM dependencies to be in package.json. This means that we must add them to it. This could be avoided
by letting Leiningen handle all the dependencies.  

```bash
npm add ws concat-stream content-type cookies etag lru multiparty random-bytes qs simple-encryptor url xregexp
npm add source-map-support --save-dev
```

After that running the server should print to console:

`INFO [macchiato-test.core:19] - macchiato-test started on 127.0.0.1 : 3000.`

We can test the server by invoking `curl localhost:3000` which should return

`hello macchiato`

# Adding Reitit
_Branch:  03-reitit-added_

First we need to add Metosin Reitit and Spec-Tools to Shadowcljs dependencies. These dont have any NPM dependencies
so there is no need to update `package.json` as well.
```
[metosin/reitit "0.5.1"]
[metosin/spec-tools "0.10.3"]
```

Then replace `core.cljs` with the next content.

```clojure
(ns macchiato-test.core
  (:require [taoensso.timbre :refer [info]]
            [macchiato.server :as http]
            [reitit.ring :as ring]
            [reitit.coercion.spec :as c]
            [reitit.swagger :as swagger]
            [macchiato.middleware.params :as params]
            [reitit.ring.coercion :as rrc]
            [macchiato.middleware.restful-format :as rf]))

(def routes
  [""
   {:swagger  {:info {:title       "Example"
                      :version     "1.0.0"
                      :description "This is really an example"}}
    :coercion c/coercion}
   ["/swagger.json"
    {:get {:no-doc  true
           :handler (fn [req respond _]
                      (let [handler (swagger/create-swagger-handler)]
                        (handler req (fn [result]
                                       (respond (assoc-in result [:headers :content-type] "application/json"))) _)))}}]
   ["/test"
    {:get  {:parameters {:query {:name string?}}
            :responses  {200 {:body {:message string?}}}
            :handler    (fn [request respond _]
                          (respond {:status 200 :body {:message (str "Hello: " (-> request :parameters :query :name))}}))}
     :post {:parameters {:body {:my-body string?}}
            :handler    (fn [request respond _]
                          (respond {:status 200 :body {:message (str "Hello: " (-> request :parameters :body :my-body))}}))}}]
   ["/bad-response-bug"
       {:get  {:parameters {:query {:name string?}}
               :responses  {200 {:body {:message string?}}}
               :handler    (fn [request respond _]
                             (respond {:status 200 :body {:messag (str "Hello: " (-> request :parameters :query :name))}}))}}]])

(defn wrap-coercion-exception
  "Catches potential synchronous coercion exception in middleware chain"
  [handler]
  (fn [request respond _]
    (try
      (handler request respond _)
      (catch :default e
        (let [exception-type (:type (.-data e))]
          (cond
            (= exception-type :reitit.coercion/request-coercion)
            (respond {:status 400
                      :body   {:message "Bad Request"}})

            (= exception-type :reitit.coercion/response-coercion)
            (respond {:status 500
                      :body   {:message "Bad Response"}})
            :else
            (respond {:status 500
                      :body   {:message "Truly internal server error"}})))))))

(defn wrap-body-to-params
  [handler]
  (fn [request respond raise]
    (handler (-> request
                 (assoc-in [:params :body-params] (:body request))
                 (assoc :body-params (:body request))) respond raise)))

(def app
  (ring/ring-handler
    (ring/router
      [routes]
      {:data {:middleware [params/wrap-params
                           #(rf/wrap-restful-format % {:keywordize? true})
                           wrap-body-to-params
                           wrap-coercion-exception
                           rrc/coerce-request-middleware
                           rrc/coerce-response-middleware]}})
    (ring/create-default-handler)))


(defn server []
  (info "Hey I am running now!")
  (let [host "127.0.0.1"
        port 3000]
    (http/start
      {:handler    app
       :host       host
       :port       port
       :on-success #(info "macchiato-test started on" host ":" port)})))
```
## Middlewares 

First two middlewares are needed for parameter wrapping. `params/wrap-params` does query params parsing and reads possible
body of a HTTP request. `rf/wrap-restful-format` does encoding/decoding depending on Content-Type of the request. `wrap-body-to-params`
is a new middleware which I made because Reitit expects body params to be in `body-params` named map in the Ring request.

`wrap-coercion-exception` is a middleware which catches request and response coercion errors and returns 400 or 500 level 
error messages. In real development at least 400 error should include also some information why the request are rejected. 
Reitit error object contains data which could be transformed to more human friendly way pretty easily.

## Asynchronous handlers

Compared to regular Clojure Ring handlers Macchiato uses asynchronous variant of a handler which have three parameters
instead of regular one. The additional parameters are respond and raise callbacks. For Node.js we only need to use
respond.

## Testing the server

Start the server and run the next commands:

`curl localhost:3000/swagger.json` returns the swagger file.

```bash
# Missing parameter gives error
curl localhost:3000/test
{"message":"Bad Request"}
# Request with good parameter returns expected response
curl localhost:3000/test?name=heikki
{"message":"Hello: heikki"}
# Reitit coerces bad response
curl localhost:3000/bad-response-bug?name=heikki
{"message":"Bad Response"}
```

# Conclusion
I hope that this post shows necessary ways to use Reitit with Macchiato. Personally I think that using Reitit and Macchiato 
is also a very good way to develop AWS ApiGateway backed Lambdas locally. Development is of course possible by using local 
ApiGateway but this leads to a situation where we cant use the REPL. I will introduce one way to mix Macchiato and Reitit 
with Lambdas in the future post so stay tuned on Solita Dev Blog!