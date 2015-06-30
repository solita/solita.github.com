---
layout: post
title: Interfaces and components in a functional world... or "how I stopped worrying and let Clojure into my heart"
author: tatut
excerpt: Functional programming encourages the use of data and functions instead of creating new concrete types.
---

Reusability of code is something most programmers would probably agree is a good thing. At least on a small scale.
Often reusability is achieved by using design patterns (eg. Gang of Four) and abstracting things that vary behind
interfaces.

We all know how interfaces and classes are used in object-oriented languages to create reausable code.
But how does functional programming accomplish the same when we mostly use functions and data?
Well, by using functions and data.

OOP interfaces are but one tool for reusability. In this post I will try to show that a simpler way exists.
I'll use a pseudo Java syntax to describe an OOP interface based solution to a reusable UI component and then show an alternative
interface using Clojure.


## What is an interface?

A brief digression on the meaning of interfaces. We Clojurists like to ponder on the definitions of words.
Programming is not only about making the computer do what we want, but also to communicate the intent of our
code to other humans. 
What actually is an interface? As a non-native English speaker, I've only used the word interface in programming
and never bothered to look it up. 

A dictionary definition says that an interface is "a point where two systems, subjects, organizations, etc. meet and interact".
That definition suggests to me that interfaces are something quite primitive and abstract.
What does meeting and interacting mean? If we follow our dictionary we can go further down and see that to meet is to "arrange or happen to come into the presence or company of" and interacting is to "act in such a way as to have an effect on each other".

Enough with the dictionary, I think we can derive from these definitions that interfaces must have some sort of boundary where code from two (or more) components are put together (the meeting part). And the code in one component has an effect on the behaviour of the other(s) (the effect part).

In programming, what we usually mean by interfaces is a way to specify the rules of the interaction in a way that humans and compilers can check. An interface is a contract of how the interaction between software components takes place.

## Example interface

In our quest to create reusable UI components, we might define a component for listing tabular data (like sales records, shopping cart items and so on). For a component to be reusable, it must have an interface that defines how other components can use the functionality provided by our listing component.

In an OO language, we might define the following listing component:

```java
class Listing extends Widget {
  Listing(ListingColumns columns, ListingData data);
  render() { ...code to render...}; // defined by Widget superinterface
}
```

This defines a basic component, with a constructor that takes in the definition of the columns to list and a way to access the actual data to show. The render() method is obviously the actual meat of the component and will render the data we passed in.

Well now we have two new interfaces to consider, perhaps they could be something like:

```java
interface ListingColumns {
  int getColumnCount();
  Column getColumnAt(int column);
}

interface ListingData {
  int getRowCount();
  Row getRowAt(int row);
}

interface Column {
  String getTitle();
  boolean isSortable();
  ...
}
interface Row {
  ...
}
```
 
Ok, looking good. We now have more abstractions for Column and Row. I left out one important part: we still don't have a way to get at the actual data we want to list. At the minimum we need to decide whose responsibility it is to do the accessing. Does a Column know how to get the data from a Row object? Or does the Row know how to return a given column? Perhaps a separate accessor mapping is required for complex cases. What about computed fields, can we have a column that is computed from multiple items in the row? For example a sales tax that is calculated from the price and product category.

The above code looks completely reasonable and if we design our interfaces right, will give us the right balance between ease of use and power.

## Another way of doing things

The above code, while looking perfectly readable, is decidedly not what most functional programmers would come up with. Functional programming values data over creating new concrete types. Instead of going down the rabbit hole of creating new types for every possible interaction, we can use the most general thing we have: data and functions.

What is the essence of a "column definition"? I would argue it is a mapping of attributes. The aggregation of listing columns is simply a sequence (or vector) of maps.

In the same vein, the essence of a row is also a mapping of attributes and the aggregate is a vector of rows. Now it becomes clear that the data is just data and we don't want data to have behaviour. Does a sales record row have behaviour? No, so a logical place for our accessing logic is in the column definitions.

But since our column definition is also data we must turn to the other power tool: functions (which are also data). We simply put the accessing logic as an attribute of the column definition.

In ClojureScript (using Reagent, a React wrapper), our component would simply be:

```clojure
(defn listing [columns data]
   ...code to output the listing html...)
```

Looks like a pure function, sweet! And using it would be something like:

