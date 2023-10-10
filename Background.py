import pygame
import random

from pygame import Vector2

class Background:
    def __init__(self, window_size):
        self.color = (126, 148, 50)  # Hex #7e9432 in RGB
        self.grass_images = [
            pygame.image.load(f'assets/landscape/grass2.png'),
            pygame.image.load(f'assets/landscape/grass3.png')
        ]
        self.initial_window_size = window_size
        self.window_size = window_size
        self.grass_positions = []
        self.grass_types = []
        self.previous_window_size = None

        self.populate_grass()

    def populate_grass(self):
        self.grass_positions.clear()
        self.grass_types.clear()
        i = 0
        while len(self.grass_positions) < 10 and i < 200:
            i = i + 1
            scale_factor = self.window_size[0] / self.initial_window_size[0]
            chosen_grass = random.choice(self.grass_images)
            width, height = chosen_grass.get_size()
            width, height = int(40 * scale_factor), int(40 * scale_factor)
            pos_x = random.randint(0, self.window_size[0] - width)
            pos_y = random.randint(0, self.window_size[1] - height)

            new_grass_rect = pygame.Rect(pos_x, pos_y, width, height)
            collision = False
            for grass_pos in self.grass_positions:
                if new_grass_rect.colliderect(grass_pos):
                    collision = True
                    break

            if not collision:
                self.grass_positions.append(new_grass_rect)
                self.grass_types.append(chosen_grass)

    def draw(self, win):
        win.fill(self.color)
        for i, grass_rect in enumerate(self.grass_positions):
            scale_factor = self.window_size[0] / self.initial_window_size[0]
            grass_image = pygame.transform.scale(self.grass_types[i], (int(grass_rect.width * scale_factor), int(grass_rect.height * scale_factor)))
            win.blit(grass_image, grass_rect.topleft)

    def update_window_size(self):
        current_window_size = pygame.display.get_surface().get_size()
        
        if self.previous_window_size != current_window_size:
            self.window_size = current_window_size
            self.populate_grass()
            
        self.previous_window_size = current_window_size
