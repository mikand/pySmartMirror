import RPi.GPIO as GPIO

class Hardware(object):

    def __init__(self):
        self.SCREEN_PIN = 37
        self.LED_PIN = 32

        GPIO.setmode(GPIO.BOARD)
        
        GPIO.setup(self.SCREEN_PIN, GPIO.OUT)
        self.screen_pwm = GPIO.PWM(self.SCREEN_PIN, 100)
        self.screen_enabled = False
        GPIO.output(self.SCREEN_PIN, self.screen_enabled)        

        GPIO.setup(self.LED_PIN, GPIO.OUT)
        self.led_pwm = GPIO.PWM(self.LED_PIN, 100)
        self.led_enabled = False
        GPIO.output(self.LED_PIN, self.led_enabled)        

    def enable_screen(self, enable=True):
        if enable and not self.screen_enabled:
            self.screen_pwm.start(100)
        elif not enable and self.screen_enabled:
            self.screen_pwm.stop()
        self.screen_enable = enable

    def dim_screen(self, level):
        assert level >= 0
        assert level <= 100
        self.screen_pwm.ChangeDutyCycle(level)

    def enable_led(self, enable=True):
        if enable and not self.led_enabled:
            self.led_pwm.start(100)
        elif not enable and self.led_enabled:
            self.led_pwm.stop()
        self.led_enable = enable

    def dim_led(self, level):
        assert level >= 0
        assert level <= 100
        self.led_pwm.ChangeDutyCycle(level)

    def deinit(self):
        if self.screen_enabled:
            self.screen_pwm.stop()

        if self.led_enabled:
            self.led_pwm.stop()
            
        GPIO.cleanup()
