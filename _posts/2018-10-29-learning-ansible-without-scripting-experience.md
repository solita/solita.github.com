---
layout: post
title: Learning Ansible without scripting or programming experience? Here are a few tips.
author: aleksei
excerpt: Learning Ansible when you have little experience with scripting or programming might seem a complicated task. Here are my tips and tricks in learning Ansible.
tags:
- Ansible
- automation
- DevOps
---

There a people in IT Operations area who are not fluent in scripting. I can say that I am probably an example of such Operations person: my background is 90% related to Microsoft systems and historically I have been mastering only simple batch or Powershell scripts when it comes to scripting experience. Those Operations folks who deal with Linux every day might feel more natural with scripting, but this is not always the case.

When not feeling natural at scripting or programing, it may seem that configuration management tools would be something that you can’t become proficient with, but this is not true, it just takes a little more effort. Great thing about Ansible that it does not require any programming knowledge to use it. This is one of the reasons why the tool is so popular. 

Below are some tips that I’ve used while learning Ansible.

**Documentation and videos**

While learning Ansible, it is essential to read its official documentation. Ansible online documentation is really good and easy to understand. Another super helpful thing is video tutorials – these show how the stuff from documentation is working in practice. There are good video courses covering Ansible basics available on Pluralsight, LinkedIn Learning and even free ones on YouTube.

**Start with little stuff**

When you start working with a configuration management tool like Ansible, it might be tempting to go all-in and setup all your systems deployment straight away. Here’s the trouble though: since you’re quite new to Ansible, you don’t know all the small details – so you have to Google for a ready solution. With the help of Google, you might achieve the desired result, but it won’t give you much understanding of what is happening under the hood in Ansible project. Start small with package installs and service restarts and work your way from there.

**Have an example**

If possible, find a real-life working example of Ansible project including hosts inventory, roles, templates, variables. When you have a ready project as an example, it is much easier to get a full picture of Ansible configuration and understand how inventories, roles and variables cooperate with each other.

**Get a decent code editor**

Use a good code editor application to work with Ansible files. Visual Studio Code is a very nifty editor.

**Get inspiration from Ansible Galaxy**

Find some simple roles on Ansible Galaxy (like *nginx*/*apache* installation etc) and see what “tasks” directory contains – seeing what actual tasks/commands are performed really helps to understand what is happening under the hood when an Ansible role is executed. After all, it’s just a set of commands executed one by one on the host – no rocket science here. Don’t underestimate reading Readme files provided with the roles – very useful stuff.

**Use playbooks**

Best practice way is to use playbooks instead of single commands, even for simple stuff. Each time you write a playbook, it helps with understanding Yaml formatting and remembering the playbook structure. 

**Learn variables**

Variables are so important thing in Ansible, it is absolutely worth spending as much time as needed to understand variable usage, syntax, precedence etc.

**Learn and use source control system**

Did I already say I am an Ops person? I knew there are things like version control, Git and all this stuff that Devs use but it has usually been a black box for me. Well, configuration management means working with code, so it’s impossible to avoid using Git or similar. It turns out that it’s not that tricky stuff at all – for the most time you just need to remember very few commands: *git pull*, *git clone*, *git push*.

**Use modules**

Finally, consider using Ansible modules instead of running plain commands in sequence wherever possible. Many modules already do the heavy lifting for you, so you just write less code in the playbook as a result. 