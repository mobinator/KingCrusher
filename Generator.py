import json

import pygame
from Empty import *
from pygame import Vector2


class Generator(CollisionShape2D):

    def __init__(self, center, current_timer_time):
        super().__init__(center, Vector2(120, 120))
        pygame.time.set_timer(Events.COIN, int(current_timer_time))
        
        self.initial_window_size = (612, 400)
        self.window_size = pygame.display.get_surface().get_size()
        
        self.building_animations = [pygame.image.load(f'assets/landscape/generator/{i}.png') for i in range(1, 8)]
        self.final_image = pygame.image.load('assets/landscape/generator/8.png')
        
        self.animation_index = 0
        self.animation_speed = 10
        self.animation_time = 0
        self.finished_building = False

    def __init__(self, center):
        super().__init__(center, Vector2(120, 120))

        self.initial_window_size = (612, 400)
        self.window_size = pygame.display.get_surface().get_size()

        self.building_animations = [pygame.image.load(f'assets/landscape/generator/{i}.png') for i in range(1, 8)]
        self.final_image = pygame.image.load('assets/landscape/generator/8.png')

        self.animation_index = 0
        self.animation_speed = 10
        self.animation_time = 0
        self.finished_building = False

    def draw(self, win):
        scale_factor = self.window_size[0] / self.initial_window_size[0]
        if not self.finished_building:
            img = pygame.transform.scale(self.building_animations[self.animation_index],
                                         (int(120 * scale_factor), int(120 * scale_factor)))
        else:
            img = pygame.transform.scale(self.final_image, (int(120 * scale_factor), int(120 * scale_factor)))
            
        win.blit(img, self.pos)

    def update(self, events):
        self.window_size = pygame.display.get_surface().get_size()
        if not self.finished_building:
            self.animation_time += 1
            if self.animation_time > self.animation_speed:
                self.animation_time = 0
                self.animation_index += 1
                if self.animation_index == len(self.building_animations):
                    self.finished_building = True

    def __str__(self):
        data = {
            "type": "Generator",
            "x": self.pos.x,
            "y": self.pos.y
        }

        return json.dumps(data)
