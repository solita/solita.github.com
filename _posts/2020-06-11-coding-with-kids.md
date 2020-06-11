---
layout: post
title: Coding with kids
author: Rinorragi
excerpt: Sharing my experience about teaching my kids to code
tags:
- programming
- parenthood
- Electronics
- Python
- Scratch
- PowerShell
- Roy
---

## Forewords

I have always loved to tinker with robotics, electronics and software with hacker mentality. Break something to figure out how it works. Build something with the knowledge you have gathered. Play with the things you have created. With kids I have tried to combine the things I love to do with the people I love to be with. This blog is not about making kids professional developers but more of a showcase of what we have done. I hope that this encourages people to try something similar with their children.  

Most of the code is not my own but I have permission to share it. No children has been harmed (hopefully, we will see that later) in the process.

## How it all started with Turtle Roy

My firstborn was four years old and she could not read. I thought that I might go and try to teach her some coding before reading. I asked her if she wants to teach computer to draw. Then I opened up [Turtle Roy](https://turtle-roy.herokuapp.com/) and let her choose the shape of the turtle (of course the princess). I showed her that we could draw a flower with princess. 

```
clear
setshape "princess-large"
let halfleaf = repeat 20 (sequence[fd 4, lt 1])
let leaf = sequence[halfleaf, lt 150, halfleaf]
let flower = repeat 36 leaf
flower
```
![Roy princess](/img/coding-with-kids/roy-princess.png)

Finally I printed out the commands for her and make some own markings to them and let her try to draw. Of course at age of four she was nowhere near in using variables or making functions but she had fun time with commanding the turtle to draw something with `fd`, `lt`, `rt` and `color`. We did this few times and she was happy to spend a total of several hours in the world of Turtle Roy. Unfortunately I have not saved the code pieces she draw back then. 

Definitely a fun and cheap way to test out if children are into programming. 

## PowerShell as a babysitter

I will not lie. I love PowerShell. I love it so much that I tried to teach it to my firstborn. I made a small function that speaks aloud given outputs and stored to my PowerShell profile `$PROFILE.CurrentUserAllHosts`.

```powershell
function Speak-Aloud
{
    [CmdletBinding()]
     param(
         [Parameter(Mandatory=$true,ValueFromPipeline)]
         [string]$textToSpeak
     )
    Write-Host $textToSpeak
	Add-Type -AssemblyName System.speech
	$speak = New-Object System.Speech.Synthesis.SpeechSynthesizer
	$speak.Speak($textToSpeak)
    $speak.Dispose()
}
```

Once I had done that I asked my kid that if she wanted to speak with the computer and learn some math. I showed her that you could make mathematical equations and let the computer to compute them for her. The computer would then both print the output and say it aloud. Robotlike speech synthesizer was fun eventhought that it did not speak her native language (it might be possible to change the language). 

```powershell
5*5 + 1 | speak-aloud
```

At the age of six or seven my kid was so enthusiastic about PowerShell that she wanted to stay at home using PowerShell instead of coming to grocery with her parents. I would bet that is quite unique thing to be told as a parent.

## Telling stories with Scratch

One all time favorite for my kids has been ScratchJr (from Play Store). It is a Scratch IDE designed specially for kids. It is not necessary so much about programming in a sense I do it for work but more of a story telling. It allows children to put cute figures into different scenes and orchestrate what the different characters do. Basically it is a way to make a short movie with programming language. 

To get a grip what it is like I proudly present one of my childrens latest piece of art. Red dragon playing soccer with cat. Well just a screen capture, not a video.

![Red dragon playing soccer](/img/coding-with-kids/dragonsoccer.jpg)

This is also hassle free for the educator. You do not know understand anything about programming only open attitude towards trying things out. 

## Scracthing with Lego

When my firstborn was just a few months old I decided that she needs Lego robots. So I went and bought Mindstorms EV3. Well it turned out that she was not that interested on robotics but his younger brother has been really enthusiastic on building anything. With him we have bought Lego Mindstorms EV3, Lego BOOST and Lego BOOST Star Wars Droid Commander. 

#### Mindstorms EV3

Neither of us has liked much on programming with Mindstorms EV3. We have deconstructed and rebuilt it several times but rather used just readymade controllers to use it as a manually controlled electronics than automated robot. The out-of-the-box programming environment feels somehow clumsy. There is possibility to run MicroPython with it but we haven´t yet tested it out. It might be that the era of Mindstorms EV3 comes later since the guy is missing few years still from the recommended age.

#### Lego BOOST

Lego BOOST is awesome. The suggestion age is few years less and it provides more storylike environment to build a robot and to give the robot some different characteristics. We did not get any instructions book with the Lego BOOST but instead it comes with a tablet software that both tells you how to build different robots from the pieces and Scratch IDE. It introduces idea where the Lego model is not absolute. For example if you built up Frankie the cat you can decorate it as you wish. Do you want it to have a hat? Which hat? Do you want it to have a bowtie or not? You can even teach Frankie to have a birthday party and teach him to play harmonica. That is awesome. Lots of building, deconstructing and programming happens in no time. Everything is even packaged in a way that our six year old could do it. Well to be honest he had some programming experience and a lots of Lego experience. This package made me hope to be a child again to have all time in the world to just rebuild it over and over again. 

#### Lego BOOST Star Wars Droid Commander

Where Lego BOOST was awesome the newer Lego BOOST Star Wars Droid Commander is something beyond that. Me and my boys are definitely Star Wars fanboys which will color my opinions on the matter. The package does not include instructions book but instead you will use tablet to use Lego app for the droids. The app is more comprehensive package than with the original BOOST. It has a whole Star Wars universe where your three droids will adventure. You can build all three droids at once but you will have only one programmable brick which is at times a bit awkward. 

Software development process with Lego Boost Star Wars Droid commander is following
- Venture in the galaxy and find somebody who has a problem
- Move programmable brick from one droid to another
- Deconstruct some parts of the droid like arms of the Gonk droid
- Build up new adjustments
- Implement software with Scratch to actually help the poor fellow in distress

I can recall first grade aged boy to sit next to this thing eight hours straight to just build and deconstruct and programming repeatable. As a parent I needed to trick him eat something of course but still. 

Here is a picture of the Lego BOOST App IDE. 

![Star Wars BOOST](/img/coding-with-kids/starwars.jpg)


## Making portable Flappy Bird game with micro:bit

BBC micro:bit is a ARM-based credit-card sized microcomputer designed for education. It is open sourced and it has an [educational foundation](https://microbit.org/) that publishes guides and more. I found a claim that over 25 million children would be using it in school, libraries and home. It costs around 20 euros and has pretty impressive list of features for a computer of that price tag.

- Two buttons (three if you count reset)
- 5x5 LED Matrix
- 3-axis accelerometer
- 3-axis magnetometer
- Light sensor
- Temperature sensor
- Radio
- MicroUSB connector
- Bluetooth Low Energy 
- 25 pins for I/O
- Two official code editors (Microsoft MakeCode and MicroPython)

![micro:bit](/img/coding-with-kids/microbit.jpg)

I used the MakeCode that could also be found for Android and Apple as an app. Children might need some help in connecting the device to tablet and learning things like flashing the rom. Beside that the actual coding could also be done yet again with scratch. As our first project we did a simplified version of Flappy Bird for the device with these [instructions](https://makecode.microbit.org/projects/crashy-bird). All my kids where thrilled about that they could do such a thing and because of that they have used pretty impressive amount of time on playing Flappy Bird with 5x5 LED matrix. 

And that is not all. [Tech Will Save Us](https://www.techwillsaveus.com/) (that by my understanding has designed and created the micro:bit for the educational foundation) also provides extension kits. It seems that there are lots of interesting electronics that supports coding hobby like [Arcade Coder](https://www.techwillsaveus.com/arcade-coder-home/) but also interesting electronics projects like building your own synthesizer that is at both time really fun and frustrating because it does provide infernal sounds. 

![synth](/img/coding-with-kids/synth.jpg)

## Looking into Sphero

Sphero provides robots. I have a good feeling about them. Maybe even too good. They feel like complete products and they have provided Bluetooth connectivity that can be used both from computer and from tablet to program them. They are sturdy and have really impressive set of features. I have had hard times on figuring out what I would like to have more. I have Sphero Bolt and Sphero RVR which both are surprisingly expensive when compared for example to Tech Will Save Us products. They have community behind them and the IDE that Sphero is providing also is a code-sharing-platform. You can instruct them with drawing routes and programming them with Scratch or JavaScript. Interestingly there is even [guidance](https://sdk.sphero.com/microbit/) how to connect the above mentioned micro:bit to your Sphero RVR. Below is a picture of my Spheros. 

![Spheros](/img/coding-with-kids/sphero.jpg)

Here is an example program that I did for my children as a showcase that what could be done. It provides matrix animations, some spinning around and scrolling text over the LED matrix and finally ends up celebrating goal by turning around while standing in one place. It seems that the 

![Sphero soccer](/img/coding-with-kids/sphero_soccer.jpg)

Scratch code done by kids is yet to be done. Instead my youngest of the pack made his first computer program at age of three using only finger to draw the what should the robot do. Color of the line dictates the color of LED matrix. I am missing video but you can still surely imagine how that Bolt ball moves back and forth with these instructions. 

![Sphero draw](/img/coding-with-kids/sphero_draw.jpg)

Long story short. They are awesome but still they are kind of gathering dust in our house. I do not know the actual reason but maybe the reason could be that they are too complete for me. I have found out that I would really like to build the robot myself. In contrast here is my old project built on top of Netduino. If you look those two Sphero robots and compare to this you surely get what I meant. Maybe I am just missing an angle from where to approach the RVR since you could add things like robotic arm to it. Nevertheless I kind of would personally like to look into arduino/netduino/F7 meadow instead of Sphero when building robots just to make the process more comprehensive but same time it could be too hard for kids.

![Netduino](/img/coding-with-kids/netduino.jpg)

## Mastering the art of Python

I needed to learn more Python to my work project so I implemented Space Invader clone with `pygame` with a twist that I replaced all the aliens with my own face. My kids loved to choose dads that were trying to catch their spaceship. The natural move was then to ask if they wanted to learn about making software like this and of course they wanted. 

In overall Python is a really good language for learning programming. There is plenty of sources. It is supported in many situations and it is simple to get started. It comes with much less boilerplate code than for example Java or C# would come which helps kids to focus into the actual thing and not to be distracted about "important but not necessary" features of many other languages.  

#### Using book to learn Python

I considered how to learn programming when you already knew Scratch, PowerShell and Turtle Roy. I decided that I could go into more comprehensive direction and lend a book from library. As always with books there were lots of words and we were not interested on every of them. We cherrypicked example projects from there that were written in english and translated them with my kid to finnish. One of the examples was using `from turtle import *` to make a drawing robot that knew how to build a house so you could command Python from commandline to provide exactly same house over and over again. That was a fun process but the endresult is rather boring. Instead I will present you a piece software that was faster to implement and provided much more fun on many occasions: generating funny phrases. The idea is really simple. Make few array of words like subjects, deeds and objects and mix them randomly to provide unexpected phrases. Use your family names in subjects to make it even funnier. Here is a hastily from finnish-to-english translated version of the implementation.

```python
subjects = ["Dad","Mother","Kid1","Kid2"]
deeds = ["eats","kicks","burns","lifts"]
objects = ["lion","bicycle","airplane","ice cream"]

from random import randint
def pickword(words):
    wordcount = len(words)
    pickedword = randint(0, wordcount-1)
    return words[pickedword]

print(pickword(subjects),pickword(deeds),pickword(objects),end='.\n')
```

Which will lead into phrases like `Dad eats lion` and `Mother kicks airplane` or the sinful deed `Dad burns ice cream`. 

#### RPG with Python

Quickly our learn how to implement software with Python turned into how to control characters in role playing game with Python. We have been using [https://codecombat.com/](Code Combat) for that. Beside Python it also supports JavaScript. Kids will quite quickly get grip on the game but there are missing translations and some new features that will require parent to support the kid on the way. Code Combat is implemented in a way that supports problem solving, learning algorhitms and learning basic of object oriented programming. It is implemented with kind of Domain Specific Language. You can only use given commands and equipment will give your character more options. For example your hero can't cleave with sword without sword. 

We also tried once to go further and check if we could find something from [CodinGame](https://www.codingame.com/) that we could do. Unfortunately it seems that the challenges there were still a bit too hard. Maybe we get back there in few years. 


## Creating the first home page - the hard way

Last and maybe the least is making the home pages. I was once told that the easiest way to make home pages is make a word document and then save it as a HTML file. If you know anything about home pages you might know that there are plenty of problems that will arise from that approach. Instead I teached my kids the same painful route that I took 25 years ago. Basically we opened up a notepad and then into another screen the [w3schools](https://www.w3schools.com/html/default.asp). Then we made an index document using the simplest possible syntax with having title with two words and the body with a sentence. We hosted it in Azure Blob Storage with static websites feature enabled that allows you to serve static html files from the blog storage. I had to check out what it has costed me and I figured out that less than 1c. Seems like a cheap way to start. 

Needless to say this was kind of boring approach and maybe we come back to this later. Now the website is "under construction" like all the webpages back in the nineties. 

## Afterwords

In summary my kids knew to how to program with few different languages before school. You do not need to know how to read to start programming because it can be done with drawing (Sphero). ScratchJr also is able to teach "try and learn" type of approach which does not require deep understanding. Later on Python is a great choice for first "real programming language" as it is widely supported and easy to learn. The basic idea for me has not been to make sure that they will be nerds but more of show what is possible. Later they can make their own decisions about what they want to do but now this is more of building something together. Still nothing beats Legos. 