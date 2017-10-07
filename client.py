import socket
import sys
import threading

class Watcher(threading.Thread):

    def __init__(self, socket):
        self.socket = socket
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        while True:
            data = self.socket.recv(64).decode()
            print(data)

class Client():

    def __init__(self, address, port, pseudo):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while self.socket.connect_ex((address,port))!=0:
            print("Waiting for server")
        self.socket.send(pseudo.encode())
        print("Successfully connected to ", address, " as ", pseudo)
        self.watcher = Watcher(self.socket)

    def writeMsg(self):
        while True:
            message = input()
            self.socket.sendall(message.encode())

address = input("Enter address: ")
port = input("Enter port: ")
pseudo = input("Enter nickname: ")
client = Client(address, int(port), pseudo)

while True:
    client.writeMsg()