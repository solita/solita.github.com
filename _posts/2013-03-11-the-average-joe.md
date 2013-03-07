---
layout: post
title: How to make an average image of people faces?
author: ruoat
excerpt: I wanted to check what an average Solita employee looks like. I had images of all Solita employees' faces, OpenCV-library, Python and some free time.
tags: opencv python solita
---
[OpenCV](http://opencv.org/) is an open source computer vision and machine learning software library. It has interfaces for C/C++, Java and Python. First I wanted to test the library with Scala but encountered some problems so I chose to fiddle with Python. Later I found that the problems probably were caused due bad (not existing) error messages in OpenCV and classpath problems.
I have not much experience in Python but the samples provided seemed to be simple enough so I could get some results quickly.

### How it works ###
At first the program reads images with specified pattern. It detects positions of eyes and calculates their average positions. In the second phase images are scaled so that the distance of the eyes in the image matches those average values. When the scaling is done eye positions are detected again.
Then images are moved to correct position so that eye positions match the average ones. Each image is then summed to the average image and result is written to disk.
Because the eye detection algorithm provided by OpenCV does not always find two eyes from the input image some images are ignored. The detection might not work if the person has eyeglasses, hair in the front of eyes or partially closed eyes. 

### And the average Solita person looks like... ###
By checking statistics we find that the average age of Solita employee is 34 years and five months. She has been working 54 months at Solita. We have 82 % of men and 18 % of women in our staff so the result looks like androgyne.
In Finnish there are some forenames, which can be given to both boys and girls. One of them is [Kaino](http://fi.wikipedia.org/wiki/Kaino). So I call the result person as Kaino Solita. And this is how (s)he looks like when 140 faces were successfully processed.
[![kaino_solita](/img/the-average-joe/small/average_solita_140.jpg)](/img/the-average-joe/average_solita_140.jpg)

### Try it yourself ###
Grab the [sources](https://github.com/ruoat/averageface) and try it yourself. I have used high quality images with the size of 787x1181 pixels. If you want to use lower quality or smaller images you may want to tweak parameters in detectMultiScale function to improve the eye detection.
After I had created the the tool I found that there are some tools, which are more [sophisticated](http://faceresearch.org/demos/average) in merging faces but I had some fun when coding it by myself! :)