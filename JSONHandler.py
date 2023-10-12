import json

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
