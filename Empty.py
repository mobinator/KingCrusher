from pygame import Vector2


class Empty:
    def __init__(self, x: float, y: float):
        self.pos = Vector2(x, y)
        self.renderLayer = None
        self.collisionLayer = None

        self.size = Vector2()

        self.children = []

    def move(self, direction: Vector2, speed: float):
        if direction.length() != 0:
            self.pos += direction.normalize() * speed

    def draw(self, win):
        pass

    def update(self, events):
        pass


class Sprite(Empty):

    def __init__(self, x, y, sprite, animated):
        super().__init__(x, y)

        self.sprite = sprite
        self.animated = animated

    def draw(self, win):
        pass

    def draw_animated(self, win):
        pass


class CollisionShape2D(Empty):

    def __init__(self, x, y, width, height):
        super().__init__(x, y)

        self.size: Vector2 = Vector2(width, height)

        self.center = self.pos + Vector2(width, height) / 2

    def __init__(self, pos, size: Vector2):
        super().__init__(pos.x, pos.y)

        self.size = size
        self.center = self.pos + self.size/2

    def move(self, direction: Vector2, speed: float):
        super().move(direction, speed)
        self.center += direction * speed
