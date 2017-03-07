---
layout: post
title: Isolated integration testing with Clojure and Postgres
author: ilmoraunio
excerpt: We take a look at a magical feature in Postgres and a derived potential solution to reduce the chattiness of Clojure integration test reports.
tags: 
- clojure
- testing
- postgres
---
I've been trying to create isolated integration tests in my hobby project to validate that my inserts work inside my database layer. I wanted to see if I could minimize the chattiness of my integration test suite, and to quicken the guesswork of what's breaking my tests. While the solution hasn't been battle-tested out in the real world, it has been initially promising. Let's check it out.

## The problem

Assume we have the following schema in postgres.

```sql
-- http://www.starkandwayne.com/blog/uuid-primary-keys-in-postgresql/
CREATE EXTENSION "uuid-ossp";

CREATE TABLE Users (
  username varchar(200) PRIMARY KEY,
  password TEXT
);

CREATE TABLE Room (
  id TEXT PRIMARY KEY DEFAULT uuid_generate_v1mc(),
  name varchar(200)
);

CREATE TABLE Participant (
  id TEXT PRIMARY KEY DEFAULT uuid_generate_v1mc(),
  Room_id TEXT NOT NULL,
  name varchar(200),
  username varchar(200),
  FOREIGN KEY(Room_id) REFERENCES Room(id),
  FOREIGN KEY(username) REFERENCES Users(username)
);

CREATE TABLE Message (
  id TEXT PRIMARY KEY DEFAULT uuid_generate_v1mc(),
  Room_id TEXT NOT NULL,
  sender TEXT NOT NULL,
  recipient TEXT NOT NULL,
  message TEXT NOT NULL,
  FOREIGN KEY(Room_id) REFERENCES Room(id),
  FOREIGN KEY(sender) REFERENCES Participant(id),
  FOREIGN KEY(recipient) REFERENCES Participant(id)
);
```

In my case, I wanted to test how `Message` insertion works.

```clojure
;; test/isolated_integration_test/db/message_test.clj

(defn message
  ([db-spec data] (jdbc/with-db-transaction [tx db-spec] (model/create! tx data))))

(deftest message-test
  (fact-group :integration
    (facts "Message insertion"
      (with-state-changes [(before :facts (empty-and-create-tables))]
        (fact "Succeeds"
          (let [{user_id1 :username}   (user db-spec {:username "foo" :password "hunter2"})
                {user_id2 :username}   (user db-spec {:username "bar" :password "hunter2"})
                {room_id :id}          (room db-spec)
                {participant_id1 :id}  (participant db-spec {:name "foo"
                                                             :username user_id1
                                                             :room_id room_id})
                {participant_id2 :id}  (participant db-spec {:name "bar"
                                                             :username user_id2
                                                             :room_id room_id})]
            (message db-spec {:room_id room_id
                              :sender participant_id1
                              :recipient participant_id2
                              :message "hello world!"}) => (contains {:id id-pattern?}
                                                                     {:room_id id-pattern?}
                                                                     {:sender id-pattern?}
                                                                     {:recipient id-pattern?}
                                                                     {:message string?})))))))
```

