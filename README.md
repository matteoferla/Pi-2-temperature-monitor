# Pi-2-temperature-monitor
Temperature sensor, logger and site

# Genesis 1:1

sudo apt update
sudo apt install apache2

cd Downloads
wget https://github.com/jjhelmus/berryconda/releases/download/v2.0.0/Berryconda3-2.0.0-Linux-armv7l.sh
chmod +x Berryconda3-2.0.0-Linux-armv7l.sh
./Berryconda3-2.0.0-Linux-armv7l.sh
pip install --upgrade pip
pip install -U $(pip freeze | awk '{split($0, a, "=="); print a[1]}')


