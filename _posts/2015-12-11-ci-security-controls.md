---
layout: post
title: Security controls in continuous integration
author: Rinorragi
excerpt: Solita was at Need 4 Speed Rovaniemi and talked about continuous integration security controls among other things. 
categories: 
- EPiServer
tags: 
- EPiServer 
- DOTNET 
- Security
---
Continuous integration and continuous delivery have been trendy topics lately. Among other things it is necessary to take care of security in your development process. I want to share few ideas how you can enhance your security in continuous integration in EPiServer CMS projects. [Need for speed](http://www.n4s.fi/en/) is a Finnish foundation and its purpose is to find new ways to deliver real time value for customers of Finnish software companies. There was a Q4 review this week at Rovaniemi and my blog post will be about [my presentation](http://www.slideshare.net/Solita_Oy/continuous-integration-and-security-testing-with-net?related=1) at there. 

## Problem domain 
![Tools](/img/n4s-q4-and-ci-security-controls/owasp_problem_domain.png)

In this picture from OWASP it is important to understand that when talking about security, the threat agents in the picture will be trying to effect your business. By understanding the motive of the attacker it will be much easier to estimate what he or she is trying to achieve. Of course there can be natural disasters that are mindless threats but for example botnets are always built for some purpose.

In continuous integration we want to find possible security vulnerabilities and make the build fail to get instant feedback about security problem for the developer. 

## Security testing as whole 
![Tools](/img/n4s-q4-and-ci-security-controls/owasp_sdlc.png)

Diagram above is from [OWASP Testing guide 4](https://www.owasp.org/images/5/52/OWASP_Testing_Guide_v4.pdf). It presents secure development lifecycle (Microsoft has its [own](https://www.microsoft.com/en-us/sdl/) too). There are many things that can't be handled with automatisation like going through customer security policies, learning industrial standards and creating security architecture but nevertheless there are areas that can be partly automated. 

## Different tools tested 

We tested various tools and divided them to different categories.

##### Static code analysis
In this category there are tools that go through source code and possibly also the application configuration. They look for problems in code and are meant for ensuring the code quality. They are capable of finding SQL injection possibilities, unvalidated parameters, memory leaks and security misconfigurations but still security testing is not the core idea behind these tools. 

* FxCop
* VisualCodeGrepper
* SonarQube
* ReSharper commandlinetools 

##### Code quality metrics
Code quality metrics is all about code quality. By having good quality enhances your security indirectly. Complex software is harder to test and bad code is more likely to contain security holes. Duplicated code easily leads to fact that problems are only fixed in one place and left open to another place. Having bugs in your code affects integrity and availability of the software and data. As you might know, the security is often modeled as CIA triangle (confidentiality, integrity and availability). 

* SonarQube
* Code metrics

##### Configuration and deployment analysis
These tools will test how your system has been set up. MBSA checks if your installation follows best practices and ASA checks what is the attack surface of your application. 

* Microsoft Baseline Security Analyzer
* Attack Surface Analyzer

##### Vulnerability scanning
These tools are meant for security professionals. Nessus is a network scanner that shines in finding known vulnerabilities in operating systems and application servers. OWASP ZAP is meant for web application security testing. Both of these test directly the security of your application. You should be careful when using these since you might be acting against the law if you scan targets without their permission. 

* Nessus
* OWASP Zed Attack Proxy

#### Performance testing 
Since availability is in the core of security, the performance testing will help you in finding bottlenecks that attacker could use to amplify his or her DOS Denial of Service attack. 

* jMeter

## How do these tools sit on secure development lifecycle?
![Tools](/img/n4s-q4-and-ci-security-controls/tools_in_sdlc.png)

As it can be clearly seen in the picture the tools can help you in development, deployment and maintenance. 

## In which layers these tools work 
![Tools](/img/n4s-q4-and-ci-security-controls/tools_in_did.png)

This picture tries to tell you something about defence in depth. Choosing tools only from one category will not be enought to cover all aspects of the security. Also keep in mind that the attacker won't care if the vulnerability is in the host or in the application. This means that seemless cooperation between development and operations is needed; thus you should embrace DevOps in your workplace to cover these gaps. 

## How do these tools mitigate OWASP TOP 10 threats
![Tools](/img/n4s-q4-and-ci-security-controls/tools_owasp_top_10.png)

[OWASP TOP 10](http://owasptop10.googlecode.com/files/OWASP%20Top%2010%20-%202013.pdf) is a list of common web application vulnerabilities. As it can be seen in the picture the OWASP ZAP is a tool that is created to mitigate these vulnerabilities. Nessus and static code analysis tools can also be helpful. Truth to be told some of these threats are really generic ones. Security misconfiguration for example can mean pretty much anything (network devices, operating systems, application servers, other services in the operating system, etc). Missing function level authorization instead is so tightly coupled to application logic that it is hard to test automatically; the only option is to write your own tests against that. 

## How do these tools mitigate Cloud Security Alliances "Notorious Nine"
![Tools](/img/n4s-q4-and-ci-security-controls/tools_csa_notorious_nine.png)

[Notorious nine](https://downloads.cloudsecurityalliance.org/initiatives/top_threats/The_Notorious_Nine_Cloud_Computing_Top_Threats_in_2013.pdf) is Cloud Security Alliance's list of most common threats for cloud computing. In the picture above you can pretty clearly see that most of the threats can't be mitigated in CI with automized tools. Instead you should read carefully how CSA suggests you to mitigate the threats. Most of the threats are handled with security policies inside companies and only way to truly mitigate them is to educate your employees to be aware of these threats. 

## How useful our few example projects felt that the tools are in security perspective
![Tools](/img/n4s-q4-and-ci-security-controls/tools_usefulness.png)

This one is interesting. You could think that OWASP ZAP and Nessus would have been better here. But the truth is that the amount of vulnerabilities found with these tools was not big when compared the effort you need to have to use them continuously in continuous integration. Nessus for example was out of the case in projects because hosting was done by 3rd party in these example projects and it makes it hard to make continuous network scans since monitoring of the 3rd party company will be disturbed by this kind of network activity. OWASP ZAP instead reports a great deal of false positives and it is meant to be used manually so its usage in CI is harder than you would think. Example for using it from Jenkins is available at [GitHub](https://github.com/solita/powershell-zap/tree/master/PowerShell-ZAP). 

Also when using only OWASP TOP 10 and CSA Notorious nine the usefulness of tools is twisted. The accuracy is great deal better in static code analysis, they can be run a lot faster and tuning them for your needs is easier. OWASP-ZAP can take a lot of time if you run it in a manner that spiders your website, scans the found urls and gathers the report. We have projects that have several thousands of pages which means that going through all of them will really take some time. 

## How does it feel to use these tools
![Tools](/img/n4s-q4-and-ci-security-controls/sonarqube.png)
In the picture there is example of SonarQube dashboard. You might think that there is a great deal of major issues in the code in the project that was scanned with SonarQube. I used three different static code analysis to get that dashboard (ReSharper commandlinetools, FxCop and SonarQubes own static code analysis). 600 of major issues are because of our software didn't have good enough commentation ratio (above 25% of code should be comments). I personally don't trust that having that much comments is a good thing; instead readability of code should be embraced and only necessary things should be commented. This way the comments won't become noise in your eyes and you will keep on reading them.

Well the bottom line is that from the around 6000 reported issues there was maybe few dozen real ones. With all the automized tools you need to spare some time to tune the tools to only report about issues you are really interested on. 

## Recommendation for implementing continuous security
Try to run static code analysis with few different tools. See what they can find and reflect that to your security needs. Take atleast one into your CI build after tuning it into your needs. 

Calculate code metrics and see what they say about your software. My recommendation would be to use SonarQube as a code quality platform that keeps at track how your code quality develops. It will be a difficult task to truly bring down the CI build with these metrics instead you will like to watch how the metrics develop over time.  

Try to scan your application manually with few different tools (MSBA, OWASP ZAP, Burp suite, nmap, nessus) and again see what they can find and think if you want to make these checks continuous. You should for example create nightly builds and/or continuous security checks separated from development if they are taking too much time. By learning the tools you can also make only specific tests in CI which would make sure that critical parts of application are secure. 

Above all else remember to educate your personnel! 
