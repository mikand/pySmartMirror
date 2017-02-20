import locale
import pygame

from modes.weather import WeatherMode
from modes.ball import BallMode
from modes.clock import ClockMode

FRAMERATE = 20
class MainLoop(object):

    def __init__(self):
        self.bg_color = (0, 0, 0)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((800, 600))#, pygame.FULLSCREEN)

        self.modes = [ClockMode(), WeatherMode(), BallMode()]
        self.current_mode = 0

        self.running = True

    def process_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.key == pygame.K_RIGHT:
                self.current_mode = (self.current_mode + 1) % len(self.modes)
            elif event.key == pygame.K_LEFT:
                self.current_mode = (self.current_mode - 1) % len(self.modes)


    def main_loop(self):
        # Generate an artificial event every 10 seconds to perform
        # updates if a mode does not require repainting
        pygame.time.set_timer(pygame.USEREVENT, 10000)

        while self.running:
            mode = self.modes[self.current_mode]

            if mode.only_waits_for_event():
                event = pygame.event.wait()
                self.process_event(event)

            for event in pygame.event.get():
                self.process_event(event)

            self.screen.fill(self.bg_color)

            mode.loop(self.screen)

            pygame.display.flip()
            self.clock.tick(mode.preferred_fps())
            pygame.display.set_caption("fps: %.2f" % self.clock.get_fps())
        pygame.time.set_timer(pygame.USEREVENT, 0)

if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, 'it_IT.utf8')


    pygame.init()
    main = MainLoop()
    try:
        main.main_loop()
    finally:
        pygame.quit()
