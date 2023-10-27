import pygame
from pygame import Vector2
from Constants import Events


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

    def set_health(self, health):
        self.health = health
        if self.health <= 0:
            self.delete()


class AnimatedSprite(Empty):

    def __init__(self, offset, sprite, init_sprites, frame_rate, size, parent, looping=False, animated=True):
        super().__init__(offset.x, offset.y, 0)

        self.pos += parent.pos
        self.parent = parent
        self.sprite = pygame.transform.scale(sprite, size)
        self.offset = offset
        self.size = size

        self.draw_pos = self.pos

        self.init_sprites = init_sprites
        self.frame_count = len(init_sprites)
        self.frame_index = 0
        self.init_finished = not animated
        self.frame_rate = frame_rate
        self.frame_counter = 0

        self.looping = looping

    def set_sprite(self, sprite):
        self.sprite = pygame.transform.scale(sprite, self.size)

    def draw(self, win):
        if self.init_finished:
            win.blit(self.sprite, self.draw_pos)
        else:
            self.draw_animated(win)

    def draw_animated(self, win):
        current_sprite = self.init_sprites[self.frame_index]
        current_sprite = pygame.transform.scale(current_sprite, self.size)
        win.blit(current_sprite, self.pos)

        if self.frame_counter >= 60 // self.frame_rate:
            self.frame_counter = 0

            self.frame_index += 1
            if self.frame_index == self.frame_count:
                if not self.looping:
                    self.init_finished = True
                else:
                    self.frame_index = 0

        self.frame_counter += 1

    def draw_static(self, win):
        win.blit(self.sprite, self.draw_pos)

    def update(self, events):
        self.pos = self.offset + self.parent.pos

        self.draw_pos = self.pos


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
        if isinstance(collision_shape, pygame.rect.Rect):
            collision_shape_bbox = collision_shape
        else:
            colliding = False

            if self.collisionLayer == collision_shape.collisionLayer:
                return False

            collision_shape_bbox = pygame.Rect(collision_shape.pos, collision_shape.size)

        bbox = pygame.Rect(self.pos, self.size)
        colliding = bbox.colliderect(collision_shape_bbox)

        return colliding

    def collide_with(self, collision_object):
        print("collision")
