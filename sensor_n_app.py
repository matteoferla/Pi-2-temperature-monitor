#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template_string
from waitress import serve
from scipy.signal import savgol_filter
import json, re
import threading
import Adafruit_DHT
import time
from datetime import datetime

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4
LOGFILE = '/home/pi/Pi-2-temperature-monitor/temp.log'


page = '''
<!doctype html>

<html lang="en">
<head>
  <meta charset="utf-8">

  <title>Temperature logger</title>
  <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>

</head>

<body>
  <div id="graph" style="height:600px;width:800px;"></div>
  <script type="text/javascript">
  var trace1 = {
  x: {{dt|safe}},
  y: {{temp|safe}},
  name: 'temperature',
  type: 'scatter'
};

var trace2 = {
  x: {{dt|safe}},
  y: {{hum|safe}},
  name: 'humidity',
  yaxis: 'y2',
  type: 'scatter'
};

var data = [trace1, trace2];

var layout = {
  title: 'Bedroom temperature',
  yaxis: {title: 'Temperature [°C]', range: [15,40], dtick: 1},
  yaxis2: {
    title: 'Humidity [%]',
    overlaying: 'y',
    side: 'right',
    range: [0,100], dtick: 100/25
  }
};

Plotly.newPlot('graph', data, layout);
  </script>
</body>
</html>
'''

def get_data():
    dt = []
    temp = []
    hum = []
    with open(LOGFILE) as fh:
        for line in fh:
            if line[0] == 'T':
                reading = re.match('Time=(?P<dt>[\d+\-\ \:]+); Temp=(?P<temp>[\-\.\d]+)C; Humidity=(?P<hum>[\-\.\d]+)%;', line).groupdict()
                t = float(reading['temp'])
                h = float(reading['hum'])
                if t > 50 or h > 100:
                    continue
                dt.append(reading['dt'])
                temp.append(t)
                hum.append(h)
    smooth = lambda a: savgol_filter(a, 31, 3).tolist()
    return dt, smooth(temp), smooth(hum)

app = Flask(__name__)


@app.route('/')
def serve_data():
    dt, temp, hum = get_data()
    return render_template_string(page,
                                  dt=json.dumps(dt),
                                  temp=json.dumps(temp),
                                  hum=json.dumps(hum))


def sensor():
    fh = open(LOGFILE, 'a')
    while True:
        humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
        if humidity is not None and temperature is not None:
            fh.write("Time={0}; Temp={1:0.1f}C; Humidity={2:0.1f}%;\n".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), temperature, humidity))
        else:
            print("Sensor failure. Check wiring!")
        time.sleep(30)

if __name__ == '__main__':
    threading.Thread(target=sensor).start()
    serve(app, host='0.0.0.0', port=8000)