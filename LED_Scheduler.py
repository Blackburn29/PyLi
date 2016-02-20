import threading
import time
import Queue
import ledcolors

from LED_Driver import Driver


class Scheduler:
    def __init__(self, led, n):
        self.q = Queue.Queue()
        self.led = led
        self.num_leds = n
        self.consumer = Consumer(self.q, self.led, self.num_leds)

    def schedule(self,  job):
        self.q.put(job);


class Consumer(threading.Thread):
    def __init__(self, queue, led, num_leds):
        threading.Thread.__init__(self)
        self.q = queue
        self.led = led
        self.num_leds = num_leds
        self.workers = []

        for i in range(self.num_leds):
            self.workers.append(Worker({'task': None}, self.led))
            print 'Worker for strip {} started'.format(i + 1)

        self.setDaemon(True)
        self.start()

    def get_worker(self, n):
        if n - 1 > self.num_leds:
            raise ValueError('{} is out of range'.format(n))

        return self.workers[n-1]

    def set_worker(self, n, worker):
        if n - 1 > self.num_leds:
            raise ValueError('{} is out of range'.format(n))

        self.workers[n-1] = worker

    def run(self):
        while True:
            values = self.q.get()
            light = int(values['light'])
            try:
                if self.get_worker(light).is_alive():
                    self.get_worker(light).kill()
            except AttributeError:
                pass
            self.set_worker(light, Worker(values, self.led))
            self.q.task_done()

class Worker(threading.Thread):
    def __init__(self, message, led):
        threading.Thread.__init__(self)
        self.kill_flag = False
        self.message = message
        self.led = led
        self.start()

    def is_alive(self):
        return not self.kill_flag

    def kill(self):
        self.kill_flag = True

    def run(self):
        if self.message['task'] == 'SET':
            r,g,b = ledcolors.hsv2rgb(self.message['h'], self.message['s'], self.message['v'])
            self.led.setRGB(self.message['light'], r, g, b)
            self.kill()
        elif self.message['task'] == 'FADE':
            self.fade_led(self.message['light'], self.led, self.message)
        elif self.message['task'] == 'FADE_ALL':
            self.fade_all_colors(self.message['light'], self.led, self.message)
        elif self.message['task'] == 'BLINK':
            self.blink_led(self.message['light'], self.led, self.message)
        elif self.message['task'] == 'BLINK_ALL':
            self.blink_all_colors(self.message['light'], self.led, self.message)
        else: # if the task was not handle or identified we should kill the worker
            self.kill()

    def blink_led(self, light, led, message):
        on = True
        while self.is_alive():
            on = led.blink_led(light, on, message)
            time.sleep(message['speed'])

    def blink_all_colors(self, light, led, message):
        on = True
        value = 0
        while self.is_alive():
            on, value = led.blink_all_colors(light, on, value)
            if not on:
                value = (value + 50) % 360
            time.sleep(message['speed'])

    def fade_led(self, light, led, message):
        increment = True
        value = 0.0
        while self.is_alive():
            increment, value = led.fade_step(light, increment, value, message)
            time.sleep(message['speed']/10)

    def fade_all_colors(self, light, led, message):
        value = 0
        while self.is_alive():
            value = led.fade_all_colors_step(light, value, message)
            time.sleep(message['speed']/10)



