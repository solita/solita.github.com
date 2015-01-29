// Copyright © 2015, Solita Oy <www.solita.fi>
// This software is released under the MIT License.
// The license text is at http://opensource.org/licenses/MIT

import static java.util.Arrays.asList;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.is;
import static org.junit.Assert.assertTrue;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

import org.junit.After;
import org.junit.Rule;
import org.junit.Test;
import org.junit.rules.ExpectedException;
import org.junit.rules.Timeout;

public class SingleThreadedTriggerableWorkerTest {

    public static final int TIMEOUT = 3000;

    @Rule
    public final ExpectedException thrown = ExpectedException.none();
    @Rule
    public final Timeout timeout = new Timeout(TIMEOUT, TimeUnit.MILLISECONDS);

    private final List<String> log = Collections.synchronizedList(new ArrayList<String>());
    private final CountDownLatch firstTaskRunning = new CountDownLatch(1);
    private final CountDownLatch allTasksTriggered = new CountDownLatch(1);

    private SingleThreadedTriggerableWorker worker;

    @After
    public void shutdown() throws InterruptedException {
        if (worker != null) {
            worker.shutdown(10, TimeUnit.SECONDS);
        }
    }


    @Test
    public void runs_the_task_when_triggered() throws InterruptedException {
        worker = new SingleThreadedTriggerableWorker(new Runnable() {
            @Override
            public void run() {
                log.add("run");
            }
        });

        worker.trigger();

        worker.awaitIdle();
        assertThat(log, is(asList("run")));
    }

    @Test
    public void runs_the_task_when_triggered_after_the_task_is_finished() throws InterruptedException {
        worker = new SingleThreadedTriggerableWorker(new Runnable() {
            @Override
            public void run() {
                log.add("run");
            }
        });

        for (int i = 0; i < 3; i++) {
            worker.trigger();
            worker.awaitIdle();
        }

        assertThat(log, is(asList("run", "run", "run")));
    }

    @Test
    public void runs_the_task_when_triggered_while_the_task_is_running() throws InterruptedException {
        worker = new SingleThreadedTriggerableWorker(new Runnable() {
            @Override
            public void run() {
                signal(firstTaskRunning);
                await(allTasksTriggered);
                log.add("run");
            }
        });

        worker.trigger();
        await(firstTaskRunning);
        worker.trigger();
        signal(allTasksTriggered);

        worker.awaitIdle();
        assertThat(log, is(asList("run", "run")));
    }

    @Test
    public void runs_the_task_only_once_when_triggered_multiple_times_while_the_task_is_running() throws InterruptedException {
        worker = new SingleThreadedTriggerableWorker(new Runnable() {
            @Override
            public void run() {
                signal(firstTaskRunning);
                await(allTasksTriggered);
                log.add("run");
            }
        });

        worker.trigger();
        await(firstTaskRunning);
        worker.trigger();
        worker.trigger();
        worker.trigger();
        signal(allTasksTriggered);

        worker.awaitIdle();
        assertThat(log, is(asList("run", "run")));
    }


    // shutting down

    @Test
    public void on_shutdown_waits_for_running_tasks_to_finish() throws InterruptedException {
        worker = new SingleThreadedTriggerableWorker(new Runnable() {
            @Override
            public void run() {
                signal(firstTaskRunning);
                await(allTasksTriggered);
                log.add("run");
            }
        });

        worker.trigger();
        await(firstTaskRunning);
        signal(allTasksTriggered);
        worker.shutdown(1, TimeUnit.SECONDS);

        assertThat(log, is(asList("run")));
    }

    @Test
    public void on_shutdown_throws_exception_if_tasks_did_not_finish_within_timeout() throws InterruptedException {
        worker = new SingleThreadedTriggerableWorker(new Runnable() {
            @Override
            public void run() {
                signal(firstTaskRunning);
                await(allTasksTriggered);
            }
        });

        worker.trigger();
        await(firstTaskRunning);

        thrown.expect(InterruptedException.class);
        thrown.expectMessage("Timed out while waiting for termination");
        try {
            worker.shutdown(1, TimeUnit.MILLISECONDS);
        } finally {
            signal(allTasksTriggered);
        }
    }


    // helpers

    private static void signal(CountDownLatch latch) {
        latch.countDown();
    }

    private static void await(CountDownLatch latch) {
        try {
            boolean noTimeout = latch.await(TIMEOUT, TimeUnit.MILLISECONDS);
            assertTrue("timed out", noTimeout);
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
    }
}
