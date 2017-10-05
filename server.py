import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = ("localhost", 44444)
sock.bind(address)
sock.listen(1)

while True:
    print("waiting")
    connection, client_address = sock.accept()
    try:
        print("connection from ", client_address)
        while True:
            data = connection.recv(64)
            print(format(data))
            if data:
                print('sending data back to the client')
                connection.sendall(data)
            else:
                print('no data from', client_address)
                break

    finally:
        connection.close()