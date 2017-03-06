import pygame
import os.path
import threading
import time
import subprocess

class FortuneMode(object):

    def __init__(self, assets_path):
        self.assets_path = assets_path
        self.font = pygame.font.Font(os.path.join(assets_path, "Helvetica.ttf"), 30)
        self.white = (255,255,255)

        original = pygame.image.load(os.path.join(self.assets_path, "fortune.png"))
        self.img = pygame.transform.scale(original, (400, 400))
        self.imgrect = self.img.get_rect()

        self.fortune = None
        self.get_fortune()

    def get_fortune(self):
        try:
            lst = None
            while lst is None or len(lst) > 3 or max(len(x) for x in lst) > 50:
                p = subprocess.Popen(['fortune', '-s'],
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
                out, _ = p.communicate()
                f = out.decode("ascii")
                lst = f.split('\n')

            self.fortune = [""] * 3
            for i, x in enumerate(lst):
                self.fortune[i] = x.strip().replace("\t"," ")
        except FileNotFoundError:
            self.fortune = [""] * 3
            self.fortune[0] = "Error: 'fortune' program not installed!"

    def loop(self, screen):
        t1 = self.font.render(self.fortune[0], True, self.white)
        t2 = self.font.render(self.fortune[1], True, self.white)
        t3 = self.font.render(self.fortune[2], True, self.white)

        space = 10
        self.imgrect.center = ((screen.get_width() // 2),
                               (screen.get_height() // 2) - t1.get_height()  - (t1.get_height() // 2) - (space // 2))
        screen.blit(self.img, self.imgrect)
        screen.blit(t1, (self.imgrect.center[0] - (t1.get_width() // 2),
                        self.imgrect.bottom + space))
        screen.blit(t2, (self.imgrect.center[0] - (t2.get_width() // 2),
                         self.imgrect.bottom + space + t1.get_height()))
        screen.blit(t3, (self.imgrect.center[0] - (t2.get_width() // 2),
                         self.imgrect.bottom + space + t1.get_height() + t2.get_height()))

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_PLUS, pygame.K_KP_PLUS,
                             pygame.K_MINUS, pygame.K_KP_MINUS]:
                self.get_fortune()

    def preferred_fps(self):
        return 10

    def deinit(self):
        pass
