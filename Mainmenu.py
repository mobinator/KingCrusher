import pygame

class MainMenu:
    def __init__(self):
        self.bg_image = pygame.image.load('assets/ui/mainmenu/bg.png')
        self.bg_image = pygame.transform.scale(self.bg_image, (612, 400))
        
        self.logo_image = pygame.image.load('assets/ui/logo.png')
        self.logo_image = pygame.transform.scale(self.logo_image, (320, 120))
        self.logo_rect = self.logo_image.get_rect()
        self.logo_rect.center = (306, 60)

        self.button_images = {
            "normal": pygame.transform.scale(pygame.image.load('assets/ui/playbutton/normal.png'), (60, 60)), 
            "hover": pygame.transform.scale(pygame.image.load('assets/ui/playbutton/hover.png'), (60, 60)),  
            "press": pygame.transform.scale(pygame.image.load('assets/ui/playbutton/press.png'), (60, 60))
        }

        self.current_button_image = self.button_images["normal"]
        self.button_rect = self.current_button_image.get_rect()
        
        screen_center = (336, 200)  # Screen / 2 + adjustment
        button_center = (self.button_rect.width // 2, self.button_rect.height // 2)
        
        self.button_rect.center = (screen_center[0] - button_center[0], screen_center[1] - button_center[1])

        self.is_button_clicked = False

    def draw(self, win):
        win.blit(self.bg_image, (0, 0))
        win.blit(self.logo_image, (145, 10))
        win.blit(self.current_button_image, self.button_rect.topleft)

    def check_button_hover(self, pos):
        if self.button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]:
                self.current_button_image = self.button_images["press"]
            else:
                self.current_button_image = self.button_images["hover"]
        else:
            self.current_button_image = self.button_images["normal"]

    def check_button_click(self, pos):
        if self.button_rect.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
            self.is_button_clicked = True
            return True
        return False
