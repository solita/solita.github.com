---
layout: post
title: "CodeSOD: Single Threaded Triggerable Worker"
author: orfjackal
excerpt: "Code snippet of the day: A simple concurrency utility class for ensuring that a background task is triggered when there is some data to process, but without triggering it unnecessarily many times."
---

Many projects need background tasks that must be run when there is some data to process. For simplicity that task will run in a single thread and when it is started, it will process all data that is then available. For good latency we will want to run that task as soon as we know there is some work to do, for example in the [after-commit hook](http://docs.spring.io/spring/docs/current/javadoc-api/org/springframework/transaction/support/TransactionSynchronizationManager.html#registerSynchronization-org.springframework.transaction.support.TransactionSynchronization-) of the transaction which wrote some data to be processed.

This is complicated by the fact that there are potentially lots of events which will trigger running the task and because every execution of the task will process all available data in a single batch (which is often faster than processing each event individually), we don't want to execute the task unnecessarily (e.g. thousands of enqueued executions even though all data is already processed).

Here is a walkthrough of a utility class that has proved to be useful in multiple projects and use cases. In one project the use case was updating a Lucene search index after new data is written to the database. In another project the use case was making some HTTP requests to external systems after some jobs are created (written to database) by a scheduler or user.

The full code is available in [SingleThreadedTriggerableWorker.java](/img/single-threaded-triggerable-worker/SingleThreadedTriggerableWorker.java) and [SingleThreadedTriggerableWorkerTest.java](/img/single-threaded-triggerable-worker/SingleThreadedTriggerableWorkerTest.java). Maybe some day they will be moved to a library, but for now you can just copy them and modify them for your specialized needs.

The test names/specification is:

- runs the task when triggered
- runs the task when triggered after the task is finished
- runs the task when triggered while the task is running
- runs the task only once when triggered multiple times while the task is running
- on shutdown waits for running tasks to finish
- on shutdown throws exception if tasks did not finish within timeout

The implementation uses a neat pattern which handles the concurrency issues in a simple and reliable manner:

```java
private final ExecutorService workerThread = Executors.newSingleThreadExecutor();
private final BlockingDeque<Runnable> triggerableTasks = new LinkedBlockingDeque<>();

public SingleThreadedTriggerableWorker(Runnable task) {
    triggerableTasks.add(task);
}

public void trigger() {
    final Runnable task = triggerableTasks.poll();
    if (task != null) {
        workerThread.execute(new Runnable() {
            @Override
            public void run() {
                triggerableTasks.add(task);
                task.run();
            }
        });
    }
}
```

To avoid the task from being triggered more than once, we keep a reserve of task instances in `triggerableTasks` and we return the task to the reserve just before executing it. This gives us the desired property of allowing the task to be triggered while the previous task is running, but limiting the number of enqueued tasks to one.

This pattern makes it also trivial to wait for all previously triggered tasks to finish executing:

```java
public void awaitIdle() throws InterruptedException {
    Future<?> done = workerThread.submit(new NoOp());
    try {
        done.get();
    } catch (ExecutionException e) {
        throw new RuntimeException(e);
    }
}

private static class NoOp implements Runnable {
    @Override
    public void run() {
    }
}
```

Because the `workerThread` is single-threaded, the `NoOp` task will execute only after all currently running and previously enqueued tasks have finished. The `Future` makes it easy to wait for that time.

All of this without using low-level concurrency primitives such as locks. :)
