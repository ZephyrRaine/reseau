import socket
import sys
import threading

#Thread watching for new clients trying to connect
class Listener(threading.Thread):

    def __init__(self, server, socket):
        self.server = server
        self.socket = socket
        self.socket.listen(10)
        threading.Thread.__init__(self)
        self.start()

    #Waits for connexion and expects an encoded nickname
    def run(self):
        while True:
            connection, client_address = self.socket.accept()
            handle = connection.recv(64).decode()
            print("Connection from " + handle + "@", client_address)
            self.server.addClient(handle, connection)

#Thread for each new client connecting to server
class ClientConnection(threading.Thread):
    def __init__(self, server, socket, handle):
        self.socket = socket
        self.handle = handle
        self.server = server
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        while True:
            try:
                data = self.socket.recv(64)
            except ConnectionError:
                print("Terminating connection thread")
                self.server.removeClient(self)
                break
            else:
                if data:
                    self.server.sendMsg(self.handle, data)

#Bridge starting main socket then handling connection sockets and forwarding messages to all
class Server:
    def __init__(self, port):
        listeningSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = ("localhost", port)
        listeningSocket.bind(address)
        Listener(self, listeningSocket)
        self.openConnections = list()
        
    #Spawns a new connection thread and adds it to the list
    def addClient(self, handle, socket):
        print("NEW CLIENT " + handle)
        self.openConnections.append(ClientConnection(self, socket, handle))

    def removeClient(self, connection):
        print("Removing ", connection.handle)
        self.openConnections.remove(connection)

    #Forwards messages to all clients (including sender)
    def sendMsg(self, handle, data):
        msg = handle + " : " + data.decode()
        for i in range(0, len(self.openConnections)):
            self.openConnections[i].socket.send(msg.encode())

port = input("Enter port: ")
server = Server(int(port))

# ¯\_(ツ)_/¯ 
while True:
    if False:
        print("How to do infinite loops in Python?")