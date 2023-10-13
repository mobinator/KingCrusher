import socket
import threading
import pygame
import VsIP


class Networking:

    def __init__(self):
        self.ownIP = VsIP.get_local_ip()
        self.enemyIP = None
        self.socketNum = 50002
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def set_enemy_ip(self, ip):
        self.enemyIP = ip

    def begin(self):
        self.socket.bind(('0.0.0.0', 50002))
