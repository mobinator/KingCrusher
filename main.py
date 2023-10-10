import pygame
from Game import Game
from Player import Player

game = True
pygame.init()
win = pygame.display.set_mode((612, 400))
clock = pygame.time.Clock()

game = Game()
game.set_player(Player(20, 20))

while game:
    clock.tick(60)
    win.fill((0, 0, 0))
    events = pygame.event.get()

    game.update(events)
    game.draw(win)

    pygame.display.update()

    for event in events:
        if event.type == pygame.QUIT:
            game = False

pygame.quit()
