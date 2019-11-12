TCP Peer to Peer Connection Example
---

> In some cases, a [peer-to-peer](https://featherbear.github.io/UNSW-COMP3331/post/peer-to-peer-architecture/) architecture may be preferred over the client-server architecture...  
One of these examples might include a messaging system - where one might wish to directly message another user without their top-secret-message being first sent to the central server.

---

This repository serves to provide an example of how a P2P connection can be set up.

## server.py

When a socket listens to an address, it does so passively and does not broadcast its presence.  
Therefore we need a broker server, to exchange connection details between clients.

`server.py` acts as this broker server, and does not know of any data sent between clients, other than their connection details (host and port)

## client.py

`client.py` connects to the broker server and waits for connection details of other clients.  
When a new host and port pair is received, the client connects to that new address and sends a message directly, without using the broker server anymore.

## Running

Ensure you have python3 installed, then launch ONE instance of `server.py`, and TWO instances of `client.py`

---

## Aside: Port Reuse

You might wonder, why do the clients listen to the same port that they use to connect to the broker?

One reason is that it decreases the chance of the listen port being used by another process.

Another reason is to do with how network are connected, or more so, _protected_ from each other. In other words firewalls.  

_By default, most firewalls will prevent inbound connections (unless explicitly opened, port forwarded etc), meaning that a remote computer will not be able to access your server on the network._

But obviously there must be a way right?!  
Otherwise how can websites send data back to you!!!

> Firewalls will temporarily allow an inbound connection to your computer **if you originate the request**.

aka - If you connect to a remote server, the port that you connect from _will be unblocked_ for a while.

Therefore, by listening on the same port as the port we used to connect to the broker server - we create a window of time to where other devices an connect directly to us!

> This concept is the essence of [NAT Holepunching](https://featherbear.github.io/UNSW-COMP6441/blog/post/something-awesome-research-connection/)
