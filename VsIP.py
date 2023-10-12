import pygame

class IPinput:
    def __init__(self):
        self.screen_size = pygame.display.get_surface().get_size()
        self.scale_factor = self.screen_size[0] / 612
        self.bg_image = pygame.transform.scale(pygame.image.load('assets/ui/mainmenu/bg_dark.png'), self.screen_size)
        
        # Laden des Exit-Buttons
        self.exit_button_images = {
            "normal": pygame.transform.scale(pygame.image.load('assets/ui/VsIP/normal.png'), (int(240*self.scale_factor), int(120*self.scale_factor))),
            "hover": pygame.transform.scale(pygame.image.load('assets/ui/VsIP/hover.png'), (int(240*self.scale_factor), int(120*self.scale_factor))),
            "press": pygame.transform.scale(pygame.image.load('assets/ui/VsIP/press.png'), (int(240*self.scale_factor), int(120*self.scale_factor)))
        }
        
        self.exit_button_image = self.exit_button_images["normal"]
        
        # Gesamte Bildposition
        self.image_position = (180*self.scale_factor, 110*self.scale_factor)
        
        # Nur ein Bereich des Bildes soll anklickbar sein
        self.exit_button_rect = pygame.Rect(376*self.scale_factor, 123*self.scale_factor, 34*self.scale_factor, 34*self.scale_factor)

    def draw(self, win):
        win.blit(self.bg_image, (0, 0))
        
        # Zeichne das gesamte Bild
        win.blit(self.exit_button_image, self.image_position)

        # Optional: Zeichne das semi-transparente Rechteck, um den anklickbaren Bereich zu zeigen (für Debugging-Zwecke)
        semi_transparent_surface = pygame.Surface((self.exit_button_rect.width, self.exit_button_rect.height), pygame.SRCALPHA)
        semi_transparent_surface.fill((255, 255, 255, 0))
        win.blit(semi_transparent_surface, self.exit_button_rect.topleft)

    def handle_event(self, event, state):
        mouse_pos = pygame.mouse.get_pos()
 
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
                print("release")
                self.exit_button_image = self.exit_button_images["normal"]
                state[0] = "MAIN_MENU"


    def check_for_enter(self, state):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            state[0] = "GAME"
