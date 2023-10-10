import pygame

from Empty import *
from Boulder import Boulder
from Generator import Generator
from Background import Background


class Game(Empty):
    def __init__(self):
        super().__init__(0, 0)

        self.render_layers = [[], [], [], [], []]
        self.collision_layers = [[], [], [], [], []]
        self.game_objects = []
        
        self.background = Background(pygame.display.get_surface().get_size())

        self.player = None
        self.coin_delay = 1000

    def update(self, events):
        self.background.update_window_size()

        for game_object in self.game_objects:
            game_object.update(events)

        for event in events:
            if event.type == Events.SHOOT:
                self.add_object(Boulder(self.player.center.copy(), event.power, event.inherited_speed), 4, 1)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.coin_delay /= 1.5
                self.add_object(Generator(self.player.center.copy(), self.coin_delay), 1, 1)

    def draw(self, win):
        self.background.draw(win)
        for render_layer in reversed(self.render_layers):
            for game_object in render_layer:
                game_object.draw(win)

    def set_player(self, player):
        self.player = player
        self.add_object(player, 2, 1)

    def add_object(self, game_object, render_layer, collision_layer):

        self.add_to_render_layer(render_layer, game_object)
        self.add_to_collision_layer(collision_layer, game_object)
        self.game_objects.append(game_object)

    def add_to_render_layer(self, layer_index, game_object):
        self.render_layers[layer_index].append(game_object)
        game_object.renderLayer = layer_index

    def add_to_collision_layer(self, layer_index, game_object):
        self.collision_layers[layer_index].append(game_object)
        game_object.collisionLayer = layer_index

