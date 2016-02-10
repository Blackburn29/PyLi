import threading
import time
import Queue

from LED_Driver import Driver


class Scheduler:
    def __init__(self, led):
        self.q = Queue.Queue()
        self.led = led
        self.consumer = Consumer(self.q, self.led)
        print "Waiting for jobs"

    def schedule(self,  job):
        self.q.put(job);


class Consumer(threading.Thread):
    def __init__(self, queue, led):
        threading.Thread.__init__(self)
        self.q = queue
        self.led = led
        #self.worker = threading.Thread(target=self.doWork, args=(queue, led,))
        self.setDaemon(True)
        self.start()

    def run(self):
        while True:
            values = self.q.get()
            try:
                if self.worker.is_alive():
                    self.worker.kill()
            except AttributeError:
                pass
            self.worker = Worker(values, self.led)

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
            print self.message
            if self.message['task'] == 'SET':
                print "Set color"
                self.led.setRGB(self.message['r'], self.message['g'], self.message['b'])
                self.kill()
            if self.message['task'] == 'FADE':
                self.fade_led(self.led)
            else: # if the task was not handle or identified we should kill the worker
                self.kill()

    def fade_led(self, led):
        increment = True
        value = 0
        while self.is_alive():
            increment, value = led.fade_step(increment, value)
            time.sleep(0.01)



