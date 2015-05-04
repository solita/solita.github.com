---
layout: post
title: Enterprise VPN insecurity
author: lokori
excerpt: Analysis of a enterprise VPN solution. There is surprising functionality opening a backdoor to end user's computer. Do you know what your VPN solution actually does? 
---


The term "enterprise software" in our field tends to carry two connotations. The programmers
tend to judge such solutions as overly complex, difficult to use and costly. On the other hand,
for marketing purposes the phrase "enterprise level solution" attempts to signify the product
as thoroughly tested, high-quality one with good support from the vendor.

I had the misfortune to run into a certain "enterprise level" VPN solution. It didn't work on 
my computer so I took it apart and found functionality I never would have expected to see 
in a [VPN](http://en.wikipedia.org/wiki/Virtual_private_network) client. This post reveals the gory details.

## Basic VPN

Basically a VPN is a client-server solution where the client encrypts and routes the traffic
through some endpoint other than the normal internet gateway. This is not very difficult and
there have been VPN clients and servers for years from multiple vendors. They work well. 

## Enterprise level VPN

![Worf is not amused](/img/vpn-insecurity/worf-security.jpg)

Simply entering your password or using a private key file is too simple for Enterprise Level. 
The solution I examined works like this:

1. The user points a web browser to URL.
2. Password is entered and a separate single-use password obtained from SMS. The necessity of the second channel is a matter of judgement.
3. The web browser downloads and runs a Java applet. 
4. The Java applet runs local commands using System.exec. 
4. The Java applet installs a native binary to the workstation.
5. The native software is run, unless it's already running. 
6. A local server socket is bound and listened on. 
7. A VPN tunnel finally opens!

### What is the point of using Java here at all?

Apparently it's legacy. Originally (it appears) that this software was used to obtain secure access simply
using a standard web browser with no client software installed. A nice idea certainly.

You might be wondering how a Java applet can use System.exec. As it happens, I was explicitly instructed to
grant special permissions that break the Java security model. How many end-users are able to this without
accidentally giving access to all malicious Java applets?


## Deconstructing the Java applet

Since the software didn't actually work and didn't provide any meaningful error messages about the reason
I decided to break it into pieces. Using [JAD](http://en.wikipedia.org/wiki/JAD_%28JAva_Decompiler%29) I decompiled the class files and did some other digging as well. 
I was disturbed by my findings.

Let's see.. why would a VPN client need to list all my open TCP/IP ports in my local machine? Hmmm.

```
    public HashSet enumPorts()
    {
        HashSet hashset = new HashSet();
        String s = "netstat -an -f inet";
```

And what could be a meaning of class named ProcessToKill?

It gets better. There is code for deleting arbitrary files from my computer.

```
    public static void deleteFile(String s)
    {
        Vector vector = expandFilePaths(s);
        for(int i = 0; i < vector.size(); i++)
        {
            String s1 = (String)vector.get(i);
            HCUtil.logInfo("HCFileRule: deleting file " + s1);
            File file = new File(s1);
            if(file.exists())
            {
                boolean flag = false;
                try
                {
                    flag = file.delete();
```

At this point I would remind you that the vendor has specifically instructed the end user to run this
"Java applet" with full privileges so this code really has ability to delete files.

There is one particularly interesting class which contains the following code in it's initialize() method.

```
        mTncClient = new TNCClient();
        mTncClient.initialize(this);
        mHandshakeRequestor.start();
        trustAllCerts();
        allowHostnameMismatch();
    }
```

trustAllCerts() Wait what?

Yes, as implied, the code in trustAllCerts() installs a special SSL security manager which skips the normal SSL certificate checks, making any HTTPS connection
valid regardless of the certificate. Since this is a JVM level setting in Java, this means the security manager is changed for all other Java software running
in the same JVM. 

## Obfuscation

For whatever reason, some parts have been obfuscated which supposedly makes the analysis more difficult. Since the log messages have been
left intact, it's not very difficult to guess what the method a() is.  

```
    static void a(boolean flag)
    {
        if(Logger.isLogging())
            Logger.log("src/Reader.java", 720, 2, "Reader thread abort, use new connection id " + flag);
```

## The cost 

Roughly half of the code inside the JAR file is related to this security functionality which has nothing to do with VPN
connections. The rules controlling file deletion and security scanning are written in some DSL and there's a crude 
parser for that. Different implementations for the special functions for different platforms are required as "netstat" 
has some other name in Windows world. All this platform specific functionality requires special testing effort to
maintain. The money comes from the customers in the end.


## Ignorance is bliss

No one told me, the end user, the "VPN client" would have functionality to access arbitrary processes and files
on my computer without my knowledge or permission. The administrators know as the admin guide spells 
it out pretty clearly:

".. is a client-side agent that performs endpoint health and security checks
for hosts that attempt to connect to .."

" -- can check for third
party applications, files, process, ports, registry keys, and custom DLLs on hosts. Based
on the results of the checks, it can then deny or allow access to protected resources."

but it goes beyond just checking and denying access..

"can scan processes that are loaded in memory on endpoints and provide real-time
file system write and execution shield to automatically remediate machines that are not
in compliance."

..

"If a client attempts to log in, and the client machine does not meet the requirements you
specify, -- can attempt to correct the deficiencies to allow the client to
successfully log in"

![Make it not so](/img/vpn-insecurity/picard-facepalm.jpg)

## Truth is deception

The words in the admin guide are "Enteprise Speak", a remote cousin of [Newspeak](http://en.wikipedia.org/wiki/Newspeak). 
Using phrases like "health check" and "remediate" is not accidental.
 
It doesn't sound so nice in Hackerspeak dialect of english:

"During log in, the client machine can be forced to comply with arbitrary rules set by the 
administrator. The VPN client may delete files, kill system processes and do other things
on the client computer without the user's knowledge or consent." 

## But it is more secure?

The file delete capability means that with a simple mistake with wildcard characters, the administrator can
basically render arbitrary number of unsuspecting VPN client computers unusable. A risk I definitely didn't
know I was taking since we were only talking about a VPN client. Somehow I would feel more secure
if I could just use a simple VPN client instead. Or just a SOCKS proxy over SSH. 

It would be nice if a software component did just one thing and did it well. Alas, outside unix ecosystem this will not
happen anytime soon. Many software products do a huge number of different things. Even if they happen to do these
things well, as demonstrated, you may got much more than you bargained for.