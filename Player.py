from Empty import Empty
import pygame
from pygame import Vector2


class Player(Empty):
    def __init__(self, x, y, color):
        super().__init__(x, y)

        self.color = color
        self.selection = 0

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.pos.x, self.pos.y, 20, 20))

        pygame.draw.rect(win, (165, 165, 165), (5, 5 + (40 + 5) * self.selection, 50, 50))

        for i in range(5):
            pygame.draw.rect(win, (65, 65, 65), (10, 10 + (40 + 5) * i, 40, 40))

    def update(self, events):
        direction = self.get_direction
        if direction.length() > 0:
            direction = direction.normalize()
        self.move(direction, 10)

        for event in events:
            if event.type == pygame.MOUSEWHEEL:
                self.selection -= event.y
                self.selection %= 5

    @property
    def get_direction(self):
        keys = pygame.key.get_pressed()
        direction = Vector2()

        if keys[pygame.K_w]:
            direction.y = -1
        if keys[pygame.K_a]:
            direction.x = -1
        if keys[pygame.K_s]:
            direction.y = 1
        if keys[pygame.K_d]:
            direction.x = 1

        return direction
