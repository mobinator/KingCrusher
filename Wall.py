import json

import pygame
from Empty import *
from pygame import Vector2, image


class Wall(CollisionShape2D):

    def __init__(self, center, enemy_wall):
        super().__init__(center, Vector2(180, 120), 5)
        self.enemy_wall = enemy_wall

        self.sprite = AnimatedSprite(Vector2(-10, 0),
                                     image.load('assets/landscape/wall/8.png'),
                                     [pygame.image.load(f'assets/landscape/wall/{i}.png') for i in range(1, 8)],
                                     6,
                                     Vector2(200, 120), self)
        self.children.append(self.sprite)

    def draw(self, win):
        pygame.draw.rect(win, (255, 0, 0), pygame.rect.Rect(self.pos, self.size))
        self.sprite.draw(win)

    def update(self, events):
        super().update(events)

    def to_json(self):
        data = {
            "type": "Wall",
            "x": self.center.x,
            "y": self.center.y
        }
        return data

    def __str__(self):
        return json.dumps(self.to_json())
