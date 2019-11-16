# Temperature monitor and webapp for Raspberry pi
Temperature sensor, logger and [site](http://temperature.matteoferla.com/).

Namely, sensor collects data every half-minute, currently DHR-11 and a Waitress served Flask app shows the data on port 8000 as a nice interactive plotly graph.

Hardware Rasberry pi 3B. I have no idea if it works with others.

Previously, I have tried twice and failed to set up a 433MHz receiever to intercept the data from an Oregon Scientific THGN132 (both versions) using code others wrote. However, I could get 433MHz communication going so I think it was the OregonPi code.


**This is the list of commands I typed. It is not a tutorial. But you are welcome to steal code.**


NB2. I have had no success getting python 3.7 on a pi 3. So this is all 3.6.

# Setup

Fresh microSD card: `Raspbian Buster with desktop and recommended software` installed with `BalenaEtcher.app`.
Pi with LCD: start-up, set wifi and activate ssh in `preferences/interface`.


## Conda

I went with conda as I don't want the pain that is the installing anything on the pi architecture. However, conda becomes a pain with `mod_wgsi` (see Apache2).

	cd Downloads
	wget https://github.com/jjhelmus/berryconda/releases/download/v2.0.0/Berryconda3-2.0.0-Linux-armv7l.sh
	chmod +x Berryconda3-2.0.0-Linux-armv7l.sh
	./Berryconda3-2.0.0-Linux-armv7l.sh -b
	yes | pip3 install --upgrade pip
	yes | pip3 install -U $(pip freeze | awk '{split($0, a, "=="); print a[1]}')
	conda install -y flask scipy numpy pandas
    yes | pip3 install --upgrade setuptools
	yes | pip3 install Adafruit_DHT
	#yes | pip3 install adafruit-circuitpython-dht
	yes | pip3 install adafruit-circuitpython-sgp30
    yes | pip3 install waitress
    #sudo apt install wiringpi # unneeded
    
## DB
For the long run having a DB would be good.
    
    pip3 install -U Flask-SQLAlchemy
    sudo apt install sqlite3
    python3
    > from sensor_n_app.py import db
    > db.create_all()
    
On my Pi 3B, the older Adafruit_DHT works while adafruit-circuitpython-dht gives me 

    >>> sensor = adafruit_dht.DHT22(board.D4)
    Unable to open chip: gpiochip0
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/home/pi/berryconda3/lib/python3.6/site-packages/adafruit_dht.py", line 255, in __init__
        super().__init__(False, pin, 1000)
      File "/home/pi/berryconda3/lib/python3.6/site-packages/adafruit_dht.py", line 66, in __init__
        self.pulse_in = PulseIn(self._pin, 81, True)
      File "/home/pi/berryconda3/lib/python3.6/site-packages/adafruit_blinka/microcontroller/bcm283x/pulseio/PulseIn.py", line 64, in __init__
        message = self._wait_receive_msg()
      File "/home/pi/berryconda3/lib/python3.6/site-packages/adafruit_blinka/microcontroller/bcm283x/pulseio/PulseIn.py", line 80, in _wait_receive_msg
        raise RuntimeError("Timed out waiting for PulseIn message")
    RuntimeError: Timed out waiting for PulseIn message
    
I have installed a few libraries, but none worked.

## Enabling
    
    sudo raspi-config
    
change the I2C to enabled.


## Apache2

In the first iteratition I was going get mod_wsgi to server. Then I remembered that all 80/443 traffic though my home modem goes to another computer anyway —not sure how I forgot. So I don't need apache2 here. 

	sudo apt update
	sudo apt install apache2
    sudo a2dissite 000-default

Reverse proxy route?

    sudo a2enmod proxy
    sudo a2enmod proxy_http
    sudo a2enmod proxy_balancer
    sudo a2enmod lbmethod_byrequests

Previously I had tried to do it with mod_wsgi. But this requires to be compiled by the version of python you are using. So for berryconda I did:

This installs using the system py2 version

    sudo apt-get install libapache2-mod-wsgi

This installs using the system py3 version

    sudo apt-get install libapache2-mod-wsgi-py3

This builds mod_wsgi

    sudo apt-get install apache2-dev
    pip3 install mod_wsgi
    reboot
    sudo /home/pi/berryconda3/bin/mod_wsgi-express install-module

However, when I added these lines to the apache2 conf file it did not work...

    LoadModule wsgi_module modules/mod_wsgi.so
    WSGIPythonHome /home/pi/berryconda/bin
    WSGIPythonPath /home/pi/berryconda/bin:/home/pi/berryconda/pkgs
    WSGIScriptAlias /temperature /home/pi/Pi-2-temperature-monitor/wsgi.py

I don't think I am the only person wanting to use berryconda and mod_wsgi.
But reverse proxy is a perfectly fine solution, the only catch is that the app needs to be on systemd.

## Repo

There is a phylosophy of where to dump files. I ignore it and put everything on the Desktop or in home.

    cd
    git clone https://github.com/matteoferla/Pi-2-temperature-monitor.git
	

But does it work?

    cd Pi-2-temperature-monitor

    python sensor.py
    #kill. Then try.
    python app.py

Great... now:

    sudo cp temperature.service /etc/systemd/system/temperature.service
    sudo systemctl start temperature
    sudo systemctl enable temperature
    #sudo cp temperature.conf /etc/apache2/sites-available/temperature.conf
    #sudo a2ensite temperature.conf


Made a mistake or a change?

    sudo systemctl restart temperature
    systemctl daemon-reload

If I am using apache2.

    sudo systemctl restart apache2
    sudo tail /var/log/apache2/error.log
    sudo systemctl status apache2.service


# Wiring
GPIO 4 is #7. 
3.3V. On upgrade I'll use a level shifter and use the 5V.

# Software upgrades

There is a silliness. 

* I apply `savgol_filter(x, 31, 3)` smoothing function to the saved data collected every 30 seconds as opposed collecting continously smoothing and interpolating the array to every 30 seconds.
* I am simply using a log file.

# Hardware upgrades

I am going to switching to Adafruit DHR_22 and SGP30 Air Quality Sensor in order to get better temperature readings and CO2 levels. I could add a barometer and I think I have one. I have a MQ-2 gas sensor (organics), but I am not sure I need a methane sensor.




I technically have a AM3202, not a DHT22. It accepts 3.3V, is it better with 5V? I think so.
My level shifter (flat board thing with 8 pins each side to change 5V <=> 3.3V) has two channels each way and two sides the 5V side has an HV next to the GND. LV is 3.5V. The RXI on either flank of the 5V side is the _in_, while the RXO is the _out_ on the 3.3V side.

SGP30 is the Adafruit CO2 sensor.

Stuff in the box of lost bits

* DHT11 temperature and humidity sensor module
* HC-SR501 infrared human body induction module
* DS1302 real time clock module
* Rain sersor module
* Sound sensor module
* HC-SR04 ultrasonic sersor
* The flame sensor module
* KY-008 laser head sersor module
* Photosensitive resistance sensor module
* YL-69 soil moisture sensor
* Obstacle avoidance sensor
* Vibration sensor module
* MQ-2 gas sensor module
* 315M 443MHz
* Tilt sensor module
* Path tracing module

I have a MCP3008, so I could use it with the photosensitive resistance sensor module
https://tutorials-raspberrypi.com/photoresistor-brightness-light-sensor-with-raspberry-pi/

Sound sensor module?

Official outside temperature and sunrise sunset
