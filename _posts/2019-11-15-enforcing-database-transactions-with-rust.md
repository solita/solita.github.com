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

Rust implements this by providing a unique feature: the borrow checker.
Essentially, the borrow checker is a compile-time feature which ensures that
objects live long enough, and at the same time prevents unsafe concurrent access
to variables. This is implemented by following a couple of simple rules:

1. If an object drops out of scope, it is destroyed
2. An object must outlive all references to it
3. An object can only have either multiple immutable references, or a single mutable reference

In this blog post we are mostly concerned about the first rule -- if an object
drops out of scope, it is destroyed.

The borrow checker is mostly praised for its ability to enable manual memory
management without suffering from null pointer exceptions or segfaults -- Safe
Rust doesn't have any null or otherwise invalid references! In my opinion, the
best benefit of the borrow checker is not the speedup it provides by
eliminating the garbage collector, but the ability to catch logic bugs. If you
manage to construct your problem as a problem around ownership, the Rust
compiler can check your logic at compile-time!

## Trait interlude

Rust doesn't have inheritance nor interfaces. Instead, generic code is
implemented around *traits*. Traits are similar to interfaces in the sense that
they contain a bunch of methods, and certain types implement those interfaces.
Types can only implement traits either where the type is defined, or where the
trait is defined. This unfortunately means that one cannot implement a
third-party trait for a third-party type. However, unlike interfaces in eg.
Java, one can implement their own traits for other types.

When writing generic code, generic type parameters can receive trait bounds to
specify things that can be done with the types. For example, in the following
function

```rust
fn debug_print<T: Debug>(t: T) { dbg!(t); }
```

the type T is required to implement the trait `Debug`, which allows turning the
object into an programmer-readable (but not necessarily human-readable) format.

The generic functions are compiled similarily as in C++: any calls to the
function are specialized to the types, which technically can create binary
bloat, but practically reduces it as the compiler has better options for
optimization.

## Modeling database queries around ownership

So, we need to be able to make a single database query without a transaction,
convert a database connection into a transaction and make multiple queries
inside a transaction.

Sounds like while making a query without a transaction, the connection should
refuse any additional queries. If the queries are made within a transaction,
additional queries should be accepted. Furthermore, the transactions should be
cleaned up when dropped, which `postgres::Transaction` does by default,
defaulting to rollback, rather than commit. Let's sketch an API for it:

```rust
pub fn one(connection: db::Connection) {
    db::find_person(connection, "Joe"); // OK
}
pub fn two(connection: db::Connection) {
    connection.transaction(|tx| {
        let person = db::find_person(&tx, "John")?;
        tx.commit()?;
        Ok(person)
    });
}
pub fn three(connection: db::Connection) {
    connection.transaction(|tx| {
        let first = db::find_person(&tx, "Mary")?;
        let second =  db::find_person(&tx, "Suzy")?;
        tx.commit()?;
        Ok((first, second))
    });
}
pub fn four(connection: db::Connection) {
    db::find_person(connection, "Foo");
    db::find_person(connection, "Bar"); // ERROR: two queries without a transaction
}
```

## Technical detals

The typical `postgres` connection types are modeled around typical usage rather
than this special case, so we clearly need some wrappers around them. Let's
start by defining them:

```rust
pub struct Connection(Box<postgres::Connection>);
pub struct Transaction<'a>(Box<postgres::transaction::Transaction<'a>>);
```

These types contain exactly one member: the respective `postgres` connection
type, with the crucial difference that `Connection` and `Transaction` do not
derive the `Clone` trait used to acquire new copies of the connection. Ignore
the `Box` and `'a`, they only tell Rust that the references to the variables
exist long enough.

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

impl Connection {
    pub fn transaction<F, R, E>(self, callback: F) -> Result<R, E>
    where F: FnOnce(Transaction) -> Result<R, E> {
        let tx = self.0.transaction().unwrap();
        let res = callback(Transaction(Box::new(tx)))?;
        Ok(res)
    }
}
```

Then we just call `into_generic_connection()` while inside the relevant
database function:

```rust
pub fn find_person<IGC: IntoGenericConnection>(db: IGC, name: &str) -> Option<Person> {
    let conn = db.into_generic_connection();
    conn.query("SELECT id, name FROM account WHERE name=$1", &[&name]).unwrap()
        .into_iter()
        .map(|row| Person { id: row.get(0), username: row.get(1) })
        .next()
}
```

With these couple lines of code, any database accesses are guarded against
accidental unsafe usage. The programmers still have access to the backdoor used
to gain a reference to the connection without using a transaction (through
`IntoGenericConnection`), but using it is explicit, rather than accidental. The
same wrapper types can also be used to enforce a transaction around database
functions which make multiple queries simply by replacing the `IGC` generic
with `Transaction`.

Now, the last example gives an error message around the lines of the following
snippet:

```text
error[E0382]: use of moved value: `connection`
 --> src/backend/src/router.rs:3:20
  |
1 | pub fn four(connection: db::Connection) {
  |             ---------- move occurs because `connection` has type
  |             `db_traits::Connection`, which does not implement the
  |             `Copy` trait
2 |     db::find_person(connection, "Foo");
  |                     ---------- value moved here
3 |     db::find_person(connection, "Bar");
  |                     ^^^^^^^^^^ value used here after move
```

## Performance

Does this provide any performance drawbacks? Both `Connection` and
`Transaction` are exactly the size of `Box`, which means moving them around is
essentially free. Both implementations of `into_generic_connection` are no-ops,
as boxes are secretly just pointers, and the trait methods are referencing the
first and only member of the struct -- which is a no-op. Thus, there shouldn't
be any performance hits when using this method.

Another way to implement this would be to use a zero-sized type for connections
and load the connection when converting to GenericConnection or Transaction,
but the implementations would be more complex.

## Conclusion

While a relatively new language, Rust can already be used to tackle practical
problems. This is just one example how Rust can be used to implement safe and
fast programs.
