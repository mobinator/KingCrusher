import pygame

class Minimap:
    def __init__(self):
        self.screen_size = pygame.display.get_surface().get_size()
        self.scale_factor = self.screen_size[0] / 612
        self.minimap_bg = pygame.transform.scale(pygame.image.load('assets/minimap/bg.png'), (int(160*self.scale_factor), int(120*self.scale_factor)))
        self.minimap_bg_rect = self.minimap_bg.get_rect(topleft=(self.screen_size[0] - int(170*self.scale_factor), 10))

    def draw(self, win):
        # Draw the semi-transparent background
        win.blit(self.minimap_bg, self.minimap_bg_rect.topleft)

        # Here, you can draw icons representing different objects in the game.
        # You would calculate their relative positions within the Minimap's rectangle and draw them accordingly.

