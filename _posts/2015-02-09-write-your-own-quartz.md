---
layout: post
title: "Write Your Own Quartz!"
author: orfjackal
excerpt: "Quartz is probably the most popular scheduler library for Java and you should not use it."
---

[Quartz](http://quartz-scheduler.org/) is probably the most popular scheduler library for Java and you **should not use it**.

(1) *Quartz is more complex and has more features than any single project needs.* This accidental complexity will make it harder to customize Quartz to fit the specialized needs of a demanding project, where there will always be some feature you need which the framework doesn't provide out of the box. This is further complicated by the fact that...

(2) *Using Quartz makes your code untestable,* because Quartz's codebase is scattered with calls to `System.currentTimeMillis()` and `new Date()` without providing any hooks for faking the current time (unlike for example [Joda-Time provides](http://www.joda.org/joda-time/apidocs/org/joda/time/DateTimeUtils.html)). This means that you won't be able to test that what happens to your application during daylight saving time (DST) transitions, leap days, leap seconds and other date & time weirdness (BTW, Quartz may [run a job 0 or 2 times when DST starts or ends](http://quartz-scheduler.org/documentation/faq#FAQ-daylightSavings)).

I've used [JMockit](http://jmockit.github.io/) to fake `System.currentTimeMillis()` just to be able to test some code that uses Quartz. You don't want to go there...

![I've seen the end... no one was spared, not even the children](/img/write-your-own-quartz/ive-seen-the-end.jpg)


## What To Do Instead

If your needs are simple enough that [Spring's built-in task scheduling](http://spring.io/guides/gs/scheduling-tasks/) works for you, use it. If you have so specialized scheduling needs that it's not enough, you should probably write your own scheduler, because ["if it's a core business function – do it yourself, no matter what."](http://www.joelonsoftware.com/articles/fog0000000007.html)

In one of my projects this was the case; the program's core feature was parameterizing and scheduling batch jobs. Originally we used Quartz, "because code reuse is good," but through the years we had death by 1000 papercuts because of Quartz-related complications. Eventually I wrote my own scheduler that did exactly what we needed and worked in a server cluster; it took only 30 hours to make, much less than we had wasted time banging our heads against Quartz's idiosyncrasies.

Because that new scheduler is highly specialized to that project's needs, releasing it as open source won't make sense, but here is some taste of what it's like and ideas for implementing your own.


### Pass the Current Time to Every Method

Testing the new scheduler is really simple, because every method which uses the current time takes it as an explicit method parameter. Here is a snippet of the high-level tests:

```java
private static final LocalDateTime NOW = new LocalDateTime(2000, 1, 1, 0, 0);

private final TimerSpy spy = new TimerSpy();
private final Logger logger = mock(Logger.class);
private final Scheduler scheduler = new Scheduler(new InMemoryScheduledTasks(), logger);

@Test
public void when_scheduled_in_the_future_then_does_not_yet_trigger_it() {
    scheduler.schedule(NOW, "the message", new FixedRhythm(NOW.plusSeconds(1)));

    scheduler.triggerExpiredTasks(NOW, spy);

    assertThat(spy.triggered, is(empty()));
}

@Test
public void when_scheduled_now_then_triggers_it() {
    scheduler.schedule(NOW, "the message", new FixedRhythm(NOW));

    scheduler.triggerExpiredTasks(NOW, spy);

    assertThat(spy.triggered, is(asList("the message")));
}

@Test
public void when_scheduled_in_the_past_then_triggers_it() {
    scheduler.schedule(NOW, "the message", new FixedRhythm(NOW.minusSeconds(1)));

    scheduler.triggerExpiredTasks(NOW, spy);

    assertThat(spy.triggered, is(asList("the message")));
}

@Test
public void triggers_expired_tasks_ordered_by_scheduled_time() {
    scheduler.schedule(NOW, "message 2", new FixedRhythm(NOW));
    scheduler.schedule(NOW, "message 1", new FixedRhythm(NOW.minusDays(1)));
    scheduler.schedule(NOW, "message 3", new FixedRhythm(NOW));

    scheduler.triggerExpiredTasks(NOW, spy);

    assertThat(spy.triggered, is(asList("message 1", "message 2", "message 3")));
}
```

Unit tests for all the various scheduling strategies are equally easy to write:

```java
private static final LocalDateTime NOW = new LocalDateTime(2000, 1, 1, 0, 0);

@Test
public void every_second_day() {
    CronRhythm rhythm = new CronRhythm("0 0 0 */2 * ?");

    assertThat(Rhythms.take(3, NOW, rhythm), is(asList(NOW, NOW.plusDays(2), NOW.plusDays(4))));
}
```

The above mentioned `CronRhythm` class uses internally Quartz's `CronExpression` class for parsing the cron expressions (which would otherwise be really complicated to parse), but we force it to make all calculations in the UTC timezone to avoid DST problems.

Speaking of DST problems, they are now really easy to unit test:

```java
@Test
public void daylight_saving_time_will_not_cause_skipped_beats_nor_duplicate_beats() {
    // in Finland, summer time starts 2014-03-30 and ends 2014-10-26
    // http://fi.wikipedia.org/wiki/Kes%C3%A4aika
    CronRhythm everyDayAt0330 = new CronRhythm("0 30 3 * * ?");

    assertThat(Rhythms.take(3, new LocalDateTime(2014, 3, 29, 0, 0), everyDayAt0330), is(asList(
            new LocalDateTime(2014, 3, 29, 3, 30),
            new LocalDateTime(2014, 3, 30, 3, 30), // Spring DST transition at 3:00 -> 4:00
            new LocalDateTime(2014, 3, 31, 3, 30))
    ));
    assertThat(Rhythms.take(3, new LocalDateTime(2014, 10, 25, 0, 0), everyDayAt0330), is(asList(
            new LocalDateTime(2014, 10, 25, 3, 30),
            new LocalDateTime(2014, 10, 26, 3, 30), // Autumn DST transition at 4:00 -> 3:00
            new LocalDateTime(2014, 10, 27, 3, 30))
    ));
}
```


### Composition

When we used Quartz, the last straw that broke the camel's back was trying to customize its [triggers](http://quartz-scheduler.org/documentation/quartz-2.2.x/tutorials/tutorial-lesson-02). Quartz contains support for "calendars" which can be used to say that on which days a job should not be executed. But in our application it was not acceptable to skip executing a job (on public holidays and Sundays), but instead it should be rescheduled to be executed on the next weekday that is not a holiday. When scheduling is a core business function, it's inevitable that you'll encounter specialized needs that no ready-made product was designed for.

We wanted to be able to compose triggers, so that we'll wrap Quartz's `CronTrigger` into a custom trigger that will take care of that postponing of job executions, but Quartz's `OperableTrigger` interface is huge (39 methods) and stateful, which makes it really hard to implement custom triggers. We were not able to implement a [bug-free](http://www.jamesshore.com/Agile-Book/no_bugs.html) version of our composed trigger.

With the new scheduler, we were able to design a simple interface for the triggers (we call them rhythms) so that all of the implementations can focus on a single thing and are immutable:

```java
public interface Rhythm {

    LocalDateTime firstBeat(LocalDateTime now);

    @Nullable
    LocalDateTime nextBeatAfter(LocalDateTime now);
}
```

With an API like this, composition is easy to implement and use:

```java
Rhythm rhythm = new HolidayAwareRhythm(new CronRhythm("0 0 12 * * ?"), holidays);
scheduler.schedule(now, message, rhythm);
```


### Clustering

One important motivation for using Quartz is that it can be run in a server cluster (e.g. duplicate servers for failover) and Quartz will take care of running each job only once, on just one of the machines. But implementing clustering for high availability isn't actually that hard to do.

In the case of this project, there are only some hundreds of scheduled jobs and they are typically executed at most once per day, so we can use a simple strategy of periodically polling the database to find expired tasks. We use the `SELECT FOR UPDATE` statement to make sure that only one of the servers will process an expired task:

```sql
SELECT task_id, message, scheduled_time, rhythm
FROM scheduled_tasks
WHERE scheduled_time <= :now
ORDER BY scheduled_time ASC
FOR UPDATE
```

Inside the same transaction we will also process the expired task and reschedule the next execution, and the database will take care of it happening atomically only once.


## Summary

If your scheduling needs are so demanding that you're considering using Quartz, it's better to write your own scheduler that is specialized to fit your needs. Otherwise the additional complexity of Quartz's features which you don't need would weight you down, and you would have a hard time trying to bend Quartz to do the last few features which you need but Quartz doesn't provide.
