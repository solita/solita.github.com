---
layout: post
title: "Two Years With React Native: Practical Experiences On Android Development"
author: jarzka
excerpt: React Native has been around for more than five years now. Is it mature enough for building high quality software while keeping developers happy? Let's find out.
tags:
 - React Native
 - JavaScript
 - Android
---

There are many ways to write software for mobile devices. When I started teaching myself mobile application development sometime in 2013, typical options were writing a native application separately for each mobile platform, or by creating a program with web technologies and possibly embedding it into a downloadable "hydrid" application. Both options have their pros and cons, so I decided to learn the essentials of both methods.

React Native entered the field in 2015. It introduced a new "hydrid native" development approach: creating truly native mobile applications by using a single JavaScript codebase which runs on multiple platforms (Android and iOS). Despite of using JavaScript, the big difference compared to embedded web applications is that the user interface layer uses platform specific native components. This makes the user interface of React Native apps feel truly native - because it is! Application logic layer can also use platform specific native APIs via large collection of open source JavaScript libraries. All of this changed my thinking of how mobile applications could be created, because in theory it makes multi-platform mobile application development much easier and faster than before.

## Jumping Aboard

I have been working in the software industry for more than five years now. Most of that time I have spent in Clojure projects, writing code for both servers and web browsers. Still, I am also familiar with more common web technologies, such as JavaScript, React and Redux. My first experience with React Native happened two years ago when I started working in a new project. The project consisted of a Clojure web application, and a separate mobile application for giving users a better offline experience. When I entered the project, the mobile application had been under development for half a year already and it had reached closed beta testing phase. 

Along with React Native itself, there were some important software libraries in use, such as **Realm** for providing a client-side mobile database, **Redux Form** for implementing forms, **React Native Navigation** for navigating between screens (not to be confused with React Navigation), and **Native Base** for additional user interface components. Even though these technologies are cross-platform, our mobile application targeted only Android devices in the beginning, since the user base consisted mostly of Android users.

## Entering React Native

Code written for React Native looks pretty familiar to anyone who has done web development with React. User interface is built around React components, which have lifecycle methods and rendering logic. The main difference between regular React and React Native is that we do not use HTML and CSS. Instead, we make use of the user interface components provided by React Native and Native Base. The component tree is written in JSX and looks pretty much the same as in React for web. CSS is not present, but styles are written as JavaScript objects that use CSS-like properties. Layout is created with Flexbox, which also works the same way as it does in CSS on the web with some minor exceptions. 

Here is an example of a React Native component:

```js
const GeneralStyles = StyleSheet.create({
  // Style maps look a lot like CSS
  MainContent: {
    padding: 5, // Values are unitless
    marginTop: 10
  },
}

class HelpSection extends Component {
  render() {
    /* Instead of div, span and other HTML elements, we use native elements,
     * which map to their native iOS and Android counterparts.
     * There are also some platform-specific components. */
    return (
      <Layout>
        <Content style={GeneralStyles.MainContent}>
          <HelpCard title="Workflow">
            <Text>React Native looks familiar.</Text>
          </HelpCard>
        </Content>
      </Layout>
    );
  }
}
```

Coming from web perspective, React Native code looked pretty familiar to me from day one in the project. Still, the big difference is that the code does not run in a web browser, but in an emulator during the development and finally in a physical mobile device. This was different, but not necessarely a difficult thing to manage. The experience of using the app in an emulator was mostly identical to running it on a physical device. There were some problems that raised only on a physical device though, so I do recommend always testing on a physical device before shipping the app to the customers.

## Development Experience with React Native

Past experience with React helped me a lot to start working in the project. Most of the time, there was not much of a difference coding React Native compared to React, which was a positive thing to me. I also enjoyed the simplicity of JavaScript much more than Java for writing Android applications - although it has been years the last time I did that. Unfortunately, when the development continued for a longer time, some problems started to rise too.

In web development, I like that my frontend code is automatically reloaded into the browser. In React Native, there was a similar hot reload functionality, but it did not always work as expected. Way too often the changes I made were simply not hot-reloaded into the emulator at all, or required me to restart the application. Debugging the user interface was also difficult. Modern browsers have comprehensive built-in tools for this type of work, but React Native contained only a basic inspector. I realised it was easier to debug UI by manually including red borders around elements to see how the layout was rendered. Fortunately, debugging application logic was possible via console logging, but for some reason React Native logging tool was unable to log big objects to the console. The log was simply cut off if the object to be logged was too big. We also had problems using some open source libraries together, for example toast messages could not be shown on top of React Native Navigation modals for some reason.

