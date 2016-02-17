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
        while self.is_alive():
            if self.message['task'] == 'SET':
                r,g,b = ledcolors.hsv2rgb(self.message['h'], self.message['s'], self.message['v'])
                print  r,g,b
                self.led.setRGB(self.message['light'], r, g, b)
                print 'SET LED on {}'.format(self.message['light'])
                self.kill()
            if self.message['task'] == 'FADE':
                self.fade_led(self.message['light'], self.led, self.message)
            else: # if the task was not handle or identified we should kill the worker
                self.kill()

    def fade_led(self, light, led, message):
        increment = True
        value = 0.0
        while self.is_alive():
            increment, value = led.fade_step(light, increment, value, message)
            time.sleep(message['speed'])



