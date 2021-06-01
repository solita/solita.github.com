---
layout: post
title: Why avoid an ORM
author: jyrimatti
excerpt: > 
  I happened to discourage using an ORM in our company internal Slack, and suddenly found myself needing to explain some problems common in ORMs. I got a little bit carried away, and the explanation turned into this blog post.

tags:
 - ORM
 - Object-orientation
 - Hibernate
 - Java
 - Antipatterns
 - Best practices
 - Database
 - SQL
---

I happened to discourage using an ORM in our company internal Slack and suddenly found myself needing to explain some problems common in ORMs. I got a little bit carried away, and the explanation turned into this blog post.

I'm certainly not alone with this opinion, see for example [here](https://wozniak.ca/blog/2014/08/03/1/index.html), [here](https://abe-winter.github.io/2019/09/03/orms-backwards.html), or [Ted Neward's classic](http://www.odbms.org/wp-content/uploads/2013/11/031.01-Neward-The-Vietnam-of-Computer-Science-June-2006.pdf).
 
## What is an ORM?
 
First of all, what counts as an ORM? This is just as difficult to answer as "what counts as an object-oriented language" or "what counts as agile". There exists no single widely accepted definitions for these things since they are more like paradigms: a specific paradigm is usually related to certain kinds of aspects, and it makes using certain design choices more natural than others.
 
For example, in an object-oriented language, it's often natural to encapsulate (mutable) state inside a structure, whereas in a functional language it's often natural to solve the same problems by moving (immutable) state outside the structure to the edges of the system. While Java is widely considered an object-oriented language, one can still do functional programming in it. On the other hand, lambda calculus can be used to model objects and encapsulation, but it's certainly not what most people would call an object-oriented language.
 
_N+1 queries_, _object identity_ and _managing object relationships_ are concepts or problems that tend to come up with ORMs. Just because a tool makes these problems possible does not yet make it an ORM, but certainly closer to being an ORM.
 
My opinion? ORM stands for **object-relational mapping**, so I'd say an ORM is a tool that does some kind of _mapping_ between a relational and an object-oriented representation of data, including querying and modifications. Just writing the tables and columns as classes and types in another language, and using them to create SQL queries, doesn't yet count as an ORM. Your mileage may vary.
 
Here follows some explanations about [Amount of queries](#amount-of-queries), [Object identity](#object-identity), and [Managing object relationships](#managing-object-relationships), and how they manifest as problems. Feel free to point out any mistakes or misunderstandings I may have.
 
 
 
## Amount of queries
 
A notable part of ORMs is to represent relational data in memory as objects with relationships. For example, _employees_ which all belong to a single _department_. This representation is not only to represent data fetched from the database but also to query new data, which is the problem.
 
The relational model and the object model might look something like this:

```sql
CREATE TABLE department (
  id NUMBER NOT NULL PRIMARY KEY,
)
CREATE TABLE employee (
  id NUMBER NOT NULL PRIMARY KEY,
  name VARCHAR NOT NULL,
  department NUMBER NOT NULL FOREIGN KEY REFERENCES department(id)
)
```

```java
class Department {
  private Id<Department> id;
  private List<Employee> employees;
 
  List<Employee> getEmployees() { return employees; }
  void addEmployee(Employee e) { employees.add(e); }
}
class Employee {
  private Id<Employee> id;
  private String name;
  private Department department;
 
  String getName() { return name; }
  void setDepartment(Department d) { department = d; }
}
```
 
If I wish to get employee names from all departments to the UI, I would, in an ORM, do something like this (in more or less pseudo code):
```java
1) EntityManager em; //or whatever the interface to the ORM
2) List<Department> deps = em.getAll(Department.class);
3) List<Employee> emps = deps.flatMap(x -> x.getEmployees());
4) return employees.map(x -> x.getName());
```

How many queries are performed to the database?
The correct answer is ”not enough information” since it depends on how the relational model is mapped to the class structure.
 
The most obvious (and usually the best) configuration is to configure all relationships as lazily fetched, and everything else (that is, "ordinary data") as eagerly fetched (oddly, [Java Persistence API](https://en.wikibooks.org/wiki/Java_Persistence) decided to default to fetching to-one relationships eagerly). In this case on `line 2` a single query is made for all departments, and on `line 3` one query is made for each department to get its employees. On `line 4` no more queries would be made since employee names would be fetched already on `line 3`. So if there are 10 departments, this is 10+1 queries. If there are 100 departments, this is 100+1 queries.
 
This is called _n+1 queries_ and it's going to blow up when there are more departments. You can say ”hey, that code is easy to fix” but the problem is that in real life that object graph traversing is separated into multiple different functions each performing their own thing, and they cannot know when they are doing database fetches.
 
ORMs of course provide ways to avoid the problem. One way is to configure the fetching strategy for a relationship to be eager so that you can say that the employees of a department are always fetched from the database whenever the department data is fetched. But imagine the performance when there are departments with thousands of employees and your use case is only interested in the department data and not the employees.
 
This can be improved by providing different fetching strategies for different use cases, but since the mapping configuration is more or less static, you can’t handle different needs easily. Well, you can (for example by using annotations/metadata to specify different fetching strategies that can be enabled one way or another), but you need to fall back to using some kind of query language where you can specify how much data you want to fetch. And since you are falling back to a query language, why not just use a query language in the first place and forget about object graphs.

Imagine if you only wanted to print the number of employees for each department. You’d be performing the same amount of queries and still fetching half the database to memory for nothing. Some ORMs optimize for this by providing collection _proxies_, which they only populate with item references (proxies) without actual data. But it’s only a hack at best, and we get to step into the rabbit hole of proxies.
 
Another problem is that maybe you have pagination and you want to display only 50 employees at a time. But you can’t specify this in an object graph since all you are saying is `getEmployees()` and doing the pagination afterward. ORMs handle this by not fetching all employees in one query, but some configurable amount at a time. Again, the amount of actual queries (or physical database fetches of the result of a single query) depends on static configuration and you’d need to fall back to a query language to vary it for different use cases.
 
Even though ORMs provide these means to handle the problems, the biggest problem is that you’d have to know if, when, and how to use them. And since you don’t even know when actual queries are being performed in the first place, it’s practically impossible. At least I’m not smart enough for it. Modern computers are blazingly fast, so these problems are rarely visible with any ordinary test data, and thus they creep up in production or only manifest themselves as ”well, this app feels somewhat sluggish...”.
 
 
 
## Object identity
 
If you have an employee, what is its identity? When are two employees the same? How do you reference a specific employee?
 
In a relational database, the identity is defined by a key. In an object graph, the identity is defined by object equality. When using an ORM, these need to be in sync. Otherwise you'll run into weird problems, like objects disappearing when you fetch them from the database to a `Set`. 

When not using an ORM, these don't need to be in sync, since after the rows are retrieved from the database they are "just data" and don't represent particular database rows anymore. For example, it might be that `email` table in the database has duplicate email addresses for some reason (maybe the data comes from somewhere else, or maybe we know we are going to extend that table later). In our object model, however, it might be beneficial to define equality on our `Email` class by the address since obviously `foo@example.com` and `foo@example.com` are equal emails. But that would break our ORM.

You can of course keep `Email` class referencing the database row with database equality, and make an ordinary `EmailAddress` type with proper equality for the actual address column. This avoids the problem but results in a bit more awkward object model. Anyway, [equality is hard](https://www.craigstuntz.com/posts/2020-03-09-equality-is-hard.html) but ORMs certainly don't make it any easier.
 
What if you want to fetch objects that don't have an identity? This is quite common in a relational database. The ORM would have to support result objects _with_ identity and result objects _without_ identity. [Hibernate](https://hibernate.org) or _Java Persistence API_ doesn't, so apparently, it's not trivial to support for some reason. If you do `SELECT firstname, lastname FROM employees` you don't have any identifiers and easily get duplicate rows, which is fine until your ORM forces you to represent everything as objects with identity.
 
When you want to change the department of an employee, in the object model you'd probably say something like this:
```java
void updateDepartment(Id<Employee> empId, Id<Department> newDepId) {
  Employee emp = em.get(empId);
  emp.setDepartment(newDepId); // uh oh
}
```
but you can't since the object model expects actual departments, not just some identifiers that repsesent them. So you have to go and fetch the department from the database even though you don't actually need it:
```java
void updateDepartment(Id<Employee> empId, Id<Department> newDepId) {
  Employee emp = em.get(empId);
  Department dep = em.get(newDepId);
  emp.setDepartment(dep);
}
```
 
To handle this performance problem, some ORMs provide a way to fetch "a department which isn't actually a department but just looks like one" which doesn't need to go to the database when you already have its identifier. Now we are again in the rabbit hole of proxies since the department is now an instance of a proxy class that will work like a regular entity. To do that, it will fetch the data from the database when you call any of its methods. Thus we face again the problem where an innocent `department.getName()` method call might be making a database query, and with some imaginative eager fetch specifications, might even fetch half the database to memory.
 
There are [different kinds of proxying mechanisms](https://bravenewgeek.com/proxies-why-theyre-useful-and-how-theyre-implemented/). In one of them, the department object isn't an actual instance of a subclass of the `Department` class, but it's an instance of a proxy class inheriting from the `Department` class. Otherwise you can't see the difference, but when you use _inheritance_ (even though you probably should [favor composition over inheritance](https://en.wikipedia.org/wiki/Composition_over_inheritance)) and you know from context that your department happens to be an instance of a `ProfitableDepartment` instead of a  `ManagementDepartment` ;)
```java
Department dep = em.getWithoutGoingToDatabase(depId);
ProfitableDepartment proDep = (ProfitableDepartment)dep; // uh oh
```
The cast blows up. Of course it does, since the proxy cannot know the actual subclass without visiting the database at some point. But who knows if it checks it from the database at some method invocation via things like [load-time weaving](https://www.baeldung.com/aspectj#load-time-weaving) or [compile-time weaving](https://www.baeldung.com/aspectj#compile-time-weaving)? Can that happen also on a cast attempt? Who knows what [magic your ORM is using](http://blog.dataobjects.net/2009/09/materializing-entities-with-unknown.html)? Who knows which kind of mechanisms the programming language even provides? It would be simpler to just not cast objects to subclasses, but then we lose one common aspect of object orientation.
 
What if you have a department proxy (like from a lazily fetched collection from `employee.getDepartment()`) and you only need to get its identifier for example to return to the UI as a reference? If you call any of the department's methods, the ORM is going the get all its data (probably including all eagerly fetched relationships). But since the proxy already knows the identifier, you wouldn't need to visit the database at all. Some ORMs optimize this so that if they know you are invoking the method returning the identifier, they won't populate the proxy. But to avoid writing useless getters and setters for everything and keeping the object interface to yourself and not the ORM implementation, you'd probably want to use field access by default (meaning that ORM populates field contents directly, and does not need you to define setter methods), which has a side effect that the ORM doesn't know anymore that the `getId()` method will only get the identifier. Populating the proxy would have to trigger on field access and not on any method access, but who knows if your programming language even supports something like that? This can be hacked at least in Hibernate by specifying field access by default and property access just for the identifier property, but the codebase just got even more complicated. 
 
You can try to always use the whole `Department` instance in code instead of its identifier. Like, change the `updateDepartment` method to:
```java
void updateDepartment(Employee empId, Department newDepId) {
  ...
}
```
But then you are using proxies all the time since otherwise everything would need to be fetched from the database every time only the reference is needed. If you do this, it would also be natural to return whole Departments instead of their identifiers and other values:
```java
Department getDepartment(Department depId) {
...
}
```
But then you run into problems with transaction boundaries. The UI can print out the department's identifier (even if it happens to be a proxy), and the name (if it's an actual instance), but the moment it tries to call its `getEmployees()` method it blows up because the database transaction isn't open anymore. This is because you shouldn't keep it open during the rendering of the result - at least for modifying transactions or if your database is not [MVCC](https://en.wikipedia.org/wiki/Multiversion_concurrency_control) - or you'll run into problems.
 
So, is it better to always use `Id<Department>` or `Department` for referencing the identity? There's no simple answer because I think `Id<Department>` would be strictly better but it's not compatible with the approach of representing the data as an object graph, which was the main point of using an ORM in the first place.
 
 
 
## Managing object relationships
 
Most likely the model discussed here would be stored in a relational database so that the employee table has a column with an id of a department, and the department table knows nothing about the employees referencing it. This is a sensible way to persist and query the data. But in object graphs, the sensible thing is to be able to traverse relationships in both directions by just following references.
 
If you update the department of an employee by saying `employee.setDepartment(newDepartment)`, the modification is probably going to happen as was intended, but what if you say:
`department.addEmployee(newEmployee);`? Is the change going to be persisted?

Probably not, since the ORM would need to implement behind the scenes some List-like collection which understood that additions and removals need to be handled with separate updates to another database table. Who knows if your ORM does this?

What if I'm already doing something with an instance of employees collection of a department, and I then set the department of one of the employees to something else:
```java
for (Employee emp: department.getEmployees())
    emp.setDepartment(anotherDepartment);
}
```

For the object model to remain internally consistent the employee would suddenly need to disappear from the collection, and now we are in the rabbit hole of concurrency and concurrent modifications to a collection possibly under iteration. Let's not go there.
 
Since the ORMs don't do this (at least I think none do), you could implement `setDepartment` and `addEmployee` methods yourself correctly so that they always work. You'd need the `getEmployees()` method to always return either an immutable or some [copy-on-write](https://en.wikipedia.org/wiki/Copy-on-write) collection, so it's not going to be 100% in sync. Also, if you happen to make copies, they won't be updated, but hey, it's at least almost perfect, right? Maybe, but no one's going to implement that since it's just too complex. Easier to just forbid add/remove methods and handle the relationship from the single side (`setDepartment`). And thus we've lost another part of our clean object model.
 
There's still the problem of keeping the sides in sync, though. And the results aren't even (locally) deterministic. If you set the department of an employee via `employee.setDepartment(newDep)`, and after that call `department.getEmployees()`, the new employee is going to be found in the collection
- unless the employees were configured to be eagerly fetched
  - in which case the collection was already populated when the department was fetched, and won't be re-populated automatically
- unless the code in the previous lines (or the previous functions) had already called `department.getEmployees()` at least once
  - in which case the collection was already populated before the modification, and will be returned in the original state
- unless some earlier code within the same session (~transaction) had already called `getEmployess()` -method of the same department which might have been a different department object retrieved from `em.get(depId)` but which at least Hibernate caches in memory and returns the same object instance on subsequent calls within the same transaction
  - thus making the collection already populated even though the code looks like everything was directly fetched from the database
 
Who's going to be able to spot this kind of problem in an actual code base with actual business logic everywhere? Who even knows if your particular ORM happens to work exactly like this?
Not me.
 
 
 
 
## Does this all sound overly complex?
 
That's because it is. There's a simple solution not to solve these problems, but to get rid of them completely: **Don't use an ORM**.

You can still use an ORM tool as long as you just avoid its ORM parts. For example, your ORM probably offers a DSL to construct type-safe queries ([LINQ](https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/concepts/linq/) or [JPA Criteria API](https://en.wikibooks.org/wiki/Java_Persistence/Criteria) for example). Using it doesn't yet create these problems because it's about constructing a specific query returning a result, and the objects don't need to have anything to do with ORMs.
 
In my current project, we are using Java Hibernate, which is an ORM. Our entities don't have any methods to return other entities. Our department wouldn't have a `getEmployees()` method. We can do the same thing with a thin query library on top of the Hibernate/JPA, so that this:
```java
List<Employee> emps = department.getEmployees();
```
would look like this:
```java
Collection<Employee> emps = dao.getMany(query.related(department, Department_.employees));
```
It makes performing queries just as easy, but explicit. And it completely avoids both n+1 and relationship problems. The amount of actual queries in more complex cases may be more than one, but it's still statically determined from the structure of the code and doesn't demend on the amount of data. This is even better typed since it returns a Collections instead of an (ordered) List since we didn't give an explicit ordering for the query.
 
We can just as easily do projections instead of fetching the whole employees:
```java
Collection<String> emps = dao.getMany(query.related(department, Department_.employees), Project.value(Employee_.name));
```
because we are just constructing a query and not trying to interpret an object graph. Easy projections are still - as far as I know - an unsolved problem in ORMs.
 
We can use `Id<Department>` for referencing the identity everywhere since we aren't pretending to be dealing with an object graph, except we still need to fetch the actual entity for updates - like `employee.setDepartment(actualDepartmentOrProxy)` - since that's how Hibernate works. But single-table updates are easier by modifying an object instead of creating SQL updates, and most of our entities are immutable anyway, so I can live with this tradeoff.
 
 
 
## So my advice,

if You decide to take it into account:
- don't use an ORM
  - In my current Java project, we use Hibernate, but something like [jOOQ](http://www.jooq.org) would probably be a lot better, and a lot less of an ORM.
- think [database first](https://blog.jooq.org/2018/06/06/truth-first-or-why-you-should-mostly-implement-database-first-designs/)
  - design your database in SQL, and make your Java/C#/etc tool understand that. Not the other way round. This also applies to migrations where (in Java) something like [DBMaintain](http://www.dbmaintain.org) or [Flyway](https://flywaydb.org) are nice tools.
- use a tool to represent database concepts (tables, views, functions, types...) in Java/C#/whatever structures
  - Hibernate has wide support for mapping different kinds of structures to Java code. Some tools may provide more, some less.
- use a tool to handle serialization/deserialization of types to and from the database to avoid [primitive obsession](https://dev.solita.fi/2013/03/01/refactoring-primitive-obsession.html)
  - an email is an Email, not a String.
  - Hibernate has good support for typing parameters and return values including multicolumn values. But this is not the most difficult problem, so other tools are probably just as good.
- use a tool to construct type-safe queries which produce type-safe results
  - you can use a thin wrapper like [query-utils](http://github.com/solita/query-utils/) on top of Hibernate/JPA, but something like jOOQ would probably be better.
- if and when you need to fall back to native SQL queries, make the parameters and return values type-safe
  - possibly with an interface like [this](https://github.com/solita/query-utils/blob/master/src/main/java/fi/solita/utils/query/generation/NativeQuery.java) unless the tool you use already provides a better one (Hibernate doesn't).
- if an ORM tool is best for you (or some "senior" made the decision for you), avoid its ORM features as much as possible
  - you can use the type system or unit tests to make sure you aren't "breaking the rules", like implementing a method in an entity that would return entities.
