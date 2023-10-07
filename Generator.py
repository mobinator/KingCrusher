from Empty import *


class Generator(CollisionShape2D):

    def __init__(self, center, current_timer_time):
        super().__init__(center, Vector2(20))
        pygame.time.set_timer(Events.COIN, int(current_timer_time))

    def draw(self, win):
        pygame.draw.rect(win, (0, 0, 255), (self.pos, self.size))
