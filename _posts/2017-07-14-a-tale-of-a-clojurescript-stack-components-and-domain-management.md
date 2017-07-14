---
layout: post
title: >
  A Tale of a ClojureScript Stack: Components & Domain Management
author: jarzka
excerpt: How the ClojureScript stack was born and evolved over time in Harja project.
tags:
- clojure
- clojurescript
- frontend
- reagent
- tuck
- specql
- stylefy
---

Frontend applications tend to be unique; every single one of them is built differently with different technologies and software stack. The lack of a standard approach requires us, software developers, to re-think the stack every time a new project begins. In big and long projects, it is almost a given that the used technology stack will become at least partially obsolete before the application hits production state. But things do not have to be this way. This is a story of how we created a frontend stack for the Harja project and how we have been able to keep it fresh as time goes on.

A brief introduction to the project: [Harja](https://github.com/finnishtransportagency/harja) is a Single-Page Web Application (SPA) built for the Finnish Transport Agency. The system helps several hundred people reporting and communication related to road caring and maintenance in Finland. The codebase contains approximately 150 000 lines of code (including all Clojure, LESS and SQL files), from which the frontend takes approximately one third, 50 000 lines of code.

## In the beginning there was ClojureScript

JavaScript has long been the *de facto* language for frontend development, but has since also become an execution platform for other languages, such as [ClojureScript](https://github.com/clojure/clojurescript). ClojureScript is a [Clojure](https://clojure.org) to [JavaScript](https://en.wikipedia.org/wiki/JavaScript) compiler and is largery the same language as Clojure with differences mainly consisting of differences in runtime environments. ClojureScript brings the power of Clojure and [functional programming](https://en.wikipedia.org/wiki/Functional_programming) to the frontend.

Why functional programming? It's well suited for manipulating data with pure functions, meaning that functions do not change any value, but instead they simply receive data and output data. This makes functions easier to manage and test. Pure functions are also always thread-safe. JavaScript already has great support for functional programming, but ClojureScript makes it even better with it's built-in immutable data structures. Other great features of ClojureScript are nifty asyncronous code management with channels, and macros, which are code that is executed at compile time. Clojure also makes it possible to share code between frontend and backend, which is a big plus. When bundled with [Figwheel](https://github.com/bhauman/lein-figwheel), code changes are automatically compiled to JS and sent to the browser, which makes the development process nice and smooth. Thus, ClojureScript was our choise for building the frontend.
 
## Building a component abstraction API

Building modern single-page applications relies heavily on the use of in-browser JavaScript to communicate with the server, manage app state and render it to the user. The Web was not originally designed to work like this, which in turn has led to the birth of different software libraries and frameworks for building SPA applications. There are many such libraries for ClojureScript too, but our preference and one of the most popular is [Reagent](https://github.com/reagent-project/reagent). Reagent is a wrapper for Facebook's [React](https://github.com/facebook/react), a very popular library for creating user interfaces from individual UI components. Reagent makes it easy to build components with small amount of code using the power of Clojure expression and so was our choise of component abstraction library.

There are three popular ways to write components in Reagent. The simplest possible component is a function, which takes data in, and returns a Clojure vector presenting HTML code as [Hiccup](https://github.com/weavejester/hiccup).

```clojure
(defn paragraph [text]
  [:p text])
```

Another way is to return a render function. This method is usually used when a component contains inner state, or is supposed to do something once when the component is created.

```clojure
(defn paragraph [text]
  ;; When this component is created, the console logging is done only once.
  (.log js/console "Mounting a component!")
  (fn [text]
    ;; This is a render function. It is potentially called multiple times during the lifetime of the component.
    [:p text]))
```

Finally, Reagent makes it possible to define a component in a map containing lifecycle functions and the render function. Component lifecycle consists of moments when the component is created, updated or deleted. It is often useful to do something when a specific moment occurs.

```clojure
(defn paragraph [text]
  (r/create-class
    {:component-will-mount #(.log js/console "Component will mount")
     :component-did-mount #(.log js/console "Component did mount")
     :component-will-update #(.log js/console "Component will update")
     :component-did-update #(.log js/console "Component did update")
     :component-will-unmount #(do (.log js/console "Component will unmount")
                                  (.log js/console "Bye bye!"))
     :render (fn [text]
               [:p text])}))
```

While the code above works perfectly, it is a little bit tedious to write and remember the names of the lifecycle methods. Our job as programmers is not only to create working software, but to minimize our work by making code writing even easier. That's why we decided to create our own component API for Reagent, which looks like this when used:

```clojure
(defn paragraph [text]
  (comp/create
    ;; Lifecycle functions can be created easily with a single function call.
    ;; No need to remember and write long lifecycle names.
    (comp/in #(.log js/console "Component will mount"))
    (comp/did-mount #(.log js/console "Component did mount"))
    (comp/will-update #(.log js/console "Component will mount"))
    (comp/did-update #(.log js/console "Component did update"))
    ;; Our component API also supports calling the same lifecycle function multiple times.
    ;; In this case, both logging functions are called in order when the component is dismounted.
    (comp/out #(.log js/console "Component will unmount"))
    (comp/out #(.log js/console "Bye bye"))
    ;; The final parameter is always a render function.
    (fn [text]
      [:p text])}))
```

Now, this start to look idiomatic Clojure; things are expressed as briefly as possible while still keeping the code perfectly readable and understandable. Neat!

## Keeping things consistent by defining general-purpose components

Reagent components can be very big or very small, which leads to a question: what kind of things should be wrapped inside a component? Generally speaking, components should be relatively small and easy to reuse. Personally, I encourage programmers to create a component even from the smallest parts of the application. Not only helps it to keep components small and reusable, but it also helps developers in a big project to keep the codebase and the UI consistent. Let's take a couple of examples.

A button element is very common in web applications. The way it was created in Harja, was usually like this:

```clojure
[:button.primary-button
  {:on-click (.log js/console "Button click detected!")
   :disabled button-disabled?}
  Press me!]
```

When a new button was needed, the code above was basically taken as a template and modified as needed. While this approach worked perfectly fine, it started to show it's disadvantages. There was no standard approach to create a button element, so modifying all of them at once was a difficult thing to do. Furthermore, there were also some inconsistencies across the UI as the same type of buttons did not always look the same as developers were mistakenly using different CSS classes. It was clearly a time to refactor the code and create an idiomatic API for creating buttons!

```clojure
(defn button
  ([text action] (button text action {}))
  ([text action options]
    [:button {:class (:type options)
              :on-click (action)
              :disabled (:disabled options)}
      text]))

(defn button-primary
  ([text action] (button-primary text action {}))
  ([text action options]
    [button text action (merge options
                               {:type "primary-button"})]))

;; More button types to come... button-secondary, button-new, button-ok, button-delete etc.
```

Now there is a standard approach for creating different type of buttons. There is one place to go if one wants to modify all of them and all different type of buttons are guaranteed to look the same. Simple things like this help us to keep the codebase and the whole application consistent.

## Atoms and reactions take over the app

Components do not provide much benefit if users cannot manipulate the world through them. When Harja was still a relatively small application, state management relied heavily on Reagent atoms and reactions. For those familiar with [reactive programming](https://en.wikipedia.org/wiki/Reactive_programming), reaction is a way to define dependencies for a value, which is then updated immediately when those dependencies change. Here is a simple example of a reaction:

```clojure
(def projects (r/atom [{::p/id 1 ::p/name "Project A"} {::p/id 2 ::p/name "Project B"}]))
(def current-project-id (r/atom 1))

;; Current project is always supposed to contain the current project map element.
;; It is immediately and automatically resolved if projects atom or current-project-id atom is changed. 
(def current-project (reaction
                       (first (filter
                                #(= (::p/id %) @current-project-id)
                                @projects))))
```

In reality, many of our reactions were more complex than this. We even created our own reaction variant, which supports fetching data from the server automatically when certain dependencies change. For example, changing filters in the UI cause the application to get new data from the server.

Managing state through reactions worked well when Harja was still a relatively small application. However, when the application started to become more complex, managing app state through atoms and reactions became more complex. It was sometimes difficult to test, track changes and debug the application as the state was scattered across multiple places. Also, some parts of the app state were inside components, while some parts were atoms or reactions on namespace level. A simpler method was needed, and so the Tuck library was born.

## Managing app state with Tuck

Tuck is a minimalistic helper library for state management. Similarly to [Redux](https://github.com/reactjs/redux), the state of the app is kept in one place, and manipulated by well defined events. Events cannot directly mutate the app state, but always return the new app state. This approach to state management become popular in many JavaScript applications during the development of Harja, and it indeed has various advantages. Not only does it provide a single source of truth for the application state, but it also makes it clear which kind of events can manipulate the state and how. Furthermore, it makes it easy to trace, inspect, replay and write tests for all possible state changes.

Here is an example of Tuck app state:

```clojure
;; Define initial app state
(def state (atom {:projects [{:harja.domain.project/id 1
                              :harja.domain.project/name "Oulaisten alueurakka"
                              :harja.domain.project/year 2017
                              :harja.domain.project/type :caring}
                             {:harja.domain.project/id 2
                              :harja.domain.project/name "Oulun alueurakka"
                              :harja.domain.project/year 2015
                              :harja.domain.project/type :caring}]
                  :fetching-projects? false
                  :filters {:year 2017 :type :caring}}))

;; Define helper function for fetching data from the server and handling responses
;; as Tuck events
(defn fetch-data
  [app service args {:keys [ok error]}]
  ;; tuck/send-async! makes it possible to create events in an
  ;; asynchronous go block
  (let [ok! (tuck/send-async! ok)
        error! (tuck/send-async! error)]
    (go
      ;; Communication namespace provides simple helper functions for communicating with the server.
      (let [response (<! (communication/post! service args))]
        (if (communication/error? response)
          (error! response)
          (ok! response))))
    app))

;; Define events that can manipulate the app state
(defrecord ChangeYearFilter [year])
(defrecord ChangeTypeFilter [year])
(defrecord GetProjects [])
(defrecord GetProjectsOK [projects])
(defrecord GetProjectsError [])

(extend-protocol tuck/Event
  ChangeYearFilter
  (process-event [{year :year} app]
    ;; All events must return new app state
    (assoc-in app [:filters :year] year))

  ChangeTypeFilter
  (process-event [{type :type} app]
    (assoc-in app [:filters :type] type))

  GetProjects
  (process-event [_ app]
    (if-not (:fetching-projects? app)
      (-> app
          (fetch-data :get-projects
                      (:filters app)
                      {:ok ->GetProjectsOK
                       :error ->GetProjectsError})
          (assoc :fetching-projects? true))
      app))

  GetProjectsOK
  (process-event [{projects :projects} app]
    (assoc app :projects projects
               :fetching-projects? false))

  GetProjectsError
  (process-event [_ app]
    (message/show! "Fetch failed!" :danger)
    (assoc app :fetching-projects? false)))

;; Finally, create Reagent component which uses the state
(defn- root* [e! app]
  (comp/create
    ;; Create an event to fetch the projects from the server when this
    ;; component is mounted.
    (comp/in #(e! (->GetProjects)))
    (fn [e! app]
      ;; Render function is called automatically when ever the app state is changed
      [:div
        (for [project (:projects app)]
          ˆ{:key (:harja.domain.project/id project)}
          [:div (:harja.domain.project/name project)])])))
```

Now that the initial state and the events to manipulate it are in place, it's time to connect them with an UI component.

```clojure
(declare root*)

(defn root []
  [tuck state root*])

;; root* component is now managed by tuck. Tuck calls is with the following arguments:
;; - e!, which can be used to create events
;; - app, which contains the current app state
(defn- root* [e! app]
  (comp/create
    ;; Create an event to fetch the projects from the server when this
    ;; component is mounted.
    (comp/in #(e! (->GetProjects)))
    (fn [e! app]
      ;; Render function is called automatically when ever the app state is changed
      [:div
        (for [project (:projects app)]
          ˆ{:key (:harja.domain.project/id project)}
          [:div (:harja.domain.project/name project)])])))
```

All changes to the app state can be tested easily. Here is an example:

```clojure
(deftest get-projects-ok
  (let [old-state {:fetching-projects? true
                   :projects []}
        new-projects [{:harja.domain.project/id 666
                       :harja.domain.project/name "Project"}]
        new-state (tuck/process-event
                    (->GetProjectsOK new-projects)
                    old-state)]
    (is (= new-state
           {:fetching-projects? false
            :projects new-projects}))))
```

For debugging, we created a simple UI component which renders the app state as a simple grid element.

![Debugging app state visually](/img/a-tale-of-a-clojurescript-stack-components-and-domain-management/tuck_debug.png)
*Debugging app state visually*

Since the idea in Tuck is to keep the application state in one place, we had one problem: the app state was already scattered across multiple namespaces and some of was kept inside components. Thus, we decided to use Tuck mainly for creating new views. When a new view is created, the state of the view is kept in an atom and manipulated through Tuck events, in one place. The view can also listen changes in important reactions and communicate them directly in to it's Tuck state. When talking about our existing UI components that take atoms in, we can use Reagent's "wrap" function to call a function when the state of the component is changed and communicate it to Tuck. This way, reactions, our existing components and Tuck work well together.

Suppose, for example, that the selected year filter value is stored in some reaction, and the project type should be manipulated using an existing input component, which takes an atom as a parameter to store it's state. Our component can listen changes in both and update the app state:

```
(comp/create
    (comp/in #(e! (->GetProjects))
    ;; watcher watches changes in a reaction or atom using cljs.core/add-watch function.
    ;; When the value is changed, we communicate the change in to the Tuck state.
    ;; When the component is dismounted, the watcher is also stopped.
    (comp/watcher selected-year #(e! (->ChangeYearFilter %))))
    (fn [e! app]
      [:div
        ;; input component takes an atom to store it's value.
        ;; r/wrap creates an atom-like value, which contains a callback function, which is
        ;; called when the value of the atom is changed inside the component.
        [input (r/wrap (get-in app [:filters :type])
                       #(e! (->ChangeTypeFilter %)))]
        (for [project (:projects app)]
          ˆ{:key (:harja.domain.project/id project)}
          [:div (:harja.domain.project/name project)])])))
```

Naturally this lead to the situation in which the state of our application is managed differently in different places: some views use only reactions, while others use Tuck to manage their state. This mixing of patterns may sound like a disadvantage, but considering the much easier way to manage app state in new views, we believe it was worth it. This also shows how flexible the used libraries are; they can be easily mix-and-matched to create the best possible outcome without refactoring the whole codebase.

## Managing domain in one place

Now that component and state management is in good shape, let's talk about a thing that every web application needs to face, regardless of the used technology stack, domain management.

In object-oriented languages, domain is usually modelled as classes. A class represents a subject in the current domain: the data as class members and behaviour as methods. Since Clojure is a functional language, we do not have a direct equivalent to a class. Instead, we prefer to use data and functions. Still, it would be nice to gather things related to a specific domain in to one place. For this, we created a namespace for every domain subject and put them under the harja.domain namespace.

What are these domain namespaced used for? Firstly, we use them to namespace keywords in a map. When a map contains keys related to a specific domain, the keys are namespaced like this:

```clojure
{:harja.domain.project/id 1
 :harja.domain.project/name "Oulaisten urakka"
 :harja.domain.project/year 2017}

;; Note: Namespacing is easier by using aliases, but fully qualified
;; names are used for demostration purposes. 
```

When a map contains data from multiple domains, namespaced keywords help us to understand the domain context of specific keywords. For example, there is an id keyword in the map, or even multiple of them, it should never be unclear in which domain the id is related to.

Secondly, domain namespaces typically contain utility functions to manipulate specific domain data. The best part is that all domain namespaces are so called CLJC code, which means the code is shared between frontend and backend. No matter if we are working with the browser or with the server, we can use the same utility functions everywhere to manipulate domain data, in one language. And since these utility functions typically manipulate data using namespaced domain keywords, we can always be sure that wrong keys are never mistakenly touched.

Finally, we want to have [specs](https://clojure.org/about/spec) for our domain data. We created [specql](https://github.com/tatut/specql/) to generate specs directly from [PostgreSQL](https://www.postgresql.org) database schema at compile time. Specs help us to automatically define what kind of data a specific domain subject contains and what are the accepted values. When needed, domain data can be validated against it's spec to see if it is valid. Usually we do this validation on the server when a specific domain service is called, but as the generated specs are shared between ClojureScript and Clojure, data validation can be done also on frontend. We have experimented a way to use database specs to add automatic validation for forms and Tuck app state.

## Experimenting even further with stylefy

specql is not made only for generating specs: we also use it to fetch data from the database on the server side by expressing SQL queries as Clojure data. Since we started using specql, most of the new code we write has been simply Clojure, excluding some complex SQL queries and LESS stylesheets. This made me think of the possibility if the whole information system could be written in a single language. At this point, LESS stylesheets were the only part of the application without the possibility to use Clojure - or at least not in the way I wanted. To fill this gap, [[stylefy](https://github.com/Jarzka/stylefy) was created.

There were already great libraries for presenting stylesheets as Clojure data, but none of which were primarily used for styling components. My original idea was to create a library in which a style could be attached in to components by using a single **use-style** macro. The macro would convert the given Clojure data in to CSS file and return a class definition for the component. This turned out to be difficult to manage, so a different a approach was needed: when a component calls **use-style**, the given Clojure map is converted to CSS on the fly and added in to DOM as class definition. This turned out to work well and provided asimple way to manage component styles:

```clojure
(defn- simple-text-component [text style]
  [:p (use-style style) text]])
```

I was happy how the library turned out and my colleagues were also excited about it. However, we decided not to use it in the current project. There was simply too much working LESS code already written, so mixing stylefy with the current stylesheets was not likely to provide us any real advantages. Still, we look forward to probably use the library in future projects. 

## And so the stack lived happily ever after

Well, at least for some time. You know, the frontend ecosystem evolves so quickly that all of this will obviously be irrelevant in 0 months. Rapid frontend development is one reason why long software projects can start to slowly become legacy already during the development phase. In Harja, we have had the courage to keep the codebase fresh by successfully adapting new ways to build web applications while still keeping the existing codebase working.

If this made you become interested in using the same technologies we did, feel free to check them out. [Tuck](https://github.com/tatut/tuck), [specql](https://github.com/tatut/specql), and [stylefy](https://github.com/Jarzka/stylefy) are all open source libraries created by people who work at Solita. The first two can be said to be battle-tested in a big SPA project, and the whole team has been happy to work with them.
