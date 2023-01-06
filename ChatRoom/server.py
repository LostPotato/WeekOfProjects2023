# Server side Chat Room
import socket, threading

# define the constant variables
# Define constants to be used

HOST_IP = socket.gethostbyname(socket.gethostname())
HOST_PORT = 12345
ENCODER = 'utf-8'
BYTESIZE = 1024

# Bind and listen
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST_IP, HOST_PORT))
server_socket.listen()

# Store info about clients conneect
client_socket_list = [] 
client_name_list = []

# 
def broadcast_message(message: str):
    '''
    Send a message to ALL clients that are connected
    '''
    for client_socket in client_socket_list:
        client_socket.send(message)

def recieve_message(client_socket: socket):
    '''
    recieve_message from a specific client
    '''
    while True:
        try:
            # get the name of the client
            index = client_socket_list.index(client_socket_list)
            name = client_name_list.index[index]
            
            print(index)
            print(name)
            # recieve the message
            message = client_socket.recv(BYTESIZE).decode(ENCODER)
            message = f'{name}: {message}'.encode(ENCODER)
            
            # print the message
            broadcast_message(message)
        
        except:
            # find the index of the client socket in the list
            index = client_socket_list.index(client_socket)
            name = client_name_list[index]
            
            # remove the client from the lists
            client_socket_list.remove(client_socket)
            client_name_list.remove(name)
            client_socket.close()
            
            # tell everyone that the client has left the chat
            broadcast_message(f'\033[5;91m{name} has left the chat...\033[0m'.encode(encoding=ENCODER))
            break

def connect_client():
    '''
    connects a client to the server socket
    '''
    while True:
        # Accepting any incoming clients to the server
        client_socket, client_address = server_socket.accept()
        print(f'CONNECTED WITH {client_address}...')
        
        # Send a name flag for the client to insert their name
        client_socket.send("NAME".encode(ENCODER))
        client_name = client_socket.recv(BYTESIZE).decode(ENCODER)
        
        # appending the name and socket to a list to keep track of clients
        client_socket_list.append(client_socket)
        client_name_list.append(client_name)

        # Update Server and ALL clients
        print(f'Name of new client is {client_name}...') # server side
        client_socket.send(f'{client_name}, you have connected to the server!\n'.encode(ENCODER))
        broadcast_message(f'{client_name} has joined the chat!'.encode(ENCODER))
        
        print(client_name)
        # Now that the client is connected start a new thread!
        recieve_thread = threading.Thread(target=recieve_message, args=(client_socket,))
        
        # run the thread
        recieve_thread.start()
        
connect_client()