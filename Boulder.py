import pygame
from Empty import *

class Boulder(CollisionShape2D):

    def __init__(self, center, charge, inherited_speed: Vector2):
        super().__init__(center, Vector2(charge*10))

        self.charge = charge
        self.animation_images = self.load_images()
        self.current_image_index = len(self.animation_images) - 1  # Starte mit dem letzten Bild
        self.animation_timer = pygame.time.get_ticks()  # Timer für Animation
        self.animation_delay = 100  # Millisekunden zwischen den Bildwechseln

        self.direction = Vector2(0, -1)

        self.direction += inherited_speed/2

        self.speed = 6 - charge/2
    
        
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)

    def load_images(self):
        scale_factor = pygame.display.get_surface().get_size()[0] / 612
        
        if 1 <= self.charge <= 2:
            path = "assets/attacks/small"
            size = (int(40 * scale_factor), int(40 * scale_factor))
        elif 3 <= self.charge <= 4:
            path = "assets/attacks/medium"
            size = (int(60 * scale_factor), int(60 * scale_factor))
        else:
            path = "assets/attacks/large"
            size = (int(80 * scale_factor), int(80 * scale_factor))

        images = [pygame.transform.scale(pygame.image.load(f"{path}/{i}.png"), size) for i in range(4, 0, -1)]

        return images

    def update(self, events):
        new_pos = self.pos + (self.direction * self.speed)
        self.pos = new_pos

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
        win.blit(current_image, self.rect.topleft)
