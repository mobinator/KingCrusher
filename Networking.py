import socket
import threading
from pygame import Vector2
import json
import VsIP
from Boulder import Boulder
from Player import Player
from Wall import Wall
from Generator import Generator


class Networking:

    def __init__(self):
        self.ownIP = VsIP.get_local_ip()
        self.enemyIP = None
        self.socketNum = 50002
        self.socket = None
        self.game = None
        self.running = True

        self.receiver = None

    def set_enemy_ip(self, ip):
        self.enemyIP = ip

    def begin(self, game):

        self.game = game

        if self.socket is None:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.bind(('0.0.0.0', self.socketNum))
        else:
            self.socket.sendto(b'0', (self.enemyIP, self.socketNum))

        self.receiver = threading.Thread(target=self.receive_messages)
        self.receiver.daemon = True
        self.receiver.start()

    def end(self):
        self.running = False
        if self.receiver and self.receiver.is_alive():
            self.receiver.join()
        if self.socket:
            self.socket.close()


    def send(self, message):
        if self.socket:
            # print("sending: ", message)
            self.socket.sendto(message.encode(), (self.enemyIP, self.socketNum))

    def receive_messages(self):
        while self.running:
            data, address = self.socket.recvfrom(128)
            if len(data.decode()) > 0: # and address[0] == self.enemyIP
                try:
                    data = json.loads(data.decode())

                    if data["type"] == "Player":
                        print("Player")
                    elif data["type"] == "Boulder":
                        center = Vector2(data["x"], data["y"])
                        charge = data["charge"]

                        self.game.add_object(Boulder())
                    elif data["type"] == "Wall":
                        print("Wall")
                    elif data["type"] == "Generator":
                        print("Generator")

                except json.JSONDecodeError:
                    print("JSONMESSAGE WAS ENCODED WORONG")
