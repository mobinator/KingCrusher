import pygame

class EscapeMenu:
    def __init__(self, state_ref):
        self.initial_window_size = (612, 400)  # start size
        self.window_size = pygame.display.get_surface().get_size()
        self.state = state_ref
        self.scale_factor = self.window_size[0] / 612
        self.image_base_path = 'assets/ui/escape_menu/'
        self.hovered_button = None
        self.images = {
            'home': {
                'hover': pygame.transform.scale(pygame.image.load(self.image_base_path + 'hover_x.png'), (240 * self.scale_factor, 280 * self.scale_factor)),
                'press': pygame.transform.scale(pygame.image.load(self.image_base_path + 'press_x.png'), (240 * self.scale_factor, 280 * self.scale_factor)),
                'rect': None 
            },
            'settings': {
                'hover': pygame.transform.scale(pygame.image.load(self.image_base_path + 'hover_r.png'), (240 * self.scale_factor, 280 * self.scale_factor)),
                'press': pygame.transform.scale(pygame.image.load(self.image_base_path + 'press_r.png'), (240 * self.scale_factor, 280 * self.scale_factor)),
                'rect': None
            },
            'resume': {
                'hover': pygame.transform.scale(pygame.image.load(self.image_base_path + 'hover_s.png'), (240 * self.scale_factor, 280 * self.scale_factor)),
                'press': pygame.transform.scale(pygame.image.load(self.image_base_path + 'press_s.png'), (240 * self.scale_factor, 280 * self.scale_factor)),
                'rect': None
            },
            'exit': {
                'hover': pygame.transform.scale(pygame.image.load(self.image_base_path + 'hover_h.png'), (240 * self.scale_factor, 280 * self.scale_factor)),
                'press': pygame.transform.scale(pygame.image.load(self.image_base_path + 'press_h.png'), (240 * self.scale_factor, 280 * self.scale_factor)),
                'rect': None
            },
            'normal': pygame.transform.scale(pygame.image.load(self.image_base_path + 'normal.png'), (240 * self.scale_factor, 280 * self.scale_factor))
        }
        self.active_image = self.images['normal']
        self.is_visible = False
        
        self.images['home']['rect'] = pygame.Rect(352 * self.scale_factor, 39 * self.scale_factor, 28 * self.scale_factor, 28 * self.scale_factor)
        self.images['settings']['rect'] = pygame.Rect(220 * self.scale_factor, 85 * self.scale_factor, 160 * self.scale_factor, 39 * self.scale_factor)
        self.images['resume']['rect'] = pygame.Rect(220 * self.scale_factor, 140 * self.scale_factor, 160 * self.scale_factor, 39 * self.scale_factor)
        self.images['exit']['rect'] = pygame.Rect(220 * self.scale_factor, 195 * self.scale_factor, 160 * self.scale_factor, 39 * self.scale_factor)

    def show(self):
        self.is_visible = True

    def hide(self):
        self.is_visible = False

    def handle_event(self, event):
        if not self.is_visible:
            return
        
        mouse_pos = pygame.mouse.get_pos()
        
        if event.type == pygame.MOUSEMOTION:
            for key in self.images:
                if key != 'normal' and self.images[key]['rect'].collidepoint(mouse_pos):
                    self.hovered_button = key
                    self.active_image = self.images[key]['hover']
                    break
            else:
                self.hovered_button = None
                self.active_image = self.images['normal']

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered_button:
                self.active_image = self.images[self.hovered_button]['press']
                
                if self.hovered_button in ['home', 'settings']:
                    self.hide()
                elif self.hovered_button == 'resume':
                    self.hide()
                    self.state[0] = "SETTINGS"
                elif self.hovered_button == 'exit':
                    self.hide()
                    self.state[0] = "MAIN_MENU"
        
        if event.type == pygame.MOUSEBUTTONUP:
            if self.hovered_button:
                self.active_image = self.images[self.hovered_button]['hover']

    def draw(self, win):
        if self.is_visible:
            win.blit(self.active_image, (180*self.scale_factor, 0))
            
            for key in ["home", "settings", "resume", "exit"]:
                semi_transparent_surface = pygame.Surface((self.images[key]['rect'].width, self.images[key]['rect'].height), pygame.SRCALPHA)
                semi_transparent_surface.fill((255, 255, 255, 0))

                win.blit(semi_transparent_surface, self.images[key]['rect'].topleft)

    def set_button_rect(self, key, rect):
        self.images[key]['rect'] = rect
