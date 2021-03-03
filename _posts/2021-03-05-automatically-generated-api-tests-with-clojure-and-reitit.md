---
layout: post
title: Automatically generated API tests with Clojure and Reitit
author: jgke
excerpt: >
  Is your entire API tested? Maybe you should test that.
tags:
 - Clojure
 - Reitit
 - Testing
---

Have you ever forgotten to write a test for some API endpoint, which then
eventually happens to break? Would it be possible to check whether all of your
API is tested? If you are using a data-driven router, it's possible to write
tests which ensure that every endpoint is tested.

The functions described in this blog post create an almost complete smoke test
suite, where a new endpoint can be tested with a few lines of code. It also
forces the API to behave consistently and give out similar errors independent
of the endpoint.

My current customer project uses something along these lines to test that the
entire API handles credentials and permissions appropriately and doesn't
randomly crash at some endpoints.

Example API
===========

For a small example API, we have the following endpoints:
- `POST:/api/resource` - Create a new resource
- `GET:/api/resource/:resource-id` - Get the created resource by ID
- `PUT:/api/resource/:resource-id` - Update the resource
- `POST:/api/authorization` - Add a user to a resource
- `DELETE:/api/authorization` - Delete a user from a resource

Only users added to a resource can update it. The creator of the resource is
added when creating the resource.

The endpoints behave in the following way: All requests without the `Auth`
header return an error. Creating resources returns the created resource ID. The
ID can be used to find the created resource.

```
$ curl -d "Hello" localhost:3001/api/resource   
{:cause :missing-authentication}
$ curl -H "Auth: 1" -H "Content-Type: application/json" -d '{"content": "Hello"}' localhost:3001/api/resource
{:resource-id "4"}
$ curl -H "Auth: 1" localhost:3001/api/resource/4
{:content "Hello"}
```

Using a different Auth ID than the one used to create the resource initially
returns an error, but if the original user adds a new user into the resource,
the new user can also access it.

```
$ curl -H "Auth: 2" localhost:3001/api/resource/4
{:cause :not-authorized}
$ curl -H "Auth: 1" -H "Content-Type: application/json" -d '{"resource-id": "4", "token": "2"}' localhost:3001/api/authorization
{}%                                 
$ curl -H "Auth: 2" localhost:3001/api/resource/4
{:content "Hello"}
```

The API looks like this:

```clojure
(def api
  [["/api"
   ["/authorization"
    {:post   add-authorization
     :delete remove-authorization}]
   ["/resource"
    ["" {:post create-resource}]
    ["/:resource-id"
     {:get    read-resource
      :put    update-resource
      :delete delete-resource}]]]])
```

Testing
=======

Traditionally testing an endpoint like this is relatively simple. Just make some requests and
check that the returned value is the expected one.

```clojure
(defn- request
  ([method token uri]
   (request method token uri nil))
  ([method token uri body]
   (-> (handler/app
         {:uri            uri
          :request-method method
          :headers        {"auth" token}
          :body-params    body})
       (select-keys [:status :body])
       (update :body clojure.edn/read-string))))

(deftest test-resource
  (let [resource-id (-> (request :post 1 "/api/resource" {:content "foo"}) :body :resource-id)]
    (is (= {:status 200 :body {:content "foo"}}
           (request :get 1 (str "/api/resource/" resource-id))))
    (is (= {:status 404 :body {:cause :not-found}}
           (request :get 1 (str "/api/resource/foo"))))
    (is (= {:status 400 :body {:cause :missing-authentication}}
           (request :get nil (str "/api/resource/" resource-id))))
    (is (= {:status 403 :body {:cause :not-authorized}}
           (request :get 2 (str "/api/resource/" resource-id))))
    (is (= {:status 200 :body {}}
           (request :post 1 "/api/authorization" {:resource-id resource-id :token 2})))
    (is (= {:status 200 :body {:content "foo"}}
           (request :get 2 (str "/api/resource/" resource-id))))))
```

However, what happens if you accidentally skip testing some endpoint? Normally
you just have to wish that the issue is spotted during code review. If you do
some larger refactoring, it's possible that both the developer and the reviewer
miss that some parts of the software aren't tested.

Clojure and Reitit makes it possible to get a list of routes and methods, which
can then be connected to tests so that you can check that your entire API is at
least somewhat tested.

Automatically testing a single endpoint
---------------------------------------

Ideally, we'd like to have something like the following code block, which would
automatically test that endpoint.

```clojure
(def test-routes
  {"/api/authorization" {:post   test-handler
                         :delete test-handler}
   "/api/resource"      {:post test-handler}
   "/api/resource/:resource-id"
                        {:get    test-handler
                         :put    test-handler
                         :delete test-handler}})

(deftest test-all-paths
  (doseq [[path props] test-routes]
    (doseq [[method handler] props]
      (handler path method))))
```

But since some routes require some endpoint-specific payload and some
preconditions (eg. to update a resource, one needs to create it first), let's
add those into the object:

```clojure
(def test-routes
  {"/api/authorization" {:post   (test-path with-resource
                                            (fn [ctx]
                                              {:resource-id (:resource-id ctx)
                                               :token       (:token ctx)}))
                         :delete (test-path with-resource
                                            (fn [ctx]
                                              {:resource-id (:resource-id ctx)
                                               :token       (:token ctx)}))}
   "/api/resource"      {:post (test-path with-token {:content "some content"})}
   "/api/resource/:resource-id"
                        {:get    (test-path with-resource)
                         :put    (test-path with-resource {:content "updated content"})
                         :delete (test-path with-resource)}})
```

