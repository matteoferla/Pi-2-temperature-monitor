# Pi-2-temperature-monitor
Temperature sensor, logger and site.

Namely, sensor collects data every half-minute, currently DHR-11 and a Waitress served Flask app shows the data on port 8000 as a nice interactive plotly graph.

Hardware Rasberry pi 2B. So ought to work with a 3, 4 etc.

This is the list of commands I typed. It is not a tutorial. But you are welcome to steal code.

There is a silliness. I apply `savgol_filter(x, 31, 3)` smoothing function to the saved data collected every 30 seconds as opposed collecting continously smoothing and interpolating the array to every 30 seconds.

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
        yes | pip3 install waitress


NB. I have had no success getting python 3.7 on a pi 2. So this is all 3.6.

## Apache2

In the first iteratition I was going get mod_wsgi to server. Then I remembered that all 80/443 traffic though my home modem goes to another computer anyway —not sure how. So I don't need apache2. 

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


Made a mistake?

       sudo systemctl restart temperature
       systemctl daemon-reload

If I am using apache2.

       sudo systemctl restart apache2
       sudo tail /var/log/apache2/error.log
       sudo systemctl status apache2.service

# Upgrades

I am going to switching to Adafruit DHR_22 and SGP30 Air Quality Sensor in order to get better temperature readings and CO2 levels. I could add a barometer and I think I have one. I have a MQ-2 gas sensor (organics), but I am not sure I need a methane sensor.

Previously, I have tried twice and failed to set up a 433MHz receiever to intercept the data from an Oregon Scientific THGN132 (both versions) using code others wrote. However, I could get 433MHz communication going so I think it was the OregonPi code.



