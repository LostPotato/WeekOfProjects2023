# Chat client side
import socket

# set some constant variables to be used
DEST_IP = socket.gethostbyname(socket.gethostname())
DEST_PORT = 12345
ENCODER = 'utf-8'
BYTE_SIZE = 1024

# Create the client socket and connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((DEST_IP, DEST_PORT))

# Send and Recieve messages
while True:
    # Recieve message and Decode
    message = client_socket.recv(BYTE_SIZE).decode(ENCODER)
    
    # Quit if connect server quits else keep sending messages
    if message == "quit":
        client_socket.send('quit'.encode(ENCODER))
        print("\n Quiting.... goodbye!")
        break
    else:
        print(f'\n{message}')
        # clients is sending message
        message = input('Message: ')
        client_socket.send(message.encode(ENCODER))

# If we have quit, close socket
client_socket.close()
