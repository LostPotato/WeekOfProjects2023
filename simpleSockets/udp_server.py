# UDP SERVER SIDE
import socket 

# create a server side socket with (AF_INET) and (SOCK_DGRAM)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Binding the new socket to tuple
server_socket.bind((socket.gethostbyname(socket.gethostname()), 12345))

# We are not waiting for a connection, UDP is connectionless protocal
message , address = server_socket.recvfrom(10)

# print the recieved message
print(message.decode('utf-8'))
print(address)

# We are not waiting for a connection, UDP is connectionless protocal
message , address = server_socket.recvfrom(1024)

# print the recieved message
print(message.decode('utf-8'))
print(address)