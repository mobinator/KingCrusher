import pygame
from JSONHandler import JSONHandler
from pygame import Vector2


class Minimap:
    def __init__(self):
        self.load_index = 1

    def load(self, win):
        self.screen_size = pygame.display.get_surface().get_size()
        self.scale_factor = self.screen_size[0] / 612
        self.minimap_bg = pygame.transform.scale(pygame.image.load('assets/minimap/bg.png'),
                                                 (int(160 * self.scale_factor), int(120 * self.scale_factor)))
        self.minimap_bg_rect = self.minimap_bg.get_rect(
            topleft=(self.screen_size[0] - int(170 * self.scale_factor), 10))

    def draw(self, win):
        # loading resized images in draw because load didnt work (idk why, everywhere else its working)
        if self.load_index < 3:
            self.load_index += 1
            self.screen_size = pygame.display.get_surface().get_size()
            self.scale_factor = self.screen_size[0] / 612
            self.minimap_bg = pygame.transform.scale(pygame.image.load('assets/minimap/bg.png'),
                                                     (int(160 * self.scale_factor), int(120 * self.scale_factor)))
            self.minimap_bg_rect = self.minimap_bg.get_rect(
                topleft=(self.screen_size[0] - int(170 * self.scale_factor), 10))
        win.blit(self.minimap_bg, self.minimap_bg_rect.topleft)

        # Load opponent data and draw icons on minimap
        opponent_data = JSONHandler.load_opponent_data()
        self.draw_icons(win, opponent_data)

    def draw_icons(self, win, game_data):
        icon_size = Vector2(int(10 * self.scale_factor), int(10 * self.scale_factor))

        # load all icons
        for obj_data in game_data["game_objects"]:
            if obj_data["type"] == "Generator":
                icon_image = pygame.image.load('assets/minimap/icon_gen.png')
            elif obj_data["type"] == "Wall":
                icon_image = pygame.image.load('assets/minimap/icon_wall.png')
            elif obj_data["type"] == "Boulder":
                if obj_data["charge"] <= 2:
                    icon_image = pygame.image.load('assets/minimap/icon_small.png')
                elif obj_data["charge"] <= 4:
                    icon_image = pygame.image.load('assets/minimap/icon_medium.png')
                else:
                    icon_image = pygame.image.load('assets/minimap/icon_large.png')

            icon_image = pygame.transform.scale(icon_image, (int(icon_size.x), int(icon_size.y)))

            # icon position
            relative_pos = Vector2(obj_data["position"]["x"] / self.screen_size[0],
                                   obj_data["position"]["y"] / self.screen_size[1])

            icon_pos = Vector2(self.minimap_bg_rect.x + relative_pos.x * self.minimap_bg_rect.width,
                               self.minimap_bg_rect.y + relative_pos.y * self.minimap_bg_rect.height)

            win.blit(icon_image, icon_pos)

        # draw king icon
        player_icon_image = pygame.image.load('assets/minimap/icon_king.png')
        player_icon_image = pygame.transform.scale(player_icon_image, (int(icon_size.x), int(icon_size.y)))
        player_pos = Vector2(game_data["player"]["position"]["x"] / self.screen_size[0],
                             game_data["player"]["position"]["y"] / self.screen_size[1])
        icon_pos = Vector2(self.minimap_bg_rect.x + player_pos.x * self.minimap_bg_rect.width,
                           self.minimap_bg_rect.y + player_pos.y * self.minimap_bg_rect.height)
        win.blit(player_icon_image, icon_pos)
