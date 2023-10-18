from Empty import CollisionShape2D
from pygame import Vector2
import pygame


class EnemyPlayer(CollisionShape2D):

    def __init__(self, x: float, y: float):
        super().__init__(Vector2(x, y), Vector2(20, 20))

    def update_pos(self, pos):
        self.pos = pos
