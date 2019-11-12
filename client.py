SERVER_HOST = "127.0.0.1"
SERVER_PORT = 1234

import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

print(f"Connecting to RELAY SERVER @ {SERVER_HOST}:{SERVER_PORT}...\n")
client.connect((SERVER_HOST, SERVER_PORT))

print("> Local connection to RELAY SERVER:", client.getsockname())

myServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
myServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

myServer.bind(client.getsockname())
myServer.listen()
assert client.getsockname() == myServer.getsockname()
print("> Starting P2P server on", myServer.getsockname())

import select
import time

readList = [client, myServer]

while True:
  conns, _, _ = select.select(readList, [], [], 1)
  for connection in conns:
    if connection is myServer:
      newConnection, client_address = myServer.accept()
      readList.append(newConnection)
      print("P2P | New connection from", client_address)
      
    elif connection is client:
      data = connection.recv(4096)
      if not data:
        print("RELAY | Server closed.")
        readList.remove(client)
      else:
        # Naively assume the data is an address tuple
        host, port = data.decode().split("|")
        port = int(port)
        print("RELAY | Got peer address:", (host,port))
        print(f"| Going to connect to {host}:{port}!")
        newClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        newClient.connect((host,port))
        newClient.send(b"Hey ;)")
    else:
      data = connection.recv(4096)
      if not data:
        print("Peer | A connection was closed.")
        readList.remove(connection)
      else:
        print("Peer | Data:", data.decode())
  time.sleep(1)
