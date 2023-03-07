---
layout: post
author: juhofriman
title: Crafting React with love
excerpt: React has been a real game changer in how we think about front-end architecture. I present a simple way of building quite robust and lovable React applications with single source of truth and one directional data flow inspired by re-frame architecture pattern.
tags:
- Frontend
- React
- Javascript
- Architecture
- State
- Programming
- Re-frame
- ClojureScript
---

Facebook's [React framework](https://facebook.github.io/react/) has been a real game changer when it comes to building single page apps. React endorses immutability and explicit state changes and hence can be seen a sort of functional front-end framework, because functional thinking, immutability and explicit state changes go pretty much hand in hand. Coming from frameworks and libraries endorsing two-way data binding and component encapsulated state this can seem really cumbersome, because one has to change whole mindset in how applications should be constructed. For instance, in [Angular](https://angularjs.org/) you hide state inside components and react accordingly (pun intended) when a state change is *detected*. In React you always perform explicit state changes and say: this is the new state, deal with it.

At first, this can feel a bit cumbersome. On top of that React does not actually give you much support or ideas in how your components should communicate with each other. React just basically says: keep state and delegate it as immutable props to child components and while at it try to keep state in as few components as you can. What if I need to (and I always do) communicate from child component to parent!? How do I do it in scenario like this:

- PhoneBookComponent (statefull)
  - PhonebookListing
    - Contact
      - DeleteButton (how to propagate click from here to state?)

Naive solution would be to pass a function as a prop from PhoneBookComponent to PhonebookListing and from there to Contact and from there to DeleteButton. Works, but is not too elegant.

