import pygame

from pygame import Vector2
from Empty import CollisionShape2D


class Player(CollisionShape2D):

    def __init__(self, x: float, y: float):
        super().__init__(Vector2(x, y), Vector2(20, 20))

    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 255), (self.pos, self.size))

    def update(self, events):
        direction = self.calculate_move_direction()
        self.move(direction, 1.8)

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