Many little issues like these slightly lowered my expectations on easy mobile development with React Native - it seemed that the single codebase approach worked much better in theory than in practice. Even if we were able to build working software, the development process and tools occasionally felt like what web development was in the 2000s. Luckily new versions of React Native were introduced during the project that could potentially make the development experience better. The problem, however, was that upgrading React Native and related libraries turned out to be intensely difficult.

## Working With Outdated Software

When I started working in the project, React Native and some of the related libraries were already lagging behind in development (we started with React Native 0.51). Despite of this, we were able to deliver a working application to closed beta testing. After this, however, the project entered a period in which we did not do much new development. Critical issues were fixed, but new features were not implemented for a long time, not to mention updating the outdated libraries.

When the development continued again, I noted that we had to try to upgrade React Native and libraries to ensure maintainability and smoother development experience. Furthermore, starting from August 2019, Google requires that all new Play Store applications and their updates have to support 64-bit architecture. The outdated React Native was unable to meet this requirement, so we would have had to make the upgrade anyway.

### Beginning Upgrade

In theory, the upgrade process should be painless. For instance, there is [React Native Upgrade Helper tool](https://react-native-community.github.io/upgrade-helper/), which shows the changes you need to make in your code in order to upgrade. You can also try to upgrade React Native automatically by running `npx react-native upgrade`. Nice and simple - or isn't it?

In practice, the upgrade process is way more difficult. React Native and Android evolve rapidly, and some libraries depend on specific React Native version. Virtually this means that when a big React Native upgrade is ahead, we cannot simply upgrade React Native without upgrading majority of the libraries at the same time. This not only makes the upgrading process arduous, but in case of problems the root cause might be difficult to clarify since so many things change at once. Also, since the whole React Native ecosystem is still relatively new, the APIs of libraries are also evolving, and not always in backwards compatible way.

### Upgrade Process

I began the upgrade process by first trying automatic upgrade. It did not work very well, so I then used the upgrade helper tool to manually make all the needed changes. Still, I was far away from software that could even be compiled again. Compiling raised a lot of not-so-developer-friendly errors, which I then googled and resolved one by one (many of these were related to BabelJS and linking native libraries). It also helped to download a working template project from GitHub and compare my configuration to it to spot potentially breaking differences. At some point, the software compiled again, but it was still far from usable as the screen was literally full of warnings and errors.

For instance, I realised that the version of React Native Navigation we used was so old that I did not even find a changelog for it. It turned out that the API of the library had changed completely, so a big part of the upgrade process was to rewrite almost all the navigation logic of our application.

Another mystical problem was caused by Realm, which we use to provide an easy to use offline database. After the upgrade, all database queries simply crashed with a mystical error. Downgrading was not an option, since the problem also occurred with the previous Realm version after upgrading React Native. The problem was reported in GitHub, but it took almost a month until a working workaround was found. A few months later, the problem was reported to be fixed.

Finally, after over 50 hours of work, the upgrade to React Native 0.62 was complete. It was clearly the most tedious software library upgrade I had ever done. Luckily, it turned out that the upgrade was worth the effort. Hot Reload worked more reliable (and it was renamed to Fast Refresh) and many minor issues were fixed. The upgrade also meant that we were able to use the latest version of [React Native Debugger](https://github.com/jhen0409/react-native-debugger).

## Notes To Self And Others

After working with React Native for two years, the experience has been mixed. Many minor issues with development tools and lack of proper debugging tools made the development process a bit painful, especially at the beginning. However, the framework and the related libraries evolve rapidly, and even if the upgrade process has been tidious, the updates have improved the ecosystem a lot. The fact that writing React Native code feels like writing a regular web application with React, but using native elements under the hood, has been a positive experience for me. The cross-platform functionality remains to be seen though as there is no iOS version of our application (yet).

All in all, despite of the mentioned challenges, I have positive attitude towards React Native. Writing separate applications for each mobile platforms is not an option for many, and embedded web applications simply cannot meet the native feel that React Native provides. Thus, I think it's safe to say that React Native and other similar frameworks are here to stay, and I'm looking forward how they will evolve in the coming years. I just hope that future upgrades of React Native are not as tedious and time-consuming as what we have experienced.