from pygame import Vector2


class Empty:
    def __init__(self, x: float, y: float):
        self.pos = Vector2(x, y)

    def move(self, direction: Vector2, speed: float):
        self.pos += direction * speed
