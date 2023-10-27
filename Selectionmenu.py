import pygame
from pygame import Vector2, image

from Empty import AnimatedSprite


class SelectionMenu:
    def __init__(self, player):
        self.initial_window_size = (612, 400)  # start size
        self.player = player
        self.window_size = pygame.display.get_surface().get_size()
        self.images = {
            "left": image.load(r'assets\ui\selection_menu\left.png'),
            "neutral": image.load(r'assets\ui\selection_menu\neutral.png'),
            "right": image.load(r'assets\ui\selection_menu\right.png')
        }
        self.state = "neutral"  # Default state
        self.active = False
        self.placement_possible = True

        self.wall_sprite = AnimatedSprite(
            Vector2(-100, -160) + player.size/2,
            image.load('assets/landscape/wall/8.png'),
            [],
            6,
            Vector2(200, 120), player)

        self.wall_sprite.init_finished = True
        self.wall_sprite.sprite.set_alpha(100)

        self.generator_sprite = AnimatedSprite(
            Vector2(-60, -160) + player.size/2,
            image.load('assets/landscape/generator/8.png'),
            [],
            6,
            Vector2(120, 120), player)

        self.generator_sprite.init_finished = True
        self.generator_sprite.sprite.set_alpha(100)

        self.current_sprite = None

    def toggle(self):
        if self.player.charge == 7:
            self.window_size = pygame.display.get_surface().get_size()
            self.active = not self.active

    def close(self):
        self.active = False

    def get_collisions(self, win):
        self.placement_possible = True
        if self.current_sprite:
            current_sprite_rect = pygame.rect.Rect(self.current_sprite.pos, self.current_sprite.size)
            if not win.get_rect().contains(current_sprite_rect):
                self.placement_possible = False

            for game_object in self.player.game.game_objects:
                if game_object and game_object.check_collision(current_sprite_rect):
                    self.placement_possible = False

    def reset_state(self):
        self.state = "neutral"
        self.current_sprite = None

    def update(self, events):
        self.generator_sprite.update(events)
        self.wall_sprite.update(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:  # Scroll Up
                if self.state == "neutral":
                    self.state = "right"
                    self.current_sprite = self.generator_sprite
                elif self.state == "left":
                    self.reset_state()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:  # Scroll Down
                if self.state == "neutral":
                    self.state = "left"
                    self.current_sprite = self.wall_sprite
                elif self.state == "right":
                    self.reset_state()

    def draw(self, win):
        if not self.active:
            return

        self.get_collisions(win)

        if self.current_sprite:
            self.current_sprite.draw(win)
            if not self.placement_possible:
                red_hue = self.current_sprite.sprite.copy()
                red_hue.fill((255, 0, 0, 100))
                win.blit(red_hue, self.current_sprite.draw_pos)

        menu_sprite = pygame.transform.scale(self.images[self.state], (80, 40))
        pos = self.player.pos + Vector2(-25, -50)
        win.blit(menu_sprite, pos)