There's two parts to testing these paths. One is creating the necessary
resources for testing, and the other is actually making the requests. Let's
start off with the context. We need functions to create valid tokens, as well
as some resources which can be updated. Here, `with-token` provides a context
with a valid token, while `with-resource` provides a context with a pre-created
resource.

```clojure
(def next-id (atom 0))

(defn- create-token [ctx]
  (assoc ctx
    :token (swap! next-id inc)))

(defn- create-resource [ctx]
  (assoc ctx
    :resource-id
    (->
      (request :post (:token ctx) "/api/resource" {:content "some content"})
      :body
      :resource-id)))

(def empty-ctx (constantly {}))

(defn with-token []
  (-> (empty-ctx)
      (create-token)))

(defn with-resource []
  (-> (empty-ctx)
      (create-token)
      (create-resource)))
```

What does `test-path` look like? Based on our usage, it needs to take in one or
two arguments, the first of which is some function which creates the resources
needed for testing, and the second is a body which will be sent to the API if
provided. The function should also replace possible path parameters with
appropriate IDs from the context. In our use case, the only possible path
parameter is `:resource-id`, but this function is easily extendable for
additional parameters.

```clojure
(defn- create-request-path [path ctx]
  (cond-> path
          (:resource-id ctx) (string/replace ":resource-id" (-> ctx :resource-id str))))

(defn test-path
  ([context-fn] (test-path context-fn nil))
  ([context-fn body]
   (fn [path method]
     (let [ctx          (context-fn)
           request-path (create-request-path path ctx)
           request-body (if (and (ifn? body) (not (map? body)))
                          (body ctx)
                          body)]
       (testing "Request without tokens returns 403"
         (is (= {:status 400 :body {:cause :missing-authentication}}
                (request method nil request-path request-body))))
       (testing "Request with tokens returns 200"
         (is (= 200
                (:status
                  (request method (:token ctx) request-path request-body))))))
     ; todo: add a test here which adds / removes the token from the resource
   )))
```

With those two pieces of code, the  `test-all-paths` method goes over every
path in the `test-routes` object, and creates API requests for the route.

Collecting a list of routes
---------------------------

If we don't add all of the routes to the `test-routes` object, nothing in the
system notifies us about it. Since we can just ask `reitit` for a list of
routes, let's also test that our test blob matches the routes in the system.

When your API looks something like this:
```clojure
(def api
  [["/api"
    ["/authorization"
     {:post   add-authorization
      :delete remove-authorization}]
    ["/resource"
     ["" {:post create-resource}]
     ["/:resource-id"
      {:get    read-resource
       :put    update-resource
       :delete delete-resource}]]]])
```

You can use the `reitit-impl/resolve-routes` function to get a list of routes,
and check that all of those are tested:

```clojure
(defn- route-to-data-row [[route properties]]
  [route (keys (select-keys properties [:get :post :put :patch :delete :options]))])

(deftest all-paths-tested
  (let [route-data      (reitit-impl/resolve-routes handler/api (reitit-core/default-router-options))
        routes          (into {} (map route-to-data-row route-data))
        missing-routes  (apply dissoc routes (keys test-routes))
        extra-routes    (apply dissoc test-routes (keys routes))
        missing-methods (keep
                          (fn [[route methods]]
                            (let [route-methods  (set methods)
                                  tested-methods (set (keys (get test-routes route)))
                                  missing        (set/difference route-methods tested-methods)]
                              (when (and (get test-routes route) (not-empty missing))
                                [route missing])))
                         routes)]

    (is (= 0 (count missing-routes))
        (str "The following routes are not tested: \n - "
             (string/join "\n - " (sort (keys missing-routes)))))
    (is (= 0 (count extra-routes))
        (str "The following paths contain tests, but the API doesn't have paths for them: "
             (keys extra-routes)))

    (is (= 0 (count missing-methods))
        (str "The following routes are not tested: \n - "
             (string/join "\n - " (map (fn [[route method]] (str route ": " method))
                                       missing-methods))))))
```


Going to the next level
-----------------------

If you implement this with a larger Clojure project, you are going to end up
with a single test function which tests a lot of different paths. If something
goes wrong in the middle of the test, it can be difficult to find out which
path actually failed. Using Clojure macros it's possible to generate a test for
each path.

```clojure
(defmacro generate-test [path method]
  `(let [test-name# (symbol (string/replace (str "test-all-paths__" ~path "_" ~method) #"[^a-zA-Z-]" "_"))
         path#      ~path
         method#    ~method]
     `(deftest ~test-name#
        ((-> test-routes (get ~path#) (get ~method#))
         ~path# ~method#))))

(doseq [[path props] test-routes]
  (doseq [[method _] props]
    (eval (generate-test path method))))
```

This creates individual tests for each test, with somewhat-readable names, such
as `(test-all-paths___api_resource__resource-id__put)` which tests
`PUT:/api/resource/:resource-id`.

How about automatically generating data?
----------------------------------------

Depending on your use case, it might be possible to also generate the entire
`test-routes` object. In our case, we had way too much endpoint-specific
business logic that autogenerating the whole thing would be feasible. if you
have a simpler (or, ahem, more consistent) API and you use something like
`spec` for input validation, it might be possible to use that data to generate
the request bodies, and input special cases for the couple of endpoints which
require more specific data. I'd guess that this is probably not worth the
effort though.

Conclusions
===========

It's possible to semi-automatically generate tests with standard Clojure and
check that your entire API is tested. Clojure macros enable fine tuning the
generated tests for easier debugging.

This kind of semi-automatic testing isn't a replacement for more exact unit
tests -- you should still write those as well. They will provide you a lot
clearer error messages if you have bugs in your server. After all, this test is
closer to a smoke test than a complete test suite.

See the code for this blog post at
[GitHub](https://github.com/solita-jaakkoha/clojure-generating-tests).
