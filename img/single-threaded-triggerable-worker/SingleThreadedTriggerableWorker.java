// Copyright © 2015, Solita Oy <www.solita.fi>
// This software is released under the MIT License.
// The license text is at http://opensource.org/licenses/MIT

import java.util.concurrent.BlockingDeque;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.LinkedBlockingDeque;
import java.util.concurrent.ThreadFactory;
import java.util.concurrent.TimeUnit;

/**
 * Executes a {@code Runnable} task in a single worker thread when requested.
 * Every call to {@link #trigger} will be followed by a task execution,
 * but multiple triggerings may be handled with just a single task execution.
 */
public class SingleThreadedTriggerableWorker {

    private final ExecutorService workerThread;
    private final BlockingDeque<Runnable> triggerableTasks = new LinkedBlockingDeque<>();

    public SingleThreadedTriggerableWorker(Runnable task) {
        this(task, Executors.defaultThreadFactory());
    }

    public SingleThreadedTriggerableWorker(Runnable task, ThreadFactory threadFactory) {
        workerThread = Executors.newSingleThreadExecutor(threadFactory);
        triggerableTasks.add(task);
    }

    public void shutdown(long timeout, TimeUnit unit) throws InterruptedException {
        workerThread.shutdown();
        if (!workerThread.awaitTermination(timeout, unit)) {
            throw new InterruptedException("Timed out while waiting for termination");
        }
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
}
