import pygame

from pygame import Vector2
from Empty import CollisionShape2D, Events


class Player(CollisionShape2D):

    def __init__(self, x: float, y: float):
        super().__init__(Vector2(x, y), Vector2(20, 20))
        
        self.initial_window_size = (612, 400)  # start size
        self.window_size = pygame.display.get_surface().get_size()

        self.money = 0
        self.charge = 0
        self.base_speed = 1.8
        pygame.time.set_timer(Events.COIN, 1000)

        # animations
        self.animations = {
            "walking": [pygame.image.load(f'assets/king/walking/{i}.png') for i in range(1, 5)],
            "idle": [pygame.image.load(f'assets/king/idle/{i}.png') for i in range(1, 5)],
            "damage": [],  # TODO
            "stamina": [pygame.image.load(f'assets/ui/stamina/{i}.png') for i in range(8)]
        }
        self.current_animation = "idle"
        self.current_frame = 0
        self.animation_time = 0
        self.flip_image = False
        
    def draw(self, win):
        scale_factor = self.window_size[0] / 612
        #print("Scale Factor: ",scale_factor)
        image = pygame.transform.scale(self.animations[self.current_animation][self.current_frame],
                                       (int(40 * scale_factor), int(80 * scale_factor)))

        if self.flip_image:
            image = pygame.transform.flip(image, True, False)

        win.blit(image, self.pos)
        
        scale_factor = self.window_size[0] / self.initial_window_size[0]
        stamina_image = pygame.transform.scale(self.animations["stamina"][self.money], 
                                           (int(120 * scale_factor), int(80 * scale_factor)))
        stamina_pos = self.pos - Vector2(40 * scale_factor, 10 * scale_factor)
        win.blit(stamina_image, stamina_pos)

    def update(self, events):
        direction = self.calculate_move_direction()
        
        # calculating speed factor by different screen size
        self.window_size = pygame.display.get_surface().get_size()
        speed_factor = (self.window_size[0] * self.window_size[1]) / (self.initial_window_size[0] * self.initial_window_size[1])        
        
        # limit for balancing
        speed_factor = max(0.8, min(speed_factor, 7))
        #print("Speed Factor: ",speed_factor)
        
        self.move(direction, self.base_speed * speed_factor)

        for event in events:
            if event.type == Events.COIN:
                self.process_coins()
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                if self.charge > 0:
                    pygame.event.post(pygame.event.Event(Events.SHOOT, power=self.charge, inherited_speed=direction))
                    self.charge = 0
        
        self.animation_time += 1
        if self.animation_time > 5:  # animation speed
            self.animation_time = 0
            self.current_frame = (self.current_frame + 1) % 4

        if direction.length() == 0:
            self.current_animation = "idle"
        else:
            self.current_animation = "walking"
            self.flip_image = direction.x < 0

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
