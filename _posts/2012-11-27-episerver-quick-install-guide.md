---
layout: post
title: EPiServer in the Cloud – a quick start guide
author: timole
excerpt: This is a short guide for installing EPiServer on a cloud server. The target audience is TUT students on course MATHM-37200 Hypermediajärjestelmät, where a visiting lecture was held on Wed 28.11.2012. Please feel free to ask questions on installing EPiServer, if you have any problems.
tags: episerver cms TUT
---

This is a short guide for installing EPiServer 7 on a cloud server. If you have any problems, please feel free to ask questions at the bottom of the page! This articles target group is students of TUT that parricipated the guest lecture ([.ppt slides](/files/episerver/Solita%20-%20Vierailuluento%20-%20TTY%20-%20EPiServer%20.NET-asiakasprojekteissa.pptx))

The goal is to get EPiServer 7 up and running on a Windows 2008 cloud server. The URL of your server will be http://yourownaccount.no-ip.org. What you need to do is:

1. Get a free domain name from [No-IP.com](http://www.no-ip.com/).
2. Get a free Windows 2008 cloud server from [Upcloud](http://fi.upcloud.com/).
3. Configure your server and install the prerequisites.
4. Install EPiServer on the cloud server.
5. Browse to http://yourownaccount.no-ip.org.


### Step 1: Get a free domain name from No-IP.com ###
1. Register at [No-IP](http://www.no-ip.com/).
2. Create a new Host by clicking *Add Host*.
![no-ip](/img/episerver/no-ip.png)
3. Use the default values for the IP address and the other fields, and click *Save*.

### Step 2: Create a cloud server at Upcloud ###

1. Register at [Upcloud](http://fi.upcloud.com/rekisteroidy).
2. Log in and create a new virtual Windows server (choose Windows Server 2008 R2 as the image).
![upcloud-new-server](/img/episerver/upcloud-new-server.png)
3. Enter yourownaccount.no-ip.org as the FQDN name.
4. Click *Create* and wait until your virtual cloud server is ready. Choose the *Send password to email* option.
5. Link the domain name to the cloud server: Copy the IP address of your server (e.g. 80.69.174.99) onto the clipboard. Paste the IP address to your host settings at [No-IP](http://www.no-ip.com/).
6. Wait a minute or two while the DNS records are being updated.

### Step 3: Configure your server and install the prerequisites ###

1. Log in to the server at yourownaccount.no-ip.org with RDP: Start a *Remote Desktop Connection* from the Start menu (Mac users, start CORD) and enter yourownaccount.no-ip.org as the host name. Use the user name *Administrator* and the password sent to you by email.
2. Now you should see the desktop of your server:
![virtual-server](/img/episerver/virtual-server.png)
3. Create a new user called *episerver* with administrator privileges: go to *Control panel* &rarr; *Add or remove user accounts* &rarr; *Create a new account* (choose *Administrator* as the account type).
4. Log out and log in again, now as the user *episerver*.
5. Install the .NET Framework 4: [Download the installer](http://www.microsoft.com/en-us/download/details.aspx?id=17851) to your desktop computer.
6. Copy the file onto the clipboard.
7. Paste the file onto the virtual server's desktop:<br/>
![paste](/img/episerver/paste.png)
8. Install the .NET Framework by double clicking the installer on the server.
9. Install ASP.NET MVC 4: [Download the installer](http://www.asp.net/mvc/mvc4) to your desktop computer. Then copy & paste the file to the virtual server, and run the installer by double clicking the file.

### Step 4: Install EPiServer on the cloud server ###

1. Install EPiServer 7: [Download the installer](http://world.episerver.com/Download/Items/EPiServer-CMS/EPiServer-7---CMS/), copy it to the virtual server, and run it there.
2. When the installation is finished, start the *Deployment center*.
3. Choose the option *Install site and SQL Server database*
4. Use the default values for everything except the port (80) and the UI URL (/cms/ui). By using the port 80 your server will be available at the URL http://yourownaccount.no-ip.org
![epi-config](/img/episerver/epi-config.png)
5. You need to start your newly created application: Go to the *IIS Manager* (*Start* &rarr; *Run*, type *IIS* and choose *IIS Manager*), and stop the default site by choosing *Stop*. Then start the EPiServer site by selecting it and clicking *Start*.
![iis-config](/img/episerver/iis-config.png)

### Step 5: Browse to <span style="white-space: nowrap">http://yourownaccount.no-ip.org</span> ###

1. Congratulations, you now have the EPiServer up and running, and you can start using it at http://yourownaccount.no-ip.org
2. Finally, please add a comment to this page if you made it this far -- just to know if anyone did it :) And if you encounter any problems, don't hesitate to ask for help in the comments.
