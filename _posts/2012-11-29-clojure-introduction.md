---
layout: post
title: Clojure introduction
author: timole
excerpt: This is a short guide for getting familiar with Clojure programming language and its basic development tools. This article is targeted to the students at TAMK that participated the visiting lecture on Thu 29.11.2012. Please feel free to ask questions, if you have any problems setting up Clojure.
tags: episerver cms TUT
---

This is a short guide for getting familiar with Clojure programming language and its basic development tools. This article is targeted to the students at TAMK that participated the visiting lecture on Thu 29.11.2012. Please feel free to ask questions, if you have any problems setting up the Clojure development environment.

### Let's install Eclipse with Clojure support ###

1. Download [zipped Eclipse with Clojure support](/files/eclipse-4.2-classic-with-clojure.zip)
2. Unzip the package and start Eclipse by double-clicking **eclipse.exe**
3. Choose a location for the workspace. It can be any directory and will contain the source files.
4. Create a new Leiningen project by choosing **File -> New -> Leiningen Project** and give it a name like "testi" or anything. (Leiningen is a build tool built on top of Maven)
![new-leiningen-project](/img/clojure/new-leiningen-project.png)
5. Close the welcome screen and navigate to testi -> src -> testi -and open file **core.clj** by double clicking it.
6. Edit the file as follows:
{% highlight clojure %}
(defn -main
  "This is my Hello, world!"
  [& args]
  (println "Hello, World!"))
{% endhighlight %}
7. Run code by clicking right mouse button -> Clojure -> Load File in REPL
8. Type the following expression to the console below:
{% highlight clojure %}
(-main)
{% endhighlight %}
9. Congratulations, Hello world works! Now type another expression like the following: (+ 1 2)

### Follow a video on how to code Clojure ###

We started a Clojure project at Solita a couple of months ago. We held some introduction sessions and recorded them on video. We thought that someone else could also find them useful and thus put them to YouTube. The guy teaching us Clojure on the video is [Jari Länsiö from Metosin](http://metosin.fi/). Thanks Jarppe for sharing your knowledge on Clojure! 

<iframe width="720" height="405" src="http://www.youtube.com/embed/Q6c8We-WMkk" frameborder="0">    </iframe>

See also a couple of other videos made by Jarppe: [Clojure gently part 1](http://www.youtube.com/watch?v=dQ6hhnitzHg) and [part 2](http://www.youtube.com/watch?v=LZ4H_oczIt4).

Congratulations, you have now familiarized yourself with Clojure! I would like to hear your comments on the material. How could we improve it? What kind of topics are you interested in?
