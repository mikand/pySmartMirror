import requests
import time
import pygame
import os.path

WEATHER_ICON_MAP = {
    "01d" : "Sun.png",
    "01n" : "Moon.png",
    "02d" : "PartlySunny.png",
    "02n" : "PartlyMoon.png",
    "03d" : "Cloud.png",
    "03n" : "Cloud.png",
    "04d" : "Cloud.png",
    "04n" : "Cloud.png",
    "09d" : "Rain.png",
    "09n" : "Rain.png",
    "10d" : "Rain.png",
    "10n" : "Rain.png",
    "11d" : "Storm.png",
    "11n" : "Storm.png",
    "13d" : "Snow.png",
    "13n" : "Snow.png",
    "50d" : "Haze.png",
    "50n" : "Haze.png",
}


class WeatherMode(object):

    def __init__(self, assets_path):
        self.assets_path = assets_path
        self.forecast = None
        self.last_forecast = -1
        self.font = pygame.font.Font(os.path.join(assets_path, "Helvetica.ttf"), 70)
        self.white = (255,255,255)
        self.weather = None
        self.weatherrect = None
        self.forecast_interval = 600
        self.retry_interval = 5

    def get_forecast(self, city, country):
        print("Querying forecasts...")
        try:
            address="http://api.openweathermap.org/data/2.5/weather?q=%s,%s"\
                "&APPID=9cbbd3bcaf15a45dfe96196597575b82&units=metric"
            address = address % (city, country)

            response = requests.get(address)
            data = response.json()

            icon_id = data['weather'][0]['icon']
            temperature = data['main']['temp']
            humidity =  data['main']['humidity']
            icon = os.path.join(self.assets_path, WEATHER_ICON_MAP[icon_id])

            return icon, temperature, humidity
        except requests.exceptions.ConnectionError:
            return None

    def loop(self, screen):
        ti = time.time()
        if ti - self.last_forecast > self.forecast_interval:
            self.forecast = self.get_forecast("trento", "it")
            if self.forecast is not None:
                self.last_forecast = ti
                original = pygame.image.load(self.forecast[0])
                self.weather = pygame.transform.scale(original, (300, 300))
                self.weatherrect = self.weather.get_rect()
            else:
                self.last_forecast = ti - self.forecast_interval + self.retry_interval
                original = pygame.image.load(os.path.join(self.assets_path,
                                                          "disconnected.png"))
                self.weather = pygame.transform.scale(original, (300, 300))
                self.weatherrect = self.weather.get_rect()


        if self.forecast:
            t = self.font.render(u"%.1f \u00B0C  %.1f %%" % self.forecast[1:],
                                 True, self.white)
        else:
            t = self.font.render(u"No Internet", True, self.white)

        space = 15
        self.weatherrect.center = ((screen.get_width() // 2),
                                   (screen.get_height() // 2) - (t.get_height() // 2) - (space // 2))
        screen.blit(self.weather, self.weatherrect)
        screen.blit(t, (self.weatherrect.center[0] - (t.get_width() // 2),
                        self.weatherrect.bottom + space))

    def process_event(self, event):
        pass

    def preferred_fps(self):
        return 10

    def deinit(self):
        pass
