---
layout: post
title: Reinforcement Learning With Deepracer
author: arto
excerpt: >
  Machine Learning is a wide field, and Reinforcement Learning is a very interesting part of it. I chose to learn something new by starting to train a Deepracer car to autonomously drive around a track, as fast as possible. This blog tells how I got started with AWS Deepracer, and what I learned about reinforcement learning.
tags:
 - Software development
 - AI
 - Machine learning
 - Competence development
---

![AWS Deepracer car with stereo vision](/img/reinforcement-learning-deepracer/deepracer_without_shell.jpg)
*AWS Deepracer car with stereo vision*

So, we've got a new toy. This one is called Deepracer, although my nickname for it is Diddy. It's a 1/18th scale race car that can learn how to navigate a racetrack, without any human intervention. I've spent a bit of time with it now, as have some of my colleagues, so wanted to write an article on my experiences.

## What is reinforcement learning?

Machine learning is a wide field with lots of different subtopics. One of the most interesting subtopics for me is reinforcement learning. It's a form of unsupervised learning, which means that the idea is not to teach a car how to drive but to teach it **how to learn how to drive**. It's not unlike training a puppy. You let it dwell in the inherent chaos, but keep a good feedback loop going, so you can reward it for making good decisions. Eventually the trainee, in this case Deepracer will learn to associate good input (state) with good decisions (actions) that further its goal: the ability to navigate a racetrack fast.

What fascinates me in reinforcement learning is that we as humans are used to expert rules system: We think we can see which actions produce favorable outcomes. And often we do, we're very good at that. This is how old-school hierarchical management works: Based on your superior experience, you tell how things should be done - even micro-managing things to get the details in. But that's a very rigid way of thinking - and makes also an assumption that the expert rule is so far optimized, there's nothing left to learn or to improve, and also idea is that one size fits all: For a new situation, new expert rules are needed, because there's no adaptation. By the way, you cannot do this with dogs, because they wouldn't understand your explanation, and would not be automatically motivated to follow it.

With the reinforcement learning approach, we take a bit of a different viewpoint, with the keywords being adaptation, learning, and reward. And because it's unsupervised, now and then we can learn something new from that data, too.

In a nutshell, this is how you do it with a dog:

- Dog is playing randomly in the backyard, doing dog things
- You add a bit of stimulus, for example, a sound, a visual stimulus, or both, trying to activate the dog towards doing something. For example: fetch, bark, stay in place, or run. This would be the state the dog is observing, with its sensors, eyes, and ears.
- When it does things that you don't want it to do, you ignore it. When it does useful things that you want it to perform, you immediately reward it.
- In essence, you are reinforcing good actions as a response to the specific stimuli/state. Eventually, the reward is not even needed, at least not every time, as the dog has learned what you want it to do.

Have to say, in real life, dogs often have no clue what you want, so you would typically alter the order of things above slightly. When a dog sits down, you give it a treat and repeat the audio stimulus you want to associate. Dogs will happily inject chaos into the system, doing quite random things first, and learning from it.

This is different from the machine learning version because due to the processing power we have these days, we can run simulations in **parallel**, eventually one will figure out the right thing to do even without any human intervention. Once the training process finds one right thing from the chaos and gets a reward, it can start favoring that action and refining to get a bigger reward. We can also leverage the modern cloud platforms, the massive computing power at our fingertips, to accelerate the learning process, using simulations to run multiple scenarios even in parallel, and in **accelerated time**.

Here is a bit more technical explanation of the reinforcement learning for the Deepracer:

