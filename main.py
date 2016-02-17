from flask import Flask, request, render_template
import time
from LED_Driver import Driver
from LED_Scheduler import Scheduler

app = Flask(__name__)
NUM_LEDS = 2

@app.route('/')
def basic_page():
    return render_template('index.html')

DRIVER = Driver()
QUEUE = Scheduler(DRIVER, NUM_LEDS)

@app.route('/set/_basic', methods=['POST'])
def basic():
    values = getRGB()
    values['task'] = 'SET'
    QUEUE.schedule(values)
    return 'OK'

@app.route('/fade/_basic', methods=['POST'])
def fade():
    values = getRGB()
    values['task'] = 'FADE'
    values['speed'] = float(request.get_json()['speed'])
    QUEUE.schedule(values)
    return 'OK'

def getRGB():
    data = request.get_json()
    h = data['h']
    s = data['s']
    v = data['v']
    light = data['light']
    return {
            'light': int(light),
            'h': h,
            's': s,
            'v': v,
    }
    
if __name__ == '__main__':
    app.debug = True
    app.run(host='192.168.1.16')
    for i in range(NUM_LEDS):
        DRIVER.setRGB(i, 255, 255, 255)
        time.sleep(0.01)
    for i in range(NUM_LEDS):
        DRIVER.setRGB(i, 0, 0, 0)
        time.sleep(0.01)

