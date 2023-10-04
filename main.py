import pygame
from Player import Player

game = True
pygame.init()
win = pygame.display.set_mode((612, 400))
clock = pygame.time.Clock()

player = Player(0, 0, (255, 0, 0))

while game:
    clock.tick(16)
    win.fill((0, 0, 0))
    events = pygame.event.get()

    player.update(events)
    player.draw(win)

    pygame.display.update()

    for event in events:
        if event.type == pygame.QUIT:
            game = False
