# UDP Client Side
import socket

# create a udp ipv4 socket
client_socekt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# setting the place that the socket is sending info too
Local_IP = socket.gethostbyname(socket.gethostname())

# Send some info via a connectionless protocal
client_socekt.sendto('Hello server world!!'.encode('utf-8'), (Local_IP, 12345))

