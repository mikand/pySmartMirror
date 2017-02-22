import pygame
import os.path

class BallMode(object):

    def __init__(self, assets_path):
        self.ball = pygame.image.load(os.path.join(assets_path, "ball.gif"))
        self.ballrect = self.ball.get_rect()
        self.speed = [4, 6]

    def loop(self, screen):
        self.ballrect = self.ballrect.move(self.speed)
        if self.ballrect.left < 0 or self.ballrect.right > screen.get_width():
            self.speed[0] = -self.speed[0]
        if self.ballrect.top < 0 or self.ballrect.bottom > screen.get_height():
            self.speed[1] = -self.speed[1]
        screen.blit(self.ball, self.ballrect)

    def only_waits_for_event(self):
        return False

    def preferred_fps(self):
        return 60
