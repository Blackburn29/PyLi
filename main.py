import colorsys as colors
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

def getRGB():
    rgb = colors.hsv_to_rgb(int(request.form['h']), int(request.form['s']), int(request.form['v']))
    return {
            'r': rgb[0],
            'g': rgb[1],
            'b': rgb[2],
    }

if __name__ == '__main__':
    app.run(host='192.168.1.16')
