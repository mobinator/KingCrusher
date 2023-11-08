import pygame
from pygame import Vector2
from Generator import Generator
from Player import Player
from Boulder import Boulder
from EnemyPlayer import EnemyPlayer
from Wall import Wall


class Minimap:
    def __init__(self, game):
        self.screen_size = pygame.display.get_window_size()
        self.minimap_bg_rect = None
        self.minimap_bg = None
        self.load_index = 1
        self.game = game

    def load(self, win):
        self.minimap_bg = pygame.transform.scale(pygame.image.load('assets/minimap/bg.png'),
                                                 (160, 120))
        self.minimap_bg_rect = self.minimap_bg.get_rect(
            topleft=(self.screen_size[0] - int(170), 10))

    def draw(self, win):
        # loading resized images in draw because load didnt work (idk why, everywhere else its working)
        if self.load_index < 3:
            self.load_index += 1
            self.minimap_bg = pygame.transform.scale(pygame.image.load('assets/minimap/bg.png'),
                                                     (160, 120))
            self.minimap_bg_rect = self.minimap_bg.get_rect(
                topleft=(self.screen_size[0] - 170, 10))
        win.blit(self.minimap_bg, self.minimap_bg_rect.topleft)

        # Load opponent data and draw icons on minimap
        self.draw_icons(win)

    def draw_icons(self, win):
        icon_size = Vector2(10, 10)
        is_enemy = False

        # load all icons
        for obj_data in self.game.game_objects:
            if isinstance(obj_data, Generator):
                icon_image = pygame.image.load('assets/minimap/icon_gen.png')
                is_enemy = obj_data.enemy_generator
            elif isinstance(obj_data, Wall):
                icon_image = pygame.image.load('assets/minimap/icon_wall.png')
                is_enemy = obj_data.enemy_wall
            elif isinstance(obj_data, Player):
                icon_image = pygame.image.load('assets/minimap/icon_king.png')
                is_enemy = False
            elif isinstance(obj_data, EnemyPlayer):
                icon_image = pygame.image.load('assets/minimap/icon_king.png')
                is_enemy = True
            elif isinstance(obj_data, Boulder):
                if obj_data.charge <= 2:
                    icon_image = pygame.image.load('assets/minimap/icon_small.png')
                elif obj_data.charge <= 4:
                    icon_image = pygame.image.load('assets/minimap/icon_medium.png')
                else:
                    icon_image = pygame.image.load('assets/minimap/icon_large.png')
                is_enemy = obj_data.enemy_boulder
            else:
                icon_image = pygame.image.load('assets/minimap/icon_gen.png')

            if obj_data:
                icon_image = pygame.transform.scale(icon_image, (int(icon_size.x), int(icon_size.y)))

                # icon position
                relative_pos = Vector2(obj_data.pos.x / self.screen_size[0],
                                       -obj_data.pos.y / self.screen_size[1])

                icon_pos = Vector2(self.minimap_bg_rect.x + relative_pos.x * self.minimap_bg_rect.width,
                                   self.minimap_bg_rect.height - relative_pos.y * self.minimap_bg_rect.height)

                if is_enemy:
                    win.blit(icon_image, icon_pos)
