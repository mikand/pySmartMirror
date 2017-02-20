import pygame
import time
import math

class ClockMode(object):

    def __init__(self):
        self.clockfont = pygame.font.SysFont("assets/Helvetica.ttf", 70)
        self.datefont = pygame.font.Font("assets/Arimo-Regular.ttf", 20)
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

        center = (200, 100)
        radius = 80

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
                           (center[0]+((radius - clock_thickness/2)*math.cos(s_angle)),
                            center[1]+((radius - clock_thickness/2)*math.sin(s_angle))))

        t = self.clockfont.render(time.strftime("%H:%M:%S"), True, self.white)
        d = self.datefont.render(time.strftime("%A %d %B %Y"), True, self.white)

        screen.blit(t, (center[0] - (t.get_width() / 2), center[1] + radius + 30))
        screen.blit(d, (center[0] - (d.get_width() / 2),
                        center[1] + radius + 30 + t.get_height() + 10))

    def only_waits_for_event(self):
        return False

    def preferred_fps(self):
        return 5
