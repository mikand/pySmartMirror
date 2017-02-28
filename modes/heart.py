import pygame
import os.path
import random

class Heart(object):
    def __init__(self, radius):
        self.radius = radius

        self.last_pos = [random.randint(radius, 800-radius), random.randint(radius, 600-radius)]
        self.speed = [random.randint(-6, 6), random.randint(-6, 6)]
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.randint(-2, 2)

    def loop(self, screen, ball):
        rball = pygame.transform.rotate(ball, self.rotation)
        self.rotation = (self.rotation + self.rotation_speed) % 360
        rballrect = rball.get_rect()
        rballrect.center = self.last_pos
        rballrect = rballrect.move(self.speed)
        if rballrect.center[0] - self.radius  <= 0 or rballrect.center[0] + self.radius >= screen.get_width():
            self.speed[0] = -self.speed[0]
            self.speed[1] += random.choice([-1, 0, 1])
            self.rotation_speed += random.choice([-2, -1, 0, 1, 2])
            self.rotation_speed = max(-6, self.rotation_speed)
            self.rotation_speed = min(6, self.rotation_speed)

        elif rballrect.center[1] - self.radius <= 0 or rballrect.center[1] + self.radius >= screen.get_height():
            self.speed[1] = -self.speed[1]
            self.speed[0] += random.choice([-1, 0, 1])
            self.rotation_speed += random.choice([-2, -1, 0, 1, 2])
            self.rotation_speed = max(-6, self.rotation_speed)
            self.rotation_speed = min(6, self.rotation_speed)

        screen.blit(rball, rballrect)
        self.last_pos = rballrect.center


class HeartMode(object):

    def __init__(self, assets_path, num_hearts=5):
        self.ball = pygame.image.load(os.path.join(assets_path, "heart.png"))
        self.ballrect = self.ball.get_rect()
        self.radius = self.ballrect.width / 2

        self.hearts = []
        for _ in range(num_hearts):
            self.hearts.append(Heart(self.radius))

    def loop(self, screen):
        for h in self.hearts:
            h.loop(screen, self.ball)

    def process_event(self, event):
        pass

    def preferred_fps(self):
        return 60

    def deinit(self):
        pass
