import pygame

class Settings:
    def __init__(self):
        self.button_sizes = {
            "small": (60, 60),
            "medium": (60, 60),
            "large": (60, 60)
        }

        self.buttons = {
            "small": pygame.transform.scale(pygame.image.load('assets/ui/settingbutton/normal.png'), self.button_sizes["small"]),
            "medium": pygame.transform.scale(pygame.image.load('assets/ui/settingbutton/hover.png'), self.button_sizes["medium"]),
            "large": pygame.transform.scale(pygame.image.load('assets/ui/settingbutton/press.png'), self.button_sizes["large"])
        }

        self.current_buttons = {
            "small": self.buttons["small"],
            "medium": self.buttons["medium"],
            "large": self.buttons["large"]
        }

        # Positioniere die Buttons vertikal untereinander
        self.positions = {
            "small": (30, 60),
            "medium": (30, 140),
            "large": (30, 220)
        }

    def draw(self, win):
        for key in self.current_buttons:
            win.blit(self.current_buttons[key], self.positions[key])
    
    def check_button_hover(self, pos):
        # Überprüfe, ob der Mauszeiger über einem der Buttons ist
        for key in self.positions:
            rect = pygame.Rect(self.positions[key], self.button_sizes[key])
            if rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0]:
                    self.current_buttons[key] = self.buttons["large"]  # "press" Image
                else:
                    self.current_buttons[key] = self.buttons["medium"]  # "hover" Image
            else:
                self.current_buttons[key] = self.buttons["small"]  # "normal" Image

    def check_button_click(self, pos):
        # Überprüfe, ob einer der Buttons geklickt wurde
        for key in self.positions:
            rect = pygame.Rect(self.positions[key], self.button_sizes[key])
            if rect.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
                self.change_screen_size(key)
                return True
        return False

    def change_screen_size(self, size_key):
        sizes = {
            "small": (612, 400),
            "medium": (1024, 768),
            "large": (1920, 1080)
        }
        pygame.display.set_mode(sizes[size_key])