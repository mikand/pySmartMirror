import time
import math
import locale
import pygame
import pygame.gfxdraw
import requests
import json

locale.setlocale(locale.LC_ALL, 'it_IT.utf8')
pygame.init()

weather_icon_map = {
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

def do_forecast(city, country):
    #address="http://api.openweathermap.org/data/2.5/forecast?q=%s,%s&APPID=9cbbd3bcaf15a45dfe96196597575b82"
    print("Querying forecasts...")
    address="http://api.openweathermap.org/data/2.5/weather?q=%s,%s&APPID=9cbbd3bcaf15a45dfe96196597575b82&units=metric"
    address = address % (city.replace(" ", "%20"), country.replace(" ", "%20"))

    response = requests.get(address)
    data = response.json()

    icon_id = data['weather'][0]['icon']
    temperature = data['main']['temp']
    humidity =  data['main']['humidity']

    return weather_icon_map[icon_id], temperature, humidity


FRAMERATE = 20
black = (0, 0, 0)
white = (255,255,255)
clock = pygame.time.Clock()

size = width, height = 800, 600
screen = pygame.display.set_mode(size)#, pygame.FULLSCREEN)

ball = pygame.image.load("assets/ball.gif")
ballrect = ball.get_rect()
speed = [2, 2]

weather = None
weatherrect = None

modes = ["weather", "clock", "ball"]
mode = 0

clockfont = pygame.font.SysFont("assets/Helvetica.ttf", 70)
datefont = pygame.font.Font("assets/Arimo-Regular.ttf", 20)

forecast = None
last_forecast = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_RIGHT:
                mode = (mode + 1) % len(modes)
            elif event.key == pygame.K_LEFT:
                mode = (mode - 1) % len(modes)

    modename = modes[mode]

    screen.fill(black)

    if modename == "ball":
        ballrect = ballrect.move(speed)
        if ballrect.left < 0 or ballrect.right > width:
            speed[0] = -speed[0]
        if ballrect.top < 0 or ballrect.bottom > height:
            speed[1] = -speed[1]
        screen.blit(ball, ballrect)

    elif modename == "weather":
        ti = time.time()
        if forecast is None or ti - last_forecast > 600:
            forecast = do_forecast("trento", "it")
            last_forecast = ti
            original = pygame.image.load(forecast[0])
            weather = pygame.transform.scale(original, (400, 400))
            weatherrect = weather.get_rect()
        weatherrect.center = (250,250)
        screen.blit(weather, weatherrect)
        t = clockfont.render("%.1f \u00B0C  %.1f %%" % forecast[1:], True, white)
        screen.blit(t, (weatherrect.center[0] - (t.get_width() / 2), weatherrect.height + 10))

    elif modename == "clock":
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

        pygame.draw.circle(screen, white, center, radius, 0)
        pygame.draw.circle(screen, black, center, radius-clock_thickness, 0)
        pygame.draw.line(screen, white, center, (center[0]+(((radius-clock_thickness)*0.5)*math.cos(h_angle)), center[1]+(((radius-clock_thickness)*0.5)*math.sin(h_angle))), 4)
        pygame.draw.line(screen, white, center, (center[0]+(((radius-clock_thickness)*0.9)*math.cos(m_angle)), center[1]+(((radius-clock_thickness)*0.9) *math.sin(m_angle))), 3)
        pygame.draw.aaline(screen, white, center, (center[0]+((radius - clock_thickness/2)*math.cos(s_angle)), center[1]+((radius - clock_thickness/2)*math.sin(s_angle))))
        t = clockfont.render(time.strftime("%H:%M:%S"), True, white)
        d = datefont.render(time.strftime("%A %d %B %Y"), True, white)
        screen.blit(t, (center[0] - (t.get_width() / 2), center[1] + radius + 30))
        screen.blit(d, (center[0] - (d.get_width() / 2), center[1] + radius + 30 + t.get_height() + 10))

    else:
        assert False

    pygame.display.flip()
    clock.tick(FRAMERATE)
    pygame.display.set_caption("fps: %.2f" % clock.get_fps())

pygame.quit()
