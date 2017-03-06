import pygame
import math
from random import randrange as rr
import utils

class LinesMode(object):

    def __init__(self, assets_path):
        self.assets_path = assets_path
        self.todraw = []
        self.index = 0

    def circle_points_generator(self, center, radius, n_points, offset=0):
        while True:
            a = 2*math.pi/n_points * offset
            yield (radius*math.cos(a) + center[0], radius*math.sin(a) + center[1])
            offset = (offset + 1) % n_points

    def loop(self, screen):
        if self.index >= len(self.todraw):
            if not rr(6) or len(self.todraw) > 1000:
                self.todraw = []
                self.index = 0

            color = utils.randcolor()
            q = rr(1,100)

            a = self.circle_points_generator((rr(screen.get_width()), rr(screen.get_height())),
                        screen.get_width()/rr(1,5), q*rr(1,10))
            b = self.circle_points_generator((rr(screen.get_width()), rr(screen.get_height())),
                        screen.get_width()/rr(1,5), q*rr(1,10), q*rr(100))

            for _ in range(rr(1,10) * q):
                self.todraw.append((color, next(a), next(b)))

        for i in range(self.index):
            c, a, b = self.todraw[i]
            pygame.draw.aaline(screen, c, a, b)

        self.index += 1


    def process_event(self, event):
        pass

    def preferred_fps(self):
        return 60

    def deinit(self):
        pass
