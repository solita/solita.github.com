---
layout: post
title: "Building a Static Website from JSON Data with Astro"
author: jarzka
excerpt: An overview of the Astro web framework and practical experiences using it to build a static website from a large collection of JSON data files.
tags:
  - Astro
  - JavaScript
  - TypeScript
  - JSON
---

After spending a decade creating interactive web applications with React, I had almost forgotten the beauty of building static, pre-generated websites. After all, this was how the whole web started: sending ready-to-use HTML files with useful information for people in the 90s. How did our ancestors survive without reactive components or complex state management libraries?

Our team recently got an opportunity to revisit this "nostalgia" when we needed to create a graphical user interface for a large amount of JSON data files. To do this, we decided to build a simple website focused on content and minimal user interaction. Perhaps we wouldn't need JavaScript at all (you know, many interactive elements like menus and accordions can be created solely with modern HTML and CSS).

But how are static websites built in 2024? What tools are available, and are they suitable for generating good-looking websites from JSON data? It was time to find out.

## Prerequisites

We had some prerequisites for our JSON-to-HTML generator. At a minimum, it should not only transform a single JSON file into an HTML document but also allow us to structure the pages based on data relations and pre-process the data before rendering if necessary. After all, we are building a website, not just a collection of individual pages.

We valued tools that felt modern, focused on creating a minimal build, had a foreseeable future, and promised quick generation speeds. Additionally, since multiple people will maintain our product over time, the technology should be relatively easy for an average developer to pick up.

## Picking the Perfect Fit

We found many tools that could potentially satisfy our needs. We checked names like Jekyll, Hugo, Gatsby, and Next.js. We spent time testing and comparing their features to understand which one to pick. To my surprise, all the tested tools either lacked the features we needed or were unable to produce a minimal HTML/CSS output without unnecessary JavaScript.

