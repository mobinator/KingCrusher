import socket
import threading
import pygame
import VsIP


class Networking:

    def __init__(self):
        self.ownIP = VsIP.get_local_ip()
        self.enemyIP = None
        self.socketNum = 50002
        self.socket = None

    def set_enemy_ip(self, ip):
        self.enemyIP = ip

    def begin(self):
        if self.socket is None:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.bind(('0.0.0.0', 50002))

    def end(self):
        self.socket.close()

    def send(self, message):
        if self.socket:
            print("sending: ", message)
            self.socket.sendto(message.encode(), (self.enemyIP, 50002))