I was building single page app in ClojureScript with great great great [Reagent framework](http://reagent-project.github.io/), which is a minimalistic ClojureScript wrapper for React. I needed some guidance in how I should construct my application when it got bigger and re-frame architecture seemed intresting. [Re-frame](https://github.com/Day8/re-frame) is an opinionated architecture in building SP-apps and it's pretty darn simple yet clean and elegant to my taste. I realised, that [Re-frame](https://github.com/Day8/re-frame) is an improved and more structured version of what I initially was doing when I was learning React.

This post presents a simple re-framish or reframe influenced architecture in building rather small scale vanilla React apps. It is more for you to improve your thinking in React and it's not a comprehensive guide in building robust React applications. For more comprehensive architecture you can check out [Flux](https://facebook.github.io/flux/).

## The big picture

[Re-frame](https://github.com/Day8/re-frame) is based on a simple idea of strictly one directional data flow. Re-frame introduces concept of app-database which contains all the state. In [Re-frame](https://github.com/Day8/re-frame) all the state really means **all the state**. State is kept *strictly* in single place and it is not encapsulated inside components. On top of that, components modify the state by events and do not interfere with it directly.

![Re-frame](/img/crafting-react-with-love/reframe.png)

This can feel really awkward, because everyone have told you before to isolate the state in well defined components. It can be even considered as a bad practice to have this sort of *global* state container. Now, take the red pill and really take some time to consider what user interfaces really are. User interface is a rendered state with functions for user to give input to modify that state and render it again. Sounds exactly like re-frame to me.

Using such architecture grants us a couple of really beneficial aspects. Firstly, you have *a single source of truth*. Everything that is in application state is in one place and not scattered around in million components. Secondly, most of your application is totally immutable, which means you can test rendering in isolation really simply by just altering the props given to components. This is really lean way of building ui-components, which you can just hook to application state when rendering satisfies you. Thirdly, you can test your state handling in isolation as well, because you are able to separate state functionalities in a separate module.

## How to do this then?

React comes out of the box with everything we need to build app in this sort of manner except one crucial part. We need some sort of event bus to trigger events from components which are then handled in stateful part of our application. Luckily, building simple eventbus is a no brainer in javascript. Here's my take.

```javascript
var eventbusState = {};

(function() {

    var handlers = {};

    eventbusState.publish = function(eventId) {
      if(handlers[eventId]) {
        handlers[eventId].func.apply(handlers[eventId].thisRef, Array.prototype.slice.call(arguments, 1));
      } else {
        console.warn('No handler for ' + eventId);
      }
    }

    /* Registers callback which is invoked for event id */
    eventbusState.on = function(thisReference, eventId, fn) {
      handlers[id] = { thisReference: thisReference, func: fn};
    }

    module.exports.publish = eventbusState.publish;
    module.exports.on = eventbusState.on;

})();
```

It could support multiple handlers for same event id and such, but let's keep it simple. Now we can utilize our event bus as a communication means between two React components.

```javascript
'use strict'

var React = require('react');
var ReactDom = require('react-dom');
var eb = require('./eventbus.js');

var CoolestButtons = React.createClass({
  cooler: function(){
    // Trigger event
    eb.publish('COOLER');
  },
  warmer: function(){
    // Trigger event
    eb.publish('WARMER');
  },
  coolerLabel: function() {
    if(this.props.currentTemp < -10) {
      return "More like in Hoth";
    }
    if(this.props.currentTemp < -5) {
      return "Even freezier";
    }
    return "Cooler"
  },
  render: function() {
    return (
      <div>
        <button onClick={this.cooler}>{this.coolerLabel()}</button>
        <button onClick={this.warmer}>Warmer</button>
      </div>
    );
  }
});

var CoolestApp = React.createClass({
  getInitialState: function() {
    // This is the app database!
    return { temp: 0 };
  },
  componentDidMount: function() {
    // Register handlers for events
    eb.on(this, 'COOLER', function() {
      this.setState({temp: this.state.temp - 1});
    });
    eb.on(this, 'WARMER', function() {
      this.setState({temp: this.state.temp + 1});
    });
  },
  render: function() {
    return (
      <div>
        <h1>Coolest app ever</h1>
        Temperature is {this.state.temp} C.
        <CoolestButtons currentTemp={this.state.temp}/>
      </div>
    );
  }
});

ReactDom.render(<CoolestApp />, document.getElementById('app-container'))
```

Note that the CooleastApp component passes the current temperature state as an immutable prob to CoolestButtons component which then uses it for rendering. When button is clicked an event is triggered to event bus which eventually modifies app database via handlers registered in CoolestApp component. The state propagates again to those lovely immutable child components. Really nice thing is that you can try out your component in complete isolation:

```javascript
ReactDom.render(<CoolestButtons currentTemp="-100" />, document.getElementById('app-container'))
```

![Coolest app](/img/crafting-react-with-love/coolest-app.png)

This application is overly simple, but the principle is very much the same with much larger applications.

## Phone book application in React with one directional data flow

Next, we construct a phonebook application using this sort of approach. Our application supports adding new contacts, deleting existing ones and live filtering for contact list. Because we are visual beings, we plan our application by connecting a couple of boxes together.

![Coolest app](/img/crafting-react-with-love/phonebook.png)

Code is available from [here](http://github.com/Solita/react-phonebook){:target="_blank"}. At initial stage, our application looks like this.

![Phonebook-1](/img/crafting-react-with-love/phonebook-1.png)

It doesn't actually do anything but looks fancy! Most certainly it does not have 1 000 contacts!

### Stage 1. Filtering input

First we create app database, the heart of our application containing all the state, and add some mock connections to it. We just getInitialState function for this. Then we pass connections in state as an immutable prop to ContactListing and vóila!

```javascript
module.exports = React.createClass({
  getInitialState: function() {
    return {
      contacts: [
        {firstname: 'Günther', lastname: 'Haapanen', phone: '045-422452525'},
        {firstname: 'Mock', lastname: 'Mockelson', phone: '045-2409209284'},
        {firstname: 'Guybrush', lastname: 'Threepwood', phone: '045-467467467'},
        {firstname: 'Ada', lastname: 'Lovelace', phone: '045-43746776'},
        {firstname: 'Jane', lastname: 'Doe', phone: '045-34646347'}
      ],
      nameFilter: ''
    };
  },
  // and so on...
})
  // <ContactListing contacts={this.state.contacts}/>
```

![Phonebook-2](/img/crafting-react-with-love/phonebook-2.png)

Now. Don't panic. Here's the real deal. When user enters something to the filtering input form, we want to trigger event UPDATE_FILTER and update our app database. We do that byt adding "nameFilter" attribute to out app database and pass that as a prop to FilterInput component. Then we trigger UPDATE_FILTER event with new value as a parameter and update state accordingly in handler. This is the data flowing almost in Zen-like manner unidirectionally. After this we simply pass contacts as a prop to listing component but do it via function which is aware of the name filter kept in the state.

![Phonebook-3](/img/crafting-react-with-love/phonebook-3.png)

Filtering! It works! [This is how it's done](https://github.com/solita/react-phonebook/commit/3cad440678caa92a3fc64a2c3950ba0fa28d2046){:target="_blank"}.

### Stage 2. displaying total count of connections

I'm sure you can figure this one out, it's such a trivial task. If not, checkout my [commit](https://github.com/solita/react-phonebook/commit/dbeae053ba66d40011d3c9e56027c5a994cf49d7){:target="_blank"}.

![Phonebook-4](/img/crafting-react-with-love/phonebook-4.png)

### Stage 3. Adding a new connection

It's important to realize that forms always have a state. When user inputs something to text field, he or she effectively changes the application state. Coming from here, it's clear that our application database must contain state of this form!

So first thing to do, is to define this into the application state!

```javascript
getInitialState: function() {
  return {
    // mock contacts omitted for brevity
    contacts: [],
    nameFilter: '',
    forms: {
      newContact: {
        firstname: '',
        lastname: '',
        phone: ''
      }
    }
  };
},
```

Then we pass that state as a prop to NewContactForm.

```
<NewContactForm data={this.state.forms.newContact}/>
```

And from there, we pass separate fields onward to FormInput components. Now it's a good time to test value propagation by setting something to state and expect it to render in inputs.

```javascript
getInitialState: function() {
  return {
    // mock contacts omitted for brevity
    contacts: [],
    nameFilter: '',
    forms: {
      newContact: {
        firstname: 'Can you see me? Firstname here!',
        lastname: 'Lastname calling!',
        phone: 'Phone number'
      }
    }
  };
},
```

![Phonebook-5](/img/crafting-react-with-love/phonebook-5.png)

Nice. Then just fire onChange events to eventbus and again, update the state accordingly.

```javascript
var FormInput = React.createClass({
  fireChangeEvent: function() {
    eb.publish('UPDATE_FORM_FIELD', this.props.id, this.refs.fieldValue.value);
  },
  render: function() {
    return (
      <input ref="fieldValue"
        value={this.props.value}
        type={this.props.type}
        name={this.props.id}
        id={this.props.id}
        onChange={this.fireChangeEvent}/>
    );
  }
});
```

If you try to modify fields now, they won't "echo" what you typed. This is because value is bound to a prop and it is not updated in the app database. Just hook event handler and update value in state.

Committing form should be just as easy. Just fire event from a click to add button and update app database accordingly. Do not try to send values from NewContactForm or something like that! Trust the state Luke! Just copy form values as a new contact to contact array. Whole point is that the app database is the only source of truth. Also, remember to reset the state of the form after succesful commit in order to clear inputs.

If you don't get it, maybe [my commit will clarify this](https://github.com/solita/react-phonebook/commit/4820f9ad0eda7ca27d0311ac2af1f442495705f7){:target="_blank"}.

![Phonebook-6](/img/crafting-react-with-love/phonebook-6.png)

### Stage 4: Deleting connection

This is easy as a pie. Just create button, and fire a event from it and update the app database accordingly. I'm sure you can figure it out, but [check out my commit](https://github.com/solita/react-phonebook/commit/99bab576bc7398be6e8fd6d5e883941a6e848ab9){:target="_blank"}.

![Phonebook-7](/img/crafting-react-with-love/phonebook-7.png)

## Onward!!!

This post did not deal with issues such as validation or talking to back ends. Validation is not that different. You just pass the state to components and validation result is derived from state. You must decide whether the component itself or the main application is responsible for validating data. In our example we should activate that add button only if every field has value in it. I would prefer passing "canCommit" or similar prop to component because it allows me to test component in complete isolation. This also keeps application logic in single place - components are stupid and just act according to props. It also allows to just render it without any state and see how it behaves when props are changed.

Talking to backend is even more straigh forward! Just fire an ajax-call, set flag in your app database which propagates as a loader or dirty state etc. in your components. When component is told to be loading by prop, render a spinner or similar. When response is received, just update app database and swich flag and you are done! Data still just flows from app database to components.
