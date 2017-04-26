sudo apt-get update

# Remove libx11-6 to remove x11 and all dependent packages (anything GUI related, basically)
## ...turns out they're required for linphone :|
sudo apt-get purge libx11-6 libgtk-3-common xkb-data lxde-icon-theme raspberrypi-artwork penguinspuzzle -y

# Clean up redundant packages
sudo apt-get autoremove -y

sudo apt install python-setuptools git screen build-essential pkg-config -y
sudo easy_install pip
sudo pip install --upgrade pip
sudo pip install wheel

wget http://linphone.org/releases/linphone-python-raspberry/linphone4raspberry-3.9.1-cp27-none-any.whl
sudo pip install linphone4raspberry-*
