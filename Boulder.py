import pygame.draw

from Empty import *


class Boulder(CollisionShape2D):

    def __init__(self, center, charge, inherited_speed: Vector2):
        super().__init__(center, Vector2(charge*10))

        if inherited_speed.length() > 0:
            self.direction = Vector2(0, -1) + inherited_speed/2

        self.direction = Vector2(0, -1)
        self.speed = 8 - charge

    def update(self, events):
        self.move(self.direction, self.speed)

    def draw(self, win):
        pygame.draw.rect(win, (0, 200, 0), (self.pos, self.size))
