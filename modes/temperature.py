import pygame
import os.path

class TemperatureMode(object):

    def __init__(self, assets_path):
        self.assets_path = assets_path
        self.font = pygame.font.Font(os.path.join(assets_path, "Helvetica.ttf"), 70)
        self.white = (255,255,255)

        original = pygame.image.load(os.path.join(self.assets_path, "temperature.png"))
        self.img = pygame.transform.scale(original, (300, 300))
        self.imgrect = self.img.get_rect()

    def loop(self, screen):
        t = self.font.render(u"%.1f \u00B0C  %.1f %%" % (10, 20), True, self.white)

        space = 10
        self.imgrect.center = ((screen.get_width() // 2),
                               (screen.get_height() // 2) - (t.get_height() // 2) - (space // 2))
        screen.blit(self.img, self.imgrect)
        screen.blit(t, (self.imgrect.center[0] - (t.get_width() // 2),
                        self.imgrect.bottom + space))

    def process_event(self, event):
        pass

    def preferred_fps(self):
        return 10