Here "Message insertion" is an ordinary integration test. The test is about sending a message from foo to bar. For this test it's required that we create a room, a couple of users foo and bar, and put these users inside the room as participants. It's a given that all of above insertion points are susceptible to failure. For an integration test that's probably okay. We do want to know if something doesn't work between multiple components, or we risk ending up with [broken software](https://twitter.com/ThePracticalDev/status/687672086152753152).

Still, how do I quickly tell if it's just the depending models breaking up or the model-under-test that's broken as well? For that, I would need separate tests in which I temporarily disable my foreign key checks to insert just the message. One solution would be to to operate the foreign keys manually, dropping them and creating them to each table before and after my test cases had run. The problem was, this was a potentially faltering mechanism when all I really needed was a simple switch command from postgres and maybe some light wrappers in Clojure.

Turns out, you might be able to implement this simply with postgres (and Clojure).

## A potential solution

Using a postgres-only feature called `session_replication_role` we can insert rows into our schema tables without adhering to foreign key constraints.

Here's what the postgres [documentation](https://www.postgresql.org/docs/9.4/static/runtime-config-client.html) has to say about the feature:

> Controls firing of replication-related triggers and rules for the current session. Setting this variable requires superuser privilege and results in discarding any previously cached query plans. Possible values are origin (the default), replica and local. See ALTER TABLE for more information.

There's not really much to how it works: you need to enable replication mode (as a postgres superuser), enter data, and disable replication mode afterwards.

```sql
SET session_replication_role = 'replica';
INSERT INTO Message (Room_id, sender, recipient, message) VALUES ('ebe1b9be-f7a7-11e6-a440-573a04afc920', 'f480dd34-f7a7-11e6-a440-0f01535615fc', 'f9086be2-f7a7-11e6-a440-13d4ffe62295', 'hello world!');
SET session_replication_role = 'origin';
```
*The gist in raw SQL*

Replication mode is enabled only for the duration of your SQL session, unless you turn it off before. That said, you'll probably always want to turn it off the moment you've inserted your data to minimize any potential errors in your other tests.

In our example below, `without-fk-constraints` allows all forms within to be free of any foreign-key constraint checks. Notice that we use `DEFAULT` instead of `origin` to end the replication mode, these two are considered to be the same by default.

```clojure
;; test/isolated_integration_test/test_util.clj

(defmacro without-fk-constraints [tx & body]
  `(do
    (jdbc/execute! ~tx ["SET session_replication_role = replica"])
    (let [result# (do ~@body)]
      (jdbc/execute! ~tx ["SET session_replication_role = DEFAULT"])
      result#)))
```

Now we can add another test into `message_test.clj`, with a simplified structure and with the rest of the database insertions cleaned up.

```clojure
;; test/isolated_integration_test/db/message_test.clj

(deftest message-test-isolated
  (fact-group :integration-isolated
    (facts "Message insertion (isolated)"
      (with-state-changes [(before :facts (empty-and-create-tables))]
        (fact "Succeeds"
          (jdbc/with-db-transaction [tx db-spec]
            (without-fk-constraints tx
              (let [room_id "ebe1b9be-f7a7-11e6-a440-573a04afc920"
                    sender "f480dd34-f7a7-11e6-a440-0f01535615fc"
                    recipient "f9086be2-f7a7-11e6-a440-13d4ffe62295"]
                (message tx {:room_id room_id
                             :sender sender
                             :recipient recipient
                             :message "hello world!"}) => (contains {:id id-pattern?}
                                                                    {:room_id room_id}
                                                                    {:sender sender}
                                                                    {:recipient recipient}
                                                                    {:message "hello world!"})))))))))
```

As a result our test is now
1. more isolated,
2. more deterministic, and
3. slightly more readable.

As you may have already noticed, midje's `fact-group` allows me to categorize tests with profile metadata `:integration` and `:integration-isolated`. Using lein-midje's `:filter` keyword we can run a subset of our integration tests.

A naive introducible problem is to add a field with default value to `Users` and check the report with `lein midje` using the profile metadata.

```sql
ALTER TABLE Users ADD COLUMN foo TEXT NOT NULL DEFAULT 'bar';
```

```bash
$ lein midje :filter integration-isolated

= Namespace isolated-integration-test.test-util
= Namespace isolated-integration-test.db.participant-test
= Namespace isolated-integration-test.db.message-test
>>> Output from clojure.test tests:
= Namespace isolated-integration-test.db.participant-test
Checking Participant insertion (isolated)
Checking Succeeds
= Namespace isolated-integration-test.db.message-test
Checking Message insertion (isolated)
Checking Succeeds
= Namespace isolated-integration-test.db.user-test
Checking User insertion
Checking Succeeds

FAIL "User insertion - Succeeds" at (form-init4343624100477613268.clj:22  user)
Actual result did not agree with the checking function.
        Actual result: clojure.lang.ExceptionInfo: Value does not match schema: {:foo disallowed-key} {:type :schema.core/error, :schema {:username java.lang.String, :password java.lang.String}, :value {:username "foobar", :password "hunter2", :foo "bar"}, :error {:foo disallowed-key}}
              # (stacktrace redacted)
    Checking function: (contains {:username "foobar"} {:password "hunter2"})
    # (explanation redacted)
= Namespace isolated-integration-test.db.room-test
Checking Room insertion
Checking Succeeds

1 failures, 0 errors.
>>> Midje summary:
FAILURE: 1 check failed.  (But 3 succeeded.)
Subprocess failed
```

In this instance, the test report with the profile `integration-isolated` provides less noise than its counterpart `lein midje :filter integration`.

## Caveats

Like all things simple on the outside, there are some tradeoffs which you may definitely want to know about. Despite having mentioned some of them already, it's worth underlining them all:

1. Triggers are disabled.
2. Rules are disabled.
3. Database user needs to be superuser.
4. Postgres-only.

[ALTER TABLE](https://www.postgresql.org/docs/9.1/static/sql-altertable.html) section delves a little bit on its trigger implications:

> Simply enabled triggers will fire when the replication role is "origin" (the default) or "local". Triggers configured as ENABLE REPLICA will only fire if the session is in "replica" mode, and triggers configured as ENABLE ALWAYS will fire regardless of the current replication mode.

However, UNIQUE constraints and CHECK constraints are enabled in replication mode.

If you're interested in reading more about `session_replication_role`, there's a [great article on it](http://blog.endpoint.com/2015/01/postgres-sessionreplication-role.html) which explains its function in great detail.

## Not a silver bullet, still a WIP

Basically, what we have here is a runtime congruity test between the database model in our application code and the table schema in our database. I've found that it's worked for me in my particular database and software setup, but YMMV. Plus as noted at the beginning, the solution is yet to be tested out in the real world, so it's still a work-in-progress.

It should be emphasized that isolated integration tests should always be paired with real integration tests. This is because we're still essentially breaking parts of our database integrity to test our insertion.

Also, if you find yourself using this solution with real foreign key references by mocking only some dependencies, then it may be best to use proper integration tests or knowingly deal with the consequences.

So, in all, `session_replication_role` seems like a really powerful tool which should be doubly considered before using it.

You have been warned. Have fun!

The repository for the examples above can be found [here](https://github.com/ilmoraunio/isolated-integration-test-example). If you have any criticisms about this design, I'd be interested in hearing it out. [Create an issue](https://github.com/ilmoraunio/isolated-integration-test-example/issues/new) or drop me a comment so we can talk.