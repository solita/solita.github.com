---
layout: post
title: Making Software Testing Easier with Clojure
author: jarzka
excerpt: Introducing 4 things in Clojure that can reduce the hassle of writing automated software tests.
tags:
- clojure
- clojurescript
- software testing
---

Your shiny new feature is almost complete. All you need do is simply to make sure that a few corner cases work properly by writing a few more automated tests. But knowing the hassle it is to setup the tests and mock components, you are not very excited. Sound familiar? Obviously, it should not be this way; testing should not be more difficult than writing production code. I want to talk about 4 things in Clojure that have made writing automatic software tests a bit easier and enjoyable. And if you are not using Clojure (yet), you might get some new ideas to adopt to your current toolset.

## 1. Using fixtures for setup and teardown

If I was about to test a big system with a lot of components, I would test individual components both separately and together. But I do not want to setup the whole system manually for every test, but to automate it. That's exactly what our current project team has done. The system is built from components using [Stuart Sierra's component library](https://github.com/stuartsierra/component). In the beginning of each test, we use **use-fixtures** function (found in clojure.test) to setup the testable system and all the needed components and tear down the system when testing is complete.

```clojure
;; Let's define a simple system with common components, such as database and http components.

(def system nil)

(defn system-fixture [tests]
  ;; At the beginning of the test the system variable is
  ;; altered to contain the testable system's components.
  (alter-var-root #'system 
    (fn [_]
      ;; The tests are supposed to use a testing data running in PostgreSQL database.
      ;; Make sure the test data is in initial state before running any tests.
      (reset-test-database!)
      (component/start
        (component/system-map
          ;; Define all the needed components and their dependencies.
          :db (db/create test-db)
          :https-server (https-server/create)
          :some-testable-component (component/using
                                   (->TestableComponent)
                                   [:https-server :db])))))

  ;; Run the tests
  (tests)
  ;; Perform teardown
  (alter-var-root #'system component/stop))
```

The defined system fixture works well, but since most of the testable components are going to depend on db and https server component, defining these over and over again in every test file would be a waste of time. We would like to simply initialise the test system and add the testable components in it. This problem can be solved by writing a [Clojure macro](https://clojure.org/reference/macros) which defines the testable system with common components, db and https-server in this case, and lets us add more components if we wish:

```
(defmacro extend-system-fixture
  [& custom-component-deps]
  `(alter-var-root #'system 
    (fn [_]
      (reset-test-database!)
      (component/start
        (component/system-map
          :db (db/create test-db)
          :https-server (https-server/create)
          :some-testable-component (component/using
                                   (->TestableComponent)
                                   [:https-server :db])
          ;; Our own custom components are added here:
          ~@custom-component-deps))))
     (tests#)
     (alter-var-root #'system component/stop)))
```

Macros allow us to write code which is evaluated in compile time and which can take any code as input and return any code as output. Thus, once the macro is ready, the it can be called in the following way:

```
(def extended-system-fixture
  ;; Call a macro, which builds the testable system in compile time and adds
  ;; our :custom-component in it.
  (extend-system-fixture
    :custom-component (component/using
                        (custom-component/->SomeCustomComponents)
                        [:https-server :db])))
```

Everything is working quite nicely, but what if we are going to use some common data from the test database in every test. Do we need to retrieve it every time on each individual test? You guessed it, no! We could write a custom fixture for that purpose:

```clojure
(defn db-values-fixture [tests]
  (reset! custom-value (db/get-some-value))
  (tests)
  (reset! custom-value nil)
```

Finally we can combine the extended-system-fixture and db-values-fixture together with **compose-fixtures** function and use combined fixture in the test with **use-fixtures**:

```clojure
(def test-fixture (compose-fixtures extended-system-fixture db-values-fixture))

(use-fixtures :once test-fixture)
```

 Now everything is ready. When we begin writing tests, the test is system ready and the custom value is retrieved for us from the test database before the tests are run. As you see, fixtures make it easy to setup the testable system and the components we are about to tests. The common components needed in all tests are defined once and custom functionality can be added afterwards.

## 2. Faking things for testing purposes

Testing functions that have dependencies to external components is always a bit tricky. A common approach to this is to test against a mock component, which contains fake success and errors responses. In Clojure, this idea can be taken even further. Clojure makes it easy to fake not only external system components, but virtually any function or variable!

A concrete example: I was having a problem on testing an API which is highly dependant on current time. The API was supposed to return a state for the current moment of time. Testing the function today might work well, but not tomorrow, since the API returns a different result every day. Luckily, Clojure's with-redefs function allowed me to fake the current time by writing my own definition for [clj-time's](https://github.com/clj-time/clj-time) **now** function:

```clojure

(deftest test-state
  (with-redefs [t/now #(t/date-time 2017 4 2)]
    (is (= (state-api/get-state) :too-early)))

  (with-redefs [t/now #(t/date-time 2017 4 8)]
    (is (= (state-api/get-state) :good-time)))

  (with-redefs [t/now #(t/date-time 2017 4 15)]
    (is (= (state-api/get-state) :too-late))))
```

Now whenever state-api tries to receive the current time using clj-time, it gets the fake date-time and thus passes the tests, now and in the foreseeable future.

**with-redefs** can be used to fake http requests as well. However, if you are using [HTTP Kit](http://www.http-kit.org/), the library has made it already very easy to fake http requests with **with-fake-http** function. Let's say we want to test an API endpoint, which internally communicates with some external system during processing the API call. The system response can be faked easily:

```clojure
(deftest  test-api
  (with-fake-http
      ;; By default, with-fake-http blocks all requests that are not specifically allowed
      ;; or faked in the binding vector.
      ["http://system.example.com/api/get-state" "OK" ;; Faked "OK" response if HTTP request is sent to this url during the test
       #".*api\/get-status.*" :allow] ;; This is our own API, allow all requests
      (let [response (test-utils/send-post "/api/get-status"]
        (is (= 200 (:status response)))))))
```

Generally I would not recommend overusing with-redefs or other faking methods, as they might make things difficult to understand. Optimally functions should be kept pure so that there is no need to fake things at all. For example, if the state API would have accepted the current time as a parameter, it would have been easier to test without faking anything. But since not all functions cannot be made pure, it is good to know that faking things is not a problem in Clojure.

## 3. Generative testing with spec

At the time of writing this, Clojure 1.9 and the [spec library](https://clojure.org/guides/spec) is still under development. Luckily that has not stopped us using spec already, since there is a [backport](https://github.com/tonsky/clojure-future-spec) for Clojure 1.8. As you might already know, spec makes it possible to specify what kind of input and output a specific function is supposed handle. This makes it easy to validate data in critical parts of the system. In addition, speccing things give us an opportunity to generate testing data automatically. This also makes it possible to write generative tests for services. No need to worry about trying to test every possible combination as generative tests based on Clojure specs already know how your data should look like.

```clojure
;; Define a spec for :id and :name
(s/def ::id nat-int?)
(s/def ::name string?)

;; Define a spec for a request, it is a map which should always contain :id and :name.
(s/def ::request (s/keys :req [::id ::name]))

(deftest generative-test
  ;; s/gen returns a generator which we pass to gen/sample, which then
  ;; gives us a sample of test requests (10 requests by default).
  ;; We then send every test request to the server and expect all
  ;; answers to be :ok
  (let [test-requests (gen/sample (s/gen ::request))]
    (doseq [test-request test-requests]
      (let [response (handle-request test-request)]
        (is (= response :ok))))))
```

We could even make the test run quicker by running all requests asynchronously. In Clojure, this is usually done with channels. Threads are not supposed to compete on access on some common mutable state, but instead data is send and received between threads via channels.

```clojure
(deftest generative-test
  (let [test-requests (gen/sample (s/gen ::request))
        answer-chan (chan)] 

    (doseq [test-request test-requests]
      ;; Run every request asynchronously. Once the answer is received,
      ;; put it to the answer-chan
      (go (let [response (handle-request test-request)]
            (>! answer-chan response))))

    ;; Main thread start to listen the answer-chan. Whenever it receives a new answer,
    ;; it adds it to the the loop's binding vector. The listening loops start again and continues
    ;; as long as all answers are gathered.
    (loop [all-answers []]
      (if (< (count all-answers) (count test-requests))
        (let [answer (<!! answer-chan)]
          (recur (conj all-answers answer)))
        (is (every? #(= :ok %) all-answers))))))
```

And that's it! Without comments, this multithreaded generative test example takes only 13 lines of code!

## 4. Frontend component testing

I imagine I am not the only one who has found frontend tests to be one of the trickiest part to write, especially if we are not talking about testing function inputs and outputs, but the look and behaviour of the UI. Our frontend is written in [ClojureScript](https://github.com/clojure/clojurescript) using [Reagent library](https://github.com/reagent-project/reagent). Behind the scenes, Reagent uses [React](https://github.com/facebook/react), so we can also take advantage of React's test utilities using a Clojure wrapper library called [cljs-react-test](https://github.com/bensu/cljs-react-test). These tools make it possible to mount UI components in a test container, querying their state in DOM and interact with them with simulated user inputs, such as clicks and keyboard inputs.

Let's take a look at a simple UI test. We begin by defining some utilities that can be used in all UI tests:

```clojure
(def test-container (atom nil))

;; Define a macro which will setup and unmount the test container
(defmacro prepare-component-tests []
  `(use-fixtures :each
     {:before (fn [] (reset! test-container (cljs-react-test.utils/new-container!)))
      :after (fn [] (unmount! @test-container))}))

;; Define a macro which will render the given component in the test
;; container and run the body (tests)
(defmacro with-component [component & body]
  `(do
     (reagent.core/render ~component @test-container)
     ~@body))

;; Define some little utilities which will help us to write component tests
(defn sel1 [path]
  ;; Select an element in the test container
  (dommy/sel1 @test-container path))

(defn click-and-render [element]
  (cljs-react-test.simulate/click element nil)
  (reagent/flush)) ;; Force render
```

And next, the test itself:

```clojure
(prepare-component-tests)

;; Define test for button-component. button-component is a small UI component
;; which takes an atom value to manipulate. The UI contains a button element with a class "number-button".
;; When the button is pressed, the atom's value will be reset to 1.
;; The button will also disable itself and contain another class "button-pressed".
(deftest simple-ui-test
  (let [button-value (atom nil)]
    ;; Define a test which uses the button-component and passes the button-value atom in.
    (with-component [ui/button-component button-value]
      ;; First we expect the button to be mounted in the DOM by finding it's DOM node
      (let [number-button (sel1 [:.number-button])]
        (is number-button "Number-button mounted correctly")

        ;; Press the button and expect it to change the button-value atom's state
        (click-and-render number-button)
        (is (= 1 @current-input-atom))
        (is (str/includes? (.-className number-button) "button-pressed"))

        ;; We expect the button to disable itself after one click,
        ;; so pressing the button again should do nothing
        (click-and-render number-button)
        (is (= 1 @current-input-atom))))))
```

While this test confirms that the component is working properly, it does not take much of a stand on how the component UI looks. Yup, writing efficient tests for CSS is still a challenge.

I have to admit that writing frontend tests, especially very comprehensive ones, can sometimes be a time-consuming process. Still, experience has shown that writing good tests for at least the most commonly used UI components can pay itself back with the fact that bugs are found much earlier.

## Conclusion

One reason that can possibly reduce the eagerness to write comprehensive software tests is the hassle one needs to face when writing tests. I strongly believe that we should use the same care in writing tests that we use when writing production code. Taking the time to write simple and reusable test utilities and knowing your tools are not going to fail you, can reduce the mental load associated to writing tests. Writing tests may sometimes feel unproductive, but you, or your colleague, will thank you later for not breaking things.