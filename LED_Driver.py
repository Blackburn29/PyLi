from Adafruit_Driver import PWM
import ledcolors

MAX_RGB = 5 # The max  number of LED strips that can be plugged in
SCALAR = 4096/255 #Used to scale the PWM from 0-255
PWM_MAX = 4000 # Max pulse length out of 4096

class Driver:

    def __init__(self):
        self.pwm = PWM()
        self.pwm.setPWMFreq(1000)

    def checkRGB(self, r, g, b):
        if r < 0 or r > 255:
            return False
        if g < 0 or g > 255:
            return False
        if b < 0 or b > 255:
            return False
        return True


    def setRGB(self, strip, r, g, b):
        if self.checkRGB(r, g, b) == False:
            raise Exception("{0}, {1}, {2} is an invalid RGB value".format(r,g,b))

        offset = strip * 3

        self.pwm.setPWM(offset, 0, r * SCALAR)
        self.pwm.setPWM(offset+1, 0, g * SCALAR)
        self.pwm.setPWM(offset+2, 0, b * SCALAR)

    def fade_step(self, light, increment, value, color):
        if increment == True:
            value = value + 0.01
            if value >= 1.0:
                increment = False
        else:
            value = value - 0.01
            if value <= 0:
                increment = True
        r,g,b = ledcolors.hsv2rgb(color['h'], color['s'], value)
        self.setRGB(light, r, g, b)
        return increment, value
