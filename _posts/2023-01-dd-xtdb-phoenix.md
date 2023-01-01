---
layout: post
title: Using XTDB with Phoenix LiveView
author: tatut
excerpt: Immutable Datalog databases are often used in Clojure but other frameworks, like Phoenix LiveView, can benefit from them as well.
tags:
- Elixir
- Datalog
---

Relational SQL databases are still the "de facto" choice for most new web applications these days,
but there are other interesting options to consider. There has been a lot of interest in Clojure circles
related to Datalog databases, like [Datomic](https://www.datomic.com)
and [XTDB](https://xtdb.com), which provide a different model of programming especially as it relates
to time.

Datalog need not only be for Clojure programmers, many programming languages can use it, especially ones
that have good facilities for describing data.
In this post, I will give a short introduction to a new library that allows using XTDB with the Erlang
ecosystem (specifically Elixir) and how to integrate that with the popular [Phoenix Framework](https://phoenixframework.org).
We will briefly introduce Datalog and the library, then create a sample app with a simple
LiveView component.

## Datalog, what?

What is datalog then and why should a web developer care about it? Datalog provides a different
programming model from the relational "table" view of things and instead focuses on entities that
have attributes. Entities are open in that they can have any attributes without limitations, so
there is no need to know all the columns beforehand or write migrations to add them.

Instead of tables having columns, you have entity attribute value triples (EAV) like
`[:bob :likes :pizza]` and `[:bob :date-of-birth 1997-04-09]`. Even joins are similarly
marked by having an attribute value be the identity of another entity.

One of the best things about XTDB (and Datomic) is that it doesn't update in-place like SQL.
When you write new data, the old one is still available and you can time-travel to the past
to answer queries about the state of the database at that time. Developers use git themselves
to retain the full history of their work, it's high time we give the same benefits to the
users of our software!

For more details on datalog, you can watch [my video on it](https://youtu.be/_PDul4C6qYI) or
follow along the [Learn XTDB Datalog Today](https://nextjournal.com/learn-xtdb-datalog-today/learn-xtdb-datalog-today)
tutorial.

## Introducing xtdberl

To leverage XTDB from the Erlang ecosystem, I wrote a library called [xtdberl](https://github.com/tatut/xtdberl)
(yes, naming is difficult) that integrates an XTDB node (JVM) to Erlang processes using [jinterface](https://www.erlang.org/doc/apps/jinterface/jinterface_users_guide.html).
While XTDB does provide an HTTP API, using regular Erlang messaging makes it possible to
control serialization and hook into the XTDB transaction listeners better.

%%%% tähän joku kuva?

As a good example tells more than a long description, here is how one would use it in Elixir:

```elixir
alias :xt_mapping, as: M
defmodule Person do
  ## Define struct fields
  defstruct [:id, :first_name, :last_name, :email]

  ## Define how the struct is mapped to an XTDB document
  def mapping() do
    M.register(
      M.mapping(
        %Person{},
        [M.idmap(:id, :":person"),
         M.required(M.field(:":person/first-name", :first_name)),
         M.field(:":person/last-name", :last_name),
         M.field(:":person/email", :email)]))
  end
end
```

In the above example, we define a Person struct that has 4 fields, one of which will be made into the
document id when storing it. The fields are defined as Clojure keywords and we add a namespace of person
to them just for clarity (you could have attributes without namespaces as well, but I find namespaces
keep them clear). We defined the first name as a required field, this is handy because all queries will
then assert that that attribute must be present. As documents themselves are not typed in any way, we
need to have at least one required attribute that is not present in documents generated from other struct
types (or we can add a static type attribute with `M.static`).

That is all the definition we need to do to be able to store and query persons. Calling `Person.mapping()`
will register the mapping for use. Calls to install mappings should be placed in the application startup.

We can now store new Persons by calling `:xt.put/1` like:
```elixir
:xt.put(%Person{id: "demo1",
                first_name: "Dear",
                last_name: "Reader",
                email: "dear.reader@example.com"})
{:ok,{42,{timestamp,1672312695820}}}
```

That call sends the transaction to the server and waits for a response. Here the server
responds with ok and a tuple containing the new transaction id and a timestamp.

How about querying the data? That is also simple as xtdberl allows querying by providing a "candidate"
instance and automatically generates a query that will pull all instances that match the candidate.
The candidate can have field values (tested with equality) or operations like `{:<, 42}` or `{:textsearch, "D*"}`.
The comparison operators work on all types, not just numbers, so you can compare things like strings
and dates as well. The included Lucene `textsearch` operator only works for text.

```elixir
## Query by specific value
:xt.ql(%Person{first_name: "Dear"})
[%Person{id: "demo1",
         first_name: "Dear",
         last_name: "Reader",
         email: "dear.reader@example.com"}]

## Or by an operator, here a Lucene text search
:xt.ql(%Person{email: {:textsearch, "example"}})
[...same result as above...]
```


## Putting it all together

![Happy family ready for business](/img/2023-xtdb-phoenix/all-together.png)

With the introduction in place, it's time to put everything together and build our app.
This section assumes that you have Elixir and Phoenix Framework installed and ready to go.
You will also need Java (17+) to run the XTDB database.

### Create a new app

First we initialize a new Phoenix app and remember to use the `--no-ecto` parameter. Ecto
is the Elixir library typically used for interacting with datastores, especially SQL databases.
Here we don't need it as we use XTDB directly.

```shell
mix phx.new xthello --no-ecto
cd xthello
```

Then we modify `mix.exs` file and include the dependency by adding the
following line inside deps:

```elixir
  {:xt, git: "https://github.com/tatut/xtdberl", branch: "main"}
```

Then we run `mix deps.get` to fetch all the dependencies and we are ready to launch!

Launch an interactive shell and the application by using the command: `iex --erl "-sname xthello" -S mix phx.server`.
You should see startup messages and a URL that points you to `http://localhost:4000`.
You should also see an alert notifying that XTDB is not available. That is fine for now
as we haven't started that service yet. When we do, the application will reconnect to
to it.

Verify that you have the app up and running by visiting the local URL above.
![Index page of a newly created Phoenix app](/img/2023-xtdb-phoenix/index-page.png)

### Modeling and connecting the database

Next, we want to create the datamodel we will be storing and querying. We can use the
person structure we used as a sample earlier, just place that in `lib/model.ex`.

You can type `c "lib/model.ex"` in the interactive shell and the code will be compiled
and loaded. You can then call `Person.mapping()` to register the mappings for now.

Now that we have everything ready on the Elixir side, we need to go boot up our XTDB node.
The easiest way to do that is to download a release and run it in demo mode:

```shell
java -jar xtdberl.jar demo
```

The demo parameter starts up the node with an in-memory database with default
mailbox settings that doesn't persist anything. This is good for a quick trial, but for
actual use, see documentation on how to configure it properly.

After starting up the database, you should see the line ```[notice] 1 XTDB node is now available.```
in your Phoenix console. We are ready for action!


... FIXME: next up, explain the full code the a liveview component that shows a Person?


## Closing remarks

In this post we covered a simple Phoenix LiveView component that conveniently reflects
our database and even updates automatically when the underlying data changes. In my opinion
this is a very handy way to develop many types of web applications without the need for
cumbersome Single Page Applications. Many web developers have found a new appreciation for
Server Side Rendering. See my earlier post about [Ripley](https://dev.solita.fi/2020/06/01/rethinking-the-frontend.html)
which implements a similar approach for Clojure.

There's no denying the popularity of relational databases and SQL, but I think many applications
will benefit from an approach that provides a more convenient programming model for developers.
Many people [want to avoid Object-Relational Mapping](https://dev.solita.fi/2021/06/01/why-avoid-an-orm.html)
and for good reasons. The current crop of Datalog solutions also provide full history which makes the
complicated "soft delete" patterns in SQL completely unnecessary, further simplifying application code.
