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
        if self.socket:
            self.socket.close()

    def send(self, message):
        if self.socket:
            # print("sending: ", message)
            self.socket.sendto(message.encode(), (self.enemyIP, self.socketNum))

    def receive_messages(self):
        while self.running:
            data, address = self.socket.recvfrom(128)
            if len(data.decode()) > 0:  # and address[0] == self.enemyIP
                try:
                    data = json.loads(data.decode())
                    # print(data)

                    if data["type"] == "Player":
                        print("Player")
                    elif data["type"] == "Boulder":
                        print(data)

                        center = Vector2(data["x"], -data["y"])
                        charge = data["charge"]
                        inherited_speed = Vector2(data["inherited_speed"]["x"], data["inherited_speed"]["y"])

                        self.game.add_object(Boulder(center, charge, inherited_speed, True), 1, 1)
                    elif data["type"] == "Wall":

                        center = Vector2(data["x"], -data["y"])

                        self.game.add_object(Wall(center), 1, 1)

                    elif data["type"] == "Generator":

                        center = Vector2(data["x"], -data["y"])

                        self.game.add_object(Generator(center), 1, 1)

                except json.JSONDecodeError:
                    print("JSONMESSAGE WAS ENCODED WORONG")
