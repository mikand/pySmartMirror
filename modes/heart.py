import pygame
import os.path
import random
import utils



class Heart(object):
    def __init__(self, assets_path):
        fname = random.choice(["heart1.png", "heart2.png", "heart3.png"])
        self.heart = pygame.image.load(os.path.join(assets_path, fname))
        self.heartrect = self.heart.get_rect()
        self.radius = self.heartrect.width / 2

        self.color = utils.randcolor() + (0,)
        # zero out RGB values
        self.heart.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
        # add in new RGB values
        self.heart.fill(self.color, None, pygame.BLEND_RGBA_ADD)

        self.last_pos = [random.randint(self.radius, 800-self.radius),
                         random.randint(self.radius, 600-self.radius)]
        self.speed = [random.randint(-6, 6), random.randint(-6, 6)]
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.randint(-2, 2)


    def loop(self, screen):
        rheart = pygame.transform.rotate(self.heart, self.rotation)
        self.rotation = (self.rotation + self.rotation_speed) % 360
        rheartrect = rheart.get_rect()
        rheartrect.center = self.last_pos
        rheartrect = rheartrect.move(self.speed)
        if rheartrect.center[0] - self.radius  <= 0 or \
           rheartrect.center[0] + self.radius >= screen.get_width():
            self.speed[0] = -self.speed[0]
            self.speed[1] += random.choice([-1, 0, 1])
            self.rotation_speed += random.choice([-2, -1, 0, 1, 2])
            self.rotation_speed = max(-6, self.rotation_speed)
            self.rotation_speed = min(6, self.rotation_speed)

        elif rheartrect.center[1] - self.radius <= 0 or \
             rheartrect.center[1] + self.radius >= screen.get_height():
            self.speed[1] = -self.speed[1]
            self.speed[0] += random.choice([-1, 0, 1])
            self.rotation_speed += random.choice([-2, -1, 0, 1, 2])
            self.rotation_speed = max(-6, self.rotation_speed)
            self.rotation_speed = min(6, self.rotation_speed)

        screen.blit(rheart, rheartrect)
        self.last_pos = rheartrect.center


class HeartMode(object):

    def __init__(self, assets_path, num_hearts=5):
        self.assets_path = assets_path
        self.hearts = []
        for _ in range(num_hearts):
            self.hearts.append(Heart(assets_path))

    def loop(self, screen):
        for h in self.hearts:
            h.loop(screen)

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_PLUS, pygame.K_KP_PLUS]:
                self.hearts.append(Heart(self.assets_path))
            if event.key in [pygame.K_MINUS, pygame.K_KP_MINUS]:
                if len(self.hearts) > 0:
                    self.hearts.pop(random.randrange(len(self.hearts)))


    def preferred_fps(self):
        return 60

    def deinit(self):
        pass
