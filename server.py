import socket
import sys
import threading

class Listener(threading.Thread):

    def __init__(self, server):
        self.server = server
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = ("localhost", 50000)
        self.socket.bind(address)
        self.socket.listen(1)
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        while True:
            connection, client_address = self.socket.accept()
            pseudo = connection.recv(64).decode()
            print("Connection from " + pseudo + "@", client_address)
            self.server.addClient(pseudo, connection)

class ClientConnexion(threading.Thread):

    def __init__(self, server, socket, pseudo):
        self.socket = socket
        self.pseudo = pseudo
        self.server = server
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        while True:
            data = self.socket.recv(64)
            if data:
                self.server.sendMsg(self.pseudo, data)



class Server: # Définition de notre classe Personne

    def __init__(self): # Notre méthode constructeur
        self.openConnections = list()
        
    def addClient(self, pseudo, socket):
        print("NEW CLIENT " + pseudo)
        self.openConnections.append(ClientConnexion(self, socket, pseudo))

    def sendMsg(self, pseudo, data):
        msg = pseudo + " : " + data.decode()
        for i in range(0, len(self.openConnections)):
            self.openConnections[i].socket.send(msg.encode())


    # def chat(self):
    #     if len(self.users) != 0:
    #         print(str(len(self.sockets)) + " personnes")
    #         for i in range(0, len(self.sockets)):
    #             print("USER " + str(i))
    #             try:
    #                 data = self.sockets[i].recv(64)
    #                 print(data.decode())
                # if data:
                #     pseudo = self.users[i]
                #     msg = data.decode()
                #     new = pseudo + " : " + msg 
                #     for j in len(self.users):
                #         self.sockets[j].send(new.encode())
            

server = Server()
listener = Listener(server)
while True:
    if False:
        print("How to do infinite loops in Python?  ¯\_(ツ)_/¯ ")
