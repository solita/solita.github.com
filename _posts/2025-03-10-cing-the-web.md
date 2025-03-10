---
layout: post
title: C-ing the web, a front-end story
author: tatut
excerpt: >
  C is the grand old man of systems programming, still widely used today, but
  not often used for web development. Let's try to make a client side front-end
  with it.
tags:
 - C
 - Frontend
---

The C programming language is the grand old man of systems programming.
It is undeniably that C makes the world go around, being the implementation
language for such "minor" things as the [Linux kernel](https://git.kernel.org/), [sqlite](https://sqlite.org/index.html), and [many](https://github.com/python/cpython) [programming](https://github.com/ruby/ruby) [language](https://github.com/SWI-Prolog/swipl-devel) [runtimes](https://github.com/Perl/perl5).

Although C was used in the early web through [Common Gateway Interface](https://en.wikipedia.org/wiki/Common_Gateway_Interface),
it has never been the go-to language for web development, especially not on the front end!

Compared to JS [WebAssembly](https://webassembly.org) provides a much lower level virtual machine in
the browser that can be used as a compilation target for any native code.
There are [many languages](https://github.com/appcypher/awesome-wasm-langs) that have a WebAssembly 
port.
It is time to try making a client-side web app in (mostly) pure C. In this post, we will make the
traditional simple to-do-list application.

## HTML generation

The first obvious step is generating some HTML. There are text-templating solutions
for C, but I want to avoid any dependencies so we'll roll our own.

We can have a static buffer that all rendering is done to:
```c
// I have it on good authority that 640k ought to be enough for anyone
#define HTML_MAX_MEMORY 640 * 1024
char _html_memory[HTML_MAX_MEMORY];
char *_html_out;
```

Then we can have utilities to output things like tag start, attributes, and tag end.
```c
void tag_start(const char *name);
void tag_end(const char *name);
void attr_s(const char *name, const char *value);
void attr_i(const char *name, int value);
void attr_b(const char *name);
```

We implement these as calls to [`snprintf`](https://www.geeksforgeeks.org/snprintf-c-library/) to output formatted text into the buffer
without going over the statically allocated memory limit.

Then we can finish things by adding some convenience macros:
```c
#define tag(name, body) \
  {                     \
    tag_start(name);    \
    body tag_end(name); \
  }
```

This allows us to write HTML generation code that looks like this:
```c
  tag("div", {
      attr_s("class", "todo-form");
      tag("input", {
          attr_s("placeholder", "What needs to be done?");
          attr_s("onchange", "add_todo(event.target.value); event.target.value='';");
        });
    });
```

It ain't exactly pretty like [hiccup](https://github.com/weavejester/hiccup) or [JSX](https://react.dev/learn/writing-markup-with-jsx),
but if you squint hard enough you can kind of see the HTML structure.
You can see the HTML-generating code on GitHub: [`html.c`](https://github.com/tatut/todoC/blob/main/html.c)

## Data model and state management

Next up is modeling and managing the data. What we want again is something simple,
especially as we need to manage memory manually.

We can model the `Todo` as C struct, containing the index, label, and completion
status of the item as well as links to previous and next entries.
We could use a [dynamic array](https://www.geeksforgeeks.org/dynamic-array-in-c/)
to store the data, but again we will have a statically allocated pool with 1024
entries. If anyone has more things on their to-do-list, they need better software to
manage it anyway!

```c
typedef struct Todo Todo;

struct Todo {
  int idx;
  char label[255];
  bool complete;
  Todo *prev;
  Todo *next;
};

#define MAX_TODOS 1024
Todo todo_memory[MAX_TODOS]; // memory holding the todos
Todo *todos = NULL;          // list of active todos
Todo *last_todo = NULL;      // the last todo, for adding to end
Todo *free_todos = NULL;     // list of free todos
int num_todos = 0;           // number of active todos
```

The purpose of having the index is that we can modify any item by just looking
it up from the `todo_memory` and manipulating it. The doubly linked list is to
maintain the order.

We initially add all todos to the `free_todos` list. When we add a todo we take the
first one from that list and add it to the active `todos` list.

The "API" that we need for JS handlers is:
* adding a todo
* deleting a todo
* toggling a todo's completion.

After any change from JS side, we rerender the application.

Toggling is easy, we can just access the memory by index:
```c
void toggle_todo(int idx) {
  if(valid_idx(idx)) todo_memory[idx].complete = !todo_memory[idx].complete
  rerender();
}
```

Adding a new todo is a little more involved:
```c
void add_todo(char *data) {
  Todo *t = free_todos;
  if(t == NULL) {
    printf("No more free todos!\n");
  } else {
    free_todos = t->next;
    t->next = NULL;
    if(todos == NULL) { // first todo
      todos = t;
    } else {
      last_todo->next = t;
      t->prev = last_todo;
    }
    last_todo = t;

    // copy to our own memory
    size_t len = strlen(data);
    len = len > 255 ? 255 : len;
    memcpy(&t->label[0], data, len);
    t->label[len] = 0;
    t->complete = false;
    t->next = NULL;

    rerender();
  }
}
```

Deletion returns the Todo to the front of the `free_todos` list.
You can view the full code on GitHub: [`todo.c`](https://github.com/tatut/todoC/blob/main/todo.c)

## Compiling and integrating

After we have rendering and data management we are ready to hook this up to a page
and have some JS bindings.

For compilation we use [emscripten](https://emscripten.org) which will also create
a host HTML page based on our shell.

```shell
$ emcc -o todo.html                                                      \
   todo.c html.c                                                         \
   -s EXPORTED_FUNCTIONS=_init,_add_todo,_delete_todo,_toggle_todo,ccall \
   --no-entry                                                            \
   --shell-file shell.html
```

This will compile our app and create 3 files:
* `todo.js` contains emscripten JS integration code
* `todo.wasm` the compiled WebAssembly binary
* `todo.html` HTML page for the application

In our [`shell.html`](https://github.com/tatut/todoC/blob/main/shell.html) we add some
styling and have a div with id `app` which the application will render to once loaded.
We also add JS wrappers to call our C-side functions.

```javascript
function add_todo(label) {
  Module.ccall("add_todo", null, ["string"], [label]);
}
```

See emscripten documentation for [interacting with code](https://emscripten.org/docs/porting/connecting_cpp_and_javascript/Interacting-with-code.html)
for more details.

Once the app is compiled, we can serve it locally with a simple HTTP server.

![see it in action](/img/2025-cing-the-web/todoC.gif)

## Further work

There's lots more that could be done, but I'll leave these as an exercise for the reader.

*TodoMVC*

The app could be styled according to the [TodoMVC](https://todomvc.com) app and the full functionality added.

*Persistent storage*

You could load and save the todo's into client side [IndexedDB](https://en.wikipedia.org/wiki/Indexed_Database_API) storage
using [emscripten File System API](https://emscripten.org/docs/api_reference/Filesystem-API.html#filesystem-api-idbfs).

*More fine grained updates*

The current implementation simply rerenders the whole app and sets the `innerHTML` of the
application element. You could update only changed items (think implementing some form of virtual DOM
in C). Alternatively you could just use a library like [Idiomorph](https://github.com/bigskysoftware/idiomorph)
to mutate the DOM.

## Final remark

Should you start doing front-ends with C? Probably not, but this was a fun experiment.
Emscripten itself is a robust tool and WebAssembly looks like it could become a sort of
universal bytecode.

Even if you won't do front-end work in C, there are so many languages that compile to C
or have an implementation in C that WebAssembly can help reach the browser.

Happy hacking!
