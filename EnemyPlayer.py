from Empty import CollisionShape2D
from pygame import Vector2
from Constants import Events
import pygame


class EnemyPlayer(CollisionShape2D):

    def __init__(self, x: float, y: float):
        super().__init__(Vector2(x, y), Vector2(30, 40), 12)

    def update_pos(self, pos):
        self.pos = pos

    def delete(self):
        pygame.event.post(pygame.event.Event(Events.WIN))
        super().delete()

    def get_health_string(self):
        if self.health >= 10:
            return str(self.health)
        elif self.health < 0:
            return "00"
        else:
            return "0" + str(self.health)
