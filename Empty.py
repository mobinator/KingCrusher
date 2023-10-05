from pygame import Vector2


class Empty:
    def __init__(self, x: float, y: float):
        self.pos = Vector2(x, y)
        self.renderLayer = None
        self.collisionLayer = None

    def move(self, direction: Vector2, speed: float):
        self.pos += direction * speed

    def draw(self, win):
        pass

    def update(self, event):
        pass

