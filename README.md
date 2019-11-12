# Pi-2-temperature-monitor
Temperature sensor, logger and site

* Logging is do

# Setup

Fresh microSD card: `Raspbian Buster with desktop and recommended software` installed with `BalenaEtcher.app`.
Pi with LCD: start-up, set wifi and activate ssh in `preferences/interface`.

## Apache2

	sudo apt update
	sudo apt install apache2

## Conda

	cd Downloads
	wget https://github.com/jjhelmus/berryconda/releases/download/v2.0.0/Berryconda3-2.0.0-Linux-armv7l.sh
	chmod +x Berryconda3-2.0.0-Linux-armv7l.sh
	./Berryconda3-2.0.0-Linux-armv7l.sh -b
	yes | pip install --upgrade pip
	yes | pip install -U $(pip freeze | awk '{split($0, a, "=="); print a[1]}')
	yes | conda install -y flask scipy numpy pandas
	yes | pip install Adafruit_DHT

## Repo

	cd
	git clone https://github.com/matteoferla/Pi-2-temperature-monitor.git



