---
layout: post
title: Speed Up Data Processing in Node with p-limit and Worker Threads
author: jarzka
excerpt: >
  We'll explore practical strategies to accelerate a real-world Node application that reads several large JSON files from disk, processes their contents, and outputs the results as large number of smaller JSON files.
tags:
  - Node
  - JavaScript
  - TypeScript
  - plimit
  - worker_threads
---

When I started writing this blog post, I realized that Node.js is now a teenager — at that age I was setting up my first website with PHP and only _thinking_ about becoming a software developer. Back then, Node.js was created to let web servers use JavaScript, the same language powering websites. While Node.js is well-suited for I/O driven web servers, it faces challenges with CPU-intensive computations due to its single-threaded event loop. When heavy computations run on the main thread, they can block other events and degrade overall performance.

In this blog post, we'll explore practical strategies to accelerate a real-world Node application that reads several large JSON files from disk, processes their contents, and outputs the results as a large number of smaller JSON files. We'll introduce two powerful Node.js tools: `p-limit` library for managing concurrent I/O operations, and `worker_threads` for parallelizing CPU-bound tasks. By combining these techniques, we can significantly reduce processing time and make Node applications more scalable.

## Limiting Factors in Node

To make sense of how to optimize performance in Node.js, it is essential to first understand the underlying limitations. At its core, Node.js is built on the V8 JavaScript engine, which provides high-speed execution of JavaScript code, but even highly optimized code cannot match the speed of native code. This means that Node.js is hardly the fastest tool available for raw data processing, so why use it for that in the first place? Well, it is a natural choice for handling JSON-based data due to its native support for JavaScript and rich node_modules ecosystem. It's also a widely used tool and can be easily picked up by virtually any web developer.

Node's architecture is fundamentally event-driven and single-threaded. This works fine for most web interfaces and servers, but can be seen as a limitation for pure data processing. In simple terms, single-threaded means that only a single JavaScript event or function can be on execution at a time. Even if you put your code in a Promise-returning function, its synchronous parts are still run sequentially and block the event loop from executing other tasks. Luckily, Node.js is still efficient for handling I/O operations such as reading/writing files and handling network traffic. These operations are delegated to run by the underlying system (mainly **libuv thread pool**) and thus do not overload Node's main event loop.

To optimize our Node process, we are going to maximize the performance of parallel I/O operations and also parallelize CPU-bound operations. How much of an increase can we expect? It's difficult to give a precise prediction, as it largely depends on the use case. In our case, we start with a processing time of **about 40 seconds**. Let's see how much we can improve it.

## Processing Data Overview

Let's begin with a simple example of processing data and writing the result to the disk:

```js
for (const file of files) {
  const result = await processData(file);
  await fs.promises.writeFile(result.path, result.data); // I/O operation, handled by libuv
}
```

Each file is processed and written to the disk one-by-one. This is simple and straightforward, and if it's fast enough for you, you could stop reading here. Otherwise, we can see that this code is not very efficient since we are only either processing data **or** waiting for the write operation to complete. Let's improve it by running the write operation in the background:

```js
for (const file of files) {
  const result = await processData(file);
  fs.promises.writeFile(result.path, result.data); // no await here, let it run in background
}
```

Here we do not wait for file writing to complete, but schedule it and immediately continue processing the next file. However, error checking is still missing and we do not wait for those background operations to complete. Let's fix it:

```js
const writePromises = [];

for (const file of files) {
  const result = await processData(file);
  const p = fs.promises.writeFile(result.path, result.data);
  writePromises.push(p);
}

// Data processing done, wait for all write operations to successfully complete. This throws an exception if even one write failed.
await Promise.all(writePromises);
```

This looks better from performance perspective as we are now doing more than one thing at a time, but the gained performance highly depends on how fast `processData` is compared to file writing. If it's slow, we might not gain much benefit at all. We also have a potential memory problem since we are queuing up all write operations to **libuv** at once. If `result` is large and there are many files to process, this could lead to high memory peaks. While **libuv** has some limits of how many write operations it does in parallel by default, the remaining operations are still put into queue. Let's see if we can improve this further using **p-limit**.

## p-limit

