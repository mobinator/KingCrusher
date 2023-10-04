import socket
import threading

toni = ('192.168.1.7', 50002)
nico = ('192.168.1.3', 50002)


def receive_messages(sock):
    while True:
        data, address = sock.recvfrom(128)
        print(f"Received message from {address[0]}: {data.decode()}")


mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mySocket.bind(('0.0.0.0', 50002))

receiver_thread = threading.Thread(target=receive_messages, args=(mySocket,))
receiver_thread.daemon = True
receiver_thread.start()

while True:
    message = input("> ")

    mySocket.sendto(message.encode(), toni)
