import pygame

from Boulder import Boulder
from Empty import Empty


class Events:
    DELETE = pygame.USEREVENT + 1
    COIN = pygame.USEREVENT + 2
    ATTACK = pygame.USEREVENT + 3


class Game:
    def __init__(self):

        self.game_objects: [Empty] = []
        self.renderLayers = [[], [], [], [], []]
        self.collisionLayers = [[], [], [], [], []]
        self.player = None

    def draw(self, win):
        for layer in reversed(self.renderLayers):
            for game_object in layer:
                game_object.draw(win)

    def update(self, events):
        for event in events:
            if event.type == Events.DELETE:
                print("Delete-Event", event.game_object)
                self.remove_game_object(event.game_object)
            if event.type == Events.ATTACK:
                self.add_game_object(Boulder(self.player.pos.x, self.player.pos.y, event.direction, event.power), 4, 2)

        for game_object in self.game_objects:
            game_object.update(events)

    def set_player(self, player):
        self.player = player
        self.add_game_object(player, 2, 1)

    def add_to_render_layer(self, layer, game_object):
        self.renderLayers[layer].append(game_object)

    def add_to_collision_layer(self, layer, game_object):
        self.collisionLayers[layer].append(game_object)

    def add_game_object(self, game_object, render_layer, collision_layer):

        game_object.renderLayer = render_layer
        game_object.collisionLayer = collision_layer

        self.game_objects.append(game_object)

        self.add_to_render_layer(render_layer, game_object)

    def remove_game_object(self, game_object):

        try:
            self.renderLayers[game_object.renderLayer].remove(game_object)
            self.game_objects.remove(game_object)
            self.collisionLayers[game_object.collisionLayer].remove(game_object)
        except ValueError:
            print("Couldn't find game_object")



