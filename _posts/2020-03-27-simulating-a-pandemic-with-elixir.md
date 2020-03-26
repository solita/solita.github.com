---
layout: post
title: Simulating a pandemic with Elixir
author: jgke
excerpt: >
  Wash your hands! Just how many deaths can you prevent by this simple trick?
  Take a look with this Elixir-based pandemic simulator.
tags:
 - Elixir
---

<img src="/img/simulating-pandemics-with-elixir/simulation.gif"
     alt="Simulation animation with 9 nodes" />

As I'm typing this, Finland has entered a state of emergency over COVID-19 and
it is generally recommended to apply social distancing for the time being. The
drastic measures aim to lessen the exponential curve and thus the impact of the
virus on Finland's healthcare services. How much does this actually help? Let's
find out.

Elixir is a dynamic language designed with scalability in mind. Built around
message passing and lightweight processes, building a simulator with nodes (=
persons) communicating with each other sounds like a good opportunity to use
Elixir.

Additionally, we want to visualize the social graphs for persons. GraphViz,
also known by its markup language dot, is a piece of software designed for
drawing graphs. It scales nicely into reasonable graph sizes.

What is message passing?
------------------------

A lot of Elixir is based around passing around messages. If you squint your
eyes just right, it's actually pretty close to calling methods in some
object-oriented language.

```elixir
# Create a process with initial state %{infected: false}
{:ok, pid} = Agent.start_link(fn -> %{infected: false} end)
# Update the :infected key to be true
Agent.update(pid, &Map.put(&1, :infected, true))
# Assert that the state has been updated
true = Agent.get(pid, &Map.get(&1, :infected))
```

A process is created here using the Agent abstraction, which is a wrapper
around GenServer. GenServer is an abstraction for Erlang processes, while Agent
provides a wrapper for managing its state. The process is initialized with a
map containing a single key `:infected`. `Agent.update/2` (that is, a function
taking 2 arguments) is then used to update the state of the process, and
`Agent.get/2` is used to get the current state of the process. The `&` syntax
is shorthand for lambdas, consider the Clojure equivalent `#(assoc % :infected
true)`.

Behind the scenes, `Agent.update/2` sends a message to the process created by
start_link. In the process itself, the process receives the message and handles
the update to its state. In both `update` and `get` the caller waits until the
operation is complete, and thus the functions are synchronous.

Scientific stuff
----------------

<img src="/img/simulating-pandemics-with-elixir/science.jpeg"
     alt="A picture of a dog behing chemistry equipment with text 'I have no idea what I'm doing'" />

I'm not a virologist, statistician nor do I have anything to do with
healthcare. None of the numbers or formulas are based on real-life data. That
said, my computer science background has taught me to use the
[Stetson-Harrison method](https://www.urbandictionary.com/define.php?term=Stetson-Harrison%20method)
for approximating various results, so that's what we're using here. The end
result looks nice, and that's all that matters, right?

```elixir
{dx, dy} = distance(person_count, a, b)
delta = :math.sqrt(:math.pow(dx, 2) + :math.pow(dy, 2))
probability = (person_count / (100 * delta)) * infection_rate
```

Nodes will be placed in a grid. On every simulation tick, each infected person
has a chance to infect each connected cell based on node distance. Each
infected person also has a small chance (0.001%) to die on each tick. If there
are enough infected persons at any given time (20% of the population) the death
chance grows tenfold.

Scaling up
----------

<figure>
  <video width="600" height="248" controls="controls">
  <source src="/img/simulating-pandemics-with-elixir/output-1.webm" type="video/webm"></source>
  </video>
  <figcaption style="text-align: center">Video: simulator ran with 400 nodes</figcaption>
</figure>
<br />

How big graphs Elixir can handle without thinking too much about the
implementation? I built a simple simulator that connects a bunch of nodes to
each other, forming a weighted undirected graph with weights based on node
distance. The weights are used for probabilities of the infection spreading. If
infected, each node has a small chance to die on every tick. The probability of
death increases if the network has too many simultaneously infected nodes. With
10000 persons, the simulator runs without any optimizations at roughly 1 second
per tick. Since the simulator runs for roughly 50 ticks before nobody is
infected anymore, this is fast enough. Note that the processes are not executed
concurrently: each process is sent a message, then that process is waited for a
reply before sending a message to the next process.

```elixir
def step(self) do
  # Get all persons from the simulator's state, then call Person.interact/1
  # which returns a list of that person's connections while updating its state,
  # then call Person.infect/2 which infects the person with probability p
  Agent.get(
    self,
    fn state ->
      Map.values(state[:victims])
      |> Enum.flat_map(&Person.interact/1)
      |> Enum.map(fn {pid, p} -> Person.infect(pid, p) end)
      :ok
    end
  )
end
```

So back onto the original question. How much can flattening the curve help? Let's start with a
baseline simulation:

<img src="/img/simulating-pandemics-with-elixir/graph-1.png" alt="Line graph from 10000 nodes" />

Roughly 1000 people died in about 40 ticks. What happens if we drop the
infection rate to a tenth of the original by sticking home, washing hands et
cetera?

<img src="/img/simulating-pandemics-with-elixir/graph-2.png" alt="Line graph from 10000 nodes" />

The death rate is roughly halved, which means about 500 additional persons get
to live another day.

Summary
-------

Elixir can easily handle 10000 processes without having to think too much about
optimized implementations. A straightforward implementation can simulate a
complex system with thousands of processes with a couple of lines of code.

Washing hands saves lives. Check out more tips on keeping yourself and others
safe from [WHO's web site.](https://www.who.int/emergencies/diseases/novel-coronavirus-2019/advice-for-public)

Check out the code behind this blog post at [GitHub](https://github.com/jgke/epidemic).
