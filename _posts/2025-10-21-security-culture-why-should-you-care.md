---
layout: post
title: Security culture - why should you care
author: petteri.poyhtari
excerpt: >
  In this blog, we explore what security culture really means, what holds it back, and why we need both organizations and individuals to strengthen it together.
tags:
  - Security
  - Security Culture
  - Organization Culture
  - Software security
---

Just like company culture, security culture forms whether we intend it or not. Without attention, however, it can develop in the wrong direction. In this blog, I discuss the importance of security culture, the challenges it brings, and ways to strengthen it — both at the organizational and individual level.

## Security culture != security awareness

If you ask 150 companies what _security culture_ means, you’ll likely get 150 different answers. At its simplest, it’s about people’s attitudes toward security. Whether it’s seen as a burden or an asset. That attitude is reflected in an organization’s values and ways of working.

There are countless examples of poor security culture. One of the most striking in Finland was the [Vastaamo](https://en.wikipedia.org/wiki/Vastaamo_data_breach) case, where employees from management to system administrators paid little attention to information security. The consequences were devastating.

Excessive trust can also be costly. Russia obtained complete seabed data of the Gulf of Finland through a Finnish vocational school’s simulator project ([engineer colonel (ret.) Jyri Kosola, Futucast #517](https://www.youtube.com/watch?v=aOFIToSlqQ4&ab_channel=Futucast)). A stark reminder that a little paranoia can be healthy.

![Gulf of Finland](/img/2025-10-23-securitu-culture/boat.jpg)

Someone might think, _“It’s not that serious if our small company’s security is a bit lacking.”_ But very few operate in isolation. Even if your company isn’t directly connected to others, mere physical proximity can pose a risk. For instance, a Russian APT actor [once breached a target company’s network](https://www.securityweek.com/russian-cyberspies-hacked-building-across-street-from-target-for-wi-fi-attack/) by exploiting the Wi-Fi of a neighboring business.

Security culture could also be described as **security hygiene**. What’s the state of your organization’s hygiene? Could it endanger others as well? Small companies often serve as stepping stones for larger attacks, as seen in the [Maersk](https://www.wired.com/story/notpetya-cyberattack-ukraine-russia-code-crashed-the-world/) case.

## What Drives Individuals and Organizations Toward Poor Security Practices

> _Even if they are aware, it does not mean that they care_.

Everyone wants to build secure products. Very few neglect security intentionally. The reasons often come down to three factors: haste, laziness, or ignorance. These manifest in everyday choices - some safe, others not.

The biggest culprit is haste: there’s simply no time to do things properly. But relying on that excuse is dangerous. In software development, there’s _always_ time pressure and that perfect moment to “add security later” never actually comes.

Laziness is a close second. Classic examples include reusing passwords or skipping updates because applying them is too much work. _Shadow IT_ often emerges from this mix of laziness and haste. Shadow IT refers to employees finding ways to bypass organizational restrictions to get things done. For instance, using self-selected tools, services, or systems that the IT department doesn’t manage or even know about. This was a key factor in the [LastPass incident](https://duo.com/decipher/lastpass-attacker-compromised-employee-s-personal-machine). Shadow IT can also originate within IT itself: rigid processes and strict controls drive people to create risky workarounds. In one hospital, for example, a nurse kept bundles of doctors’ professional access cards and inserted them into hospital computers on request so doctors could log in remotely. Shadow IT inevitably [expands a company’s attack surface](https://www.bleepingcomputer.com/news/security/shadow-it-is-expanding-your-attack-surface-heres-proof/).

The third factor is ignorance. Sometimes it’s about using weak passwords, other times about lacking the technical skills to build secure network environments for services. Often, ignorance stems from the same roots — haste or laziness. Asking for help costs nothing, so it’s always better to seek guidance early.

## Practical Steps for Organizations

Once the three most common causes of poor security behavior are identified, we can start addressing them. Culture cannot be forced, it grows from people. And while changing human behavior is difficult, it’s both necessary and worth the effort.

- **Haste**
  - An organization should foster an environment that doesn’t reward results at any cost. Despite tight schedules, employees should feel empowered to care about security and to speak up when something seems wrong. To make that possible, leadership must show genuine concern for their people. No one should be punished for raising an issue.
  - Of course, time pressure will still strike and exceptions may be unavoidable. When intentional security compromises are made, document them carefully — what was done, why it was done, and what potential risks it introduces. Communicate this openly with the project team and the client. Mitigate the risks and discuss acceptance of any residual risk. To manage risks and threats effectively, regular threat modeling from the very start of a project is strongly recommended.
- **Laziness**
  - This is a challenging area to improve. Overly strict controls often provoke a backlash, as creative people find ways to bypass them. Security can easily be seen as a nuisance that slows work down. The situation improves when the organization provides well-functioning systems, clear processes, and responsive IT support. These measures help eliminate shadow IT.
- **Ignorance**
  - Security training and clear guidelines are essential. Without them, employees may not even know where to report phishing attempts or data breaches. Collaboration and breaking down silos help build awareness and shared understanding. When an organization encourages cooperation across teams and projects, its security culture strengthens. In contrast, individual bonuses and team-based competition tend to narrow focus to personal goals and security becomes “someone else’s problem,” usually IT’s.

An organization should also work to eliminate the **blame culture**, that is an atmosphere of fear. When every mistake leads to finger-pointing, people stop raising issues, and nothing improves. Employees who fail a phishing test shouldn’t be shamed; the result should be seen as feedback that guidance or training needs improvement. Blaming only drives problems underground — in the worst case, an employee who accidentally downloads malware might hide the mistake until it’s too late. Instead, raising concerns should be encouraged and rewarded.

Organizations trapped in a blame culture also tend to conceal incidents. Reporting is delayed, details are hidden, or breaches are outright denied. The outcome is always the same: the situation worsens and grows larger than it initially was.

A strong security culture needs role models. Leadership and senior employees must set the example. They should show that things are done properly and thoroughly. If they cut corners, everyone else will too.

Certifications like [ISO 27001](https://www.solita.fi/news/solitalle-iso-27001-tietoturvasertifikaatti/), which Solita recently achieved, or frameworks such as [NIS2](https://eur-lex.europa.eu/eli/dir/2022/2555/oj?locale=en), are excellent call-to-action tools. However, they alone do not guarantee a strong security culture.

Monitoring is also necessary, even though it’s not security culture in itself. It helps uncover weaknesses and identify opportunities for improvement.

## Practical Steps for Individuals

The internet is full of lists on how to improve security: use MFA, keep your passwords strong, don’t share personal information, and so on. Here, however, I want to look at the topic from a slightly different angle.

![Help your friends](/img/2025-10-23-securitu-culture/SolitaOulu-11.jpg)

- **Help your colleagues**
  - Not everyone is a security expert so let’s help each other. Someone might be a brilliant neurosurgeon yet still [copy-paste a fake CAPTCHA command into the terminal](https://www.malwarebytes.com/blog/news/2025/03/fake-captcha-websites-hijack-your-clipboard-to-install-information-stealers).
- **Communicate!**
  - Be clear about what you’re doing and why. Misunderstandings can come with a hefty price tag.
- **Write good instructions**
  - Good documentation helps people do things correctly and prevents both accidental and intentional security misconfigurations. It also reduces project risks across the board.
- **Be honest**
  - If a private key accidentally ends up in a Git repository (yes been there), fix it immediately. It’s easy to think, _“It’s just the dev environment”_ or _“I’ll handle it later”_, but don’t leave it hanging. Reissue the certificate right away. Even if it stings your schedule or your ego. Everybody makes mistakes.
- **Don’t cut corners**
  - The next time you’re tempted to push a security ticket _“few sprints forward”_, stop and think twice. Could you just do it now? Delay too long, and it might never get done.

## Summary

Security culture is built on everyday actions and attitudes. Guidelines and policies should be seen as partners on the journey toward stronger security, not as obstacles. When everyone takes responsibility for their actions and feels empowered to speak up about issues, the entire organization grows stronger. At Solita, this culture has been built patiently over time, and a strong security mindset is evident in our daily work. When we care and act responsibly, security is not a burden — it’s an enabler of trust, collaboration, and innovation that protects us all.
