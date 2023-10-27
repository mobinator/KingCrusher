import json
import pygame
from pygame import Vector2

from Empty import CollisionShape2D
from Constants import *
from Generator import Generator
from Selectionmenu import SelectionMenu
from Wall import Wall


class Player(CollisionShape2D):

    def __init__(self, x: float, y: float, game):
        super().__init__(Vector2(x, y), Vector2(30, 40), 12)

        self.game = game

        self.initial_window_size = (612, 400)  # start size
        self.window_size = pygame.display.get_surface().get_size()

        self.build_menu = SelectionMenu(self)

        self.money = 0
        self.charge = 0
        self.base_speed = 1.8
        pygame.time.set_timer(Events.COIN, 1000)

        # animations
        self.animations = {
            "walking": [pygame.image.load(f'assets/king/walking/{i}.png') for i in range(1, 5)],
            "idle": [pygame.image.load(f'assets/king/idle/{i}.png') for i in range(1, 5)],
            "damage": [],
            "stamina": [pygame.image.load(f'assets/ui/stamina/{i}.png') for i in range(8)]
        }
        self.current_animation = "idle"
        self.current_frame = 0
        self.animation_time = 0
        self.flip_image = False

    def draw(self, win):
        # print("Scale Factor: ",scale_factor)
        player_sprite = pygame.transform.scale(
            self.animations[self.current_animation][self.current_frame],
            (40, 80)
        )

        # Draw Collision-Box
        if SHOW_HIT_BOXES:
            pygame.draw.rect(win, (255, 0, 0), pygame.rect.Rect(self.pos, self.size))

        if self.flip_image:
            player_sprite = pygame.transform.flip(player_sprite, True, False)

        player_sprite_offset = self.center-Vector2(player_sprite.get_size())/2
        player_sprite_offset += Vector2(0, -20)

        win.blit(player_sprite, player_sprite_offset)

        stamina_image = pygame.transform.scale(
            self.animations["stamina"][self.money],
            (120, 80)
        )
        stamina_pos = self.center-Vector2(stamina_image.get_size())/2
        stamina_pos += Vector2(0, -20)

        self.build_menu.draw(win)
        win.blit(stamina_image, stamina_pos)

    def move(self, direction: Vector2, speed: float):

        old_pos = self.pos.copy()
        old_center = self.center.copy()
        super().move(direction, speed)
        bbox = pygame.Rect(self.pos, self.size)

        for collision_object in self.game.collision_layers[1]:
            collision_shape_bbox = pygame.Rect(collision_object.pos, collision_object.size)
            if bbox.colliderect(collision_shape_bbox):
                self.pos = old_pos
                self.center = old_center

    def update(self, events):
        direction = self.calculate_move_direction()
        # calculating speed factor by different screen size
        self.window_size = pygame.display.get_surface().get_size()
        speed_factor = (self.window_size[0] * self.window_size[1]) / (
                    self.initial_window_size[0] * self.initial_window_size[1])

        # limit for balancing
        speed_factor = max(0.8, min(speed_factor, 7))
        # print("Speed Factor: ",speed_factor)

        self.move(direction, self.base_speed * speed_factor)

        # all selection menu options
        for event in events:
            if event.type == Events.COIN:
                self.process_coins()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.build_menu.toggle()
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                self.build_menu.close()
                if self.build_menu.state == "right":
                    if self.build_menu.placement_possible:
                        self.game.coin_delay /= 2.1
                        self.game.add_and_send_object(Generator(self.center.copy() + Vector2(0, -100), self.game.coin_delay), 1, 1)
                    else:
                        self.charge = 0
                        self.money = 7
                elif self.build_menu.state == "left":
                    if self.build_menu.placement_possible:
                        self.game.add_and_send_object(Wall(self.center.copy() + Vector2(0, -100), False), 1, 1)
                    else:
                        self.charge = 0
                        self.money = 7
                elif self.charge > 0:
                    pygame.event.post(pygame.event.Event(Events.SHOOT, power=self.charge, inherited_speed=direction))
                    self.charge = 0

                self.build_menu.reset_state()

        self.build_menu.update(events)
        self.animation_time += 1
        if self.animation_time > 5:  # animation speed
            self.animation_time = 0
            self.current_frame = (self.current_frame + 1) % 4

        if direction.length() == 0:
            self.current_animation = "idle"
        else:
            self.current_animation = "walking"
            self.flip_image = direction.x < 0

    @staticmethod
    def calculate_move_direction():

        direction = Vector2()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            direction.y = -1
        if keys[pygame.K_a]:
            direction.x = -1
        if keys[pygame.K_s]:
            direction.y = 1
        if keys[pygame.K_d]:
            direction.x = 1

        return direction

    def process_coins(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            if self.money > 0:
                self.charge += 1
                if self.charge == 7:  # Prüfen, ob charge 7 erreicht hat
                    self.build_menu.toggle()
            self.money -= 1
        else:
            self.money += 1
            self.charge = 0

        self.money = max(0, min(self.money, 7))

    def delete(self):
        pygame.event.post(pygame.event.Event(Events.LOOSE))
        super().delete()

    def get_health_string(self):
        if self.health >= 10:
            return str(self.health)
        elif self.health < 0:
            return "00"
        else:
            return "0" + str(self.health)

    def to_json(self):
        data = {
            "type": "Player",
            "x": self.center.x,
            "y": self.center.y
        }
        return data

    def __str__(self):
        return json.dumps(self.to_json())
