import json

import pygame
from Empty import *
from pygame import Vector2, image


class Generator(CollisionShape2D):

    def __init__(self, center, enemy_generator, current_timer_time=None,):
        size = Vector2(120, 120)
        super().__init__(center, size, 2)
        if current_timer_time:
            pygame.time.set_timer(Events.COIN, int(current_timer_time))

        self.enemy_generator = enemy_generator

        self.sprite = AnimatedSprite(Vector2(0, 0),
                                     image.load('assets/landscape/generator/8.png'),
                                     [pygame.image.load(f'assets/landscape/generator/{i}.png') for i in range(1, 8)],
                                     6,
                                     Vector2(120, 120), self)
        self.children.append(self.sprite)

    def draw(self, win):
        pygame.draw.rect(win, (255, 0, 0), pygame.rect.Rect(self.pos, self.size))
        self.sprite.draw(win)

    def update(self, events):
        super().update(events)

    def to_json(self):
        data = {
            "type": "Generator",
            "x": self.center.x,
            "y": self.center.y
        }
        return data

    def __str__(self):
        return json.dumps(self.to_json())
