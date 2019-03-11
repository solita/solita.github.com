---
layout: post
title: Code quality inspection for Clojure using SonarQube  
author: hjhamala
excerpt: Clojure has good libraries for code quality analyzing and vulnerabilities detection. I introduce the support for Kibit, ancient-clj, lein-nvd and Cloverage in existing Clojure SonarQube plugin. 
tags:
- SonarQube
- Clojure
- ClojureScript
- Code quality
- Vulnerabilities detection
- Continuous inspection
---
Building good and secure code has never been easy. Programmers make mistakes during development. Programs use external libraries which may contain bugs and vulnerabilities. New vulnerabilities are revealed constantly which enforces patching existing programs.

Software development has many ways to battle against bugs. For example testing, code reviews and pair programming can help us to make better and safer programs. Fortunately we may also use code analyzers which automate the testing and vulnerability finding.

[**Clojure**](https://clojure.org/) is not immune to bugs or vulnerabilities. Clojure being a dynamic language leads to situations where some problems may occur at runtime which in static languages are found out at compile time. The Clojure community has produced many useful tools such as linters and security scanners.

## Clojure code quality tools

### Eastwood
[Eastwood](https://github.com/jonase/eastwood) is a linting tool for Clojure (no CLJS support) which detects many kinds of potentially problematic code. 

For an example the following Clojure code contains a potential bug:

```clojure
(if (and x)
  (foo))
```

When running `lein eastwood` it produces next result:
```
== Eastwood 0.3.3 Clojure 1.8.0 JVM 11.0.1
Directories scanned for source files:
 src test
== Linting clojure-sonar-example.core ==
Entering directory `/Users/heikkiha/src/sonarqube/clojure-sonar-example'
src/clojure_sonar_example/core.clj:3:5: suspicious-expression: and called with 1 args.  (and x) always returns x.  Perhaps there are misplaced parentheses?
```
 
Eastwood may find false positives. Fortunately, it is possible to suppress linter rules which may find any false positives.
 
### Kibit
[Kibit](https://github.com/jonase/kibit) is a static code analyzer which detects code that can be rewritten with a more idiomatic function or a macro. It supports also ClojureScript. 

Example: 

```clojure
(> x 0) 
```

`lein kibit` produces the following result:

```
At src/clojure_sonar_example/core.clj:13:
   Consider using:
     (pos? x)
   instead of:
     (> x 0)
```

I think Kibit is good advice for beginning Clojure programmers but it contains some good advices for more experienced developers also. 

### Cloverage

[Cloverage](https://github.com/cloverage/cloverage) is a code coverage tool for Clojure which runs the tests of a program 
and calculates line and form coverage for namespaces. 

Sample output looks like this:

|                    Namespace | % Forms | % Lines |
|------------------------------|---------|---------|
|foo.bar                       |   70.00 |   84.62 |
|foo.baz                       |   94.61 |   96.89 |
|foo.config                    |   60.71 |   80.65 |
|foo.router                    |   31.75 |   69.62 |
|foo.login                     |   68.67 |   82.76 |
|foo.util                      |    2.89 |   20.00 |
|------------------------------|---------|---------|
|                    ALL FILES |   67.36 |   82.93 |


### Lein-nvd

[Lein-nvd](https://github.com/rm-hull/lein-nvd) is a dependency-checker plugin whichs checks JARS in the program's classpath with known vulnerabilites against 
the [National Vulnerability Database](https://nvd.nist.gov/). 

Output of Lein-nvd gives status of the JARs with found vulnerabilities:


| dependency             | status|
|------------------------|-------|
| bcpkix-jdk15on-1.58.jar | OK    | 
| bcprov-jdk15on-1.58.jar| CVE-2017-13098, CVE-2018-1000180, CVE-2018-1000613|

It should be noted that Lein-nvd does not tell exactly which direct or transitive dependency pulls a vulnerable JAR file. Most time JAR name matches a dependency. The full dependency tree can be inspected by running the `lein deps :tree` command.

### Ancient

[Ancient-clj](https://github.com/xsc/lein-ancient/tree/master/ancient-clj) is a plugin to check your project for outdated dependencies and plugins and  suggest updates. 

Sample output looks like this:

```
[ring "1.7.1"] is available but we use "1.6.3"
```

Ancient can be started with command `lein ancient upgrade :interactive` which gives the option to decide one by one if the upgrade is made or not. The upgrade also runs tests and persists the changes only if the tests run correctly. 

Ancient cannot analyze if the new version is backwards compatible or not. Many libraries uses semantic versioning major.minor.patch (1.2.3) where minor (1.**2**.3) and patch (1.1.**2**) version changes should be backwards compatible. Whether this is really the case can differ.


## Consolidating code quality and vulnerability findings using SonarQube

[SonarQube](https://www.sonarqube.org/) is a code inspection tool which supports many currently used languages like Java, Python, C++ out the box . SonarQube server has a browser GUI for browsing the findings.

![SonarQube GUI](/img/code-quality-inspection-for-clojure-with-sonarqube/sonar-results.png)

SonarQube unfortunately doesnt have out of the box support for Clojure. Fortunately SonarQube can be extended to support more languages with plugins. 

There have been many different Clojure plugins for SonarQube but most of them have not been maintained and don't work with newer versions of SonarQube. When I started to look for SonarQube plugin the only working one was [plugin](https://github.com/fsantiag/sonar-clojure) made by Felipe Santiago. The plugin only supported Eastwood based linting.

Because the plugin was open sourced and the maintainer was active I made the necessary changes to the plugin which added support for Kibit, Cloverage, Lein-nvd and Ancient which are now merged. The plugin has also a minimal SonarQube docker image file for testing the plugin locally. 

### Running SonarQube locally
* Install Docker if not installed earlier
* Clone the source `git clone https://github.com/fsantiag/sonar-clojure`
* Run `start-sonarqube.sh` which builds the plugin with Maven, creates a new docker SonarQube image with plugin copied on to it and finally starts the SonarQube.
* Open http://localhost:9000 to check that SonarQube works correctly. Use admin/admin as the administrator password.
* Download SonarQube client from [https://docs.sonarqube.org/display/SCAN/Analyzing+with+SonarQube+Scanner](https://docs.sonarqube.org/display/SCAN/Analyzing+with+SonarQube+Scanner) and install it to path.

### Changes to Clojure application

Use an already existing application or clone a sample application with existing vulnerabilities and code smells `git clone https://github.com/hjhamala/sonar-clojure-example`.

Create a sonar-project.properties file in the root folder of your app:

```properties
sonar.projectKey=your-project-key
sonar.projectName=YourProjectName
sonar.projectVersion=1.0
sonar.sources=src,project.clj
sonar.clojure.lein-nvd.json-output-location=target/nvd/dependency-check-report.json
sonar.clojure.cloverage.json-output-location=target/coverage/codecov.json
```

Add following dependencies to project.clj or user profile file:

```clojure
:plugins [[lein-ancient "0.6.15"]
          [jonase/eastwood "0.3.3"]
          [lein-cloverage "1.0.13"]
          [lein-kibit "0.1.6"]
          [lein-nvd "0.6.0"]]
```

Run `sonar-scanner` in the root folder of the project.

Open a web browser in http://localhost:9000/dashboard?id=your-project-key

You should see something like this:

![Example Dashboard](/img/code-quality-inspection-for-clojure-with-sonarqube/example-dashboard.png)

Opening project.clj shows vulnerability findings and outdated dependency warning:

![Project vulnerabilities](/img/code-quality-inspection-for-clojure-with-sonarqube/project-vulnerabilities.png)

Core.clj has findings from Kibit, Eastwood and code coverage from Cloverage:

![Bad Smell Code](/img/code-quality-inspection-for-clojure-with-sonarqube/smell.png)

## Limitations of the plugin

The SonarQube plugin currently marks all the found vulnerabilites to the first line of project.clj because the lein-nvd only returns JAR name not the dependency which pulls it directly or transitively.

Only line coverage is supported by SonarQube and the calculation seems to be somehow different compared to Cloverage itself by few percents.

Clojure language parser for Sonarcube has not been implemented. This means that for example syntax highlighting does not currently work. I have a work in progress for adding the [syntax highlighting](https://github.com/hjhamala/sonar-clojure/tree/syntax-highlight-and-tokenization) and hopefully this can be added to the plugin very soon.

## Future improvements

Current version of the plugin is a native Java plugin which invokes Leiningen to analyze source code once per sensor. Running Leiningen takes few seconds per a sensor. Instead of invoking Leiningen we could make a native Clojure plugin which includes the analyzing libraries. This would make running the analyzers very much faster because multiple Leiningen invocations are not needed any more. Also the need to install Leiningen plugins with correct versions is no more needed. 

Following improvements should also be considered as well:

* Cloverage form coverage could be added as custom metric to files. 
* Lein-nvd vulnerabilities could be mapped to correct dependency and namespaces requires. This can be made by generating full dependency tree and trying to match the JAR name with dependencies.
* Dead code detection could be added with [yagni](https://github.com/venantius/yagni)
* [Spectrum](https://github.com/arohner/spectrum) analyzator support should be considered when the project matures.

Plugin source code:
[https://github.com/fsantiag/sonar-clojure](https://github.com/fsantiag/sonar-clojure)