- You have a model of the environment, but it's not straightforward to 'solve' the problem, especially if you want a model that would adapt to any racetrack easily.
- We have an agent, that can act in said environment. Agent must have some kind of input (for example camera feed), some kind of output (for example steering angle and speed), and some kind of memory, to keep track of favorable actions.
- We also need a reward algorithm for the training. The reward algorithm decides how to interpret the environment, for example: is the car on the track? How far is it from the centerline? What's its current speed?
- Based on the environment state, the reward algorithm will assign rewards of varying sizes, based on how well the agent is doing.
- Reward function is only used for training the model, so once we have evaluated the model to be good enough, and we start using it, the reward function is forgotten - until the next time we want to train some models.
- A suitable amount of chaos aka randomness is injected first into actions, so the actor will start taking random actions, to trigger the reward function evaluation. 
- From there, the training will combine a bit of chaos, and a lot of previous learnings, and keep note of which action for which state brings the best rewards.
- Training typically also contains evaluations, so you can focus on the best performing models.

## What is AWS Deepracer?

AWS Deepracer is many things. It's an AWS service you can use (for a cost). It's a physical scale model car you can drive on a physical track. It also is associated with Deepracer league, and community, where you can race your models, should you choose to do so. Races happen both virtually, and sometimes also on physical racetracks. Therefore it's also a sport, you can participate in. There are even significant rewards for the best racers, every year.

It was designed to be a fun entry to machine learning and AWS services, similar to Deeplens, and Deep Composer initiatives. So it's a great way to learn about machine learning and AWS, and have some fun.

Underneath the Deepracer service, there are several more basic AWS services like IAM, S3, and Sagemaker notebooks. The Robomaker service is used for the simulation environment. All these services can also be used directly for training, and there's even a local environment where you can use these as containerized services, without running anything in the cloud. Perhaps more on that in a future blog.

We decided to get one physical scaled-down car, mostly for the fun factor. This is a new model, with stereo vision, and a Lidar sensor, to be able to understand its environments better than before. Having these available opens up new modes for the car. Old cars can only do time trials, but with stereo cameras and Lidar, it's also possible to do obstacle avoidance or even race with multiple cars on the track simultaneously.

![AWS Deepracer car with Lidar on top](/img/reinforcement-learning-deepracer/deepracer_with_shell_side.jpg)
*AWS Deepracer car with Lidar on top*

In theory, there's a possibility to set up a racetrack somewhere and try some time trials and even obstacle avoidance one day. We'll see..

## Why is it fun?

As mentioned, it's a great way to learn something new, and that's always fun. It attaches to the sports part, which some people, including me, enjoy a lot. You can test how good a model you got, vs others. It's a bit of creative coding because there are many variables to nudge and tweak. It's not all about the reward algorithm, it's also about the hyperparameters, and your ambition level - is your model the fastest on a good lap? Or a consistent, robust model that can always handle the track? Or is it a general-purpose model that can be used against multiple tracks?

![Deepracer Virtual Racing](/img/reinforcement-learning-deepracer/deepracer_video.gif)

The tracks themselves also keep on changing, so to get the best results, you need to be able to adapt, even your old superior models, to the new environment. And obstacle avoidance makes things much more interesting and dynamic - a tiny boulder on the track can become a huge obstacle some models never learn how to avoid.

As with many things, this one is also best shared with friends. We decided to do a bit of Deepracer training mostly to get a good excuse to sit down with friends, and share some pizza. I'm also right now sharing this with you, the reader, in hopes you find it interesting, and perhaps a small spark ignites today because of that. There's also a global Deepracer Community - I'll drop the link at the end of this article - who's been doing this for years, and are very friendly.

![Deepracer April 2022 Qualifier](/img/reinforcement-learning-deepracer/deepracer_qualifier.jpg)

The racing part is also a bit addictive, due to competitiveness. There are constantly virtual races going on, pretty easy to attend with your own models. If you climb to the top 10 in the open track results (quite a feat by the way), you can enter the pro races, with more challenging tracks and setups. And best of the pro racers then move on to AWS re:Invent for the really big races.

## Why is it useful?

The idea was to pick something that would unlikely be part of our customer projects, or customer needs, just for fun. It leaves more artistic freedom to play with it, as you like, simply focus on the fun of learning.

That being said, there's a huge demand for people who understand the cloud services well, and even though Deepracer is just a toy, it's still a great way to learn about the AWS services. In fact, it's essential to learn at least a bit of them. While services like IAM, S3, and Sagemaker have everyday uses, the Robomaker environment is a bit more exotic, which might be fun to learn as well.

