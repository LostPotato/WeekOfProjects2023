# client side chat room
import socket, threading, time

# Constants
DEST_IP = socket.gethostbyname(socket.gethostname())
DEST_PORT = 12345
ENCODER = 'utf-8'
BYTE_SIZE = 1024

# create the client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((DEST_IP, DEST_PORT))

def send_message():
    '''Send a message to the server to be broadcasted'''
    while True:
        message = input()
        client_socket.send(message.encode(ENCODER))
        
        
def recieve_message()-> None:
    '''Recieve an incoming message from the server'''
    while True:
        try: 
            # Recieve message and Decode
            message = client_socket.recv(BYTE_SIZE).decode(ENCODER)
            
            # Check for the name flag, else show the message
            if message == 'NAME':
                name = input("Please pick a chat room name: \n")
                client_socket.send(name.encode(ENCODER))
            else:
                print(message)
        
        # error handling
        except:
            # An error occured close the connection
            print("FATAL ERROR HAS OCCURED... CLOSING CONNECTION")
            client_socket.close()
            break

# create multiple threads to keep sending an recieving
recieve_thread = threading.Thread(target=recieve_message)
send_thread = threading.Thread(target=send_message)

# Starting the client Thread
recieve_thread.start()
send_thread.start()