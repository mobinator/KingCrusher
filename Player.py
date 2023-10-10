import pygame

from pygame import Vector2
from Empty import CollisionShape2D, Events


class Player(CollisionShape2D):

    def __init__(self, x: float, y: float):
        super().__init__(Vector2(x, y), Vector2(20, 20))

        self.money = 0
        self.charge = 0
        
        self.base_speed = 1.8
        # Holt die aktuelle Fenstergröße
        self.window_size = pygame.display.get_surface().get_size()

        pygame.time.set_timer(Events.COIN, 1000)

    def draw(self, win):
        pygame.draw.rect(win, (255, 55, 55), (self.pos, self.size))

        font = pygame.font.SysFont("Arial", 24)
        text = font.render(str(self.money), True, (255, 255, 255))
        win.blit(text, (20, 20))
        font = pygame.font.SysFont("Arial", 24)
        text = font.render(str(self.charge), True, (255, 255, 255))
        win.blit(text, (20, 60))

    def update(self, events):
        direction = self.calculate_move_direction()
        
        # calculating speed factor by different screen size
        current_window_size = pygame.display.get_surface().get_size()
        speed_factor = (current_window_size[0] * current_window_size[1]) / (self.window_size[0] * self.window_size[1])
        
        # limit for balancing
        speed_factor = max(0.8, min(speed_factor, 7))
        #print(speed_factor)
        
        self.move(direction, self.base_speed * speed_factor)

        for event in events:
            if event.type == Events.COIN:
                self.process_coins()
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                if self.charge > 0:
                    pygame.event.post(pygame.event.Event(Events.SHOOT, power=self.charge, inherited_speed=direction))
                    self.charge = 0

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

    def process_coins(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            if self.money > 0:
                self.charge += 1
            self.money -= 1
        else:
            self.money += 1
            self.charge = 0

        self.money = max(0, min(self.money, 7))
