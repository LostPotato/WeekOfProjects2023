 #TCP Client side
 
import socket
 
# creating the client side IPV4 socket(AF_INET) and TCP (Socekt_stream)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to a server at given ip and port
client_socket.connect((socket.gethostbyname(socket.gethostname()), 12345)) 

# Receive a Method from the server...specify the max number of bytes to recieve
message = client_socket.recv(1024)

# printing the message
print(message.decode("utf-8"))

# close the client socket
client_socket.close()
