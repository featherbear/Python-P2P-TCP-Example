TCP Peer to Peer Connection Example + NAT Holepunching
---

[peer-to-peer]: https://featherbear.github.io/UNSW-COMP3331/post/peer-to-peer-architecture/

> In some cases, a [peer-to-peer] architecture may be preferred over the client-server architecture...  
One of these examples might include a messaging system - where one might wish to directly message another user without their top-secret-message being first sent to the central server.

---

This repository serves to provide an example of how a P2P connection can be set up.

# Getting Started

Ensure you have Python 3.6 or later installed, then launch ONE instance of `server.py`, and TWO instances of `client.py`

# Theory / Rationale

## server.py

When a socket listens to an address, it does so passively and does not broadcast its presence.  
Therefore we need a broker server, to exchange connection details between clients.

`server.py` acts as this broker server, storing the connection details of its clients, and relaying them to other clients.  
When two clients establish a [peer-to-peer] connection, any data sent between them is no longer sent through this server.

## client.py

`client.py` connects to the broker server and waits for connection details of another client.  
When a new host and port pair is received, the client connects to that new address and sends a message directly, without using the broker server anymore.  
To faciliate other peers connecting to the client, a server is actually hosted within the client as well, listening to the same port that it used to connect to the broker server.

---

## Aside: Port Reuse

You might wonder, why does the client listen to the same port that it uses to connect to the broker server?

One reason is that it **decreases the chance of the listening port being used already**.

Another reason is to do with how networks are connected, or more so, _protected_ from each other. In other words, firewalls _(and routing)_.  
Most firewalls will block inbound connections (unless explicitly opened through port forwarding, DMZ, etc), meaning that a remote device will not be able to access your computer.  
However, firewalls will temporarily allow an inbound connection to your computer **if you originate the request**.

In other words, if you connect to a remote server, the port used to connect to the remote server **will be unblocked** for a while.  
Therefore, by listening on that same port, we open up a window of time where other devices can connect directly to us!

> This concept is the essence of [NAT Holepunching](https://featherbear.github.io/UNSW-COMP6441/blog/post/something-awesome-research-connection/)
