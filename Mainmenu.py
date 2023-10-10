import pygame

class MainMenu:
    def __init__(self):
        self.bg_image = pygame.image.load('assets/ui/mainmenu/bg.png')
        self.bg_image = pygame.transform.scale(self.bg_image, (612, 400))
        
        self.logo_image = pygame.image.load('assets/ui/logo.png')
        self.logo_image = pygame.transform.scale(self.logo_image, (320, 120))  # Die gewünschte Größe
        self.logo_rect = self.logo_image.get_rect()
        self.logo_rect.center = (306, 60)  # Zentriert das Logo horizontal und platziert es 60 Pixel von der Oberseite

        self.button_images = {
            "play": {
                "normal": pygame.transform.scale(pygame.image.load('assets/ui/playbutton/normal.png'), (60, 60)),
                "hover": pygame.transform.scale(pygame.image.load('assets/ui/playbutton/hover.png'), (60, 60)),
                "press": pygame.transform.scale(pygame.image.load('assets/ui/playbutton/press.png'), (60, 60))
            },
            "settings": {
                "normal": pygame.transform.scale(pygame.image.load('assets/ui/settingbutton/normal.png'), (60, 60)),
                "hover": pygame.transform.scale(pygame.image.load('assets/ui/settingbutton/hover.png'), (60, 60)),
                "press": pygame.transform.scale(pygame.image.load('assets/ui/settingbutton/press.png'), (60, 60))
            }
        }

        self.play_button_image = self.button_images["play"]["normal"]
        self.play_button_rect = self.play_button_image.get_rect()
        screen_center = (306, 200)
        self.play_button_rect.center = (screen_center[0], screen_center[1])

        self.settings_button_image = self.button_images["settings"]["normal"]
        self.settings_button_rect = self.settings_button_image.get_rect()
        self.settings_button_rect.topleft = (0, 340)

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
