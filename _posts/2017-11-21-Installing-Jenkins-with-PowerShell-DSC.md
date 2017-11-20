---
layout: post
title: Installing Jenkins with PowerShell DSC
author: Rinorragi
date: 2017-11-21 13:20:00 +0200
excerpt: How to use PowerShell DSC in installing your continuous integration server.
categories: 
- Episerver
tags: 
- Episerver 
- DOTNET 
- DevOps
- PowerShell
- Jenkins
---
I have been struggling to find a good reference about how to setup a Jenkins environment in Microsoft environment with automatic installation script. So I decided to write a blog post about it. I also want to write about how to do continuous integration with Episerver DXC but felt that I need to first tell how to setup the Jenkins. Our aim is to put up a Jenkins server that can build .NET FrameWork MVC application and front end. If you are not a reader type of a person, then [here](https://github.com/solita/powershell-dsc-jenkins) is a GitHub link to example scripts.

## About the PowerShell DSC

You might not be familiar about the PowerShell DSC and it comes from Desired Stage Configuration. It is not new anymore, instead it have been there now for years still in my experience most .NET developers are unfamiliar with it. DSC exists for various reasons:

* Make scripting less complex
* Make scripting to look the same for smaller learning curve 
* Make scripting pieces to be more reusable
* Make installation scripts to be idempotent (repeatable)

The DSC is all about the setting the state of a machine to be certain. Most used example is to make sure that a service is running or that certain file is found on certain location. If you dig further on to this world you will find concepts of pull and push servers that would help you to set a farm of machines into certain state. We will not use those but we run the script locally with the help of LCM which is "local configuration manager". If you are looking for basics of PowerShell Desired State Configuration then this [blog](https://red-gate.com/simple-talk/sysadmin/powershell/powershell-desired-state-configuration-the-basics/) was a well-written one.

## DSC resources 

Before we start the configuration we need to talk about DSC resources which are libraries for DSC. Resources provide you functionality for DSC. For our purpose we are needing needing at least one that helps us to grab software from [Chocolatey](https://chocolatey.org/) (a package repository for windows). These resources would normally be where you start the script from (which might take you back to push and pull servers). In this scenario I just install them locally. [Here](https://github.com/solita/powershell-dsc-jenkins/blob/master/install-modules.ps1) is what my Install-Modules.ps1 script has inside.

```powershell
Install-Module cChoco -f
Install-Module xNetworking -f
Install-Module xWebAdministration -f
```

Three modules that provide you three type of functionality. Something to get stuff for Choco, configuring network stuff and managing IIS. If you run this for the first time you might get question about if you want to install nuget package provider for PowerShell. You should if you want to follow this path. It grabs you the wanted modules from [PowerShellGallery](https://www.powershellgallery.com/packages/cChoco/2.3.1.0). 

## Our objective 

We want to have a Jenkins server running in the end with following requirements:

* Install all the needed dependencies
* Install Jenkins itself
* Configure Jenkins startup parameters 
* Setup authentication for Jenkins 
* Install plugins for Jenkins
* Protect Jenkins by settings IIS in front of it 
* Make sure that all traffic is HTTPS

Once our objective is now clear we can look how I managed to do it.

## Starting the scripting

In the below I have the basic structure of my PowerShell script. There are few important parts in the script. The most important one is the Configuration JENKINS_CI which states that here is my DSC configuration. It has few steps in it:

1. State the name of the configuration (JENKINS_CI)
2. Declare parameters (JenkinsPort with default value of 8080)
3. Import necessary DscResources (cChoco)
4. For all the nodes make sure of the following
5. Make sure NetFrameworkCore WindowsFeature is present
6. Make sure Choco is installed

```powershell
Configuration JENKINS_CI
{
    param (
        $JenkinsPort = 8080
	)
	
	Import-DscResource -ModuleName 'cChoco'
	
	Node $AllNodes.NodeName {       
		# Install .NET 3.5
		WindowsFeature NetFrameworkCore 
		{
			Ensure    = "Present" 
			Name      = "NET-Framework-Core"
		}

		# Install Chocolatey
		cChocoInstaller installChoco
		{
			InstallDir = "c:\choco"
			DependsOn = "[WindowsFeature]NetFrameworkCore"
		}
	}
}
```

You should notice from above that you can mark one resource to be dependent on another with DependsOn. This is super important since we have multiple requirements for actually installing most of the stuff in our configuration later on. Now when we have the basic DSC configuration in place we can call it. 

1. We need to define the AllNodes.NodeName that we referred in the script. 
2. We also need to call give the parameters we want to the configuration. 
3. Finally we start the configuration with Start-DscConfiguraiton 

```powershell
$ConfigData = @{
    AllNodes = 
    @(
        @{
            NodeName = "LocalHost"
        }
    )
}

JENKINS_CI -JenkinsPort 8080 -ConfigurationData $ConfigData
Start-DscConfiguration -Path .\JENKINS_CI -Wait -Verbose -Force
```

## All the needed dependencies

We will need a bunch of stuff to be able to build a .NET application. 

* Java for the Jenkins
* Visual Studio and MSBuild for all the build targets and compilation. 
* NodeJs for the front end compilation.
* Git for grabbing few more resources
* Firefox for OWASP Zap 
* Notepad++ for comfort
* Nuget.exe (I like to have a fixed version of this)
* Python for ... things 
* Jenkins for the actual goal 
* Zap for web application security testing automation

Here is the installation of the stuff above. So we insert more stuff under our $AllNodes.NodeName. 

```powershell
# Install Visual Studio, todo: optional features (F#) with param --includeOptional
cChocoPackageInstaller installVisualStudio
{
	Name = "visualstudio2017professional"
	DependsOn = "[cChocoInstaller]installChoco"
}

# Install Visual Studio Web tools 
cChocoPackageInstaller installVisualStudioWebWorkload
{
	Name = "visualstudio2017-workload-netweb"
	Params = "--includeOptional"
	DependsOn = "[cChocoInstaller]installChoco","[cChocoPackageInstaller]installVisualStudio"
}

# Install NuGet
File installNuget 
{
	DestinationPath = "C:\tools\nuget\nuget.exe"
	SourcePath = (Join-Path $InstallConfDirectory "nuget.exe")
	Ensure = "Present"
	Type = "File"
	Checksum = "modifiedDate"
	Force = $true
	MatchSource = $true
}
```

I think that the above script is quite self-explanatory although I made it shorter for easier reading. The full script can be found [here](https://github.com/solita/powershell-dsc-jenkins/blob/master/jenkins_dsc.ps1) We have bunch of resources, most of them depends on something earlier. Afterwards we want to have all those resources in place. Only odd thing is on the installVisualStudioWebWorkload where I add includeOptional parameter for the choco. This is to get F# installed on the target machine as well. It does not come by default. If you need to dig on to those additional options in nuget packages you should head to chocolateys web page and investigate the packages you need to figure out if there is any customization options.

## Installing custom made stuff

We have something in our GitHub repositories that we would like to use with Jenkins. Those are marvelous libraries jmeter-perfotrator and powershell-zap. We can fetch the git repository directly into Jenkins server and whatever what is there with the help of just installed git client. Here is an example resource for that.

```powershell
# Install powershell-zap module 		
Script installPowershellZap 
{
	GetScript = {
		return @{ Result = gci "C:\tools\powershell-zap-master" }
	}
	SetScript = {
		mkdir "C:\tools\powershell-zap-master"
		$gitexe = "${ENV:ProgramFiles}\Git\cmd\git.exe"
		$arguments = 'clone https://github.com/solita/powershell-zap.git "C:\tools\powershell-zap-master"'
		$null = start-process $gitexe $arguments 
	}
	TestScript = {
		Return (Test-Path "C:\tools\powershell-zap-master")
	}
	DependsOn = "[cChocoPackageInstaller]installJdk8","[cChocoPackageInstaller]installGit" 
}
```

## The ugly

Only big let down that I have had with DSC is manipulating environments PATH variable. You can do it really easily but only once. 

```powershell
Environment setVS2017ToolsPath 
{
	Name = 'PATH'
	Ensure = 'Present'
	Path = $true
	DependsOn = "[cChocoPackageInstaller]installVisualStudio"
	Value = "${ENV:ProgramFiles(x86)}\Microsoft Visual Studio\2017\Professional\Common7\IDE"
}
```

After you have done that once and try to manipulate the exactly same named environment variable in the same configuration you will get error. Same applies also creating and deleting same file in the same configuration. Instead you can workaround with having multiple configurations or by using script resources in DSC. I have used script resources for this and well it is really ugly. 

```powershell 
# Set Java to path
Script SetJavaToPath 
{
	GetScript = {
		return @{ Result = $env:Path }
	}
	SetScript = {
		# Try to find Java bin path and force the result to string 
		[string]$javaBinPath = gci "${Env:ProgramFiles}\Java" -r -filter java.exe | Select Directory | Select-Object -first 1 | % { $_.Directory.FullName }
		# Adds javaBinPath to path variable 
		$newPathValue = $env:Path + ";"+$javaBinPath
		# You might need to reset your console after this 
		[Environment]::SetEnvironmentVariable("Path", $newPathValue, [EnvironmentVariableTarget]::Machine)
		# Add also path to current session
		$env:Path = $newPathValue
	}
	TestScript = {
		# Try to find Java bin path and force the result to string 
		[string]$javaBinPath = gci "${Env:ProgramFiles}\Java" -r -filter java.exe | Select Directory | Select-Object -first 1 | % { $_.Directory.FullName }
		if(-not $env:Path.Contains($javaBinPath))
		{
			# Do update
			Return $False
		}
		# Don't update
		Return $True
	}
	DependsOn = "[cChocoPackageInstaller]installJdk8"
}
```

Script resources are separated into three stages. 

1. GetScript which returns something to be printed 
2. SetScript which sets the value
3. TestScript which finds out if we need to set or not. 

Test is like unit test, it fails with false which means that DSC needs to run the SetScript. I have multiple copies in my script of this so check them from GitHub repository.

## Setup Jenkins startup parameters 

I must warn you. The next part will have some ugly stuff where I do xml regex replace with PowerShell to configure Jenkins and stuff like that. But we start with easier things. Here are all the variables that I have for Jenkins configuration in my script.

```powershell
param (
	$JenkinsPort = 8080,
	$JenkinsPlugins = @{},
	$JenkinsUsername = "",
	$JenkinsPassword = "",
	$JenkinsXmx = 1024,
	$JenkinsMaxPermSize = 128,
	$InstallConfDirectory = "./",
	$JenkinsInitScriptPath = "",
	$JenkinsUsernameTemplate = "",
	$JenkinsPasswordTemplate = ""
)
```

Now that you have seen all the variables we will introduce some mindblowing PowerShell magic and use them to setup Jenkins (it was already installed earlier. We can refer to those parameters with $Using:ParamName. 

```powershell
Script SetJenkinsServiceArguments
{
	SetScript = {
		$argString = "-Xrs -Xmx"+$Using:JenkinsXmx+"m -XX:MaxPermSize="+$Using:JenkinsMaxPermSize+"m -Djenkins.install.runSetupWizard=false -Dhudson.lifecycle=hudson.lifecycle.WindowsServiceLifecycle -jar `"%BASE%\jenkins.war`" --httpPort="+$Using:JenkinsPort+" --webroot=`"%BASE%\war`""
		Write-Verbose -Verbose "Setting jenkins service arguments to $argString"
		
		$Config = Get-Content `
			-Path "${ENV:ProgramFiles(x86)}\Jenkins\Jenkins.xml"
		$NewConfig = $Config `
			-replace '<arguments>[\s\S]*?<\/arguments>',"<arguments>${argString}</arguments>"
		Set-Content `
			-Path "${ENV:ProgramFiles(x86)}\Jenkins\Jenkins.xml" `
			-Value $NewConfig `
			-Force
		Write-Verbose -Verbose "Restarting Jenkins"
	}
	GetScript = {
		$Config = Get-Content `
			-Path "${ENV:ProgramFiles(x86)}\Jenkins\Jenkins.xml"
		$Matches = @([regex]::matches($Config, "<arguments>[\s\S]*?<\/arguments>", 'IgnoreCase'))
		$currentMatch = $Matches.Groups[1].Value
		Return @{
			'Result' = $currentMatch
		}
	}
	TestScript = { 
		$Config = Get-Content `
			-Path "${ENV:ProgramFiles(x86)}\Jenkins\Jenkins.xml"
		$Matches = @([regex]::matches($Config, "<arguments>[\s\S]*?<\/arguments>", 'IgnoreCase'))
		$argString = "-Xrs -Xmx"+$Using:JenkinsXmx+"m -XX:MaxPermSize="+$Using:JenkinsMaxPermSize+"m -Djenkins.install.runSetupWizard=false -Dhudson.lifecycle=hudson.lifecycle.WindowsServiceLifecycle -jar `"%BASE%\jenkins.war`" --httpPort="+$Using:JenkinsPort+" --httpListenAddress=127.0.0.1 --webroot=`"%BASE%\war`""
		$currentMatch = $Matches.Groups[1].Value
		
		Write-Verbose "Current service arguments: $currentMatch"
		Write-Verbose "Should be service arguments: $argString"
		
		If ($argString -ne $currentMatch) {
			# Jenkins port must be changed
			Return $False
		}
		# Jenkins is already on correct port
		Return $True
	}
	DependsOn = "[cChocoPackageInstaller]installJenkins"
}
```

I admit. The script could be cleaner. Nevertheless it sets startup arguments in jenkins.xml file to have given memorylimit parameters and listen only localhost on the given port. We listen only localhost because I don't feel Jenkins should be open in any network. I'll later on show how to setup IIS to be a reverse proxy in front of the Jenkins. 


## Initial authentication setup for Jenkins

If we would startup the Jenkins at this moment it would not be ready to get api requests from us which we will need to install plugins. So what we need to do is to setup a initialization script to setup authentication. We can do it by making sure that there is groovy script under Jenkins/init.groovy.d/ folder. All the groovy scripts are run on that folder are run on the Jenkins startup. Yes. That is a bit scary. The actual script setup is easy one:


```powershell
File JenkinsAuthenticationSetup 
{
	DestinationPath = $JenkinsInitScriptPath
	SourcePath = (Join-Path $InstallConfDirectory "solita_jenkins_security_realm.groovy")
	Ensure = "Present"
	Type = "File"
	Checksum = "modifiedDate"
	Force = $true
	MatchSource = $true
	DependsOn = "[cChocoPackageInstaller]installJenkins"
}
```

So we put a groovy script there and it is set. That script checks the authorization strategy and sets it to be full control once logged in authorization strategy. It also creates a user with given username and password. The script file has placeholders for username and password so we just use again some a pretty ugly scripting to replace them with given parameters. 

```powershell 
Script SetJenkinsAuthenticationUsername
{
	SetScript = {
		$username = $Using:JenkinsUsername
		(Get-Content $Using:JenkinsInitScriptPath).Replace($Using:JenkinsUsernameTemplate,$username) | Set-Content $Using:JenkinsInitScriptPath
	}
	GetScript = {
		$containsReplacaple = (get-content $Using:JenkinsInitScriptPath) | % {$_ -match $Using:JenkinsUsernameTemplate } | ? { $_ -contains $true }
		$aResult = $containsReplacaple -eq $True
		Return @{
			'Result' = $aResult
		}
	}
	TestScript = {
		$containsReplacaple = (get-content $Using:JenkinsInitScriptPath) | % {$_ -match $Using:JenkinsUsernameTemplate } | ? { $_ -contains $true }
		if($containsReplacaple -eq $True)
		{
			# needs configuration
			Return $False
		}
		Return $True
	}
}
Script SetJenkinsAuthenticationPassword
{
	SetScript = {
		$password = $Using:JenkinsPassword
		(Get-Content $Using:JenkinsInitScriptPath).Replace($Using:JenkinsPasswordTemplate,$password) | Set-Content $Using:JenkinsInitScriptPath 
	}
	GetScript = {
		$containsReplacaple = (get-content $Using:JenkinsInitScriptPath) | % {$_ -match $Using:JenkinsPasswordTemplate } | ? { $_ -contains $true }
		$aResult = $containsReplacaple -eq $True
		Return @{
			'Result' = $aResult
		}
	}
	TestScript = {
		$containsReplacaple = (get-content $Using:JenkinsInitScriptPath) | % {$_ -match $Using:JenkinsPasswordTemplate } | ? { $_ -contains $true }
		if($containsReplacaple -eq $True)
		{
			# needs configuration
			Return $False
		}
		Return $True
	}
}
```

## Start the Jenkins 

Nothing fancy here. This is the most common example of DSC usage. Script is really simple. Make sure that Jenkins is started automatically and that it is running. 

```powershell
Service JenkinsService
{
	Name        = "Jenkins"
	StartupType = "Automatic"
	State       = "Running"
	DependsOn = "[cChocoPackageInstaller]installJenkins","[Script]SetJenkinsServiceArguments","[File]JenkinsAuthenticationSetup","[Script]SetJenkinsAuthenticationUsername","[Script]SetJenkinsAuthenticationPassword"
} 
```

## Install plugins 

My coworker argued that the Jenkins is bad build server because it does not even give you timestamps on the console log by default. For all of this kind of arguments there is always the same counterargument. There is a plugin for that! We will need plugins. A lot of plugins. Actually more than 40 in our setup which would make with dependencies ... well a huge amount of foreign code running on your build server. A full list of plugins can be found at [here](https://github.com/solita/powershell-dsc-jenkins/blob/master/misc/jenkins_plugins.txt).

Now when we have happily setup the Jenkins and made sure that it is running we can start using its API to install some plugins. Here is a script that expects to have a list of plugins as a parameter. 

```powershell 
Script InstallJenkinsPlugins
{
	SetScript = {
		$plugins = $Using:JenkinsPlugins
		$port = $Using:JenkinsPort
		$password = $Using:JenkinsPassword
		$username = $Using:JenkinsUsername
		
		# Make sure that Jenkins is in the configurated state
		Restart-Service `
			-Name Jenkins
		Start-Sleep -s 15
		
		# Wait a bit for Jenkins to get online 
		$request = [system.Net.WebRequest]::Create("http://localhost:${port}")
		for ($i = 1; $i -le 10; $i++) {
			try {
				   $result = $request.GetResponse()
			} catch [System.Net.WebException] {
				   $result = $_.Exception.Response
			}
			
			if ($result -is "System.Net.HttpWebResponse" -and $result.StatusCode -ne "") {
				$done = "Got status"
				break
			}
			
			Write-Host "Get status attempt number $($i) failed. Retrying..."
			Start-Sleep -s 5
		}
		
		# Install plugins
		
		foreach ($jplug in $plugins) {
			Write-Verbose "installing $jplug"
			java -jar ${ENV:ProgramFiles(x86)}\Jenkins\war\WEB-INF\jenkins-cli.jar  -s "http://localhost:${port}" install-plugin $jplug --username $username --password $password
			# Wait a bit, Jenkins is kind of slow 
			Start-Sleep -s 5
		}
		Write-Verbose -Verbose "Restarting Jenkins"
		Restart-Service `
			-Name Jenkins
	}
	GetScript = {
		Return @{ Result = Get-ChildItem "${ENV:ProgramFiles(x86)}\Jenkins\plugins" | Select Name }
	}
	TestScript = {
		# Check if there are plugins
		$directoryInfo = Get-ChildItem "${ENV:ProgramFiles(x86)}\Jenkins\plugins" | Measure-Object
		# Directory is empty, do the update
		if ($directoryInfo.Count -eq 0) {
			Return $False
		}
		# Do not make update 
		Return $True
	}
	DependsOn = "[cChocoPackageInstaller]installJenkins","[Script]SetJenkinsServiceArguments","[File]JenkinsAuthenticationSetup","[Service]JenkinsService","[Script]SetJenkinsAuthenticationUsername","[Script]SetJenkinsAuthenticationPassword"
}
```

Now we have actual build server running that listens localhost. We have installed all the tools, all the plugins and setup the authentication so that we can start working on creating build jobs. At this point you might want to delete the authentication initialization script. You can't dot it with the same DSC script because it disallows manipulating same file twice in same configuration. Although you can do it afterwards with a single liner.

## Install IIS

I created separated script for this just because I felt that this script is a reusable one. So let's start from the beginning and introduce some Windows Features that we want to use in a brand new DSC script. The modules that we are using are the same as stated in the beginning so you would need to import them first. Here are the resources that we need: 

```powershell 
# Check the windowsfeature names with Get-WindowsFeature
# Install .NET 3.5
WindowsFeature NetFrameworkCore 
{
	Ensure    = "Present" 
	Name      = "NET-Framework-Core"
}
# Install Chocolatey
cChocoInstaller installChoco
{
	InstallDir = "c:\choco"
	DependsOn = "[WindowsFeature]NetFrameworkCore"
}
# Install the IIS role
WindowsFeature IIS
{
	Ensure          = "Present"
	Name            = "Web-Server"
}
# Install the ASP .NET 4.5 role
WindowsFeature AspNet45
{
	Ensure          = "Present"
	Name            = "Web-Asp-Net45"
}
# Install the web management console
WindowsFeature WebManagementConsole
{
	Ensure          = "Present"
	Name            = "Web-Mgmt-Console"
	DependsOn 		= "[WindowsFeature]IIS"
}
```

Basically we installed IIS WebServer with some tooling. Yet again the full script can be found at [here](https://github.com/solita/powershell-dsc-jenkins/blob/master/iis_reverse_proxy_dsc.ps1)

## Setup a website for proxying

The next thing would be to get rid of the "Default Web Site" just because I hate having it laying around. This is really simple task to do. 

```powershell
# Make sure to get rid of default web site
xWebsite DefaultWebSite
{
	Ensure          = "Absent"
	Name            = "Default Web Site"
	State           = "Stopped"
	PhysicalPath    = "C:\inetpub\wwwroot"
	DependsOn = "[WindowsFeature]AspNet45","[WindowsFeature]IIS"
}
```

Once we have got rid of that ugly thing we can create our own physical folder for the website and also the actual website. I have index.html ready for the proxy site just to make recognizing problems easier. 

```powershell
File JenkinsProxyFolder 
{
	DestinationPath = "C:\inetpub\JenkinsProxy\index.html"
	SourcePath = (Join-Path $InstallConfDirectory "index.html")
	Ensure = "Present"
	Type = "File"
	Checksum = "modifiedDate"
	Force = $true
	MatchSource = $true
}
# Create jenkins proxywebsite
xWebsite JenkinsProxyWebSite
{
	Ensure          = "Present"
	Name            = "JenkinsProxyWebSite"
	State           = "Started"
	PhysicalPath    = "C:\inetpub\JenkinsProxy"
	BindingInfo     = @(
		MSFT_xWebBindingInformation
		{
			Protocol              = "HTTPS"
			Port                  = 443
			CertificateThumbprint = $thumbPrint
			CertificateStoreName  = "My"
		}
	)
	DependsOn = "[WindowsFeature]AspNet45","[WindowsFeature]IIS","[File]JenkinsProxyFolder"
}
```

You might have noticed that the site was setup with HTTPS and it has a thumbprint as a parameter. I was lazy and did just some manual script step before DSC for installing the certificate into the machine. It requires that you know how to get a .pfx for TLS. 

```powershell 
$thumbPrint = "your_thumbprint"
$thumb = Get-ChildItem cert:\localmachine\my | Where { $_.Thumbprint -like $thumbPrint }| Select Thumbprint
if($thumb -eq $NULL) 
{
	$mypwd = Read-Host -AsSecureString "Give password for certificate"
	Import-PfxCertificate -FilePath .\your_certificate.pfx cert:\localMachine\my -Password $mypwd
}
```

If you have no idea how to get a certificate. Then you might want to try this script. It creates a self-signed certificate and gives you the thumbprint that my script is asking.
```powershell
New-SelfSignedCertificate -DnsName "www.jenkinstest.fi" -CertStoreLocation "cert:\LocalMachine\My"
```

With this setup we should have in place a website that is running and responding in 443 port. If you want to support redirects from 80 to 443 too then you need to allow the 80 port too. 

## UrlRewrite and ApplicationRequestRouting 

To be able to finish the setup we will need a few more dependencies. Those are UrlRewrite and IIS-ApplicationRequestRouting. Here is a yet again easy setup for those two. 

```powershell 
# Install UrlRewrite
cChocoPackageInstaller UrlRewrite
{
	Name = "urlrewrite"
	DependsOn = "[cChocoInstaller]installChoco"
}
# Install UrlRewrite
cChocoPackageInstaller ApplicationRequestRouting
{
	Name = "iis-arr"
	DependsOn = "[cChocoInstaller]installChoco"
}
```

And then the fun ends and we will fall back to the ScriptResources and do some configuration madness. First of all we need to make sure that certain server variables are allowed. We can do it in this way:

```powershell 
Script ReWriteRules
{
	#Adds rewrite allowedServerVariables to applicationHost.config
	DependsOn = "[cChocoPackageInstaller]UrlRewrite"
	SetScript = {
		$current = Get-WebConfiguration /system.webServer/rewrite/allowedServerVariables | select -ExpandProperty collection | ?{$_.ElementTagName -eq "add"} | select -ExpandProperty name
		$expected = @("HTTPS", "HTTP_X_FORWARDED_FOR", "HTTP_X_FORWARDED_PROTO", "REMOTE_ADDR")
		$missing = $expected | where {$current -notcontains $_}
		try
		{
			Start-WebCommitDelay 
			$missing | %{ Add-WebConfiguration /system.webServer/rewrite/allowedServerVariables -atIndex 0 -value @{name="$_"} -Verbose }
			Stop-WebCommitDelay -Commit $true 
		} 
		catch [System.Exception]
		{ 
			$_ | Out-String
		}
	}
	TestScript = {
		$current = Get-WebConfiguration /system.webServer/rewrite/allowedServerVariables | select -ExpandProperty collection | select -ExpandProperty name
		$expected = @("HTTPS", "HTTP_X_FORWARDED_FOR", "HTTP_X_FORWARDED_PROTO", "REMOTE_ADDR")
		$result = -not @($expected| where {$current -notcontains $_}| select -first 1).Count
		return $result
	}
	GetScript = {
		$allowedServerVariables = Get-WebConfiguration /system.webServer/rewrite/allowedServerVariables | select -ExpandProperty collection
		return $allowedServerVariables
	}
}
```

Then once we have that setupped we can make the rewrite rules for routing all the traffic from 443 port to jenkins running in different port. 

```powershell 
Script JenkinsReverseProxy
{
	DependsOn = "[cChocoPackageInstaller]UrlRewrite","[cChocoPackageInstaller]ApplicationRequestRouting"
	SetScript = {
		$Name = "HTTPS Reverse Proxy to Jenkins"
		$proxyTargetPath = ("http://localhost:"+$Using:JenkinsPort+"/{R:0}")

		Clear-WebConfiguration -pspath $PsPath -filter "$Filter/rule[@name='$Name']"
		$Filter = "system.webserver/rewrite/rules"
		Clear-WebConfiguration -location $Site -pspath $PsPath -filter "$Filter/rule[@name='$Name']"
		Add-WebConfigurationProperty -location $Site -pspath $PsPath -filter "$Filter" -name "." -value @{name=$Name; patternSyntax='ECMAScript'; stopProcessing='True'}
		Set-WebConfigurationProperty -location $Site -pspath $PsPath -filter "$Filter/rule[@name='$Name']/match" -name url -value "(.*)"
		Set-WebConfigurationProperty -location $Site -pspath $PsPath -filter "$Filter/rule[@name='$Name']/action" -name "type" -value "Rewrite"
		# R:0 Is full phase, R:1 Is the domain with the port and R:2 is the querypart
		Set-WebConfigurationProperty -location $Site -pspath $PsPath -filter "$Filter/rule[@name='$Name']/action" -name "url" -value $proxyTargetPath
	}
	TestScript = {
		$current = Get-WebConfiguration /system.webServer/rewrite/rules | select -ExpandProperty collection | select -ExpandProperty name
		$expected = @("HTTPS to Jenkins")
		$result = -not @($expected| where {$current -notcontains $_}| select -first 1).Count
		return $result
	}
	GetScript = {
		$rules = Get-WebConfiguration /system.webServer/rewrite/rules | select -ExpandProperty collection
		return $rules
	}
}
```

If you are looking UrlRewrite rules first time that might look confusing. Basic idea is just to make a xml configuration for IIS. Next up we will need to setup an ARR proxy to actually get the proxy functionality enabled. Yet again we go with the ScriptResource and make some XML configuration.

```powershell
Script EnableARRProxy
{
DependsOn = "[WindowsFeature]WebManagementConsole","[WindowsFeature]IIS","[cChocoPackageInstaller]UrlRewrite","[cChocoPackageInstaller]ApplicationRequestRouting"
	SetScript = {
		$assembly = [System.Reflection.Assembly]::LoadFrom("$env:systemroot\system32\inetsrv\Microsoft.Web.Administration.dll")
		$manager = new-object Microsoft.Web.Administration.ServerManager
		$sectionGroupConfig = $manager.GetApplicationHostConfiguration()

		$sectionName = 'proxy';

		$webserver = $sectionGroupConfig.RootSectionGroup.SectionGroups['system.webServer'];
		if (!$webserver.Sections[$sectionName])
		{
			$proxySection = $webserver.Sections.Add($sectionName);
			$proxySection.OverrideModeDefault = "Deny";
			$proxySection.AllowDefinition="AppHostOnly";
			$manager.CommitChanges();
		}

		$manager = new-object Microsoft.Web.Administration.ServerManager
		$config = $manager.GetApplicationHostConfiguration()
		$section = $config.GetSection('system.webServer/' + $sectionName)
		$enabled = $section.GetAttributeValue('enabled');
		$section.SetAttributeValue('enabled', 'true');
		$manager.CommitChanges();
	}
	TestScript = {
		$assembly = [System.Reflection.Assembly]::LoadFrom("$env:systemroot\system32\inetsrv\Microsoft.Web.Administration.dll")
		$sectionName = 'proxy';
		$manager = new-object Microsoft.Web.Administration.ServerManager
		$sectionGroupConfig = $manager.GetApplicationHostConfiguration()
		$config = $manager.GetApplicationHostConfiguration()
		$section = $config.GetSection('system.webServer/' + $sectionName)
		return ($section -eq $null -and $section.GetAttributeValue('enabled') -eq $False)
	}
	GetScript = {
		$assembly = [System.Reflection.Assembly]::LoadFrom("$env:systemroot\system32\inetsrv\Microsoft.Web.Administration.dll")
		$sectionName = 'proxy';
		$manager = new-object Microsoft.Web.Administration.ServerManager
		$sectionGroupConfig = $manager.GetApplicationHostConfiguration()
		$config = $manager.GetApplicationHostConfiguration()
		$section = $config.GetSection('system.webServer/' + $sectionName)
		return $section.GetAttributeValue('enabled')
	}
}
```

Only last thing is to actually run the script. 

```powershell 
$ConfigData = @{
	AllNodes = 
	@(
		@{
			NodeName = "LocalHost"
		}
	)
}
$thumbPrint = "certificate_thumbprint"
$currentPath = (split-path -parent $MyInvocation.MyCommand.Definition)
$installConfPath = (join-path $currentPath "misc")
IIS_REVERSE_PROXY -ThumbPrint $thumbPrint -InstallConfDirectory $installConfPath -JenkinsPort 8080 -ConfigurationData $ConfigData
Start-DscConfiguration -Path .\IIS_REVERSE_PROXY -Wait -Verbose -Force
```

## Conclusion 

I really like how the PowerShell DSC makes some things to be so easy and self-explanatory. What I didn't like was the need to step down on to creating ScriptResources. Creating a script resource takes time and a lot of testing. You will need to run your script multiple times. This is of course there the idempotent nature of the DSC comes really handy. Although I was able to corrupt my PATH variable (in a VM) into horrible state while testing. Protip would be to get a VM for developing scripts. My usual setup is something like this: 

1. Windows 2016 server running on Hyper-V
2. Snapshot before running any scripts 
3. Another snapshot when all the software is installed (downloading all the stuff takes ages)
4. Develop on your own machine, throw in the new script for the VM
5. Run the script 
6. Repeat 4 and 5 and if you screw up badly then go back to snapshot from point 3.
7. Finally when you think you are ready go back to snapshot from point 2.

I hope you liked it. All the script is available at our [GitHub](https://github.com/solita/powershell-dsc-jenkins). 

## Known problems 

Few things that might be broken at the repository. If you are trying to setup the ZAP as a daemon you need to start it manually and change the port to something else since it have same default (8080) as my scripts have. Another thing that might be broken is that later on if you would like to use OWASP dependency check module that was installed. Then you might hit the problem (or not) that Java cacerts does not have let's encrypt intermediatory certificate. A  [fix](https://github.com/solita/powershell-dsc-jenkins/tree/master/certs) is in the repository in case you need it. 