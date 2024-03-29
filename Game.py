import pygame

import Constants
from Empty import *
from Constants import Events
from Boulder import Boulder
from Generator import Generator
from Background import Background
from Minimap import Minimap
from Wall import Wall


class Game(Empty):
    def __init__(self, networking):
        super().__init__(0, 0, 69)
        # collision and render layers
        self.render_layers = [[], [], [], [], []]
        self.collision_layers = [[], [], []]
        self.game_objects = []

        self.networking = networking
        
        self.background = Background(pygame.display.get_surface().get_size())
        
        self.minimap = Minimap(self)

        self.player = None
        self.enemy_player = None
        self.coin_delay = 750
        self.generator_count = 0

        self.health_bar_own = AnimatedSprite(
            Vector2(pygame.display.get_window_size()[0]/2 - 100, pygame.display.get_window_size()[1] - 100),
            pygame.image.load("assets/ui/lifebar/12.png"),
            [],
            0,
            Vector2(200, 120),
            self,
            animated=False
        )

        self.health_bar_enemy = AnimatedSprite(
            Vector2(pygame.display.get_window_size()[0] / 2 - 100, -60),
            pygame.image.load("assets/ui/lifebar/12.png"),
            [],
            0,
            Vector2(200, 120),
            self,
            animated=False
        )

    def update(self, events):
        self.background.update_window_size()

        for game_object in self.game_objects:
            if game_object:
                game_object.update(events)

        self.get_collisions()

        for event in events:
            if event.type == Events.SHOOT:

                self.add_and_send_object(Boulder(self.player.center.copy(), event.power, event.inherited_speed, False), 4, 0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    self.player.set_health(self.player.health - 1)
                if event.key == pygame.K_l:
                    self.enemy_player.set_health(self.enemy_player.health - 1)
                if event.key == pygame.K_g and Constants.ENABLE_DEBUG:
                    self.add_and_send_object(Generator(self.player.center + Vector2(0, -100), False), 1, 1)
                    self.add_generator()
                if event.key == pygame.K_h and Constants.ENABLE_DEBUG:
                    self.add_and_send_object(Wall(self.player.center + Vector2(0, -100), False), 1, 1)
                    self.add_generator()

            if event.type == Events.DELETE:
                self.delete_object(event.game_object)

            if event.type == Events.WIN:
                print("You Won")
                font = pygame.font.Font('assets/fonts/alagard.ttf', int(40))
                win_text = AnimatedSprite(
                    Vector2(pygame.display.get_window_size()) / 2 - Vector2(150, 20),
                    font.render("Du Hast Gewonnen!", True, (0, 0, 0)),
                    [],
                    30,
                    Vector2(300, 40),
                    self,
                    animated=False
                )
                self.add_to_render_layer(4, win_text)
            if event.type == Events.LOOSE:
                print("You Lost")
                font = pygame.font.Font('assets/fonts/alagard.ttf', int(40))
                win_text = AnimatedSprite(
                    Vector2(pygame.display.get_window_size()) / 2 - Vector2(150, 20),
                    font.render("Du Hast Verloren :(", True, (0, 0, 0)),
                    [],
                    30,
                    Vector2(300, 40),
                    self,
                    animated=False
                )
                self.add_to_render_layer(4, win_text)

        self.health_bar_own.set_sprite(pygame.image.load(f"assets/ui/lifebar/{self.player.get_health_string()}.png"))
        self.health_bar_enemy.set_sprite(pygame.image.load(f"assets/ui/lifebar/{self.enemy_player.get_health_string()}.png"))

    def draw(self, win):
        self.background.draw(win)
        for render_layer in reversed(self.render_layers):
            for game_object in render_layer:
                game_object.draw(win)
        self.minimap.draw(win)

        self.health_bar_own.draw(win)
        self.health_bar_enemy.draw(win)

    def get_collisions(self):

        for game_object in self.game_objects:
            for collision_object in self.game_objects:
                if collision_object != game_object and collision_object and game_object:
                    if game_object.check_collision(collision_object):
                        game_object.collide_with(collision_object)

    def set_player(self, player):
        player.game = self
        self.player = player
        self.add_object(player, 2, 0)

    def set_enemy_player(self, player):
        player.game = self
        self.enemy_player = player
        self.add_object(player, 3, 2)

    def add_object(self, game_object, render_layer, collision_layer):
        self.add_to_render_layer(render_layer, game_object)
        self.add_to_collision_layer(collision_layer, game_object)
        self.game_objects.append(game_object)
        game_object.objectIndex = len(self.game_objects) - 1

    def add_and_send_object(self, game_object, render_layer, collision_layer):

        self.add_object(game_object, render_layer, collision_layer)
        self.networking.send(str(game_object))

    def remove_generator(self):
        self.generator_count -= 1
        self.update_coin_delay()

    def add_generator(self):
        self.generator_count += 1
        self.update_coin_delay()

    def update_coin_delay(self):
        if self.generator_count == 0:
            self.coin_delay = 750
        elif self.generator_count == 1:
            self.coin_delay = 500
        elif self.generator_count == 2:
            self.coin_delay = 300
        elif self.generator_count == 3:
            self.coin_delay = 250
        else:
            self.coin_delay = 200

        print(self.coin_delay)

        pygame.time.set_timer(Events.COIN, int(self.coin_delay))

    def delete_object(self, game_object):
        # Log Nachricht zum Debuggen
        print(f"Deleting object: {self.game_objects[game_object.objectIndex]}")

        if isinstance(game_object, Generator) and not game_object.enemy_generator:
            self.remove_generator()

        # Objekt aus der allgemeinen Spielobjektliste entfernen
        object_index = game_object.objectIndex
        if 0 <= object_index < len(self.game_objects):
            self.game_objects[object_index] = None  # Setzen Sie das Element an dieser Position auf None, anstatt zu löschen, um den Index aller anderen Objekte zu erhalten

        # Objekt aus der entsprechenden Render-Schicht entfernen
        render_layer_index = game_object.renderLayer
        if 0 <= render_layer_index < len(self.render_layers):
            render_layer = self.render_layers[render_layer_index]
            render_layer_object_index = game_object.renderLayerIndex
            if 0 <= render_layer_object_index < len(render_layer):
                # Wir entfernen das Objekt direkt aus der Liste
                render_layer.pop(render_layer_object_index)

                # Aktualisieren Sie die renderLayerIndex-Eigenschaft für die restlichen Objekte
                for idx, obj in enumerate(render_layer[render_layer_object_index:]):
                    obj.renderLayerIndex = render_layer_object_index + idx

        # Objekt aus der entsprechenden Kollisionsschicht entfernen
        collision_layer_index = game_object.collisionLayer
        if 0 <= collision_layer_index < len(self.collision_layers):
            collision_layer = self.collision_layers[collision_layer_index]
            collision_layer_object_index = game_object.collisionLayerIndex
            if 0 <= collision_layer_object_index < len(collision_layer):
                # Wir entfernen das Objekt direkt aus der Liste
                collision_layer.pop(collision_layer_object_index)

                # Aktualisieren Sie die collisionLayerIndex-Eigenschaft für die restlichen Objekte
                for idx, obj in enumerate(collision_layer[collision_layer_object_index:]):
                    obj.collisionLayerIndex = collision_layer_object_index + idx

    def add_to_render_layer(self, layer_index, game_object):
        self.render_layers[layer_index].append(game_object)
        game_object.renderLayer = layer_index
        game_object.renderLayerIndex = len(self.render_layers[layer_index]) - 1

    def add_to_collision_layer(self, layer_index, game_object):
        self.collision_layers[layer_index].append(game_object)
        game_object.collisionLayer = layer_index
        game_object.collisionLayerIndex = len(self.render_layers[layer_index]) - 1
