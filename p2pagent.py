import socket
import threading
import pygame


pygame.init()
win = pygame.display.set_mode((612, 400))
clock = pygame.time.Clock()

game = True

myFields = []
enemyFields = []

toni = ('192.168.1.7', 50002)
nico = ('192.168.1.3', 50002)


def receive_messages(sock):
    while True:
        data, address = sock.recvfrom(128)
        newField = data.decode().replace('(', '').replace(')', '').split(',')
        if len(data.decode()) > 2:
            print("received new Message: " + str(newField))
            enemyFields.append((int(newField[0]), int(newField[1])))


mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mySocket.bind(('0.0.0.0', 50002))

receiver_thread = threading.Thread(target=receive_messages, args=(mySocket,))
receiver_thread.daemon = True
receiver_thread.start()

while game:
    clock.tick(16)
    win.fill((255, 255, 255))

    if pygame.mouse.get_pressed()[0]:
        message = str(pygame.mouse.get_pos())
        print("sending " + message + " to toni")
        mySocket.sendto(message.encode(), toni)
        myFields.append(pygame.mouse.get_pos())

    for field in enemyFields:
        pygame.draw.rect(win, (200, 30, 30), (field[0], field[1], 10, 10))

    for field in myFields:
        pygame.draw.rect(win, (30, 200, 30), (field[0], field[1], 10, 10))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

