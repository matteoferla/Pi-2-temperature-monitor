import Adafruit_DHT
import time
from datetime import datetime
 
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

fh = open('/home/pi/temp.log', 'a')
while True:
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        fh.write("Time={0}; Temp={1:0.1f}C; Humidity={2:0.1f}%;\n".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), temperature, humidity))
    else:
        print("Sensor failure. Check wiring!")
    time.sleep(30)
