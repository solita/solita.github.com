---
layout: post
title: Taming Advanced Compilation bugs in ClojureScript projects
author: tonidahl
excerpt: >
  Closure Compiler's Advanced Compilation can sometimes produce quirky errors. 
  It's better to avoid them by taking advanced optimizations into account from the beginning of the project.
  On rare occasions, some weirder errors might arise that you have to swiftly resolve.
tags:
 - Development
 - ClojureScript
 - Closure Compiler
 - Advanced Compilation
 - Best Practices
---


Imagine this: You have a large multi-module ClojureScript project, and you are planning to make a new deployment in the
production.
Your project is using CLJS Compiler's Advanced Optimizations mode.
Everything seems to be working smoothly. You are performing some last E2E tests before making a release.  
Then, a faulty module loads.  
**BAM!** You are slapped in the face with an error something like this: 

```text
Uncaught Error: No protocol method IMultiFn.-add-method defined for type function: function XR() { [native code] }
    at Nb ((index):964)
    at yh ((index):443)
    at (index):236
(index):143 Uncaught TypeError: Cannot read property 'j' of undefined
    at NU ((index):143)
    at login-a5a67c0fffdfa158b7220c8c2553253b645e4e2e.js:169
```

You did not expect this. There were no significant new changes since the last build, and the unit tests were all
hunky-dory.  
Additionally, everything worked fine when using Firefox, but now the compiled code crashes on Google Chrome. 
What is going on? The release deadline is looming and you have to fix this ASAP.

![Holy Stack Trace, Batman!](/img/taming-cljs-advanced-compilation/slap.png)  
*Holy Stack Trace, Batman!*

When you build your code with the CLJS compiler, it emits JavaScript code that is compatible with the 
advanced_optimizations level of the Google Closure compiler. Then, if `":optimizations :advanced"` compiler option is
enabled, the CLJS compiler will minify the result with Closure Compiler's Advanced Optimizations.

Closure Compiler's Advanced Optimizations mode can cause some errors in your build that can be uncomfortable to
track down if you are new to Closure Compiler.
On top of that, help might be hard to find if you are trying to search the web with the error message because the function
names are all mangled up.

It is better to avoid these errors by keeping the Advanced Compilation mode in mind from the start of the project. 
I'll describe some common methods to help you to avoid and resolve advanced compilation issues, and 
show how to resolve the more uncommon issue that was described in the beginning and what is the reason behind it.

## Avoiding issues with Advanced Compilation

