echo ===============================
echo       UPDATING SOFTWARE
echo ===============================

sudo apt-get update
sudo apt upgrade -y

echo ===============================
echo         REMOVING X11
echo ===============================

# Remove libx11-6 to remove x11 and all dependent packages (anything GUI related, basically)
sudo apt-get purge libgtk-3-common xkb-data lxde-icon-theme raspberrypi-artwork penguinspuzzle -y

# Clean up redundant packages
sudo apt-get autoremove -y

echo ===============================
echo      INSTALLING LINPHONE
echo ===============================

sudo apt install python-setuptools git screen build-essential pkg-config libx11-6 libopus-dev libspeex-dev -y
sudo easy_install pip
sudo pip install --upgrade pip
sudo pip install wheel

wget http://linphone.org/releases/linphone-python-raspberry/linphone4raspberry-3.9.1-cp27-none-any.whl
sudo pip install linphone4raspberry-*
