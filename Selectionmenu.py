import pygame
from pygame import Vector2

class SelectionMenu:
    def __init__(self, player):
        self.initial_window_size = (612, 400)  # start size
        self.player = player
        self.window_size = pygame.display.get_surface().get_size()
        self.images = {
            "left": pygame.image.load(r'assets\ui\selection_menu\left.png'),
            "neutral": pygame.image.load(r'assets\ui\selection_menu\neutral.png'),
            "right": pygame.image.load(r'assets\ui\selection_menu\right.png')
        }
        self.state = "neutral"  # Default state
        self.active = False

    def toggle(self):
        if self.player.charge == 7:
            self.window_size = pygame.display.get_surface().get_size()
            self.active = not self.active
    
    def close(self):
        self.active = False

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:  # Scroll Up
                if self.state == "neutral":
                    self.state = "right"
                elif self.state == "left":
                    self.state = "neutral"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:  # Scroll Down
                if self.state == "neutral":
                    self.state = "left"
                elif self.state == "right":
                    self.state = "neutral"

    def draw(self, win):
        if not self.active:
            return

        scale_factor = self.window_size[0] / self.initial_window_size[0]
        image = pygame.transform.scale(self.images[self.state], (int(80 * scale_factor), int(40 * scale_factor)))
        pos = self.player.pos + Vector2(0, -40 * scale_factor)
        pos[0] = pos[0] - 20 * scale_factor
        win.blit(image, pos)
