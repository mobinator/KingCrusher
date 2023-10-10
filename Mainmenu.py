import pygame

class MainMenu:
    def __init__(self):
        self.button_rect = pygame.Rect(250, 150, 100, 50)
        self.button_color = (255, 0, 0)
        self.is_button_clicked = False

    def draw(self, win):
        pygame.draw.rect(win, self.button_color, self.button_rect)

    def check_button_click(self, pos):
        if self.button_rect.collidepoint(pos):
            self.is_button_clicked = True
            return True
        return False