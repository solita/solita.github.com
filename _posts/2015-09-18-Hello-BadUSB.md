---
layout: post
title: Hello BadUSB
author: Rinorragi
excerpt: Introduction to USB Rubber Ducky keystroke injection platform
---

There was a big security flaw in a 2014 Jeep Cherokee. Chrysler didn't have a way to patch cars over the air so [they mailed 1.4 million USB drives](http://www.wired.com/2015/09/chrysler-gets-flak-patching-hack-via-mailed-usb/) via the US Postal Service. By doing that they teached their customers to trust USB drives that are delivered by mail. What security professionals are fearing is of course malicious USB devices. Let's peek into world of BadUSB.

## How do I get one?
I ordered my BadUSB from [hakshop](http://hakshop.myshopify.com/). It is called USB Rubber Ducky Deluxe. In short it is a USB drive that acts as a USB Human Interface Device. When you plug it into your device it presents itself as a keyboard. Within a package there is the BadUSB itself, microSD card and microSD card reader. Because it is a keyboard it works with any device that supports USB keyboard (Windows, Mac, Linux, Android, etc). The payload has to be chosen by knowing the target system because the same keyboard injection won't do desired things in different operating systems. 

![Tools](/img/hello-badusb/ducky_usb.jpg)
The device itself looks just like an USB drive

![Tools](/img/hello-badusb/ducky_embedded_microsd.jpg)
From inside the Ducky is actually embedded device with microSD reader

## How to script Ducky
Ducky has its own script language called [DuckyScript](https://github.com/hak5darren/USB-Rubber-Ducky/wiki/Duckyscript). It is simple language which allows you to define what keyboard actions you want to script. There is no actual IDE for it but community has created an User Defined Language for Notepad++ which can be found from [hak5 forums](https://forums.hak5.org/index.php?/topic/21045-encoder-duckyscript-notepad-userdefinedlanguage/). My first payload script simply opened PowerShell with Win-R shortcut and downloaded an executable which was then executed. 

![Tools](/img/hello-badusb/duckyscript.png)

The script itself is quite self-explanatory. 
1. At the top of the script there are few lines of comments with REM keyword. 
2. Then DELAY for 10s is added because Ducky was anxious to start executing the script before Windows has finished installing HID drivers thus my payload failed without it. 
3. WINDOWS r opens the run prompt and yet again delay is added for waiting the prompt to truly open. 
4. Then PowerShell is written to prompt following with ENTER. 
5. PowerShell is used to invoke a webclient command to download a file and store it under temp folder. 
6. Finally the executable is started with Start-Process command in PowerShell. 

There are plenty of ready scripts available. [Here](https://github.com/hak5darren/USB-Rubber-Ducky/wiki/Payloads) are few samples. There is also community made toolkit available. You should [check it out](http://www.ducktoolkit.com) since it allows you to generate scripts with certain payload. Toolkit also allows you to compile scripts on the internet but my precautioness didn't let me to test it out. 

## Building the script for Ducky
This was for me the trickiest part. Wiki tells you to download [this Duck Encoder](https://github.com/hak5darren/USB-Rubber-Ducky/wiki/Downloads). It was straightforwart to use.

```powershell
java -jar duckencoder.jar -i exploit.txt -o /media/microsdcard/inject.bin
```

Although there was an annoying problem. It only supported US layout. The script didn't work unless you chose the correct keyboard layout from Windows first. Luckily community has solved this problem. There were newer versions of [commandline compiler](https://github.com/midnitesnake/USB-Rubber-Ducky) available. I just needed to pass new parameter for the encoder!

```powershell
java -jar encoder.jar -i exploit.txt -o inject.bin -l resources\fi.properties
```

## Exploiting innocent victims
After that there is only one more thing to do. To upload the payload for your device. You need to take microSD card from your Ducky device and upload inject.bin into device. After inserting microSD card back the device is ready to use. If you plan to buy multiple microSD cards you should know that there are pretty strict limitations what kind of microSD cards are eligible. The device can't handle big cards at all. 

After injecting the BadUSB to a Windows machine the following things will happen.

![Tools](/img/hello-badusb/ducky_cmd.png)

Run prompt is shown and "powershell" is typed to it

![Tools](/img/hello-badusb/ducky_powershell.png)

Once PowerShell has started the script downloads an executable and runs it

![Tools](/img/hello-badusb/ducky_exe.png)

The executable itself was this time a pretty harmless one that opens notepad and prints an adorable ascii dragon.

## Wait there is more
Dangerousness of Human Interface Device USB is that all the user actions are always trusted. How do you bypass UAC in Windows? With user action.

This kind of BadUSB device is pretty easy to notice because it didn't do what user expected (it wasn't a USB drive). With Ducky there are community made firmwares that can be both USB Drive and USB Keyboard at the same time. This way the victim could download e.g. PDF document from USB drive and after that you could just disrupt him when the HID keyboard starts to build a backdoor for you. 

## How to protect yourself from BadUSB?
Once your car manufacturer sends you an USB drive via email do not plug it in! It is simple as that. You should go to meet your local car service company and ask them to do the needed job. 

Another way around would be to whitelist the allowed devices and deny all others. This might be burdensome especially if user does not have privileges to bypass this restriction. 