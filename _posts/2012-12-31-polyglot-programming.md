---
layout: post
title: Polyglot programming
author: harmia
excerpt: The idea of polyglot programming is to render more natural and simpler solutions by combining the best solutions available from different programming languages and paradigms.
tags: Polyglot programming, poly-paradigm programming, multi language programming, cross-language programming
---

### Motivation and background ###

Software composed of artifacts written in multiple programming languages is pervasive in modern-day software business. The idea of polyglot programming is to render more natural and simpler solutions by combining the best solutions available from different programming languages and paradigms, thus polyglot programming is also poly-paradigm programming. Polyglot programming is mainly about the realization that there is ``No Silver Bullet''. In software development this raises an examination of languages, frameworks and development tools most suitable for the task at hand.

Polyglot programming has also been known as multi language programming. Lately it has also been referred as cross-language programming merely in the field of code analysis and refactoring. Similar ideas are also expressed in language oriented programming as a development methodology focusing on creation of domain specific languages.

### Definition ###

The term polyglot programming was [first introduced](http://www.drdobbs.com/polyglot-programming/184414854) in software development context in 2002. A hypothesis was made for several programming languages within one environment. Latter authors tend to use slightly [different approaches](http://olabini.com/blog/2008/06/fractal-programming/) describing polyglot programming. The best description to work with was given by [Watts](http://thewonggei.wordpress.com/2008/01/22/even-more-than-polyglot-programming/) as programming in more than one language within the same context.

Though this just postpones the definition onto what the context is. Definition of using a different languages on the same managed runtime was suggested. Means of managed runtime is definitely polyglot programming, but the definition should not restrict the architecture.

From a business perspective as well as from the developers perspective, the context can be seen around the people working on the project. And more so, the context depends on the number of teams and the way the produced applications are integrated. Polyglot programming is constituted even if one team uses different language regardless of architecture. If the integration between application parts developed by two separate teams using different languages is tight it will constitute as polyglot programming. However, when the different teams do not require information about the languages the other teams are using, the application is no longer considered as polyglot. Denoting that the application parts could be seen as distinct. An example would be a service-to-service application where knowledge of the interfaces between are the only requirements.

Fjeldberg defines and expands the previously described polyglot programming within a context for the first time in academic field in 2008. The formal definition of polyglot programming is considered as

>programming in more than one language within the same context, where the context is either within one team, or several teams where the integration between the resulting applications require knowledge of the languages involved.

In addition, a degree of polyglotism is suggested to differentiate use of polyglot programming. Presented levels of polyglotism are integration, organization of code, the processes within languages run, and the data being manipulated. Integration is either networked or non-networked, the organization of code differentiate the code within same or different files. Either the same or different processes can be used, and the languages manipulate either the same object or the same data.

Example architectures for utilizing polyglot programming are service oriented architecture (SOA), managed runtime, continuous integration (CI) and embedded polyglotism where different languages are presented in the same file. HTML in conjunction with CSS, JavaScript and a server side language is an example of a polyglot program (referred as HTML++ for abbreviation).

<table border="1" rules="groups">
<caption>Levels of polyglot programming of the presented architectures.</caption>
<thead style="background-color:#D0D0D0">
	<tr>
		<th style="padding-right:30px">Architecture</th>
		<th style="padding-right:30px">Integration</th>
		<th style="padding-right:30px">Organization</th>
		<th style="padding-right:30px">Process</th>
		<th style="padding-right:30px">Data/object</th>
	</tr>
</thead>
<tbody>
	<tr>
		<td>SOA</td>
		<td>Networked</td>
		<td>Different files</td>
		<td>Different</td>
		<td>Same data</td>
	</tr>
	<tr>
		<td>Managed runtime</td>
		<td>Non-networked</td>
		<td>Different files</td>
		<td>Same</td>
		<td>Same object</td>
	</tr>
	<tr>
		<td>HTML++ server</td>
		<td>Non-networked</td>
		<td>Different files</td>
		<td>Different</td>
		<td>Same data</td>
	</tr>
	<tr>
		<td>HTML++ client</td>
		<td>Non-networked</td>
		<td>Same file</td>
		<td>Same</td>
		<td>Same object</td>
	</tr>
	<tr>
		<td>CI</td>
		<td>Non-networked</td>
		<td>Different files</td>
		<td>Different</td>
		<td>Same data</td>
	</tr>
</tbody>
</table>

### Associated advantages ###

The definition and measurement of productivity are much debated aspects of programming languages. Two of the most used metrics are lines of code (LOC) and function points per unit time. Regardless of metrics an additional problem assessing the productivity of different programming languages exist, although it is stated that productivity is constant regardless of programming language. Evidence to the contrary is presented based on the assumption of insufficient data. Due to the nature of the problems within the scope of the productivity measurement, the findings from case studies are hard to generalize. Problems include human based factors like motivation, skill and experience and environmental factors like integrated development environment (IDE) and library support.

Basis for the increased productivity comes from the main idea of polyglot programming to combine and integrate the best solutions from different languages thus rendering simpler solution to the problem at hand. A suitable language for a particular problem will normally render a shorter solution regarding LOC because of the built-in primitives and idioms. Following the assumption that developers produce the same amount of LOC regardless of programming language, the high-level languages that require less LOC would be more productive. In addition to reduced LOC, the thought process will normally be shorter because the solution comes naturally in the appropriate language. The work can be done on the problem and not the required plumbing. For example taking advantage of functional nature, the race conditions and deadlocks in message passing between processes can be avoided. The nature of interpreted languages can further enhance the productivity in polyglot environment because no compile cycles are needed. 

A realization that developers are more expensive than hardware denotes that the importance of developers productivity transcends the runtime performance. Resulting in shorter development cycle providing faster time-to-market or the possibility of fewer developers working on the same application. However the initial development of application is only a part of the life cycle spanning often from 5 to 10 years. Therefore the increased productivity from choosing the appropriate language would become even more important in the maintenance phase. Furthermore the application written with less LOC will have fewer LOC to maintain, as well as fewer instructions to follow. The effort to maintain an application increases exponentially with the numbers of instructions, therefore the amount of instructions should be kept in minimum. Research also reveal that the number of faults per LOC increases with the total LOC in the application.

### Associated disadvantages ### 

Knowledge of different languages is essential in order to benefit from polyglot and poly-paradigm programming. Different problem areas should also be revised. This renders a problem because not all developers have vast knowledge over different programming languages and are not interested in learning new ones. Although it is suggested that developers should learn at least one new language per year to evolve, in many cases this has been proven not realistic, and also in many situations learning a new language takes more than a year. This is further enhanced when developers have accustomed in one language and the infrastructure, tools and certifications built around it. In addition, the knowledge required is increased especially in the hiring process and when selecting programming languages to use.

A conceptual hierarchy with more expressive and succinct programming languages at the top is presented. The so-called blub paradox after a hypothetical programming language of average complexity called ``Blub'' states that anyone preferentially using a particular programming language knows that it is more powerful than some, but not that it is less powerful than others. Resulting that writing in some language means thinking in that language, and that typically programmers are satisfied with whatever language they happen to use, because it dictates the way they think about programs.

Sufficient knowledge of the language used is required in the administration phase to conduct maintenance. The administration of a large application with a long life cycle spanning from 5 to 10 years is likely conducted by different developers or even by a different company than that who developed the application. This is further enhanced every time a new language is added, resulting in decrease in the pool of developers with enough knowledge to maintain the application. Also using a new paradigm parallel to a previously used will render following the application code even harder.

Developers using Java and .NET are accustomed having a diverse and comprehensive IDE support with integrated and plugin features like version control, syntax highlighting, refactoring, debugging et cetera. A support for a new programming language will normally only be implemented if it gains enough traction and popularity, because adding a support requires usually a tremendous amount of work. Therefore the overhead using different programming languages will increase if the tools do not offer interoperability, and different tools must be configured and used.
