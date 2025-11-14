---
layout: post
title: C-ing the web part 2: Lambda boogaloo
author: tatut
excerpt: >
  Last time on in this series we created a web application front end in C.
  Now it's time to conquer the back end as well. Let's bring C to serverless
  back end programming by making an AWS Lambda custom runtime.
tags:
 - C
 - AWS
 - Lambda
 - Serverless
---

[Last time](https://dev.solita.fi/2025/03/10/cing-the-web.html) we implemented a simple front end
application in C and compiled it to run in the browser using via WebAssembly.

Now, let's consider the a back end. The traditional way would be to run a C application
in a web server like [Apache httpd](https://httpd.apache.org) using the
[Common Gateway Interface](https://en.wikipedia.org/wiki/Common_Gateway_Interface).
    Instead of doing that, let's run our C code inside AWS Lambda using the
[custom runtime](https://docs.aws.amazon.com/lambda/latest/dg/runtimes-custom.html) support.

With a custom runtime, you can create serverless functions using any language.
The custom runtime bootstrap is based on a simple loop that uses HTTP API to:
- issue a GET request to fetch the next invocation
- pass it on to the handler for processing
- issue a POST request to send response (or error) back to client
- repeat

To follow along or just try the code yourself, check out the code from the
[clambda repo](https://github.com/tatut/clambda).


## Getting a proper image

For making a custom runtime, we need to compile our C code in an environment that is compatible with
the AWS Lambda image.

The easiest way to do this is to just make our own Docker image for building:

```
FROM amazonlinux:2
RUM yum groupinstall -y "Development Tools" && yum install -y libcurl-devel
ENTRYPOINT ["/opt/clambda/build.sh"]
```

We start with the Amazon Linux image, install development tools and cURL headers to it.
We will run this image to build both the bootstrap and the handler code. Note that
if you are running on Apple architecture, you should specify
`--platform=linux/amd64` to Docker so that you are building for the correct environment.

For local testing, we also want to build a runtime image. We start with the provided
image and copy both the bootstrap and compiled handlers to it.

```
FROM public.ecr.aws/lambda/provided:al2023
COPY bootstrap ${LAMBDA_RUNTIME_DIR}
COPY *.o ${LAMBDA_RUNTIME_DIR}
```

## Designing the API

We need some way for our bootstrap to hand off requests to the handler and we want it
to be minimal and feel natural from C.

I came up with a simple function interface:

```C
typedef struct Invocation {
  uint8_t *payload; // the JSON payload, NUL terminated
  size_t size; // size of payload, not counting NUL byte

  // File handle to write the response to
  FILE *out;

  void *user_data;
} Invocation;

// optional _init fn to initialize user_data
void *handle_init();

// the handler itself
bool handle(Invocation *inv);
```

The handler code may provide a `_init` function that returns arbitrary user data
pointer that is passed along in all invocations. This can be used to initialize
any libraries or state needed in the actual invocations. The init is only called
once before handling any events.

The handler itself takes a pointer to an invocation that contains the received
data as a raw pointer and a file pointer for writing output.

The incoming data is not parsed in any way, it is up to the handler to make sense
of it, like parse JSON. See next part.

The output is simpler, the handler doesn't need to allocate memory buffers, the
bootstrap will provide a `FILE*` handle so the handler can simply call functions
like `fprintf` to write output. Handler can also set the content type.

Finally, if the handler returns `false`, the handler is considered failed and an
error reply is sent.

The bootstrap will load the handler code via a shared library. The handler only
needs to include the `clambda.h` header file and implement the function.

## Working with JSON

As Lambda is mainly for receiving and sending JSON, we should provide some
facilities for working with it. C doesn't really have data structures like objects
builtin and manual memory management makes this more awkward.

Luckily JSON (as defined by
[ECMA-404](https://ecma-international.org/wp-content/uploads/ECMA-404_2nd_edition_december_2017.pdf))
is quite a simple format. We can write our own code to extract data from it.
For memory management, especially strings, we can modify and return pointers to the
input buffer directly. Those will be valid for the duration of the Lambda handler.

We can use some C preprocessor macro magic to make extracting object fields to
C structs a little more convenient. This on-demand extraction obviates the need to
parse the JSON data fully into an in-memory representation. We can just directly
grab what we need from it.

Here's an example for extracting a JSON like this:
```json
{"id": "line1",
 "points": [{"x": 42.0, "y": 100},
            {"x": 66.2, "y": 90},
            {"x": 140,  "y": 123.4}]}
```

```C
typedef struct Point {
  double x, y;
} Point;

typedef struct Line {
  char *id;
  size_t npoints;
  Point *points;
} Line;

bool parse_point(char **at, Point *p) {
  json_object(at, {
    json_field("x", json_double, &p->x);
    json_field("y", json_double, &p->y);
  });
  return true;
}

bool parse_points(char **at, Line *line) {
  json_array(at, &line->points, &line->npoints, Point, parse_point);
  return true;
}

bool parse_line(char **at, Line *line) {
 json_object(at, {
    json_field("id", json_string_ptr, &line->id);
    json_field("points", parse_points, line);
  });
  return true;
}

```

The above might look a little bit involved when compared to some language that has
convenient generic data structures, but I like that we get the data extracted into
typed structures. The `json_array` macro even handles dynamic size of arrays for us
automatically. The application layer just needs to `free` any arrays at the end.

Outputting the response JSON is done with regular C formatted printing.
Utilities for that are left as an exercise for the reader.


## Putting it together

We have the API, the bootstrap and even JSON parsing utilities ready. Let's make
a simple Lambda that analyzes a line and returns how many points it has and its
length.

Taking the example from above and adding the handler function:
```C
bool analyze_line(Invocation *inv) {
  char *json = (char*) inv->payload;
  char **at = &json;
  Line line = {0};
  if(!parse_line(at, &line)) return false;

  printf("Line %s has %d points\n", line.id, line.npoints);
  double len = 0;
  if(line.npoints) {
    for(int i=0; i<line.npoints-1; i++) {
      double dx = abs(line.points[i].x - line.points[i+1].x);
      double dy = abs(line.points[i].y - line.points[i+1].y);
      len += sqrt(dx*dx + dy*dy);
    }
  }
  fprintf(inv->out, "{\"npoints\": %d, \"length\": %f}",
          line.npoints, len);

  free(line.points); // remember to clean up!
  return true;
}
```

That's all there is to it. To test is locally we can build it We can test it
locally by running the following commands:

```shell
$ make build
$ ./build-handler.sh example
$ make runtime-image
$ docker run -p 8080:8080 -t clambda/runtime example.analyze_line

# in another shell, call it:
$ curl http://localhost:8080/2015-03-31/functions/function/invocations \
       -d '{"id": "viiva", "points":[{"x": 10, "y": 10}, {"y":20, "x": 100}, {"x": 200, "y": 222}]}'
{"npoints": 3, "length": 315.951278}
```

See the file `example.c` for more examples, including a counter with state that
keeps state between calls.

For deploying to actual AWS environment, see instructions in [AWS documentation site](https://docs.aws.amazon.com/lambda/latest/dg/runtimes-walkthrough.html).

## Caveat and final remarks

C is quite a low level language and doesn't offer memory safety. You should carefully test any code
you are exposing over the internet. There are mitigation strategies like fuzzing (using tools like
[radamsa](https://gitlab.com/akihe/radamsa)), using [AddressSanitizer](https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html#index-fsanitize_003daddress)
or even compiling with a memory safe C variant [Fil-C](https://fil-c.org).

The upside is that using C can give us small fast starting and fast executing native code for when
you have a Lambda that needs to do some heavier processing.

Happy hacking!
