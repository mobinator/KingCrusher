import pygame
from pygame import Vector2


class Empty:
    def __init__(self, x: float, y: float, health: int):
        self.pos = Vector2(x, y)
        self.renderLayer = None
        self.collisionLayer = None
        self.renderLayerIndex = None
        self.collisionLayerIndex = None
        self.objectIndex = None
        self.health = health
        self.deleting = False

        self.size = Vector2()

        self.children = []

    def move(self, direction: Vector2, speed: float):
        if direction.length() != 0:
            self.pos += direction.normalize() * speed

    def draw(self, win):
        pass

    def update(self, events):
        if self.health <= 0:
            self.delete()

    def delete(self):
        if not self.deleting:
            pygame.event.post(pygame.event.Event(Events.DELETE, game_object=self))
            self.deleting = True


class Sprite(Empty):

    def __init__(self, x, y, sprite, animated):
        super().__init__(x, y, 0)

        self.sprite = sprite
        self.animated = animated

    def draw(self, win):
        pass

    def draw_animated(self, win):
        pass


class CollisionShape2D(Empty):

    def __init__(self, x, y, width, height, health=1):
        super().__init__(x, y, health)

        self.size: Vector2 = Vector2(width, height)

        self.center = self.pos + Vector2(width, height) / 2

        self.sprite = None

    def __init__(self, center: Vector2, size: Vector2, health=1):
        self.pos = center - size / 2
        super().__init__(self.pos.x, self.pos.y, health)

        self.deleting = False
        self.size = size
        self.center = center
        self.collision_cooldown = 10

        self.sprite = None

    def move(self, direction: Vector2, speed: float):
        super().move(direction, speed)
        self.center = self.pos + self.size / 2

    def draw(self, win):
        self.draw_sprite(win)

    def draw_sprite(self, win):
        pass

    def set_sprite(self, sprite):
        self.sprite = sprite

    def check_collision(self, collision_shape):
        colliding = False

        if self.collisionLayer == collision_shape.collisionLayer:
            return False

        bbox = pygame.Rect(self.pos, self.size)
        collision_shape_bbox = pygame.Rect(collision_shape.pos, collision_shape.size)

        colliding = bbox.colliderect(collision_shape_bbox)

        return colliding

    def collide_with(self, collision_object):
        print("collision")


class Events:
    COIN = pygame.USEREVENT + 1
    SHOOT = pygame.USEREVENT + 2
    DELETE = pygame.USEREVENT + 3
