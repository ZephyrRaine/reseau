import socket
import sys
import threading
import random

#Thread watching for new clients trying to connect
class Listener(threading.Thread):

    def __init__(self, server, socket):
        self.server = server
        self.socket = socket
        self.socket.listen(2)
        threading.Thread.__init__(self)
        self.start()

    #Waits for connexion and expects an encoded nickname
    def run(self):
        while True:
            if len(self.server.openConnections) < 2:
                connection, client_address = self.socket.accept()
                handle = "Player " + str(len(self.server.openConnections))
                print("Connection from " + handle + "@", client_address)
                self.server.addClient(handle, connection)
            else:
                self.server.startGame()
                break
#Thread for each new client connecting to server
class ClientConnection(threading.Thread):
    def __init__(self, server, socket):
        self.socket = socket
        self.server = server
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        while True:
            try:
                data = self.socket.recv(64)
                print(data.decode())
            except ConnectionError:
                print("Terminating client connection thread with ", self.socket.family)
                self.server.removeClient(self)
                break
            else:
                if data:
                    self.server.sendMsg(data.decode().encode())

#Bridge starting main socket then handling connection sockets and forwarding messages to all
class Server:
    def __init__(self, port):
        self.openConnections = list()
        listeningSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = ("localhost", port)

        listeningSocket.bind(address)
        Listener(self, listeningSocket)
        
    def startGame(self):
        print("YOOOO")
        self.sendMsg(str(random.randint(0,1)).encode())

    #Spawns a new connection thread and adds it to the list
    def addClient(self, handle, socket):
        print("NEW CLIENT " + handle)
        c = ClientConnection(self, socket)
        self.openConnections.append(c)
        c.socket.send(str(len(self.openConnections)-1).encode())

    def removeClient(self, connection):
        connection.socket.close()
        self.openConnections.remove(connection)

    #Forwards messages to all clients (including sender)
    def sendMsg(self , data):
        for i in range(0, len(self.openConnections)):
            self.openConnections[i].socket.send(data)

port = input("Enter port: ")
server = Server(int(port))

# ¯\_(ツ)_/¯ 
while True:
    if False:
        print("How to do infinite loops in Python?")