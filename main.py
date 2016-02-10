import colorsys as colors
import math
from flask import Flask, request, render_template
from LED_Driver import Driver
from LED_Scheduler import Scheduler

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')



DRIVER = Driver()
QUEUE = Scheduler(DRIVER)

@app.route('/basic', methods=['POST'])
def basic():
    values = getRGB()
    values['task'] = 'SET'
    QUEUE.schedule(values)
    return 'OK'

@app.route('/fade', methods=['POST'])
def fade():
    values = getRGB()
    values['task'] = 'FADE'
    QUEUE.schedule(values)
    return 'OK'

def getRGB():
    h = int(float(request.form['h']))
    s = float(request.form['s'])
    v = float(request.form['v'])
    rgb = hsv2rgb(h, s, v)
    print rgb
    return {
            'r': rgb[0],
            'g': rgb[1],
            'b': rgb[2],
    }

def hsv2rgb(h, s, v):
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return r, g, b

if __name__ == '__main__':
    app.debug = True
    app.run(host='192.168.1.16')
