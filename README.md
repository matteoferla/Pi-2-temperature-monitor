# Pi-2-temperature-monitor
Temperature sensor, logger and site

* Logging is do

# Setup

Fresh microSD card: `Raspbian Buster with desktop and recommended software` installed with `BalenaEtcher.app`.
Pi with LCD: start-up, set wifi and activate ssh in `preferences/interface`.


## Conda

	cd Downloads
	wget https://github.com/jjhelmus/berryconda/releases/download/v2.0.0/Berryconda3-2.0.0-Linux-armv7l.sh
	chmod +x Berryconda3-2.0.0-Linux-armv7l.sh
	./Berryconda3-2.0.0-Linux-armv7l.sh -b
	yes | pip3 install --upgrade pip
	yes | pip3 install -U $(pip freeze | awk '{split($0, a, "=="); print a[1]}')
	yes | conda install -y flask scipy numpy pandas
        yes | pip3 install --upgrade setuptools
	yes | pip3 install Adafruit_DHT

## Apache2

	sudo apt update
	sudo apt install apache2
        sudo apt-get install libapache2-mod-wsgi-py3
        sudo a2dissite 000-default
        sudo apt-get install apache2-dev
        pip3 install mod_wsgi
        sudo /home/pi/berryconda3/bin/mod_wsgi-express install-module

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

        sudo cp temperature.conf /etc/apache2/sites-available/temperature.conf
        sudo a2ensite temperature.conf
        sudo cp temperature.service /etc/systemd/system/temperature.service
        sudo systemctl start temperature
        sudo systemctl enable temperature

Made a mistake?

       sudo systemctl restart apache2
       sudo systemctl restart temperature
       sudo tail /var/log/apache2/error.log
       sudo systemctl status apache2.service



