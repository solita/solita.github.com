---
layout: post
title: Enforcing database transactions with Rust
author: jgke
excerpt: >
  Rust's ownership model enables enforcing the use of database transactions,
  while still allowing single queries without transactions.
tags:
 - Database
 - Rust
---

Consider this Clojure snippet:

```clojure
(defn fetch-thing [user-id thing-id]
  (if (db/has-permission user-id thing-id)
    {:status 200 :body (db/fetch-thing thing-id)}
    {:status 400})
```

It's clean, does clearly what it looks like it does, but there's a small
problem; it doesn't use a transaction. If something happens in the database
between the second and the third line, for example if the `thing` referenced by
`thing-id` is deleted, the output of `db/fetch-thing` can get quite
unpredictable. Could we make this kind of programs safer?

## Enter Rust

Rust is a relatively new programming language, with focus on speed and safety.
Rust has the unique notion of 'ownership', which enables memory safety without
relying on a garbage collector. Nowadays in most languages all variables are
actually references, which are just thrown around and are either wildly mutable
or completely immutable. Rust provides a way to write code where mutation is
explicit and safe.

In my opinion, the best benefit of the borrow checker is not the speedup it
provides by eliminating the garbage collector, but the ability to catch logic
bugs. If you manage to construct your problem as a problem around ownership,
the rust compiler can check your logic at compile-time!

## Modeling database queries around ownership

So, we need to be able to
1. Make a single database query without a transaction
2. Convert a database connection into a transaction
3. Make multiple queries inside a transaction

Sounds like while making a query without a transaction, the connection should
refuse any additional queries. If the queries are made within a transaction,
additional queries should be accepted. Let's sketch an API for it:

```rust
pub fn one(connection: db::Connection) {
    db::get_person(connection, "Joe"); // OK
}
pub fn two(connection: db::Connection) {
    connection.transaction(|tx| {
        db::get_person(&tx, "John")
    });
}
pub fn three(connection: db::Connection) {
    connection.transaction(|tx| {
        let first = db::get_person(&tx, "Mary")?;
        let second =  db::get_person(&tx, "Suzy")?;
        Ok((first, second))
    });
}
pub fn four(connection: db::Connection) {
    db::get_person(connection, "Foo");
    db::get_person(connection, "Bar"); // ERROR: use of moved value: `connection`
}
```

## Technical detals

Clearly we need some wrappers around the typical `postgres` connection types.
Let's start by defining them:

```rust
pub struct Connection(Box<postgres::Connection>);
pub struct Transaction<'a>(Box<postgres::transaction::Transaction<'a>>);
```

These types contain exactly one member: the respective `postgres` connection
type, with the crucial difference that `Connection` and `Transaction` do not
derive the `Clone` trait used to acquire new copies of the connection.

Next, we need a trait and relevant implementations to convert these types to
the trait provided by `postgres` which provides methods such as `query`.

```rust
pub trait IntoGenericConnection {
    type G: postgres::GenericConnection;
    fn into_generic_connection(&self) -> &Self::G;
}

impl IntoGenericConnection for Connection {
    type G = postgres::Connection;

    fn into_generic_connection(&self) -> &Self::G {
        &self.0
    }
}

impl<'a> IntoGenericConnection for &'a Transaction<'a> {
    type G = postgres::transaction::Transaction<'a>;

    fn into_generic_connection(&self) -> &Self::G {
        &self.0
    }
}
```

Then we just call `into_generic_connection()` while inside the relevant
database function:

```rust
pub fn get_person<IGC: IntoGenericConnection>(db: IGC, name: &str) -> Option<Person> {
    let conn = db.into_generic_connection();
    conn.query("SELECT id, name FROM account WHERE name=$1", &[&name]).unwrap()
        .into_iter()
        .map(|row| Person { id: row.get(0), username: row.get(1) })
        .next()
}
```

## Performance

Does this provide any performance drawbacks? Both `Connection` and
`Transaction` are exactly the size of `Box`, which means moving them around is
essentially free. Both implementations of `into_generic_connection` are no-ops,
as boxes are secretly just pointers, and the trait methods are referencing the
first and only member of the struct -- which is a no-op. Thus, there shouldn't
be any performance downsides to this.

Another way to implement this would be to use a zero-sized type for connections
and load the connection when converting to GenericConnection or Transaction,
but the implementations would be more complex.


## Conclusion

While a relatively new language, Rust can already be used to tackle practical
problems. This is just one example how Rust can be used to implement safe and
fast programs.
