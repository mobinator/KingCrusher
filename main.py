import pygame
from Game import Game
from Player import Player
from Mainmenu import MainMenu
from Settings import Settings
from Escapemenu import EscapeMenu
from VsIP import IPinput
from JSONHandler import JSONHandler
from Minimap import Minimap
from Networking import Networking

pygame.init()
win = pygame.display.set_mode((612, 400))
clock = pygame.time.Clock()

networking = Networking()
game = Game(networking)
game.set_player(Player(200, 200, game))

menu = MainMenu()
settings = Settings(menu)

state = ["MAIN_MENU"]

escape_menu = EscapeMenu(state)
ip_input = IPinput(networking)
minimap = Minimap()

while True:
    clock.tick(60)
    win.fill((0, 0, 0))
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            networking.end()
            pygame.quit()
            exit()

    match state[0]:
        case "MAIN_MENU":
            menu.check_button_hover(pygame.mouse.get_pos())
            menu.draw(win)
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if menu.check_button_click(event.pos):
                        ip_input.load(win)
                        minimap.load(win)
                        state[0] = "VS_IP"
                    elif menu.check_settings_click(event.pos):
                        state[0] = "SETTINGS"

        case "VS_IP":
            ip_input.draw(win)
            ip_input.check_for_enter(state)
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP or event.type == event.type == pygame.KEYDOWN:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            minimap.load(win)
                            game.networking.begin(game)

                    ip_input.handle_event(event, state)

        case "SETTINGS":
            settings.check_button_hover(pygame.mouse.get_pos())
            settings.draw(win)
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if settings.check_button_click(event.pos):
                        pass
                    elif settings.check_back_button_click(event.pos):
                        state[0] = "MAIN_MENU"

        case "GAME":
            game.update(events)
            game.draw(win)
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        escape_menu.show()
                    if event.key == pygame.K_F5:  # F5 zum Speichern
                        JSONHandler.save_game_to_json(game)
                escape_menu.handle_event(event)
            escape_menu.draw(win)

            networking.send(str(game.player))

            # print(game.enemy_player.pos, game.player.pos)

    pygame.display.update()
