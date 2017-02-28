import pygame
import time
import math
import os.path

class ClockMode(object):

    def __init__(self, assets_path):
        self.clockfont = pygame.font.Font(os.path.join(assets_path, "Helvetica.ttf"), 70)
        self.datefont = pygame.font.Font(os.path.join(assets_path, "Arimo-Regular.ttf"), 20)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)

    def loop(self, screen):
        now = time.localtime()
        h = now.tm_hour
        h_angle = ((h - 3) * math.pi) / 6.0
        m = now.tm_min
        m_angle = ((m - 15) * math.pi) / 30.0
        s = now.tm_sec
        s_angle = ((s- 15) * math.pi) / 30.0

        t = self.clockfont.render(time.strftime("%H:%M:%S"), True, self.white)
        d = self.datefont.render(time.strftime("%A %d %B %Y"), True, self.white)

        space = 10
        big_space = 30

        radius = 80
        center = (screen.get_width() // 2,
                  (screen.get_height() // 2) - (t.get_height() // 2) - radius)

        clock_thickness = 10

        # Clock panel
        pygame.draw.circle(screen, self.white, center, radius, 0)
        pygame.draw.circle(screen, self.black, center, radius-clock_thickness, 0)


        pygame.draw.line(screen, self.white, center,
                         (center[0]+(((radius-clock_thickness)*0.5)*math.cos(h_angle)),
                          center[1]+(((radius-clock_thickness)*0.5)*math.sin(h_angle))), 4)
        pygame.draw.line(screen, self.white, center,
                         (center[0]+(((radius-clock_thickness)*0.9)*math.cos(m_angle)),
                          center[1]+(((radius-clock_thickness)*0.9) *math.sin(m_angle))), 3)
        pygame.draw.aaline(screen, self.white, center,
                           (center[0]+((radius - clock_thickness//2)*math.cos(s_angle)),
                            center[1]+((radius - clock_thickness//2)*math.sin(s_angle))))


        screen.blit(t, (center[0] - (t.get_width() // 2), center[1] + radius + big_space))
        screen.blit(d, (center[0] - (d.get_width() // 2),
                        center[1] + radius + big_space + t.get_height() + space))

    def process_event(self, event):
        pass

    def preferred_fps(self):
        return 10

    def deinit(self):
        pass
