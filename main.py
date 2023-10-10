import pygame
from Game import Game
from Player import Player
from Mainmenu import MainMenu

pygame.init()
win = pygame.display.set_mode((612, 400))
clock = pygame.time.Clock()

game = Game()
game.set_player(Player(20, 20))

menu = MainMenu()
in_menu = True

while True:
    clock.tick(60)
    win.fill((0, 0, 0))
    events = pygame.event.get()

    if in_menu:
        menu.draw(win)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu.check_button_click(event.pos):
                    in_menu = False
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
    else:
        game.update(events)
        game.draw(win)
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    pygame.display.update()
