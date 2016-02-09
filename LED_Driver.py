from Adafruit_Driver import PWM

SCALAR = 4096/255 #Used to scale the PWM from 0-255
PWM_MAX = 4000 # Max pulse length out of 4096

class Driver:

    def __init__(self):
        self.pwm = PWM()
        self.pwm.setPWMFreq(120)

    def checkRGB(self, r, g, b):
        if r < 0 or r > 255:
            return False
        if g < 0 or g > 255:
            return False
        if b < 0 or b > 255:
            return False
        return True


    def setRGB(self, r, g, b):
        if self.checkRGB(r, g, b) == False:
            raise Exception("{0}, {1}, {2} is an invalid RGB value".format(r,g,b))

        self.pwm.setPWM(0, 0, r * SCALAR)
        self.pwm.setPWM(1, 0, g * SCALAR)
        self.pwm.setPWM(2, 0, b * SCALAR)

    def fade_step(self, increment, value):
        if increment == True:
            value = value + 50
            if value >= PWM_MAX:
                increment = False
        else:
            value = value - 50
            if value <= 0:
                increment = True
        self.pwm.setPWM(0, 0, value)
        self.pwm.setPWM(1, 0, value)
        self.pwm.setPWM(2, 0, value)
        print(increment, value)
        return increment, value
