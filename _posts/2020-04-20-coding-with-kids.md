---
layout: post
title: Coding with kids
author: Rinorragi
excerpt: Sharing my experience about teaching my own kids to code
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
![processes](/img/coding-with-kids/roy-princess.png)

Finally I printed out the commands for her and make some own markings to them and let her try to draw. Of course at age of four she was nowhere near in using variables or making functions but she had fun time with commanding the turtle to draw something with `fd`, `lt`, `rt` and `color`. We did this few times and she was happy to spend a total of several hours in the world of Turtle Roy. 

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

Once I had done that I asked my kid that if she wanted to speak with the computer and learn some math. I showed her that you could make mathematical equations and let the computer to compute them for her. The computer would then both print the output and say it aloud. Robotlike speech synthesizer was fun eventhough that it did not speak her native language. 

```powershell
5*5 + 1 | speak-aloud
```

## Scracthing with Lego

## Mastering the art of Python

## Creating the first home page - the hard way

## Tinkering with electronics

