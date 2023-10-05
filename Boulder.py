from Empty import Empty
import pygame
from pygame import Vector2


class Boulder(Empty):
    def __init__(self, x, y, inherited_speed, power):
        super().__init__(x, y)
        self.inherited_speed:Vector2 = inherited_speed
        self.power = power

    def draw(self, win):
        pygame.draw.rect(win, (0, 0, 255), (self.pos.x, self.pos.y, 20*self.power/2, 20*self.power/2))

    def update(self, event):
        if self.inherited_speed.length() != 0:
            self.move(self.inherited_speed.normalize() + Vector2(0, -1.5), 3/(self.power / 3))
        else:
            self.move(Vector2(0, -1.5), 3/(self.power / 3))