It is recommended to use `":optimizations :advanced"` CLJS compiler option for your production builds.
You will greatly reduce your final build size by using more aggressive advanced transformations such as dead code 
removal and aggressive renaming.  
Read more about the advanced transformations at here: [Closure Compiler compilation levels](https://developers.google.com/closure/compiler/docs/compilation_levels#advanced_optimizations)

Different build tools such as lein-cljsbuild and shadow-cljs might pass different default options to Closure Compiler.
I won't cover the differences in this blog post, but instead, I will provide some general guidelines on how to avoid
issues with advanced compilation in your project.

### Keep your externs in a good shape
[Extern](https://clojurescript.org/guides/externs) is a mechanism for declaring names that should not be munged (renamed) by Closure Compiler.
When you are using external libraries, make sure that they come [bundled](http://cljsjs.github.io/)
with externs if you are using a build tool like lein-cljsbuild. Or, provide externs files of your own if needed. 
Otherwise, Closure Compiler will munge references to externally defined symbols unintentionally during advanced 
compilation causing errors found only later when running the compiled code.

To add externs of your own, use a compiler option for example: `":externs ["externs.js"]"` and provide an
externs.js file in your working directory.

Also, It is good to use `":infer-externs true"` compiler option. This option will enable generating externs automatically
for JavaScript interop calls.

It is worth to know, that Closure Compiler includes externs for stable JavaScript APIs, but newer features that have an
experimental status might not be included yet. The experimental APIs change very quickly, so it makes no sense to include
them in the Closure Compiler tool. So, if you are planning to use some experimental features, make sure 
you add them to your own externs file.

Read more about using external JavaScript libraries from [here](http://lukevanderhart.com/2011/09/30/using-javascript-and-clojurescript.html)

### Splitting code might cause name collisions
If you are [splitting](https://clojurescript.org/guides/code-splitting) your CLJS code into ```:modules```, you might want
to use `:rename-prefix "..."` compiler option.  
Split modules are running in the global JavaScript scope, so they might interfere with other code loaded on the same page 
(e.g. Google Analytics) and cause unpredictable errors if name collisions occur.
When using `":rename-prefix"`, it is best to use a very short string as a prefix, for example: `:rename-prefix "r_"`

This will increase the final (gzipped) build size slightly because now each munged global variable will be prefixed with "r_".


### Wrap CLJS output to prevent global scope pollution
Closure Compiler will generate a lot of global variables during advanced compilation that can cause name collisions
with other code running on the same page.
If you are loading other code on the same page, and you are not splitting code into multiple modules you can utilize
 the `":output-wrapper true"` compiler option. The compiler will wrap the outputted JavaScript code with the default 
`"(function(){…​};)()"`. This will prevent polluting the global JavaScript scope and thus will prevent conflicts
with other external code.

However, if you have multiple modules in your project you must add a compiler option `:rename-prefix-namespace "..."`.
This enables each module to access the variables defined in the other modules it depends on.
This works similarly to the `":rename-prefix"` option. The difference is that every global variable will be now
scoped under one global variable instead of many. For example, if you use a prefix-namespace like this:
`:rename-prefix-namespace "P"`, the compiled code will refer to variable `"foo"` like `"p.foo"`. 
This option will also increase the final build size like the `":rename-prefix"` option, so think before using it.


There are other interesting compiler options not directly related to advanced optimizations, such as `":fn-invoke-direct"` 
which can be useful for optimizing performance-critical code. You can read more about them in CLJS 
[documentation](https://clojurescript.org/reference/compiler-options).


## Debugging Advanced Compilation bugs

If you suspect you might have a problem with advanced compilation, often hinted by errors in the browser 
console that might make no sense, it is best to approach the problem in the following way.

Add two additional compiler options `":pseudo-names true"` and `":pretty-print true"` for your Advanced Compilation build.
Your error will now show a readable name that corresponds to the name in the source code. 
This will help you to deduce if an extern definition is missing.

Additionally, if your error goes away after enabling the above-mentioned compiler options, it gives you a hint
of a possible name collision problem. When there is a problem with a munged variable name colliding with an external 
variable name, the problem disappears when the munged variable name changes, like what happens when enabling the :pseudo-names option.  
Often, if not fixed properly, the name collision issues can arise and then be magically "fixed" when one adds new 
changes, which in turn causes changes in munged variable names in the build output. It is best to eliminate these problems for good.

### Sometimes, something funky can happen
In some rare cases, there might be some advanced compilation issues that are not so easy to avoid.
Let's go back to the beginning. 
We had an error when running our built web app in Chrome. Firefox had no issues.
```
Uncaught Error: No protocol method IMultiFn.-add-method defined 
                for type function: function XR() { [native code] }
    at Nb ((index):964)
    at yh ((index):443)
    at (index):236
```

The Stack Trace was pointing to a certain multimethod in the CLJS source code. 
At the first glance, the error might make no sense. The compiled code is trying to invoke -add-method IMultiFn protocol method 
for a function named XR. When searching for the munged ```XR``` in the build output, everything seems to be fine. 
```XR``` looks good and should work, right?
The key thing to notice in the error message is the `"[native code]"` part of `"function XR() { [native code] }"`.
This tells us, that the compiled code is trying to invoke a native browser function ```XR``` instead of our munged ```XR```. 
By chance, the Closure Compiler named our multimethod to ```XR``` which happens to collide with the browser provided 
```XR``` function.

Occasionally you can encounter errors like this when using an older version of Closure Compiler.
Developers add new features to web browsers all the time. When a user upgrades his/her web browser there is a chance 
a new reserved word was added that collides with a munged variable. 

It turns out, XR is a reserved word added by the WebXR platform API. When the error occurred "XR" was added in the newest 
version of Google Chrome, but not yet in Firefox. Newer Closure Compiler versions take this into account by providing
an extern for it. It is not always easy to upgrade the ClojureScript version and thus the Closure Compiler used in a project.  
In that case, you can fix the problem fast by adding a custom extern of your own:
```javascript
// externs.js

var XR = {};
```


## Conclusion

Many times, Advanced Compilation issues with CLJS are easy to avoid with proper preparation. On rare occasions, some
stranger errors can happen. Thus, test your builds with the current browser versions and learn to debug advanced 
compilation issues swiftly to prevent wasting precious time.
