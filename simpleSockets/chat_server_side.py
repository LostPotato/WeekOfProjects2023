# Chat server side
import socket

# Define constants to be used
HOST_IP = socket.gethostbyname(socket.gethostname())
HOST_PORT = 12345
ENCODER = 'utf-8'
BYTE_SIZE = 1024

# Set up the server socket, and bind it to ip port and set it to listen
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST_IP, HOST_PORT))
server_socket.listen()

# Let the user know they connected to a client
print('Server is running...\n')
client_socket, client_address = server_socket.accept()
client_socket.send("YOU ARE CONNECTED!".encode(ENCODER))

# Sending info to the client soccet
client_socket.send('You are connected to the server'.encode(ENCODER)) 

# Send/Recieve messages
while True:
    # recieve info from the client
    message = client_socket.recv(BYTE_SIZE).decode(ENCODER)
    
    # Quit if client wants to quit
    if message == 'quit':
        client_socket.send('quit'.encode(ENCODER))
        print('Ending the chat... GOODBYE!!')
        break
    else:
        print(f'\n{message}')
        message = input("Message: ")
        client_socket.send(message.encode(ENCODER))
#Closing the socket connection
server_socket.close()