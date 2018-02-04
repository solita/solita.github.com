---
layout: post
title: Quick Tips for App Developers on Surviving with Unrealiable Network
author: jarzka
excerpt: TODO
tags:
- clojure
- network
---

You cannot always choose where your application will be hosted. Sometimes the network infrastructure can be unrealiable, meaning network requests can sometimes take a long time to complete and requests will fail at random rates. Even if these problems could not be prevented from happening, luckily we, application developers, have some tricks we can use to make our applications *feel* more stable in unrealiable network. And even if your network infrastucture is solid, these methods will probably help your application behave more stable and quickly for your end users.

These quick tips are mainly targeted for developers writing single page web applications or mobile apps. The code examples are written in [Clojure](http://www.clojure.org) but can be implemented in any language.

# Avoid Making Network Requests as Much as You Can

The best way to avoid getting failing network requests is of course to abandom making them completely.

![Failing network requests meme](/img/unrealiable-network/network_requests_meme.jpg)
**

Thought this is very efficient, it is not very practical for most of us. Majority of web and mobile apps depend on getting data from servers, and thus, making network requests is mandatory. Still, if we cannot abandom them completely, we can at least reduce the amount of them.

How can we reduce the amount of network requests? First, we should analyse what kind of requests our application is making. The developer tools of [Chrome](https://developer.chrome.com/devtools) and [Firefox](https://developer.mozilla.org/fi/docs/Tools) are very practical for this analysis. On the network tab, you can see all the requests your application is making.

![Chrome Network Tab](/img/unrealiable-network/chrome_network_tab.png)

The way to reduce the amount of requests depends of your application. The following questions can help you to find the requests that could be improved:

**Are you making two separate network requests for saving data and then getting the same data again from the server to update the view?** 

Consider changing the implementation of the data saving API to return the updated data. This way, you can save the data and update the view with one request.

**Are you making multiple network requests to get data for a specific view?**

Consider combining these requests, i.e. making a single API method to return all the data for a specific view. The services for the requests you previously made are already there and you can use them in creating a single API method.

**Is some specific request slowing down the initial render of your application?**

Your users want your application to load as quickly as possible, and thus you should only make the network requests that are absolutely mandatory to get your application up and running. If the network infrastructure is unstable, getting the application to load itself can take a long time or even fail completely.

# Retry with Increasing Timeout

Now that we have reduced the amount of requests, it is time to make sure those requests pass to the server and back as often as possible. If we cannot make modifications to the network infrastructure, we have to make changes in the application level.

Rater than calling the application environment's native functions for sending network requests every single time we make a network request, I would consider writing your communication API for your application. The idea of this API is to be a wrapper for the environment's native network request functions. The difference is that our API can automatically re-try failing requests. It does this by waiting a few seconds after a request has failed, and tries it again. If it fails again, it waits even more, and tries again. If the requests keeps failing every single time, we finally returns the failed request to the caller. Still, if the request failed randomly (SASSA), our API makes sure those requests are automatically tried again. The user of the API knows nothing about failed requests until the request has failed multiple times.

TODO KOODIESIMERKKI

In most cases, however, it is not practical to re-try every single failed requests. For exampole, if a request pointed to a file which was not found, it is probably not useful to try this request again. However, if your application is hosted behind a proxy, and you now this proxy returns a specific error code in case of failure, it is useful to try these requests again a few times before accepting the request as a failure.

# Cache Responses

Caching is our friend when we want to make things work faster, but it is also a good way to help surviving with unreliable network connections. Our ultimate goal here is to avoid making requests that would probably return the same result as we got before. Caching and be using both client and server side.

On the client side, you could consider is making a single reques

On the server side, caching can be used to avoid unnecessary network requests in the case when your server uses a third party API to load data for your client. Consider, for example, a case in which your client requests your server to the current weather conditions for a specific area, and your server requests this data from a third party API. Is it necessary to contact this third party API every single time a network condition request is made? Current weather conditions are probably not going to change radically in the next two minutes, so it should be safe to store the parameters and the response for all of the weather condition requests. If a new request is made with the same parameters in a few seconds, we can safely return the cached data, as it's likely going to be the same as the third party API would return us.

# When the Worst Happens: Tell You are Offline

This tip applies especially for single page and mobile applications, in which data is requested from the server between page loads. If the requests start to keep failing, your application is probably going to look like a bunch of loading bars or icons (DDSDSS). This is not a good user experience, as the user can stil browse the application, but without getting any content from the server. Even if we cannot prevent it from happening from time to time, we can at least inform the user about the situation.

Depending on the application, you can prevent your user from using it completely by telling it's offline (ADSD). Or, if your application works at least partially offline, you can show a status bar about the offline mode. (SDDSD)



- Koskee erityisesti Single-Page sovelluksia
- Mahdollista offline työskentely
- Tallenna asiat lähetettäväksi servulle myöhemmin

# Testing with Unrealiable Network

Experience has shown me that we should always test how our applications work in unrealiable network or slow network. When developing and testing an application locally with locally installed server and database, there is almost no network latency at all and the connections are very quick. Thus, you do not really get the real end user experience.

- Chromessa ja Firefoxissa työkalut tähän, pistä kuvat


Unfortunately these tools do not contain a feature of testing randomly failing requests, but at least you can hit the Offline-button to simulate disconnected network during the use of the application.

- Yleisesti ottaen olisi hyvä aina testata softaa myös huonolla verkolla / offline? Voi paljastaa yllätyksiä. Lokaalisti yhteydet aina nopeat. Latauspalkit jää aina pois.

# TLDR

You cannot always choose the network infastructure for your application. Sometimes it's going to be unstable. Personally, these tips have helped me to make make my application *feel* more stable, even if it operates on unrealiable network.

Minimoi requestit, yritä failaavia uudelleen, cacheta vastaukset


