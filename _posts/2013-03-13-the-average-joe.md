---
layout: post
title: Our Faces Combined
author: ruoat
excerpt: I wanted to check what an average Solita employee looks like. I had images of all Solita employees' faces, OpenCV-library, Python and some free time.
tags: 
- OpenCV 
- Python
---
When a new person joins Solita, they naturally get their photo taken. Recently, we had a company-wide staff photo update, where all the photos were taken in a standardized environment and the resulting photos all have identical lighting, colors, etc. This springed an idea: I could combine the photos and see what an average Solitan would look like.

First I tried to use [ImageMagick](http://www.imagemagick.org) to make an average image, but the result was blurry because people faces weren't perfectly in the same position.

After a brief googling I found [OpenCV](http://opencv.org/). OpenCV is an open source computer vision and machine learning software library. It has interfaces for C/C++, Java and Python. First I wanted to test the library with Scala but encountered some problems, so I chose Python instead. Later I found out that the problems were probably caused by bad (non-existing) error messages in OpenCV and classpath problems.

I don't have a lot of experience in Python but the provided samples seemed simple enough so I could get some results quickly.

### How it works ###
First, the program goes through all images, locates the eyes and calculates their average positions. In the second phase, images are scaled so that the distance of the eyes in the image matches those average values. When the scaling is done eye positions are detected again.
After scaling, the images are moved to correct position so that eye positions match the average ones. All the images are then combined to form the average image and result is written to disk.
Some images are ignored, because the eye detection algorithm provided by OpenCV does not always find two eyes from the input image. The detection might not work if the person has eyeglasses, hair in the front of their eyes or partially closed eyes.

### And the average Solita person looks like... ###
By checking statistics we find that the average age of Solita employee is 34 years and five months. He/She has been working 54 months at Solita. In our staff, 82% are men and 18% women, so the resulting image depicts an androgynous person.
In Finnish there are some names, which fit both boys and girls. One of them is [Kaino](http://fi.wikipedia.org/wiki/Kaino). So I call the  result person as Kaino Solita. And this is how (s)he looks like when 140 faces were combined.
[![kaino_solita](/img/the-average-joe/small/average_solita_140.jpg)](/img/the-average-joe/average_solita_140.jpg)

### Try it yourself ###
Grab the [sources](https://github.com/ruoat/averageface) and try it yourself. I used high quality  (787 x 1181 px) images. If you are using low(er) quality/smaller images, you may want to tweak the parameters in `detectMultiScale` function to improve the eye detection.
After creating this "face combiner", I found out that there are some tools which are more [sophisticated](http://faceresearch.org/demos/average) in merging faces. Still, I had some fun coding it by myself! :)
