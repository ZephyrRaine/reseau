import socket
import sys
import threading
from tkinter import *

#Thread taking care of receiving and displaying incoming messages
class Receiver(threading.Thread):
    def __init__(self, socket, client):
        self.client = client
        self.socket = socket
        threading.Thread.__init__(self)
        self.start()

    #Receive datas (blocking) and print them ater decoding (bytes => string)
    def run(self):
        while True:
            data = self.socket.recv(64).decode()
            if data:
                print(data)
                self.client.printMsg(data)

class Client():
    def __init__(self, address, port, handle):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while self.socket.connect_ex((address,port))!=0:
            print("Waiting for server")
        
        #Sending encoded nickname as first message (part of protocol)
        self.socket.send(handle.encode())
        print("Successfully connected to ", address, " as ", handle)

        #Init receiver thread
        self.receiver = Receiver(self.socket, self)

        ###
        # basic chat Tkinter code from the internet
        window = Tk()

        self.messages = Text(window)
        self.messages.bind("<Key>", lambda e: "break")
        self.messages.pack()

        
        self.input_user = StringVar()
        self.input_field = Entry(window, text=self.input_user)
        self.input_field.pack(side=BOTTOM, fill=X)

        frame = Frame(window)  # , width=300, height=300)
        self.input_field.bind("<Return>", self.Enter_pressed)
        frame.pack()
        
        window.mainloop()
        
        
    def Enter_pressed(self, event):
        input_get = self.input_field.get()
        self.sendMsg(input_get)
        self.input_user.set('')
        return "break"
    
        ###
    
    
    def sendMsg(self, message):
        self.socket.sendall(message.encode())

    def printMsg(self, message):
        self.messages.insert(INSERT, '%s\n' % message)

address = input("Enter address: ")
port = input("Enter port: ")
handle = input("Enter nickname: ")

client = Client(address, int(port), handle)

while True:
    if False:
        print("salut")