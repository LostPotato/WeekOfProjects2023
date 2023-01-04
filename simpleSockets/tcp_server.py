#TCP Server Side
import socket

# Creating a server side socket using ipv4 (AF_INET) and TCP (socket_stream)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Getting IP address dynamically
#print(socket.gethostname()) #Host Name
print(socket.gethostbyname(socket.gethostname())) # Gets Ip using the current hose name

# Saving host IP in var
host_IP = socket.gethostbyname(socket.gethostname())

# Bind new socket to a tuple (IP Address, Port Address)
server_socket.bind((host_IP, 12345))

# Put the socket into listening mode!
server_socket.listen()

# listen forever to accept any connection
while True:
    # Accept every single connect and store two pieces of info
    client_socket, client_address = server_socket.accept()
    
    print(type(client_socket))
    print(client_socket)
    
    print(type(client_address))
    print(client_address)
    
    # success message when a coonection is made
    print(f"Connected to {client_address}")
    
    # Send a Connected message to the client
    client_socket.send("You are connected".encode("utf-8"))
    
    # close the connection
    server_socket.close()
    
    # breaking the looop
    break
# safe exit
print("Connection stopped success.")
