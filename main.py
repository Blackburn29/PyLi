import ledcolors
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
    values = getHSV()
    values['task'] = 'FADE'
    values['speed'] = float(request.form['speed'])
    QUEUE.schedule(values)
    return 'OK'

def getRGB():
    h = request.form['h']
    s = request.form['s']
    v = request.form['v']
    rgb = ledcolors.hsv2rgb(h, s, v)
    print rgb
    return {
            'r': rgb[0],
            'g': rgb[1],
            'b': rgb[2],
    }
    
def getHSV():
    h = request.form['h']
    s = request.form['s']
    v = request.form['v']
    return {
            'h': h,
            's': s,
            'v': v,
    }

if __name__ == '__main__':
    app.debug = True
    app.run(host='192.168.1.16')
