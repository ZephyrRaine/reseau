import socket
import sys
import threading

class Server: # Définition de notre classe Personne

    def __init__(self): # Notre méthode constructeur
        self.users = list()
        self.sockets = list()
        self.userCount = 0
        
    def addClient(self, pseudo, client):
        self.users.append(pseudo)
        self.sockets.append(client)
        self.userCount+=1

    def chat(self):
        if len(self.users) != 0:
            print(str(len(self.sockets)) + " personnes")
            for i in range(0, len(self.sockets)):
                print("USER " + str(i))
                try:
                    data = self.sockets[i].recv(64)
                    print(data.decode())
                # if data:
                #     pseudo = self.users[i]
                #     msg = data.decode()
                #     new = pseudo + " : " + msg 
                #     for j in len(self.users):
                #         self.sockets[j].send(new.encode())
            

class Listener(threading.Thread):

    def __init__(self, serv):
        self.serv = serv
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = ("localhost", 50000)
        self.sock.bind(address)
        self.sock.listen(1)
        threading.Thread.__init__(self)

    def run(self):
        while True:
            print("Waiting for client")
            connection, client_address = self.sock.accept()
            print("Connection from ", client_address)
            connection.setblocking(0)
            self.serv.addClient("", connection)

server = Server()
listener = Listener(server)
listener.start()

while True:
    server.chat()