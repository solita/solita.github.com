---
layout: post
title: Vagrant, Windows 7, VirtualBox, PowerShell!
author: pvto
date: 2017-08-11 14:00:00 +0300
excerpt: When I installed the latest Vagrant version 1.9.7 on my Windows 7 machine,
I was expecting a smooth ride, but this is what I got
tags:
- vagrant
- virtualization
- windows 7
- virtualbox
- powershell
- troubleshooting

---

<span style="font-size:32px;background-color:#1563FF;color:#104EB2;">Vagrant</span> is a popular virtual machine control tool that works with different virtualization platforms like VMWare and Oracle VirtualBox.
It also works out of the box on Linux, Mac, and Windows.


Now I'll just explain how I got the latest Vagrant version 1.9.7 working on my Windows 7 workstation.

*TL;DR: It was quite simple.
Increasing logging with ```set VAGRANT_LOG=info```, then ```vagrant up```, and follow the gory trail.
In this case, updating PowerShell resolved the issue. See [bug report #8783](https://github.com/mitchellh/vagrant/issues/8783).
The rest of this is post contains a few nice troubleshooting tips for Vagrant users.*

Why Vagrant is very popular among developers, is because it saves valuable time.
You can use templates of popular virtual machines and create your own ones too.
Environment maintenance can be simplified considerably.

When I installed the latest Vagrant version 1.9.7 on my Windows 7 machine,
I was waiting for a smooth ride, but this is what I got:

```
> vagrant init hashicorp/precise64
(...OK this far...)
> vagrant up



```

```vagrant up```, as well as ```vagrant status```, with other commands, were stalling forever
with no output whatsoever.

 - my VirtualBox installation was complete, and ```VBoxSVC.exe``` was running and visible in taskmgr under user paavoto (the same running vagrant); I could also create and run a 64 bit Precise Pangolin machine manually from VirtualBox GUI <span style="color:#40ff40">✔</span>
 - I had all installations matching, 64 bit Vagrant, VirtualBox, Windows 7
 - running repair from Vagrant installer did not change the situation <span style="color:#40ff40">✔</span>
 - to be extra sure, I cleaned up my PATH variable quite a bit and reran ```vagrant up```, to no avail <span style="color:#40ff40">✔</span>
 - what then? From the manuals I learned how to increase logging with another environment variable, ```set VAGRANT_LOG=info```

Now ```vagrant up``` started to show some output, and I noticed how the output stalled
after a PowerShell command. By googling then this [bug report](https://github.com/mitchellh/vagrant/issues/8783).

 - I affirmed that this was "my" bug by killing a PowerShell process in my Windows task manager, which action
  immediately released the Vagrant process to proceed <span style="color:#40ff40">✔</span>
 - after a few more kills I could normally ```vagrant ssh``` to my newly created virtual box <span style="color:#40ff40">✔</span>
 - I halted my new virtual machine, downloaded an update to PowerShell that had been linked helpfully in the bug report, and restarted my Windows machine <span style="color:#40ff40">✔</span>

Now Vagrant worked out-of-the-box!

As a sly side note: the famous *Murphy's law* - *Anything that can go wrong will go wrong* -
has been under serious questioning and revision recently. Check it out in the Wikipedia for the gory details.
