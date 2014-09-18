---
layout: post
title: Sharing client-side components with Bower
author: massimo
excerpt: You need to build an app which uses a certain type of component. You recently built one for another project. Extracting it is a piece of cake but how are you going to share it between the two apps?
---

Suppose you need to build an app which uses a certain type of component, let's say a map. You recently built a fairly reusable one for another project. Extracting it is a piece of cake but how are you going to share it between the two apps?

![Sharing](/img/sharing-client-side-components-with-bower/sharing.jpg)
*Image by [Niklas Wikström](http://www.flickr.com/photos/niklaswikstrom/5214708665/)*

Enter [Bower](http://bower.io), the client-side package manager. Bower is installed with npm:

**npm install -g bower**

Bower works in a way familiar to npm users. Dependencies are listed in a json file and installed to a project subdirectory (bower_components). Bower commands are also familiar to npm users: **init, install, update** etc.

Bower has a central registry that contains most common client side libraries and frameworks. It can also be used without publishing your code to the registry, here's how.

## An awesome map
Let's name our component awsumap. This is awsumap's bower.json file. Bower creates one for you if you say **bower init**.
Note the _main_ property which is used by some tools, in this case [Browserify](http://browserify.org). The property ```private: true ``` prevents accidental publishing to the bower registry. The rest of the syntax is explained [here](https://github.com/bower/bower.json-spec).

```javascript
{
  "name": "awsumap",
  "main": "awsumap.js",
  "version": "0.0.1",
  "private": true,
  "ignore": [
    "bower_components"
  ],
  "dependencies": {
    "leaflet": "0.7.2"
  }
}
```

The rest of awsumap lives [here](https://github.com/mprencipe/awsumap).

## Dealing the goods
Awsumap already has a home, but can Bower find it? What other places does Bower look into when searching for packages? Besides publishing packages to the Bower registry we can share packages by referencing them via the file system or pulling them from a git repository.

File system references don't allow you to specify a version. In this mode Bower always fetches the newest available version. Be sure to bump the version on an update though. Here is an example of a file system reference from some map app's bower.json file:

```javascript
{
	"name": "somemapapp",
	...
	"dependencies": {
		"awsumap": "../common/awsumap"
	}
}
```

When pulling packages from a git repository Bower uses git tags (e.g. 1.0.0, 1.0.1) to determine the specified version for a dependency. This offers nice fine-grained control if projects use different versions of your component. The git repository can be local or remote, e.g. GitHub. Here's a git repository reference:

```javascript
{
	"name": "somemapapp",
	...
	"dependencies": {
		"awsumap": "https://github.com/mprencipe/awsumap.git#0.0.1"
	}
}
```

## Bundleweed magic
Browserify allows you to require() files. It then creates a bundle based on abstract syntax tree magic.

![Browserify](/img/sharing-client-side-components-with-bower/wizard.jpg)
*Image by [TheGiantVermin](http://www.flickr.com/photos/tudor/9201416844/)*

**Browserify transforms** process source code before parsing it for require() calls. A useful transform is [debowerify](https://github.com/eugeneware/debowerify) which uses the _main_ property in bower.json files to determine the correct file to be included in the bundle. This allows us to simply write ```require('map');``` in our app. Awsumap's dependency on Leaflet is handled correctly by Browserify and debowerify.

[An example app](https://github.com/mprencipe/somemapapp) can be found on GitHub.