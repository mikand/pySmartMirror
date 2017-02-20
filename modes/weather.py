import requests
import time
import pygame

WEATHER_ICON_MAP = {
    "01d" : "assets/Sun.png",
    "01n" : "assets/Moon.png",
    "02d" : "assets/PartlySunny.png",
    "02n" : "assets/PartlyMoon.png",
    "03d" : "assets/Cloud.png",
    "03n" : "assets/Cloud.png",
    "04d" : "assets/Cloud.png",
    "04n" : "assets/Cloud.png",
    "09d" : "assets/Rain.png",
    "09n" : "assets/Rain.png",
    "10d" : "assets/Rain.png",
    "10n" : "assets/Rain.png",
    "11d" : "assets/Storm.png",
    "11n" : "assets/Storm.png",
    "13d" : "assets/Snow.png",
    "13n" : "assets/Snow.png",
    "50d" : "assets/Haze.png",
    "50n" : "assets/Haze.png",
}


class WeatherMode(object):

    def __init__(self):
        self.forecast = None
        self.last_forecast = None
        self.font = pygame.font.SysFont("assets/Helvetica.ttf", 70)
        self.white = (255,255,255)
        self.weather = None
        self.weatherrect = None

    def get_forecast(self, city, country):
        print("Querying forecasts...")
        address="http://api.openweathermap.org/data/2.5/weather?q=%s,%s"\
            "&APPID=9cbbd3bcaf15a45dfe96196597575b82&units=metric"
        address = address % (city, country)

        response = requests.get(address)
        data = response.json()

        icon_id = data['weather'][0]['icon']
        temperature = data['main']['temp']
        humidity =  data['main']['humidity']

        return WEATHER_ICON_MAP[icon_id], temperature, humidity

    def loop(self, screen):
        ti = time.time()
        if self.forecast is None or ti - self.last_forecast > 600:
            self.forecast = self.get_forecast("trento", "it")
            self.last_forecast = ti
            original = pygame.image.load(self.forecast[0])
            self.weather = pygame.transform.scale(original, (300, 300))
            self.weatherrect = self.weather.get_rect()

        t = self.font.render(u"%.1f \u00B0C  %.1f %%" % self.forecast[1:],
                             True, self.white)

        space = 10
        self.weatherrect.center = ((screen.get_width() // 2),
                                   (screen.get_height() // 2) - (t.get_height() // 2) - (space // 2))
        screen.blit(self.weather, self.weatherrect)
        screen.blit(t, (self.weatherrect.center[0] - (t.get_width() // 2),
                        self.weatherrect.bottom + space))

    def only_waits_for_event(self):
        return True

    def preferred_fps(self):
        return 1
