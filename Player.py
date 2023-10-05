from Empty import Empty
import pygame
from pygame import Vector2

from Game import Events


class Player(Empty):
    def __init__(self, x, y, color):
        super().__init__(x, y)

        pygame.time.set_timer(Events.COIN, 1000)

        self.color = color
        self.selection = 0
        self.money = 0
        self.speed = 1.8
        self.charging = False
        self.charge = 1

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.pos.x, self.pos.y, 20, 20))

        font = pygame.font.SysFont("arial", 24)
        img = font.render(str(self.money), True, (255, 255, 255))
        win.blit(img, (20, 20))

    def update(self, events):
        direction = self.get_direction
        if direction.length() > 0:
            direction = direction.normalize()

        self.move(direction, self.speed)

        for event in events:
            if event.type == Events.COIN:
                if self.charging:
                    self.money -= 1
                    self.charge += 1
                else:
                    self.money += 1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.money >= 1:
                    # pygame.event.post(pygame.event.Event(Events.ATTACK, direction=direction*self.speed, power=1))
                    self.charging = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    pygame.event.post(pygame.event.Event(Events.ATTACK, direction=direction*self.speed, power=self.charge))
                    self.charge = 1
                    self.money -= 1
                    self.charging = False

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

    def get_center(self):
        return self.pos + Vector2(10, 10) / 2
