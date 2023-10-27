import pygame
import socket
from Minimap import Minimap
import re

def get_local_ip():
    try:
        # get internet connection
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"  # localhost if no internet


class IPinput:

    def __init__(self, networking):
        self.input_text = "192.168.2"
        self.networking = networking
    
    def load(self, win):
        
        self.screen_size = pygame.display.get_surface().get_size()
        self.scale_factor = self.screen_size[0] / 612
        self.bg_image = pygame.transform.scale(pygame.image.load('assets/ui/mainmenu/bg_dark.png'), self.screen_size)
        
        self.local_ip = get_local_ip()
        self.ip_font = pygame.font.Font('assets/fonts/alagard.ttf', int(20*self.scale_factor))
        
        self.exit_button_images = {
            "normal": pygame.transform.scale(pygame.image.load('assets/ui/VsIP/normal.png'), (int(240*self.scale_factor), int(120*self.scale_factor))),
            "hover": pygame.transform.scale(pygame.image.load('assets/ui/VsIP/hover.png'), (int(240*self.scale_factor), int(120*self.scale_factor))),
            "press": pygame.transform.scale(pygame.image.load('assets/ui/VsIP/press.png'), (int(240*self.scale_factor), int(120*self.scale_factor)))
        }
        
        self.exit_button_image = self.exit_button_images["normal"]
        
        self.image_position = (180*self.scale_factor, 110*self.scale_factor)
        
        self.exit_button_rect = pygame.Rect(376*self.scale_factor, 123*self.scale_factor, 34*self.scale_factor, 34*self.scale_factor)
        
        self.font = pygame.font.Font('assets/fonts/alagard.ttf', int(30*self.scale_factor))
        
        self.input_pos = (210*self.scale_factor, 173*self.scale_factor)

    def draw(self, win):
        win.blit(self.bg_image, (0, 0))
        
        win.blit(self.exit_button_image, self.image_position)

        #semi_transparent_surface = pygame.Surface((self.exit_button_rect.width, self.exit_button_rect.height), pygame.SRCALPHA)
        #semi_transparent_surface.fill((255, 255, 255, 0))
        #win.blit(semi_transparent_surface, self.exit_button_rect.topleft)
        
        rendered_text = self.font.render(self.input_text, True, (255, 255, 255))
        win.blit(rendered_text, self.input_pos)
        
        ip_text = self.ip_font.render("Your IP: " + self.local_ip, True, (255, 255, 255))
        win.blit(ip_text, (10, 10))


    def handle_event(self, event, state):
        mouse_pos = pygame.mouse.get_pos()
 
        #exit button events
        if event.type == pygame.MOUSEMOTION:
            if self.exit_button_rect.collidepoint(mouse_pos):
                self.exit_button_image = self.exit_button_images["hover"]
            else:
                self.exit_button_image = self.exit_button_images["normal"]
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.exit_button_rect.collidepoint(mouse_pos):
                self.exit_button_image = self.exit_button_images["press"]
                
        if event.type == pygame.MOUSEBUTTONUP:
            if self.exit_button_rect.collidepoint(mouse_pos):
                self.exit_button_image = self.exit_button_images["normal"]
                state[0] = "MAIN_MENU"
        if event.type == pygame.KEYDOWN:
            if event.unicode in '0123456789.' and len(self.input_text) < 15:
                if (len(self.input_text) == 3 or len(self.input_text) == 7 or len(self.input_text) == 11) and event.unicode not in '.' and '.' not in self.input_text[-3:]:
                    self.input_text += '.'
                self.input_text += event.unicode
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif event.key == pygame.K_RETURN:

                checked = re.search("[0-9][0-9]?[0-9]?[.][0-9][0-9]?[0-9]?[.][0-9][0-9]?[0-9]?[.][0-9][0-9]?[0-9]?", self.input_text)

                if checked and checked.group() == self.input_text:
                    print("IP:", self.input_text)
                    self.networking.set_enemy_ip(self.input_text)
                    if self.input_text == '1.1.1.1':
                        self.networking.set_enemy_ip(self.networking.ownIP)
                else:
                    print("not full ip adress")


    def check_for_enter(self, state):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            state[0] = "GAME"
