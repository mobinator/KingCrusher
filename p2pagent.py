import socket
import threading

toni = ('192.168.1.7', 50001)
nico = ('192.168.1.3', 50001)

my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.bind(('0.0.0.0', 50001))
my_socket.sendto(b'0', toni)

while True:
    my_socket.sendto(input("> ").encode(), toni)


