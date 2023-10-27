import json

import pygame
from Empty import *


class Boulder(CollisionShape2D):

    def __init__(self, center, charge, inherited_speed: Vector2, enemy_boulder):

        self.charge = charge
        self.animation_images, size = self.load_images()

        super().__init__(center, Vector2(size), charge)

        self.inherited_speed = inherited_speed
        self.deleting = False

        self.current_image_index = len(self.animation_images) - 1  # Starte mit dem letzten Bild
        self.animation_timer = pygame.time.get_ticks()  # Timer für Animation
        self.animation_delay = 100  # Millisekunden zwischen den Bildwechseln
        self.enemy_boulder = enemy_boulder

        if enemy_boulder:
            self.direction = Vector2(0, 1)
            self.direction -= inherited_speed / 2
        else:
            self.direction = Vector2(0, -1)
            self.direction += inherited_speed / 2

        self.speed = 6 - charge / 2

        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)

    def load_images(self):

        if 1 <= self.charge <= 2:
            path = "assets/attacks/small"
            size = (40, 40)
        elif 3 <= self.charge <= 4:
            path = "assets/attacks/medium"
            size = (60, 60)
        else:
            path = "assets/attacks/large"
            size = (80, 80)

        images = [pygame.transform.scale(pygame.image.load(f"{path}/{i}.png"), size) for i in range(4, 0, -1)]

        return images, size

    def update(self, events):
        super().update(events)
        new_pos = self.pos + (self.direction * self.speed)
        self.pos = new_pos

        if -1000 > self.pos.y or self.pos.y > 1000:
            self.delete()

        # Aktualisieren des Rect-Objekts, damit die Zeichnungsposition korrekt ist
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

        # Update Animation
        now = pygame.time.get_ticks()
        if now - self.animation_timer > self.animation_delay:
            self.current_image_index = (self.current_image_index + 1) % len(self.animation_images)
            self.animation_timer = now

    def draw(self, win):
        current_image = self.animation_images[self.current_image_index]
        # Hier benutzen wir topleft statt pos, weil pygame.Rect die obere linke Ecke für das Zeichnen erwartet
        pygame.draw.rect(win, (255, 0, 0), self.rect)
        win.blit(current_image, self.rect.topleft)

    def collide_with(self, collision_object):
        self.health -= 1
        collision_object.health -= 1

    def to_json(self):
        data = {
            "type": "Boulder",
            "x": self.pos.x,
            "y": self.pos.y,
            "charge": self.charge,
            "inherited_speed": {"x": self.inherited_speed.x,
                                "y": self.inherited_speed.y}
        }
        return data

    def __str__(self):
        return json.dumps(self.to_json())
