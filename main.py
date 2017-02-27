import locale
import pygame
import os.path

HAS_LIRC = True
try:
    import lirc
except ImportError:
    HAS_LIRC = False

from modes.weather import WeatherMode
from modes.ball import BallMode
from modes.clock import ClockMode

from hardware import Hardware

script_path = os.path.dirname(os.path.realpath(__file__))
assets_path = os.path.join(script_path, "assets")

class MainLoop(object):

    def __init__(self, fullscreen=False):
        self.bg_color = (0, 0, 0)
        self.clock = pygame.time.Clock()

        if fullscreen:
            self.screen = pygame.display.set_mode((800, 600), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((800, 600))

        self.modes = [WeatherMode(assets_path),
                      ClockMode(assets_path),
                      BallMode(assets_path)]
        self.current_mode = 0

        self.running = True
        
        self.hw = Hardware()
        self.led_level = 10
        

        
    def lirc2pygame(self, keys):
        k = keys[0]
        if k == "KEY_POWER":
            return pygame.event.Event(pygame.QUIT)

        # These keys are already handled by pygame!
        # if k == "KEY_LEFT":
        #     return pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT)
        # if k == "KEY_RIGHT":
        #     return pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)
        # if k == "KEY_UP":
        #     return pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)
        # if k == "KEY_DOWN":
        #     return pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)
        return None
        
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
            elif event.key == pygame.K_UP:
                self.hw.enable_led(True)
                self.led_level = min(10, self.led_level + 1)
                self.hw.dim_led(self.led_level * 10)
            elif event.key == pygame.K_DOWN:
                self.hw.enable_led(True)
                self.led_level = max(0, self.led_level - 1)
                self.hw.dim_led(self.led_level * 10)


    def main_loop(self, lirc_socket=None):
        # Generate an artificial event every 10 seconds to perform
        # updates if a mode does not require repainting
        pygame.time.set_timer(pygame.USEREVENT, 10000)
        pygame.event.set_blocked(pygame.MOUSEMOTION)

        # Hide mouse cursor
        pygame.mouse.set_visible(False)
        
        clear = self.screen.copy()
        clear.fill((0, 0, 0))

        self.hw.enable_screen(True)
        
        while self.running:
            mode = self.modes[self.current_mode]

            for event in pygame.event.get():
                self.process_event(event)
            if lirc_socket:
                keys = lirc.nextcode()
                if keys:
                    event = self.lirc2pygame(keys)
                    if event:
                        self.process_event(event)

            self.screen.blit(clear, (0, 0))

            mode.loop(self.screen)

            pygame.display.flip()
            self.clock.tick(mode.preferred_fps())
            pygame.display.set_caption("fps: %.2f" % self.clock.get_fps())

        pygame.time.set_timer(pygame.USEREVENT, 0)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--fullscreen", action="store_true")
    args = parser.parse_args()

    locale.setlocale(locale.LC_ALL, 'it_IT.utf8')

    pygame.init()
    lirc_socket = None
    if HAS_LIRC:
        lirc_socket = lirc.init("pySmartMirror",
                                config_filename=os.path.join(assets_path, "lircrc"),
                                blocking=False)
    main = MainLoop(fullscreen=args.fullscreen)
    try:
        main.main_loop(lirc_socket)
    finally:
        if HAS_LIRC:
            lirc.deinit()
        main.hw.deinit()
        pygame.quit()
