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
    if 'speed' in request.get_json():
        values['speed'] = float(request.get_json()['speed'])
    else:
        values['speed'] = 0.1;
    QUEUE.schedule(values)
    return 'OK'

@app.route('/fade/_all', methods=['POST'])
def fade_all():
    values = {}
    values['task'] = 'FADE_ALL'
    if 'speed' in request.get_json():
        values['speed'] = float(request.get_json()['speed'])
    else:
        values['speed'] = 0.1;
    if 'speed' in request.get_json():
        values['light'] = float(request.get_json()['light'])
    else:
        return 'Missing light parameter'
    QUEUE.schedule(values)
    return 'OK'

@app.route('/blink/_basic', methods=['POST'])
def blink():
    values = getRGB()
    values['task'] = 'BLINK'
    if 'speed' in request.get_json():
        values['speed'] = float(request.get_json()['speed'])
    else:
        values['speed'] = 0.1;
    QUEUE.schedule(values)
    return 'OK'

@app.route('/blink/_all', methods=['POST'])
def blink_all():
    values = {}
    values['task'] = 'BLINK_ALL'
    if 'speed' in request.get_json():
        values['speed'] = float(request.get_json()['speed'])
    else:
        values['speed'] = 0.1;
    if 'speed' in request.get_json():
        values['light'] = float(request.get_json()['light'])
    else:
        return 'Missing light parameter'
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
    app.run(host='0.0.0.0')
