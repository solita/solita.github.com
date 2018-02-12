---
layout: post
title: Why are deep learning models so popular?
author: jessevuorinen
excerpt: Thoughts on why deep learning models are popular, and some tips on how to get started with them.
tags:
- data science
- neural network
- supervised learning
- artificial intelligence
---

Deep learning (i.e. big neural networks) plays a central role in the ongoing boom of artificial intelligence and data science. Last year, a partly neural network based AI beat a human grandmaster for the first time in Go, a complex board game. Judging by the hype, it feels like deep neural networks can be found in every other state-of-the-art AI solution. In practice they have their downsides, but although they are not the be-all-end-all of machine learning algorithms, neural networks are versatile and useful. In our client projects, we have leveraged deep learning in image recognition and multivariate time series forecasting tasks, for example. What qualities make neural networks efficient?

On a high level, a neural network (and most other supervised machine learning algorithms) can be seen as a device that takes in numerical inputs and spits out numerical outputs. When the model is built, the general structure of what is inside the device, as well as the structure of its inputs and outputs, is specified. At this point, the model already "works" in the sense that it can take inputs to produce outputs, but the results are random. 

Then, the model is trained by continuously feeding it with actual data, that is, correct answers to the problem at hand. During this training process the parameters of the model (the bolts and cogs inside the device) are adjusted in very small increments. In time, the algorithm converges and learns the relationships in the training data. In the end, the model learns how to map input data to outputs using a similar logic that underlies the training data it was fed. After training, the model can be used to make predictions based on new input data, something that the model has not seen before.

## What goes in, what goes out?

The inputs to the device could be virtually anything that can be represented as arrays of numbers: images, time series data, videos, free text articles after being transformed into numerical representations, you name it. The outputs can also take various shapes. 

The output could be a single number, say a weather forecast on a given hour. Or it could be an array of several figures, like the pixel coordinates of an identified suspected cancer in an x-ray image received as input. 

The end result does not even have to be numeric, even though a neural network only crunches numbers. For example, the network can produce an array of likelihood estimates that are converted into a categorical classification in the end. Given a picture, the model could say it is a cat with 80 % certainty, a dog with 15 % certainty or a car with 5% certainty. Although almost anything can be represented in numerical format in some manner, deciding how the numerical representations of the inputs and outputs are actually done is usually not easy. This preprocessing step is an important part of the data science workflow.

## Anatomy of a neural network

In the case of neural networks, what is inside the device is a large amount of interconnected simple processing units called neurons. A neuron takes a number, squeezes it through some non-linear function and then outputs the result. In a deep neural network, the neurons are organized into layers that succeed each other. The input signal is first sent to the first layer of neurons, which send their outputs to all the neurons in the next layer. This process continues layer after layer until the output layer is reached. The construct is inspired by biological neurons, the main components of the central nervous system.

The connections between neurons are also given so called weights, which are basically little valves that determine how much of each input the unit propagates up the network. Adjusting these weights is what actually happens during the training process and what allows neural networks to fit specific problems. A deep neural network could contain millions of weights, so the good news is that adjusting the weights can be automated efficiently (using backpropagation and gradient descent methods).

## Advantages of neural networks

The idea of training a machine to transform numerical representations of inputs to outputs applies to most machine learning models, so what makes neural networks work special? Three reasons come to mind.

First, the structure of a neural network is specified only very broadly before the model is trained, which gives a lot of room for the model to adjust during training. In statistical terms, large neural networks can be thought of as being somewhere in between parametric and nonparametric models. In a parametric model, for instance a traditional regression, the number of parameters in the model is strictly determined before fitting the model. In a nonparametric model, the model structure is determined more broadly, and the training process can adjust the number of parameters as well as their values. Thus, in a nonparametric model, there is more freedom for the model structure to adjust to the problem being solved. In neural networks, the number of parameters (weights) is strictly determined beforehand, which would imply that they are parametric models. However, the number of weights can be enormous and the training process could allow many of the weights to zero out, effectively blocking certain paths through the network. For these reasons, deep and broad neural networks resemble nonparametric models in practice. The nonparametric nature gives neural networks structural freedom to adapt to many kinds of problems. 

Second, since neural networks consist of chained little functions that perform nonlinear transformations at each step, they are inherently nonlinear models. This allows them to model many problems better since many real-world relationships are nonlinear. (For example, the area of a square shaped field increases exponentially instead of linearly as its width increases.)

Third, the vanilla version of a neural network that has been discussed so far can be adjusted to make it a better fit to certain problems. Convolutional neural networks, for example, are good at making broad abstractions from very detailed inputs and work especially well for image recognition problems. In recurrent neural networks, the neuron layers have feedback loops, which essentially means that the network is able to remember previous inputs. This trait makes them a good fit for time series forecasting and natural language processing. 

Advanced deep learning models - the ones that are used in solutions that are able to beat humans in complex games or drive vehicles - combine these basic architectures. For instance, the model could begin with convolutional layers that are good at abstracting information. This network could be followed by a recurrent network that has a memory and the ability to learn sequential and spatial relationships. Finally, a regular fully connected layer could produce the final output.

## The downsides

If deep learning is so powerful, then why don't we dump all other machine learning algorithms in their favor? One of the biggest caveats of neural networks is the fact that they are black boxes: it is usually impossible to intuitively explain why a neural network has given a certain prediction. Sometimes, the intermediate outputs that the neurons produce can be analyzed and explained, but many times this is not the case. Other algorithms, such as traditional linear models or tree-based models like random forest, can usually be analyzed and explained better.

Another downside is that neural networks need large amounts of training data and can take a long time to learn. This was a huge problem in the past but has been mitigated somewhat by technological advancement. One of the reasons for the surge in deep learning's popularity can be attributed to improvements in GPU computational power and the advancements of cloud computing. Today, it is possible to train complex deep learning models in a matter of hours, not weeks.

## How to get started?

Even though they are technically formidable when you dive into details, neural networks are not that hard to experiment with. A good way to get your hands dirty, if you know Python or R, is to first google and follow through hands-on coding tutorials, like [this one](https://machinelearningmastery.com/tutorial-first-neural-network-python-keras/). It is also a good idea to register into www.kaggle.com and build a neural network solution to one of the simpler problems, say, "Titanic: Machine Learning from Disaster". 

Once familiar with the basics, try something a little more advanced by following along these inspiring blog posts, for example:
* [Digit recognition using a convolutional neural network](https://yashk2810.github.io/Applying-Convolutional-Neural-Network-on-the-MNIST-dataset/)
* [Text generation with recurrent networks](http://karpathy.github.io/2015/05/21/rnn-effectiveness/)
* [Time series forecasting with a recurrent network](https://machinelearningmastery.com/time-series-prediction-lstm-recurrent-neural-networks-python-keras/)
* [Using deep reinforcement learning to teach an AI to play a simple game](https://keon.io/deep-q-learning/)