[p-limit](https://github.com/sindresorhus/p-limit) is a lightweight library for controlling concurrency in asynchronous operations. In other words, it can be used to easily limit the number of I/O-bound promises running simultaneously. The emphasis is on the word **I/O-bound**; p-limit does not help with CPU-bound tasks since it does not magically make JavaScript multi-threaded.

Going back to our previous example, what we actually want to do is to run multiple file write operations in parallel and in the background, but avoid running _too many_ to cause high memory peaks. **p-limit** solves this for us by allowing to specify the maximum number of concurrently run promises.

The right amount of concurrent operations depends on the use case and the capability of the underlying hardware. I would suggest beginning with a value of 2-6 and finding the sweet spot manually by testing with real-world data.

Let's take a look at how to use **p-limit**, first doing it **incorrectly**.

```js
import plimit from "p-limit";
const limit = plimit(4); // Allow up to 4 concurrent operations
const tasks = [];

// Naive example: assuming that files come from somewhere and `processFile` is implemented somewhere
for (const file of files) {
  const result = await processData(file);
  // BAD! Memory peak can still occur here.
  const task = limit(() => fs.promises.writeFile(result.path, result.data));
  tasks.push(task);
}

// Wait for all writes to complete
await Promise.all(tasks);
```

In this example, we are limiting the total number of simultaneous file operations, but we are NOT limiting calls to `processData`. This means that eventually all finished `result` objects would be queued to `p-limit`, potentially causing high memory peaks if the `result` object is large.

The can be solved by limiting both data processing and file writing:

```js
import plimit from "p-limit";
const limit = plimit(4);
const tasks = [];

for (const file of files) {
  const task = limit(async () => {
    const result = await processData(file);
    return fs.promises.writeFile(result.path, result.data);
  });

  tasks.push(task);
}

// Wait for all processing + writes to complete
await Promise.all(tasks);
```

This is starting to look good as we are now allowing parallel data processing and file writing while still setting a limit of how many `result` objects can be created at once. Again, the gained performance largely depends on the relative speed of `processData` and file writing. In our case, this trick decreased the processing time **from 40 seconds to about 30 seconds**.

## p-limit with Pending Queue

Let's assume there are so many files to be processed that we need to divide them into multiple different processing functions. This would mean that we needed to use p-limit on multiple different places, possibly losing a track of overall concurrency and memory usage. Each `plimit` instance only controls the tasks submitted to it, not the total number of tasks running across all instances. This can easily lead to more tasks executing simultaneously than intended.

To manage this safely, we could use a single global concurrency limiter that all processing functions use, ensuring the total number of active heavy tasks never exceeds your safe threshold. Note that this method might not give actual performance benefits, but it helps to keep memory usage more predictable across the whole application.

Here is an example of introducing a centralized write queue using a single instance of **plimit**. When data has been processed, it can be queued for writing via `enqueueWriteToFile` function. This queue is allowed to hold no more than **eight** pending write operations, setting a clear limit for memory usage in the whole application. If the pending queue is full, the caller is forced to wait until there is free capacity available. Finally, up to **four** write operations are allowed to run in parallel.

```ts
import { promises as fs } from "fs";

import plimit from "p-limit";

const MAX_ITEMS_IN_PENDING_QUEUE = 8; // Allow up to 8 operations to wait in the queue
const writePool = plimit(4); // Allow up to 4 concurrent operations
const pendingWrites = new Set();

interface DataFile {
  path: string,
  data: string
}

function waitForFreeCapacityInPendingQueue() {
  return new Promise((resolve) => {
    const check = () => {
      if (writePool.pendingCount < MAX_ITEMS_IN_PENDING_QUEUE) {
        resolve(undefined);
      } else {
        // Wait until pending queue is free
        setTimeout(check, 10);
      }
    };

    check();
  });
}

async function enqueueWriteToFile(file: DataFile) {
  // Main thread waits here if pending queue is full
  await waitForFreeCapacityInPendingQueue();
  // Schedule the write operation and continue processing
  const task = writePool(() => fs.writeFile(file.path, file.data));
  pendingWrites.add(task);
  task.finally(() => pendingWrites.delete(task));
}

async function waitForFileWritesToComplete() {
  await Promise.all([...pendingWrites]);
}

async function main() {
  for (const file of importantFiles) {
    const processed = await processFile(file);
    await enqueueWriteToFile(processed)
  }

  for (const file of moreImportantFiles) {
    const processed = await processFile(file);
    await enqueueWriteToFile(processed)
  }

  await waitForFileWritesToComplete();
}
```

We have now solved the problem of running both data processing and file writing in parallel while also avoiding high memory peaks by limiting the number of pending write operations. However, we are still processing data sequentially, one file at a time. To make this more efficient, we are going to look at `worker_threads` module next.

## Worker Threads

Node.js has `worker_threads` module, which enables true parallelism by running code inside Workers. This practically frees us from the single-threaded limitation of Node. Hooray, all performance problems solved! But there is a catch: running code in a worker is _kind of_ like running another Node inside Node. Each worker has its own execution context, call stack, heap memory and event loop. This makes worker threads completely separated and also requires some effort to setup.

Since running a task in a Worker requires its own "Node", initialising a Worker _practically_ requires initialising it with its own script. Here is a simplified example:

First, we create the worker file and import `processData` from the main application:

```ts
// worker_types.ts
interface DataFile {
  path: string,
  data: string
}
```

```ts
// worker.ts
import { workerData, parentPort } from "node:worker_threads";
import { processData } from "data/process";
import { DataFile } from "./worker_types";

async function runWorker() {
  // Params from main thread
  const params = workerData as DataFile;
  const result: DataFile = await processData(params);
  // Send result back to the main thread
  parentPort?.postMessage(result);
}

// Run the worker
runWorker().catch(err => {
  parentPort?.postMessage({ error: err.message });
});
```

We can compile this worker using `esbuild`, with a command like this: `npx esbuild src/worker.ts --bundle --outdir=dist --format=esm --platform=node`.

Finally, we call the worker from the main thread:

```ts
// main.ts
import { fileURLToPath } from "node:url";
import { Worker } from "node:worker_threads";
import * as path from "path";

import { DataFile } from "worker_types";
import { enqueueWriteToFile } from "io/write_queue"; // From previous p-limit example

const filename = fileURLToPath(import.meta.url);
const dirname = path.dirname(filename);

function runWorker(params: DataFile) {
  return new Promise((resolve, reject) => {
    const worker = new Worker(path.join(dirname, "worker.js"), {
      workerData: params,
    });

    worker.on("message", async (result) => {
      console.log("Result from worker:", result);
      await enqueueWriteToFile(result);
      resolve();
    });

    worker.on("error", reject);
    worker.on("exit", (code) => {
      if (code !== 0)
        reject(new Error(`Worker stopped with exit code ${code}`));
    });
  });
}

async function main() {
  // Assuming file comes from somewhere
  const workerPromise = runWorker(file);
  
  console.log("Worker started, main thread is still responsive.");

  await workerPromise;
  console.log("Worker finished!");
}
```

This example shows how to offload a single computation from main thread to a dedicated worker while allowing main thread to be responsive and continue handling other tasks without being blocked. While this method works, it requires us to manually initialise a new Worker every time we want to process something in parallel. Also, the worker must be tuned to handle different data processing tasks. This process can be simplified by using a library called [workerpool](https://github.com/josdejong/workerpool).

## Worker Pool

Here is a simplified example of what **workerpool** looks like. First, we create a worker file which exposes the functions it can execute:

```ts
// worker.ts
import { processData } from "data/process"
import { DataFile } from "worker_types";

const workerpool = require('workerpool'); // Must use require

async function processDataFile(file: DataFile) {
  return await processData(file);
}

// Expose what functions this worker can execute
workerpool.worker({
  processDataFile,
});
```

Main looks like this:

```ts
// main.ts
const workerpool = require('workerpool');
import { DataFile } from "worker_types";
import { enqueueWriteToFile } from "io/write_queue";

const filename = fileURLToPath(import.meta.url);
const dirname = path.dirname(filename);

// Create a worker pool with as many workers as there are logical CPU cores
const pool = workerpool.pool(dirname + '/worker.js', {
  maxWorkers: require("os").cpus().length,
});

async function main() {
  try {
    // Assuming file comes from somewhere
    const result = await pool.exec("processDataFile", [file]);
    await enqueueWriteToFile(result);
  } catch (err) {
    console.error(err);
  }

  // Terminate all workers when everything is done
  pool.terminate();
}
```

**workerpool** takes the implementation of creating and calling workers to a higher abstraction level, simplifying code and also making it more efficient since **workerpool** keeps a pool of workers "warm", ready to be used for offloading multiple long-running computations in the background. No need to manually create them every time.

In the above examples, we have offloaded only a single data processing task to the worker pool, but naturally we want to process all data in parallel. However, in heavily parallelized applications, we have to be careful of not offloading and queueing too many operations to workers at once and thus (again) introducing potential memory peaks - just like we need to be cautious with queuing too many I/O operations. Thus, I would be careful of calling `pool.exec` for every file at once since it _could_ cause worker pool queue to overload of file parameters.

### Worker Pool with Pending Queue

If one needs to limit the number of worker tasks to be queued, we would need to use some kind of pending queue to force the main thread to wait for a free worker to be available. A simplified example would look something like this:

```ts
const pendingTasks = new Set();
let queuedTasksCount = 0;

function waitForFreeWorker() {
  return new Promise((resolve) => {
    const check = () => {
      if (pendingTasks.size < NUMBER_OF_WORKERS) {
        resolve(undefined);
      } else {
        setTimeout(check, 10);
      }
    };
    check();
  });
}

async function enqueueWorkerTask(config: WorkerParams) {
  // Wait until there is a free worker available in the pool.
  await waitForFreeWorker();
  const task = pool.exec(config.task, [config.params]);
  pendingTasks.add(task);
  
  task.finally(() => {
    console.log("Worker task completed:", config.task);
    pendingTasks.delete(task);
  });
}

async function waitForWorkerTasksToComplete() {
  await Promise.all([...pendingTasks]);
  await pool.terminate();
}
```

By using a worker pool and p-limit together, we were able to reduce the total processing time **from original 40 seconds down to about 14 seconds!** This is a significant improvement, though it comes with increased code complexity and memory usage since each worker has its own memory space and we are keeping processed results in memory until they are written to disk.

## Tips for Working with Workers

Whether you decide to use **workerpool** or implement your own solutions, here are a couple of tips I wish I had known when I started working with Workers:

- You are free to import stuff from your main application code to your worker, but everything you import gets compiled in the final `worker.js`. This can result in large bundles and potentially unwanted code if not done carefully. For example, if you introduce a worker pool in your main application code, and you accidentally import some code from there in your worker, **every worker gets its own worker pool**. Probably not what you want. This can be avoided by doing `import { isMainThread } from "worker_threads"` and checking if `isMainThread` is `false` when ever something should never be imported by a worker.
- Worker's JS code must be built separately every time you modify it and always before running tests (I'm not happy remembering spending a day figuring out why some changes in my worker code did not do anything). If you use Vitest, you can use its `setup.ts` file to run code like `execSync("npm run build:worker", { stdio: "inherit" });` to get a fresh worker every time before running tests.
- Worker threads have their own isolated memory and cannot reference objects from the main thread (okay, there is `SharedArrayBuffer`, but it's a bit advanced concept). When you instantiate a worker and pass in some parameters, these parameters are **passed by value** (i.e. structured clone), not by reference. Thus, one needs to be careful about high memory peaks when using workers.

## Conclusion

Here is a quick summary of the tools we covered:

**p-limit** is ideal for managing concurrency in I/O-bound tasks, such as reading or writing files and making HTTP requests. By limiting the number of simultaneous operations, you prevent resource exhaustion and avoid hitting system limits. The code is only slightly more complex than standard async code, making p-limit a practical choice for many I/O-heavy workloads.

**worker_threads** is designed for CPU-bound tasks that would otherwise block the event loop, virtually any heavy data processing. Worker threads run in parallel, leveraging multiple CPU cores for true concurrency. However, using worker threads increases code complexity and memory usage, as each worker has its own execution context. Using it also requires some planning of _how_ to actually divide complex computation into workers effectively and may not be sensible if tasks depend on each other. For heavy parallel data processing, I recommend taking a look at [workerpool](https://github.com/josdejong/workerpool) library.

Both **p-limit** and **worker_threads** are powerful tools for improving Node.js performance, but they serve different purposes and come with trade-offs. Even if these tools allow us to maximize performance by running things in parallel, one needs to be mindful of not fulfilling memory with a queue of tasks or cpu with too many simultaneous workers. Using either or both tools always increases code complexity and memory usage, potentially crashing your application if not managed carefully. Thus, it's important to evaluate whether the performance gains justify these costs for your specific use case.
