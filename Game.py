from Empty import Empty


class Game(Empty):
    def __init__(self):
        super().__init__(0, 0)

        self.render_layers = [[], [], [], [], []]
        self.collision_layers = [[], [], [], [], []]
        self.game_objects = []

        self.player = None

    def update(self, events):
        for game_object in self.game_objects:
            game_object.update(events)

    def draw(self, win):
        for render_layer in reversed(self.render_layers):
            for game_object in render_layer:
                game_object.draw(win)

    def set_player(self, player):
        self.player = player
        self.add_object(player, 2, 1)

    def add_object(self, game_object, render_layer, collision_layer):

        self.add_to_render_layer(render_layer, game_object)
        self.add_to_collision_layer(collision_layer, game_object)
        self.game_objects.append(game_object)

    def add_to_render_layer(self, layer_index, game_object):
        self.render_layers[layer_index].append(game_object)
        game_object.renderLayer = layer_index

    def add_to_collision_layer(self, layer_index, game_object):
        self.collision_layers[layer_index].append(game_object)
        game_object.collisionLayer = layer_index

