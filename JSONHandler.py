import json
from Player import Player
from Boulder import Boulder

class JSONHandler:
    
    @staticmethod
    def player_to_dict(player):
        """Konvertiert ein Player-Objekt in ein Dictionary."""
        return {
            "position": {
                "x": player.pos.x,
                "y": player.pos.y
            }
        }
    
    @staticmethod
    def save_player_to_json(player, filename='player_state.json'):
        """Speichert den aktuellen Zustand des Spielers in eine JSON-Datei."""
        player_data = JSONHandler.player_to_dict(player)
        
        with open(filename, 'w') as file:
            json.dump(player_data, file)

    @staticmethod
    def load_player_from_json(player, filename='player_state.json'):
        """Lädt den Spielerzustand aus einer JSON-Datei."""
        with open(filename, 'r') as file:
            player_data = json.load(file)
            
            player.pos.x = player_data["position"]["x"]
            player.pos.y = player_data["position"]["y"]
    
    @staticmethod
    def game_objects_to_dict(game_objects):
        """Konvertiert eine Liste von Spielobjekten in ein Dictionary."""
        objects_list = []

        for game_object in game_objects:
            if isinstance(game_object, Player):
                continue  # Überspringe Spielerobjekt, da es bereits separat gehandhabt wird
            obj_data = {
                "type": game_object.__class__.__name__,
                "position": {
                    "x": game_object.center.x,
                    "y": game_object.center.y
                }
            }
            if isinstance(game_object, Boulder):
                obj_data["speed"] = game_object.speed
                obj_data["direction"] = {
                    "x": game_object.direction.x,
                    "y": game_object.direction.y
                }
                obj_data["charge"] = game_object.charge
            objects_list.append(obj_data)

        return objects_list


    @staticmethod
    def save_game_to_json(game, filename='game_state.json'):
        """Speichert den aktuellen Spielzustand in eine JSON-Datei."""
        game_data = {
            "player": JSONHandler.player_to_dict(game.player),
            "game_objects": JSONHandler.game_objects_to_dict(game.game_objects)
        }

        with open(filename, 'w') as file:
            json.dump(game_data, file)
    
    @staticmethod
    def load_opponent_data(filename='game_state_opponent.json'):
        """Lädt die Daten des Gegners aus der JSON-Datei."""
        with open(filename, 'r') as file:
            game_data = json.load(file)
        return game_data

    @staticmethod
    def load_game_from_json(game, filename='game_state.json'):
        """Lädt den Spielzustand aus einer JSON-Datei."""
        with open(filename, 'r') as file:
            game_data = json.load(file)

        # Spielerdaten laden
        player_data = game_data["player"]
        game.player.pos.x = player_data["position"]["x"]
        game.player.pos.y = player_data["position"]["y"]

        # Andere Spielobjekte (aktuell nur die Position; Erweiterung möglich)
        for obj_data in game_data["game_objects"]:
            # Ein Beispiel, wie man Objekte basierend auf ihrem Typ wiederherstellt
            if obj_data["type"] == "Generator":
                generator = Generator(Vector2(obj_data["position"]["x"], obj_data["position"]["y"]), game.coin_delay)  # Hier wird der coin_delay einfach aus dem aktuellen Spielzustand verwendet
                game.add_object(generator, 1, 1)
            elif obj_data["type"] == "Wall":
                wall = Wall(Vector2(obj_data["position"]["x"], obj_data["position"]["y"]))
                game.add_object(wall, 1, 1)
            # Weitere Bedingungen können hinzugefügt werden, wenn Sie andere Spielobjekte speichern/laden möchten
