import pygame
import os.path
import Adafruit_DHT    
import threading
import time

class TemperatureMode(object):

    def __init__(self, assets_path):
        self.assets_path = assets_path
        self.font = pygame.font.Font(os.path.join(assets_path, "Helvetica.ttf"), 70)
        self.white = (255,255,255)

        original = pygame.image.load(os.path.join(self.assets_path, "temperature.png"))
        self.img = pygame.transform.scale(original, (300, 300))
        self.imgrect = self.img.get_rect()

        self.readings_lock = threading.RLock()
        self.readings = []
        self.reading_thread_run = True
        self.reading_thread = threading.Thread(target=self.reading_loop)
        self.reading_thread.start()

    def reading_loop(self):
        while self.reading_thread_run:
            self.read_temperature()
            time.sleep(5)
        
    def read_temperature(self):
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 18)
        with self.readings_lock:
            if len(self.readings) >= 10:
                self.readings.pop(0)
            self.readings.append((humidity, temperature))
            
    def temperature(self):
        with self.readings_lock:
            if len(self.readings) == 0:
                return "?"
            return sum(x[1] for x in self.readings) / float(len(self.readings))

    def humidity(self):
        with self.readings_lock:
            if len(self.readings) == 0:
                return "?"
            return sum(x[0] for x in self.readings) / float(len(self.readings))

    def loop(self, screen):
        t = self.font.render(u"%.1f \u00B0C  %.1f %%" % (self.temperature(), self.humidity()), True, self.white)

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

    def deinit(self):
        self.reading_thread_run = False
        self.reading_thread.join()
