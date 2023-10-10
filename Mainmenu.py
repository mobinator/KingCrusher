import pygame

class MainMenu:
    def __init__(self, screen_size=(612, 400)):
        self.screen_width, self.screen_height = screen_size

        self.bg_image_original = pygame.image.load('assets/ui/mainmenu/bg.png')
        self.bg_image = pygame.transform.scale(self.bg_image_original, (self.screen_width, self.screen_height))

        self.logo_image_original = pygame.image.load('assets/ui/logo.png')
        self.scale_and_position_logo()

        self.load_buttons()

    def scale_and_position_logo(self):
        logo_width = int(self.screen_width * 0.52)
        logo_height = int(self.screen_height * 0.3)
        self.logo_image = pygame.transform.scale(self.logo_image_original, (logo_width, logo_height))
        self.logo_rect = self.logo_image.get_rect()
        self.logo_rect.center = (self.screen_width / 2, self.screen_height * 0.15)

    def load_buttons(self):
        button_width = int(self.screen_width * 0.1)
        button_height = int(self.screen_height * 0.15)

        self.button_images = {
            "play": {
                "normal": pygame.transform.scale(pygame.image.load('assets/ui/playbutton/normal.png'), (button_width, button_height)),
                "hover": pygame.transform.scale(pygame.image.load('assets/ui/playbutton/hover.png'), (button_width, button_height)),
                "press": pygame.transform.scale(pygame.image.load('assets/ui/playbutton/press.png'), (button_width, button_height))
            },
            "settings": {
                "normal": pygame.transform.scale(pygame.image.load('assets/ui/settingbutton/normal.png'), (button_width, button_height)),
                "hover": pygame.transform.scale(pygame.image.load('assets/ui/settingbutton/hover.png'), (button_width, button_height)),
                "press": pygame.transform.scale(pygame.image.load('assets/ui/settingbutton/press.png'), (button_width, button_height))
            }
        }

        self.play_button_image = self.button_images["play"]["normal"]
        self.play_button_rect = self.play_button_image.get_rect()
        self.play_button_rect.center = (self.screen_width / 2, self.screen_height / 2)

        self.settings_button_image = self.button_images["settings"]["normal"]
        self.settings_button_rect = self.settings_button_image.get_rect()
        self.settings_button_rect.topleft = (0, self.screen_height - button_height)

    def set_screen_size(self, screen_size):
        self.screen_width, self.screen_height = screen_size
        self.bg_image = pygame.transform.scale(self.bg_image_original, (self.screen_width, self.screen_height))
        self.scale_and_position_logo()
        self.load_buttons()

    def draw(self, win):
        win.blit(self.bg_image, (0, 0))
        win.blit(self.logo_image, self.logo_rect.topleft)
        win.blit(self.play_button_image, self.play_button_rect.topleft)
        win.blit(self.settings_button_image, self.settings_button_rect.topleft)

    def check_button_hover(self, pos):
        if self.play_button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]:
                self.play_button_image = self.button_images["play"]["press"]
            else:
                self.play_button_image = self.button_images["play"]["hover"]
        else:
            self.play_button_image = self.button_images["play"]["normal"]

        if self.settings_button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]:
                self.settings_button_image = self.button_images["settings"]["press"]
            else:
                self.settings_button_image = self.button_images["settings"]["hover"]
        else:
            if self.play_button_image != self.button_images["play"]["press"]:
                self.settings_button_image = self.button_images["settings"]["normal"]

    def check_button_click(self, pos):
        if self.play_button_rect.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
            return True
        return False

    def check_settings_click(self, pos):
        if self.settings_button_rect.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
            return True
        return False