One night, I couldn't sleep as I was feeling uncertain about the tools we had tested. None of them felt like the winner's choice for us. I started googling for more options and found a name I had never heard before: [Astro](https://astro.build) (not to be confused with the popular video game). It was a relatively new face in town, but it did promise to be a modern and content-driven framework which outputs zero JavaScript by default. I really liked this idea so I had to try it out.

## Initiate the Launch Sequence

To begin using Astro, I simply ran `npm create astro@latest`. After that, I got the following greeting:

```bash
npm create astro@latest

 astro   Launch sequence initiated.

╭─────╮  Houston:
│ ◠ ◡ ◠  Welcome to  astro  v4.16.16, Jari!
╰─────╯
```

How could one not like a tool that welcomes you with a message like this? 🥹

Anyway, after executing this command and answering a few questions, I was given a ready-to-use site structure to begin working with. The [official documentation](https://docs.astro.build/en/basics/project-structure/) was a great starting point to learn how things work.

## Building Things in Astro

Like many web frameworks out there, Astro uses a concept of components to build websites. Similar to React, these components take data as props and return HTML code. The key difference is that in Astro, the component "function" is called at build-time, not runtime, when the site is generated.

A component in Astro is a file with a `.astro` extension. It contains the component's script and rendering logic:

```astro
---
// MyComponent.astro
import SomeAstroComponent from '../components/SomeAstroComponent';

// Access passed-in component props, like `<MyComponent title="Hello, World" />`
const { title } = Astro.props;
---

<!-- Render regular HTML elements. Variables from the component script are directly available. -->
<h1>{title}</h1>

<!-- Use other Astro components and pass props in. -->
<Banner title={title}/>

<!-- Mix HTML with JavaScript, similar to JSX: -->
<ul>
  {myPosts.map((data) => <li>{post.name}</li>)}
</ul>

<!-- Component's children will go here -->
<slot /> 

<!-- Component style. -->
<style>
  h1 { color: red; }
</style>
```

As you can see, the syntax looks somewhat familiar to React or Svelte. At the top of the file, we have the component script, which gives us the full power of TypeScript to fetch and pre-process data for our page. Next comes the component template, which is just HTML code in a JSX-like syntax. At the bottom, we have the component's CSS style in a `<style>` tag, which is automatically scoped to this component in the final build.

Here is a complete example of a simple `Greeting` component. It takes two props: `greeting` (optional) and `name`, and renders a container with a greeting text.

```astro
---
interface Props {
  name: string;
  greeting?: string;
}

const { greeting = "Hello", name } = Astro.props;
---

<div id="greetingContainer">
  <span>{ greeting }, { name }!</span>
</div>
```

## Routing

Routing means defining where each page should be located in the final build. Consider the following URL:

```
example.com/en/posts/1
```

The path of this page consists of multiple parts: domain, language, post, and post ID. Out of these, the language and post ID are dynamic, meaning there is a separate page for each post ID, and the page is available in multiple languages.

Astro uses [a file-based routing](https://docs.astro.build/en/guides/routing/), which means the generated routes are based on a specific file and folder structure. Folder names represent URL path segments (static or dynamic), and `.astro` files represent HTML files (pages are just normal Astro components).

Thus, the file and folder structure for `example.com/en/posts/1` might look like this:

```
pages
  |- index.astro
  |- [language]  
         |- index.astro 
         |- posts
              |- index.astro
              |- [postId]
                    |- index.astro
```

Folder names in square brackets are dynamic parameters that vary between pages. To resolve these parameters for each page, we export a function named `getStaticPaths` in every `index.astro` file that needs to define them. This function is automatically called by Astro at build-time and it should return an array of all possible parameter combinations. Here is an example what the `getStaticPaths` might look like:

```ts
// pages/[language]/posts/[postId]/index.astro
export async function getStaticPaths() {
  // Get data for the page, from any source you like
  const res = await fetch('https://example.com/posts');
  const posts = await res.json();
  const languages = ["fi", "en"];

  // Return a list of possible path parameters
  return languages.map((language) => (
    posts.map((post) => ({
      params: { language, postId: post.id }
    }))
  )).flat();
}
```

When this page is built, this function returns a combination of all possible path parameters and for each combination, a new page is generated. The combinations look like this:

```ts
[
  { language: "fi", postId: "1"},
  { language: "en", postId: "1"},
  { language: "fi", postId: "2"},
  { language: "en", postId: "2"},
  // ...etc...
]
```

This generates the following pages:

```
dist/en/posts/1/index.html
dist/fi/posts/1/index.html
dist/en/posts/2/index.html
dist/fi/posts/2/index.html
```

Because each page file is named `index.astro`, it outputs as `index html`, meaning most web servers serve it automatically when accessing just the folder: `example.com/en/posts/1`.

## Feeding Pages with Data

Now that we know how to build our site from components and route pages correctly, it's time to feed those pages with data. One good thing about Astro is that it doesn't care where the data comes from. When generating pages, you can read data from a file on the disk, from a database, or from an API on the network. You decide!

Despite this flexibility, Astro does contain its own built-in API called [Content Collections API](https://docs.astro.build/en/guides/content-collections/) for managing data. It essentially requires creating a folder named `content`, which is going to hold collection names as subfolders and data files (JSON, MD etc.).

The data in collections can be utilised in TypeScript by first defining the collection in `content/config.ts`. Optionally, the collection can also be typed with Zod.

```ts
// Assuming our data is located at:
// src/content/posts/1.json
// src/content/posts/2.json
// src/content/posts/3.json
// etc.

// config.ts

const postSchema = z.object({
  id: z.string(),
  title: z.string(),
  content: z.string()
});

const postCollection = defineCollection({
  type: "posts",
  schema: postSchema,
});

export const collections = {
  posts: postCollection,
};
```

You can then use the collection data anywhere in Astro. For example, a page component that represents a single post can resolve the page parameters using the newly defined posts collection and provide the post as a prop for rendering:

```astro
---
// pages/[language]/posts/[postId]/index.astro
export async function getStaticPaths() {
  const posts = await getCollection("posts"));
  const languages = ["fi", "en"];

  return languages.map((language) => (
    posts.map((post) => ({
      params: { language, postId: post.id },
      props: { language, post }
    }))
  )).flat();
}

const { language, post } = Astro.props;
---

<h1>{translate(language, post.title)}</h1>
```

## Preprocessing JSON Files for Astro

The built-in Collections API requires the data to be [structured in a specific way](https://docs.astro.build/en/guides/content-collections/): one folder per collection of data files of the same type (with one or more subfolders for better organization). This felt nice and simple, but unfortunately, not all of our original JSON files were structured this way, so we needed a way to transform them into a more Astro-compatible format.

To do this, we decided to build a separate tool. Any language or framework could be used for this, but we chose to create a minimal Node application since processing and transforming JSON data with TypeScript feels natural. We keep the original JSON files as they are and use our tool to transform them for Astro prior to the actual site generation. This method turned out to work fine, and we were pleasantly surprised by how fast JSON parsing works in Node.

## Generation speed

Generation speed, i.e., the time between converting our JSON data to HTML files, is not the most important concern for sites whose data does not change often. However, it can be an important factor when you have a large number of HTML files to generate or the pages need to be kept fresh as data changes.

The speed of generating a website with Astro depends on many factors, so one should be mindful when releasing or reading statistics on that. Still, I value when people share data based on real use cases of Astro. Even if there are variables, it can help to get a general idea of the generation speed.

On my M1 Mac, generating 14 000 HTML pages in this project takes approximately 3 minutes and 50 seconds. This speed is _okayish_, but since some pages require frequent updates, I started looking for ways to improve the generation time.

### Making Astro Faster

Don't take this 100% granted, but I assume that Astro, being a Node-based tool, does not perform much parallel processing on its own (generating multiple pages in parallel). However, parallel processing could significantly improve generation speed, especially when each page can be generated independently. Therefore, I started thinking: if Astro does not do parallel processing itself, maybe we could run multiple Astros in parallel?

Our pages are available in three languages (Finnish, Swedish, English), so I decided to generate each language in parallel by running three instances of Astro (one per language). This approach resulted in a significant performance boost, reducing the generation time for 14 000 pages to under two minutes!

It is good to note that even with parallel processing, Astro's performance is hardly the fastest on the planet, though I believe it's likely sufficient for most cases. Using a faster generator (such as Hugo) often comes with a price of using a lower level programming language and its own ecosystem, so one needs to carefully consider whether it's worth the benefit.

## Practical Experiences

So far, my experience with Astro has been mostly positive. I have been building pages by creating and composing my own Astro components and feeding them with data. Things have worked fine.

But not everything has been perfect with my powerful space rocket. Next, I'm going to reveal a few things I have been struggling with Astro - and a few tips for you to avoid them.

### Building a Breadcrumb

Breadcrumb is essentially a list of links heading from the site's root to the current page. For example, if the current page URL is `en/posts/1`, the breadcrumb of this page and its parent pages should look something like this:

```
Page: en/posts/1
Breadcrumb: Home > Posts > Hello world! This is my first blog post

Page: en/posts
Breadcrumb: Home > Posts
```

The page for rendering `/en/posts/1` is an astro file located in `/pages/[language]/posts/[postId]/index.astro`. Since we are building a static site where each page is a separate HTML file, this page and all other pages must be able to render a Breadcrumb, listing a path to the current location. A single Astro file always knows its URL and title, but how can we render a list of links to previous pages, including their page titles?

It seems that Astro does not know either, as there is no built-in way to do this. Since every page needs to render the Breadcrumb containing the current and parent page titles, we need to have some kind of "database" of all possible page paths and their matching titles. And not only that, we also need to take dynamic parameters into account! To do this, I created my own function which maps page urls to page titles. It looks like this:

```ts
interface RouteConfigParams {
  language: string,
  postId?: string,
  postTitle?: string;
}

type PathParamsToString = (routeConfigParams: RouteConfigParams) => string | undefined;

const pathTitleInBreadcrumb: Record<string, PathParamsToString> = {
  "/$language": (params) => translate(params.language, "home"),
  "/$language/posts": (params) =>  translate(params.language, "posts"),
  "/$language/posts/$postId": (params) => params.postTitle,
};
```

All my Astro pages use a common `MainLayout` component, passing in `RouteConfigParams`, which then renders `Breadcrumb`.

```astro
---
export async function getStaticPaths() {
  const posts = await getCollection("posts"));
  const languages = ["fi", "en"];

  return languages.map((language) => (
    posts.map((post) => ({
      params: { language, postId: post.id },
      props: { language, post }
    }))
  )).flat();
}

const { post, language } = Astro.props;
---

<MainLayout routeConfigParams={{ language, postId: post.id, postTitle: post.title }} />
```

The actual implementation of my `Breadcrumb` is too large to include here, but here is the general idea: `Breadcrumb` reads the value of `Astro.url` to get the current page URL at build-time and finds the matching path from `pathTitleInBreadcrumb` using the provided `RouteConfigParams`. For example, given a URL of `/en/posts/1`, it finds that this URL matches with `/$language/posts/$postId`. Once a match is found, we retrieve a function for getting the final page title. To get page titles for parent pages, we traverse the URL back, checking both `/en/posts/` and `/en` for matching page titles, and finally render all the page titles as links.

Implementing the breadcrumb took time and felt something that could utilise a bit of support from the framework. Actually, there is a plugin available for building a Breadcrumb in Astro. It may be a good fit for some, but in my case it did not solve the "database" problem nor was I able to configure it the way I wanted.

### Handling Big Data with Collections API

I was having a good time feeding the generator with more and more JSON files and seeing my data turning into beautiful web pages. But then, at some point I suddenly faced this:

```bash
<--- JS stacktrace --->

FATAL ERROR: Reached heap limit Allocation failed - JavaScript heap out of memory
 1: 0x102b76114 node::Abort() [/Users/me/.nvm/versions/node/v20.9.0/bin/node]
 2: 0x102b762fc node::ModifyCodeGenerationFromStrings(v8::Local<v8::Context>, v8::Local<v8::Value>, bool) [/Users/me/.nvm/versions/node/v20.9.0/bin/node]
 3: 0x102cfd048 v8::internal::V8::FatalProcessOutOfMemory(v8::internal::Isolate*, char const*, v8::OOMDetails const&) [/Users/me.nvm/versions/node/v20.9.0/bin/node]
 4: 0x102ed182c v8::internal::Heap::GarbageCollectionReasonToString(v8::internal::GarbageCollectionReason) [/Users/me/.nvm/versions/node/v20.9.0/bin/node]
```

Yikes! Out of memory errors are one of the last ones you want to face when everything was working well before. I did not find an official explanation, but I noticed this error happening when filling the `content` folder with files without even using them in code! It seems like Astro's Collection API is designed to eat all files from `content` in memory, making the Collections API practically useless for handling big chunk of data files.

After googling around I first found an easy "fix" by simply increasing Node memory:

```bash
export NODE_OPTIONS=--max_old_space_size=4096
npm run build
```

This worked, but it felt like a temporary solution, as I cannot guarantee that all data will fit into memory in the future. I needed a better solution. I almost started feeling that we had picked the wrong tool for the job. Fortunately, the workaround was once again to create my own solution.

To keep the mass of JSON files from filling the memory in the beginning of `astro build`, I simply moved them outside of `content` to a new folder called `content-large`. This folder has nothing to do with Astro, so I can work with it the way I want. I implemented my own helper functions for listing and reading JSON files from `content-large`, using Node's standard `fs` API.

When creating Astro pages with large JSON files, I became mindful of using `getStaticPaths`. A single Astro page component can potentially need an array of thousands of different parameter combinations. Reading large JSON files into memory at this point could cause "out of memory" errors. 

To avoid this, I read the page's matching JSON file from the disk only when the actual page is generated. This approach allowed me to generate tens of thousands of pages from multiple large JSON files without filling the memory:

```astro
---
export async function getStaticPaths() {
  const postsIds = await getPostIdsFromContentLarge());
  const languages = ["fi", "en"];

  return languages.map((language) => (
    postsIds.map((postId) => ({
      params: { language, postId: postId },
      // Pass only ids, not the whole post
      props: { language, postId: postId }
    }))
  )).flat();
}

const { postId, language } = Astro.props;
const post = await getPostFromContentLarge(postId);
---

<h1>{translate(language, post.title)}</h1>
```

It's important to note that my experience mentioned above is based on Astro version 4 (Astro 5 will introduce some changes in content management). Memory management problems can occur with any tool if large data files are not handled carefully. Still, it feels like there was not enough information available on the performance of the Collections API, other than the claim that "it's the best way to manage and author content in any Astro project."

### IntelliJ IDEA plugin

Since Astro uses its own file format `.astro`, you typically need an editor plugin to work with this file type. Luckily, there is a plugin available for IntelliJ IDEA from JetBrains, but it has left a bit to be desired.

For me and my colleagues, the plugin sometimes breaks the Astro file syntax when auto-importing files, which is kind of annoying. I also had problems resolving TypeScript types when calling `getCollection` in IDEA, something that VS Code was able to handle correctly. Based on plugin reviews, others seem to be struggling too with problems. Luckily, the plugin has not been a showstopper for us, but I hope it will get better over time.

## Astro Islands

Since I'm building a static, content-first type of website with minimal JavaScript, I'm not focusing too much on interactivity. Still, I want to say a few words about an interesting concept called Astro Islands.

Astro Islands is a term used for embedding interactive components created with a 3rd party framework (React, Vue...) to Astro pages. Yes, you can actually do that! Even if you are building static, pre-generated pages, it does not mean we cannot also use other battle-tested frameworks for adding interactivity on our pages if we want that.

For example, a React component can be used like any other Astro components:

```astro
---
import MyReactComponent from '../components/MyReactComponent.jsx';
---
<html>
  <body>
    <h1>Use React components directly in Astro!</h1>
    <MyReactComponent />
  </body>
</html>
```

Wait a minute.... haven't I mentioned that Astro outputs zero JavaScript by default? How can we embed React components that require JavaScript to run? Well, it turns out that interactive components still render at built-time as static HTML/CSS elements by default. If we want to enable interactivity, we need to "enable" JavaScript on purpose. To do this, Astro offers a set of special directives. I'm not getting into details, but here is a quick example of what it looks like:

```astro
---
import InteractiveButton from '../components/InteractiveButton.jsx';
---

<!-- This component's JS will begin importing when the page loads -->
<InteractiveButton client:load />
```

This might look confusing at first, but it is part of the magic that allows Astro to focus on speed and producing minimal builds. When generating static sites that focus on HTML and CSS, we get just that without asking more.

More information about this concept of mixing frameworks with Astro Islands can be found in [the official Astro Islands documentation](https://docs.astro.build/en/concepts/islands/).

## Conclusion

I noticed many good little things when getting to know Astro. It uses component-based approach for building things, implements an easy-to-understand file based routing, has Vite as the build tool, comes with built-in support for TypeScript, and also supports various PostCSS plugins and linters. It also did not hurt that [the framework is sponsored by Google](https://developer.chrome.com/blog/framework-fund-2022/).

Furthermore, Astro makes it possible get the data for site generation from virtually any source, process it with TypeScript how you like and finally render with JSX-like syntax. Still, it did redeem the promise of including zero percent of JavaScript in the final build by default.

Despite having to implement some things manually by hand, I have been mostly happy building things with Astro. It feels modern, robust and (mostly) well documented tool for building static and content-focused web sites. If that sounds like something you need, I can happily recommend giving Astro a try!