Additionally - who's to say there would not be customer demand in this area, too? That might be a happy accident. Perhaps someone wants to train an autonomous bot, car, or drone to deliver food, purchases, and supplies. Or challenge Tesla at their own game. Or build automated systems to pick up people's shopping carts from shelves, and put them in delivery boxes. The future will bring more autonomous systems, and people who are experienced enough to be able to make them robust and safe are always in demand. And this is a great way to start that path.

## What have I learned so far from this?

I used to race with Deepracer some years back, then life happened, and had a bit of a break there. Now that I decided to resurrect my old interest, it's been fun to see it's still much alive. Some new things have also happened: The local training has become more viable and easy to get started with. And the new obstacle avoidance mode has been added. Obviously, many more tracks are available.

Last time I was training I used a combination of an Ubuntu machine with a great graphics card, and sometimes the AWS console services. This time I was happy to see that I can also do local training with Windows, WSL2, and a Docker installation, and it works great also with the AWS console. So I can train a model locally, once it's good enough, I can refine it in the AWS console, and race with it. This is a very cost-effective way to have some fun.

Other insights. As a coder, I've been very fixated on the reward algorithm. Now I'm also trying to understand the hyperparameters, and action space, a lot better. Some experiments I've been running:

- Custom action space where the fastest speeds do not include dramatic turns: I noticed when you increase the speed a lot, the car starts to spin due to simulation physics. I can customize allowed turn angles in the action space, allowing tighter turns only for the slower speeds.
- I'm also pumping up that speed, trying to find the limit where it starts to be hard to make the model stable. Right now that's around 4m/s speed, which is the fastest I've ever tried before.
- I've been dabbling with the hyperparameters a bit, and I'm trying to find the best combination of them. To be honest, the measurable effect for me is not very consistent nor very dramatic.
- I've been practicing retraining the models and learning the rules for that. It allows to take a model that performs well on one track, and retrain it against a new track. I need to learn how to get the settings right so it makes sense.
- Overfitting is also a thing. Models do not get better and better eternally the more you train them. Typically sweet spot is around 3-5 hours I hear. It depends of course on your training environment.
- I've been learning how to use the Jupyter notebooks in local training mode. They are much richer than the ones in the AWS console, and the sky is the limit to insights you can get that way.
- I've set up the physical car, but haven't got - yet - to building even a short track for it. Perhaps one day...

## Where will it go from here?

- I've been putting the focus on local training mode. I still have things to figure out there.
- I'm using CPU training mode for now, as it's simpler to set up. If I got GPU training mode working with my RTX 3080...
- Getting a good handle on hyperparameters would rock
- Some other people in Solita are also working on this, learning and having fun. So if we get some interesting models, we might even build that track one day, and race it out.
- I haven't started obstacle avoidance yet, but I think that would be interesting, both in the virtual world and on a physical track with a physical car. I plan to play with that too before I am done.
- I found a great way to train a model by using, instead of the current position, the position of where the car is going next - this gives better control of where the car's nose is pointing. But this algorithm also goes only so far - it's great to get a great model fast, but then needs to be supplemented with something else. I'm investigating having some memory of benchmarks to beat, to make it remember to focus on speed too.

I hope this was a fun read for you, this has been a very fun and interesting journey for me. I truly anticipate more of this kind of algorithm training in the future, much much more, so it's fun to stay a bit up to date with what's going on. Stay tuned for more interesting dev blogs on this same channel! And perhaps I see you in the virtual Metaverse races somewhere in 2030 or 2040!

## Links and refs

- [AWS Deepracer](https://aws.amazon.com/deepracer/)
- [Deepracer Community](https://github.com/aws-deepracer-community)
- [Deepracer Slack Community](https://deepracing.io/)
- [Deepracer Local Training](https://github.com/aws-deepracer-community/deepracer-for-cloud)
- [Deepracer League](https://aws.amazon.com/deepracer/league/)
