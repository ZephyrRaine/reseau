import socket
import sys

# Create a TCP/IP socket
waitingFor = True
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = ("localhost", 50000)

while sock.connect_ex(address)!=0:
    print("Waiting for server")

print("Successfully connected to ", address)

while True:
    message = input("Write message: ")
    
    print(message)
    sock.sendall(message.encode())