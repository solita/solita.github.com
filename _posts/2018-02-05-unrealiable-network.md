---
layout: post
title: Quick Tips for App Developers on Surviving with Unrealiable Network
author: jarzka
excerpt: Methods that you, application developer, can do to make your app feel more stable even if the underlying network is unreliable.
tags:
- clojure
- clojurescript
- network programming
---

You cannot always choose where your application will be hosted. Sometimes the network infrastructure can be unrealiable, meaning that network requests can sometimes take a long time to complete and requests will fail at random rates. Even if these problems could not be prevented from happening, luckily we, application developers, have some tricks we can use to make our applications *feel* more stable in unrealiable network. And even if your network infrastucture is solid, these methods will probably help your application behave more stable and quickly for your end users. These quick tips are mainly targeted for developers writing single page web applications or mobile apps.

# Avoid Making Network Requests as Much as You Can

The best way to avoid getting failing network requests is of course to abandom making them completely.

![Failing network requests meme](/img/unrealiable-network/network_requests_meme.jpg)
**

Thought this is very efficient, it is not very practical for most of us. Majority of web and mobile apps depend on getting data from servers, and thus, making network requests is mandatory. Still, if we cannot abandom them completely, we can at least reduce the amount of them.

How can we reduce the amount of network requests? First, we should analyse what kind of requests our application is making. The developer tools of [Chrome](https://developer.chrome.com/devtools) and [Firefox](https://developer.mozilla.org/fi/docs/Tools) are very practical for this analysis. On the network tab, you can see all the requests your application is making.

![Chrome Network Tab](/img/unrealiable-network/chrome_network_tab.png)

The way to reduce the amount of requests depends on your application. The following questions can help you to find the requests that could be improved:

**Are you making two separate network requests for saving data and then getting the same data again from the server to update the view?** 

Consider changing the implementation of the data saving API to return the updated data. This way, you can save the data and update the view with one request.

**Are you making multiple network requests to get data for a specific view?**

Consider combining these requests, i.e. making a single API method to return all the data for a specific view. The services for the requests you previously made are already there and you can use them in creating a single API method.

**Is some specific request slowing down the initial render of your application?**

Your users want your application to load as quickly as possible, and thus you should only make the network requests that are absolutely mandatory to get your application up and running. If the network infrastructure is unstable, getting the application to load itself can take a long time or even fail completely.

# Retry with Increasing Timeout

Now that we have reduced the amount of requests, it is time to make sure those requests pass to the server and back as often as possible. If we cannot make modifications to the network infrastructure, we have to make changes in the application level.

Rater than calling the application environment's native functions for sending network requests every single time we make a network request, one would consider writing a separate communication API for your application. The idea of this API is to be a wrapper for the environment's native network request functions. The difference is that, with our own API, we can make global modifications on how the requests and responses are handled. For example, we can automatically re-try failing requests.

The idea with re-trying requests is the following: when our communication API is called to send a request to the server, it does this normally and returns the successful response to the caller. However, if the request fails, our API waits a few seconds, and tries to send the request again. If it fails again, it waits even more, and tries again. If the request keeps failing too many times, the API returns the failed request to the caller. In most cases, hopefully, the request is going to be successful after one or two attempts. The user of the API does not know anything about the failed requests. It does not need to, as our API automativally keeps trying sending the requests again. The caller is informed about the failed request only if it has failed multiple times. Here is a naive example of a communication API written in [ClojureScript](https://www.clojure.org):

```clojure
(def default-re-try-options {:timeout nil
                             :attempts 5})

(defn network-request
  ([response-chan request-options]
    ;; network-request called without re-try-options, use the default value.
   (network-request response-chan request-options default-re-try-options))
  ([response-chan request-options re-try-options]
   (let [response-handler (fn [[_ response]]
                            (if (some? response)
                              ;; Successful response, return it to the caller by using
                              ;; the given response channel.
                              (do (put! response-chan response)
                                  (close! response-chan))
                              ;; Failing response, any attempts left?
                              (if (> (:attempts re-try-options) 1)
                                ;; Try again, decrease attempts by one and increase timeout
                                (network-request
                                  response-chan
                                  request-options
                                  {:timeout (+ (:timeout re-try-options) 2000)
                                   :attempts (dec (:attempts re-try-options))})
                                ;; Return the failing response to the caller
                                (do (put! response-chan response)
                                    (close! response-chan)))))]
     ;; Send the network request, return the response to the response-handler
     (go
       ;; Before sending, wait for the timeout (if given)
       (when-let [re-try-timeout (:timeout re-try-options)]
         (<! (timeout re-try-timeout)))
       (ajax-request (merge
                       request-options
                       {:handler response-handler}))))))
```

In most cases, however, it is not practical to re-try every single failed request. For exampole, if a request pointed to a file which was not found and returned 404, it probably does not help to to try this request again. Thus, you should choose which requests you might want to try again.

# Cache Responses When Necessary

Caching is our friend when we want to make things work faster, but it is also a good way to help surviving with unreliable network connections. Our ultimate goal here is to avoid making requests that would probably return the same result as we got before. Caching can be used both client and server side.

On the client side, you could ask yourself if making a specific request with the same parameters multiple times on short intervals is absolutely necessary. If the server is probably going to return the same answer, you might consider caching the request's timestamp, parameters and response. If the same request is made again, with the same parameters, shortly after the previous one, you can simply return the answer from the cache, without making network requests. The downside is, of course, that the user does not get the most recent data from the server, so you should use clientside caching only when this is not a problem.

The idea is mostly the same on the server side. Caching can be used to avoid unnecessary network requests in the case when your server uses a third party API to load data for your client. Consider, for example, a case in which your client requests your server to the current weather conditions for a specific area, and your server requests this data from a third party API. Is it necessary to contact this third party API every single time a network condition request is made? Current weather conditions are probably not going to change radically in the next two minutes, so it should be safe to store the parameters and the response for all of the weather condition requests. If a new request is made with the same parameters in a few seconds, we can safely return the cached data, as it's likely going to be the same as the third party API would return us.

# When the Worst Happens: Tell You are Offline

This tip applies especially for single page and mobile applications, in which data is requested from the server between page loads. If the requests start failing, your application is probably going to look like a bunch of loading bars or icons. Your user can switch between application pages or views, but none of them is loading because of lost network connection. This is not a good user experience. Even if we cannot prevent network requests from failing from time to time, we can at least inform the user about the situation. A simple modal dialog or information bar at the top of your application will do fine, as long as you remember to remove it when the connection has been re-established. If possible, you might also want to consider allowing the user to keep using the application offline and sending the changes to the server when possible.

# Testing Apps By Simulating Unrealiable Network

Experience has shown me that we should always test how our applications work in unrealiable or slow network. When developing and testing an application locally with locally installed server and database, there is almost no network latency at all and the connections are very quick. Thus, you do not really get the real end user experience.

The possible problems that you do not see with fast connections can vary. A typical problem is for example a button, which when clicked, sends a network request, and is rendered as enabled for the whole time. In most cases, the user should not be able click the button when the network request is being processed, so the button should be rendered as disabled. When the request is processed very quickly on local development environment, this is not a problem, but can result unexpected errors in production environment.

Chrome and Firefox have good network throttling tools. On Chrome, the throttling tools can be found on the Network tab, while Firefox keeps them in the responsive design mode view. These tools help you to simulate slow network connections or disconnected connection. Unfortunately these tools do not contain a feature of testing randomly failing requests, but at least you can hit the Offline-button to simulate disconnected network during the use of the application.

# TLDR

Reduce the amount of network requests, combine them, re-try failed requests and cache the successful ones. And do not forget to test your application with unreliable network connection.

