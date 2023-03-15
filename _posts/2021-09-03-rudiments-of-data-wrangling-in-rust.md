---
layout: post
title: Rudiments of Data Wrangling in Rust
author: jerekapyaho
excerpt: > 
  The Rust programming language is typically positioned 
  for systems programming, but there is nothing stopping us from
  enjoying it for basic data wrangling tasks like those often done in Python.
tags:
 - Rust
 - Data
 - Programming
---

The [Rust](https://www.rust-lang.org) programming 
language has many advantages over 
its contemporary popular alternatives: memory safety, 
static typing with powerful type inference, algebraic data 
types, fearless concurrency, a friendly community, and 
the list goes on.

Rust is typically positioned as a language for "systems programming",
which usually means something rather close to the operating system,
such as networking or device drivers.
However, Rust is a general-purpose programming language, and nothing is 
stopping you from using it for tasks that often are done in
Python.

Since I started really diving into Rust in the spring of 2021, I've
gradually become more fluent with it, to the extent that I can now
create some utilities in Rust in many situations where I would normally 
reach for Python.

In this blog post I would like to demonstrate the potential of Rust
by presenting my solution to a quick (and maybe a little dirty) 
data wrangling task. It involves reading and parsing a large CSV file, 
and then extracting rows that meet certain criteria. It's nothing 
that couldn't be done in Python, or even with a shell script in Unix,
but I hope it serves as an example of how these kinds of common 
tasks could be done in Rust, and as a basis for extension.

The Rust program presented here can be found on 
[GitHub](https://github.com/solita-jereka/vehicles-rs), so that
you can clone it or fork it, run it on your own machine and experiment
further.

## Some basic Rust knowledge

If you haven't already picked up the basics of Rust programming, I'd
recommend to have a look at the 
[Getting Started](https://www.rust-lang.org/learn/get-started) section of the Rust
website. That will give you the information about how to download
the necessary tools, and how to compile and run the Rust version 
of the traditional first "Hello, world!" program.

To learn a little more of the Rust language, the canonical book 
["The Rust Programming Language"](https://doc.rust-lang.org/book/)
(often know just as "the book")
is almost mandatory reading. Rust has many characteristics that 
are somewhat familiar to anyone who has programmed in Java, C#, 
C++, or Python, but it also has many unique features borrowed 
from slightly less mainstream programming languages, for a good 
reason.

![Rudiments of the Rust programming language (actually named after a fungus)](/img/rudiments-of-data-wrangling-in-rust/rusty-chain.jpg)

*Photo by <a href="https://unsplash.com/@zmachacek?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText" target="_blank">Zdeněk Macháček</a> on <a href="https://unsplash.com/s/photos/rust?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText" target="_blank">Unsplash</a>*

The most challenging part of learning Rust is its memory management,
which is based on tracking ownership and strict control over memory
access, but doesn't have garbage collection like Java or Go. The Rust
compiler has a feature called "the borrow checker", which is responsible
for this control, so that Rust programs are as safe as possible at 
runtime.

Newcomers to Rust often find themselves initially fighting 
the borrow checker, but once they get familiar with the rules, that
changes into being grateful for yet another runtime disaster averted!

The three phases of dealing with the Rust borrow checker, based on 
the author's personal experience:

1. Why the &%$! can't I do that?!
2. Oh, I kind of see why that would be a problem.
3. Thank you, borrow checker, for looking after my code!

## Embrace the crates

Every Rust program and library is packaged into a 
[crate](https://doc.rust-lang.org/book/ch07-01-packages-and-crates.html), 
which can refer to and depend on other crates. While Rust
has a sizable [standard library](https://doc.rust-lang.org/std/), many interesting tasks
can be achieved when you start taking advantage of the work
that others have done.

The [Cargo](https://doc.rust-lang.org/cargo/) tool is an essential part of the Rust tooling,
and it is also responsible for resolving crate dependencies.
Once you indicate in your program's `Cargo.toml` file that
you would like to include a crate, Cargo picks it up,
downloads it from the [crates.io](https://crates.io) registry, and compiles it 
into your program.

Many of the tasks in the small Rust program you are about to see
are actually dependent on functionality found in crates
such as the following:

* [csv](https://crates.io/crates/csv) -- reading and writing CSV files
* [encoding_rs](https://crates.io/crates/encoding_rs) -- implementation of the Encoding Standard
* [encoding_rs_io](https://crates.io/crates/encoding_rs_io) -- transcoding from non-UTF-8 encoded content
* [chrono](https://crates.io/crates/chrono) -- manipulating dates and times

Some tasks like opening files, handling command-line arguments,
and using data structures, remain the responsilibity of
the Rust standard library. For more extensive handling of
command-line arguments, take a look at [`clap`](https://github.com/clap-rs/clap) or [`structopt`](https://docs.rs/structopt/0.3.23/structopt/).

Now, let's set the stage for the data wrangling.

## Counting electric vehicle registrations

Electric vehicles are rapidly becoming more common, and the pace will
only pick up as we try to meet ambitious climate preservation goals
also in Finland. I thought it would be interesting to know exactly 
how quickly EVs have become more popular here in the recent years.

![Electric vehicles](/img/rudiments-of-data-wrangling-in-rust/electric-vehicles.jpg)

*Photo by <a href="https://unsplash.com/@michaelfousert?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText" target="_blank">Michael Fousert</a> on <a href="https://unsplash.com/s/photos/electric-vehicles?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText" target="_blank">Unsplash</a>*

[Traficom](https://www.traficom.fi/en/) (Finnish Transport and Communications Agency) regularly
publishes information about registered vehicles in active use, 
as downloadable [open data](https://www.traficom.fi/en/news/open-data?toggle=Open%20data%20for%20vehicles%20version%205.14). This data includes the driving power of 
the vehicle, its type and first registration date, and many other
data points.

The data is in CSV format, and it is accompanied by a Microsoft Excel
spreadsheet with descriptions of the data fields. The latest iteration
of the CSV file, published in March 2021, has over five million rows,
and it includes all land vehicles (cars, buses, tractors etc.)

## Reading CSV files in Rust

The `csv` crate contains structs with functions to read and write CSV
files, although we only use the reading part in this program.

The CSV data file we use requires some special handling. Instead of
a comma, it uses the semicolon as the field delimiter. Also, the text
in the file is encoded in ISO 8859-1. The default settings of the 
CSV reader in the csv crate expect comma-delimited files with text
encoded in UTF-8 (which is the internal representation of Rust strings).

To convert the lines in the CSV file from ISO 8859-1 to UTF-8 we use the
`encoding_rs` and `encoding_rs_io` crates, which implement 
the [Encoding Standard](https://encoding.spec.whatwg.org). 
In their documentation you can also find a link to 
an interesting long-form article which also tells you why ISO 8859-1 
is treated as Windows code page 1252.
(This conversion would not be needed if the source data were already 
in UTF-8, like it should be.)

In this case it means that we need one extra step to construct 
our CSV reader from a transcoding reader supplied by the `encoding_rs_io`
crate:

    let file = File::open(filename)?;

    let transcoded_reader = DecodeReaderBytesBuilder::new()
        .encoding(Some(WINDOWS_1252))
        .build(file);

    let mut reader = csv::ReaderBuilder::new()
        .has_headers(true)
        .delimiter(b';')
        .from_reader(transcoded_reader);

We also told `csv::ReaderBuilder` that the first line of our CSV
file is the header, and the field delimiter is the semicolon
character.

## Processing the CSV records

Once we have our reader, we can start preparing to read the lines.
From the reader we get an iterator which returns values of type
`Result<csv::StringRecord, std::error::Error>`. Each `StringRecord`
is essentially a vector of `String` values, representing all the
fields. The delimiters and possible surrounding quotes are
discarded.

I'm interested in electric vehicle registrations of the last five
years, from 2016 to 2020. This can be expressed as a Rust 
[range](https://doc.rust-lang.org/reference/expressions/range-expr.html):

    let year_range = 2016..=2020;

I also need a counter that saves the number of EV registrations
for each of these years. The `HashMap` struct in the Rust standard 
library is suitable for this purpose, so let's make one, with the
years as keys, and the counts as values:

    let mut registrations = HashMap::<i32, u32>::new();

This `HashMap` is mutable because we want to change its contents
as we read in the lines from the CSV files. The default inferred
type for integer literals in Rust is `u32`, but the type of the key
is `i32` because that is also the type of the year in the date
manipulation code found in the `chrono` crate, as you'll see soon.

## Enumerated type detour

While algebraic data types (as found in functional programming
languages like [Haskell](https://www.haskell.org) and 
[F#](https://fsharp.org)) are one of the distinctive features 
of Rust, in this program I mainly used plain vanilla enumerated types
to express the content of some of the data fields in the CSV file.

I'm interested in the registrations of electric vehicles,
and I was able to see from the Excel file accompanying the data
that the driving power of a vehicle is encoded as a string with
values like "01", "02", "03" etc. The value for electricity is "04".
Rather than convert these into actual numbers, we can introduce
an enumerated type:

    enum DrivingPower {
        Petrol,
        DieselFuel,
        FuelOil,
        Electricity,
        Hydrogen,
        Gas,
        Methanol,
        BiodieselFuel,
    }

This type has a couple of more values than we need here (and this
is not even exhaustive (pun not intended)), but this
is for illustration and future use.

To be able to use this enum while processing the CSV records,
we define a function that can convert the symbolic values into the
actual strings found in the CSV field:

    impl DrivingPower {
        fn as_str(&self) -> &'static str {
            match *self {
                DrivingPower::Petrol => "01",
                DrivingPower::DieselFuel => "02",
                DrivingPower::FuelOil => "03",
                DrivingPower::Electricity => "04",
                DrivingPower::Hydrogen => "05",
                DrivingPower::Gas => "06",
                DrivingPower::Methanol => "07",
                DrivingPower::BiodieselFuel => "08",
            }
        }
    }

Here you can see another distinctive feature of Rust, namely
the `match` statement. You can use it to do a lot more than
just match the values of an enum.

Since the CSV file has entries for many types of vehicles,
I have introduced another enumerated type, `VehicleKind`,
which provides a similar mapping to the vehicle codes.
Here I'm only interested in "M1" and "M1G" types of vehicles.

    enum VehicleKind {
        Car1,
        Car2,
    }

    impl VehicleKind {
        fn as_str(&self) -> &'static str {
            match *self {
                VehicleKind::Car1 => "M1",
                VehicleKind::Car2 => "M1G",
            }
        }
    }

## Some helper functions

Rust is not an object-oriented language, and you can use free
functions instead of methods to package up computations.
In this program, the CSV records are meaningful only if they
describe a vehicle of type "M1" or "M1G", and the driving
power of the vehicle is electricity, or "04".

With the `DrivingPower` and `VehicleKind` enums defined, I could
write two predicate functions that return `true` or `false`
depending on whether the vehicle is a car or not, and whether
its driving power is electricity or not:

    fn is_car(record: &csv::StringRecord) -> bool {
        let field = &record[Field::VehicleKind as usize];
        field == VehicleKind::Car1.as_str() || field == VehicleKind::Car2.as_str()
    }

    fn is_electric(record: &csv::StringRecord) -> bool {
        let field = &record[Field::DrivingPower as usize];
        field == DrivingPower::Electricity.as_str()
    }

These functions rely on yet another enumerated type, `Field`,
which tells you the index of the corresponding field in
the `StringRecord` vector. In this case, the vehicle kind
is the first field (index is zero), while the driving power
is the 19th field (index is 18) in the record vector.
However, you can only index vectors using the `usize` type,
so I cast the enum values with `as usize` when I use them.

Functions in Rust can have an implicit return type. If there
is no return statement in the function, the last expression
becomes the return value of the function. That is also why
there is no semicolon at the end of the last line of the
function. Only statements end with a semicolon; expressions 
do not.

## Iterating over the records

With these preparations in place I can finally start 
iterating over the five million plus records in the CSV file.
The call to `reader.records()` produces an iterator which I
consume using a `for` loop. Inside the loop I get each record,
skimping a bit on the error handling (assuming in good faith
that the CSV file is well-formed):

    let mut electric_car_count = 0;
    let mut total_car_count = 0;

    for result in reader.records() {
        let record = result?;

        if !is_car(&record) {
            continue;
        }

        total_car_count += 1;

        if !is_electric(&record) {
            continue;
        }

        electric_car_count += 1;

        // ...

    }
    
I'm only interested in cars, so a record is only processed
if it passes the `is_car` predicate test. Similarly, even if 
the record describes a car, but doesn't pass the `is_electric`
predicate test, I discard it by moving to the next record
with the `continue` statement.

At this point I'm confident that I have a record that describes
an electric car, so I get the first registration date field
and parse it into a date:

    let field = &record[Field::FirstRegistrationDate as usize];
    let reg_date = NaiveDate::parse_from_str(field, "%Y-%m-%d");

I know from the data description that the registration dates
are in the form `YYYY-mm-dd`, so I use that to parse the field
into a "naïve" date using the data structure and related
functionality found in the `chrono` crate.

## Match for success or error

Now it's time for a more refined use of Rust's `match` statement.
Something could go wrong when parsing the first registration
date, and we need to deal with it. Rust has no exception handling,
but errors will still happen, and they are dealt with returning
a value of type `Result`, which is an algebraic data type with two
variants: `Ok` and `Err`.

If everything went well, you get an `Ok` with the parsed date,
and if something goes wrong, you get an `Err` with the error information.
This is how I deal with it in the program:

    match reg_date {
        Ok(d) => {
            let year = d.year();
            if year_range.contains(&year) {
                let count = registrations.entry(year).or_insert(0);
                *count += 1;
            }        
        },
        Err(e) => {
            eprintln!("CSV parsing error: {}", e);
            continue;
        },
    }

If there was no error in parsing, I have a `chrono::NaiveDate` 
with a year which might be one that I'm interested in. If 
there was an error (and in the current CSV file there were a few
records with bad dates), I print it out and move on to the 
next record, because that is an anomaly that doesn't affect 
the end result.

You can see that the match statement has two arms, one for `Ok` and
another one for `Err`, both with an associated value that can be
used in the block following the `=>` operator.

## Using the HashMap as a counter

The [`HashMap`](https://doc.rust-lang.org/std/collections/struct.HashMap.html) 
data structure in the Rust standard library can be
used for many different purposes, much like a Python `dict`. 
It is generic in terms of both the key and value, so you can 
use a suitable type as the key, and maybe use a vector as the 
value, to be able to store many values with the same key.

In this program I'm only storing simple counts as `u32` values,
keyed by the year of their occurrence, but I need to handle 
two cases:

- When there already is an entry in the hashmap for some year,
and I need to increase the count by one, and;
- When there is no entry for some year, and I need to set it up
from scratch.

Using the `HashMap` struct I can do both with two statements:

    let count = registrations.entry(year).or_insert(0);
    *count += 1;

The first statement gets a reference to the count, and the second
statement dereferences it, to increase its value by one. You can
read the first statement as "give me the entry, or else insert a
zero as its value".

Note that in order to do this, the hashmap needs to be declared
as mutable, like I did:

    let mut registrations = HashMap::<i32, u32>::new();

## Print out the results

Now that I've iterated through all the records in the CSV file,
I should have the first registration counts of all electric
cars from the years 2016 to 2020 inclusive in the hashmap,
so I can now proceed to print them in the console.

Rust uses the `println!` macro for printing. The exclamation
mark tells you without a doubt that this is a macro invocation.
Rust macros reduce boilerplate code in many
common situations. For example, initializing a vector with
the `vec!` macro lets you focus on the initial contents instead
of the code that allocates memory and adds each individual 
element.

The `println!` macro also takes care of formatting the data.
You can let Rust print a value like it pleases, but you can
also utilize the comprehensive formatting templates (also used
by the `format!` macro).

Since I stored the range of the interesting years earlier,
I can use it when I present the results. First I print out a
heading:

    println!("EV registrations {}-{} by year:", 
        year_range.start(), year_range.end());

Then, because I'm confident that I have an entry in the hashmap
for each of the years (remember, if there wasn't already an entry,
I made one, and initialized it to zero), I can just loop through
the range and print out the result for each year.

    for year in year_range {
        println!("{:>5}: {:>5}", 
            year, registrations.get(&year).unwrap());
    }

Getting an entry from the hashmap can fail, but in this case 
I just use the common Rust technique of "unwrapping" the result.
Keep in mind that if you're not writing a quick and dirty utility
like this one, unwrapping is not the best thing to do, because
failure will cause the program to panic. Using unwrap is somewhat
opinion-based, but in a case like this I think it can be justified.

Finally, I can print the total number.

    println!("Total: {:>5}", electric_car_count);

Just by eyeballing the numbers you can see that the growth 
in EV registrations has been quite rapid. I could have also 
computed the count while printing out the results, instead
of collecting it as I progressed through the records.

## There's plenty more where that came from

This has been a whirlwind tour of some common real-world tasks
involved in writing a Rust program. However, even in this small
program there are many Rust features that I was not able to
explain in depth, such as borrowing. (Even lifetimes already made a 
brief appearance!)

Also, you could easily add a visualization of the registration
counts using the [`plotters`](https://crates.io/crates/plotters) crate, and extend the analysis of the
vehicle data using the [`ndarray`](https://crates.io/crates/ndarray) crate.

As for performance, it would be interesting to compare
this program and an equivalent Python solution in terms
of speed, but also in terms of ergonomics. When you're first
starting out with any programming language it takes a lot
of time to look things up and assemble the parts to a 
working whole. With Rust the learning curve can be steep,
but I think it's time well invested.

Here are the three biggest takeaways for anyone considering
a deeper dive into Rust:

* The borrow checker is your friend.
* Embrace the crates.
* Algebraic data types FTW!

Hope you enjoy wrangling data, or anything else, in Rust!

See also: [Enforcing Database Transactions with Rust](https://dev.solita.fi/2019/11/21/enforcing-database-transactions-with-rust.html)