```clojure
[listing [{:title "Item" :get :item :sortable? true}
          {:title "Price" :get :price}
          {:title "Tax" :get (fn [row]
                               ;; a 10% tax rate
                               (* 0.10 (:price row)))}]

         [{:item "Jamaican cigars" :price 25}
          {:item "Water fluoridation formula" :price 599}
          {:item "Doomsday device" :price 999999}]]
```

I think our functional approach is very readable, it looks more like data than behaviour. The pure data approach is also very concise without losing readability or power. We can also easily have dynamic listing columns and use all the functional data processing operations to create the columns.

Some might argue that this approach is missing some flexibility of the interface based approach. *We must not allow a feature gap!*
We usually don't just list out our items in code, but we actually fetch them from somewhere. We might have different strategies for coming up with the data, some listings might have local data, others might fetch them from a server asynchronously. We need to have an interface that can be used in both cases!
Designing such an OO interface is not a trivial matter, but luckily in ClojureScript and Reagent we have atoms and reactions.

Atoms are simply a "place for data" which can be read, reset or swapped. Atoms can also be watched and Reagent handles atoms automatically. When atoms are read inside a component, that component is automatically re-rendered when the data held by the atom changes.
Atoms are an extremely simple (and elegant) interface for data. Reactions on the other hand are like Excel formulas, they are atoms that are calculated (and automatically re-calculated) based on data from other atoms.

We only change our component to dereference an atom instead of taking a raw vector of items. Now we can provide this data from anywhere, be it local data or asynchronously fetched data. Our component does not care how the data is fetched and how it is processed. We could add things like filtering the listing (for example "show only items where price > 100") without touching the listing component at all. We simply create a reaction on the initial data atom and pass that in instead. No need for new concrete FilteredListingData class to sap and impurify *all of our precious functional code*!

```clojure
(def sales (atom nil)) ;; initially empty vector of sales
(def min-price (atom nil)) ;; price filter, initially nil
(def filtered-sales
  ;; the sales data, filtered by price
  (reaction (let [all-sales @sales
                  min-price @min-price]
              ;; whenever either sales or min-price atoms change,
              ;; this is automatically run and set as value of
              ;; filtered sales
              (if min-price
                (filter #(>= (:price %) min-price) all-sales)
                all-sales))))

(defn sales-listing []
  [:div.sales-listing-ui
     "Minimum price: "
     ;; HTML input field. When changed, parse into number and set as value of min-price (or nil)
     [:input {:on-change #(reset! min-price
                                  (try
                                    (Long/parseLong (-> % .-target .-value))
                                    (catch _ _
                                      nil)))
              :value (str @min-price)}]
                 
    ;; Our listing as before, but with the filtered reaction                    
  [listing [{:title "Item" :get :item :sortable? true}
            {:title "Price" :get :price}
            {:title "Tax" :get (fn [row]
                                 ;; a 10% tax rate
                                 (* 0.10 (:price row)))}]
           ;; Read and pass in filtered sales data
           @filtered-sales])
```      



## What about type safety?

One might still prefer an interface approach especially if you are used to it.
What about type safety and validating things in the interface.
Best option in ClojureScript, in my opinion, is to use [Prismatic Schema](https://github.com/Prismatic/schema).
Schema is a library for defining the "shape" of data. We can for example define all the allowed attributes and
types our column definitions can take:

```clojure

;; define the schema
(def +column-schema+ {:title s/Str
                      :get clojure.lang.IFn
                      (s/optional-key :sortable?) s/Bool}) 

;; validate using our defined schema
(s/validate +column-schema+ some-input-data)

```

Another option is [core.typed](https://github.com/clojure/core.typed) or simply using pre/post condition asserts to verify arguments.



## Conclusion

If you have an interface where you need to pass data that you can think in terms of the usual maps, sets, list and primitives,
don't contort it to a byzantine maze of abstract interfaces and their interactions. Using simple data and describing its shape is
usually much more straightforward, at least in languages with good data processing capabilities and easy-to-use data literals.

When you create interfaces, you are locking up your data. You can no longer use the usual functions (map, filter, etc...) to
create variations of it. Every trick you need to do, you have to explicitly support.

In this post we only scratched the surface of what is possible with functional programming combined with atoms and an efficient rendering library.
If you are interested be sure to check out [React](http://facebook.github.io/react/) and [Reagent](http://reagent-project.github.io/) or my simple example project [Widgetshop](https://github.com/tatut/widgetshop) and make your life easier by letting functional programming into your heart :)
