echo ===============================
echo       UPDATING SOFTWARE
echo ===============================

sudo apt-get update
sudo apt upgrade -y

echo ===============================
echo         REMOVING X11
echo ===============================

# Remove libx11-6 to remove x11 and all dependent packages (anything GUI related, basically)
sudo apt-get remove --purge --auto-remove libgtk-3-common xkb-data lxde-icon-theme raspberrypi-artwork penguinspuzzle -y

mkdir linphone-tmp
cd linphone-tmp

sudo apt install python-setuptools git screen build-essential libtool automake cmake pkg-config libx11-6 libasound2-dev libspeexdsp-dev libavcodec-dev libgsm1-dev libopus-dev libspeex-dev  libopencore-amrnb-dev libopencore-amrwb-dev -y

echo ===============================
echo    INSTALLING MEDIASTREAMER
echo ===============================

echo 
echo    INSTALLING DEP: MBEDTLS
echo -------------------------------
git clone https://github.com/ARMmbed/mbedtls
cd mbedtls
cmake .
make
sudo make install
cd ..

echo 
echo   INSTALLING DEP: BCTOOLBOX
echo -------------------------------
wget http://www.linphone.org/releases/sources/bctoolbox/bctoolbox-latest.tar.gz
tar xzf bctoolbox-latest.tar.gz
cd bctoolbox*
cmake . -DENABLE_TESTS_COMPONENT=NO
make
sudo make install
cd ..

echo 
echo     INSTALLING DEP: oRTP
echo -------------------------------
wget http://www.linphone.org/releases/sources/ortp/ortp-latest.tar.gz
tar xzf ortp-latest.tar.gz
cd ortp*
cmake .
make
sudo make install
cd ..

echo 
echo    INSTALLING MEDIASTREAMER
echo -------------------------------
wget http://www.linphone.org/releases/sources/mediastreamer/mediastreamer-latest.tar.gz
tar xzf mediastreamer-latest.tar.gz
cd mediastreamer*
cmake -DENABLE_VIDEO=NO -DENABLE_ALSA=YES -DENABLE_NON_FREE_CODECS=YES -DENABLE_G729B_CNG=YES.
make
sudo make install
cd ..
export MEDIASTREAMER_CFLAGS=-I/usr/local/include/mediastreamer2
export MEDIASTREAMER_LIBS=-L/usr/local/lib

echo ===============================
echo      INSTALLING PLUGINS
echo ===============================

echo 
echo      INSTALLING BCG729
echo -------------------------------

wget http://www.linphone.org/releases/sources/plugins/bcg729/bcg729-latest.tar.gz
tar xzf bcg729-latest.tar.gz
cd bcg729-latest.tar.gz
cmake .
make
sudo make install
cd ..

echo 
echo       INSTALLING MSAMR
echo -------------------------------
wget http://www.linphone.org/releases/sources/plugins/msamr/msamr-latest.tar.gz
tar xzf msamr-latest.tar.gz
cd msamr*
cmake .
make
sudo make install
cd ..

 echo 
 echo       INSTALLING MSiLBC
 echo -------------------------------
 git clone https://github.com/Linphone-sync/libilbc-rfc3951
 cd libilbc-rfc3951
 ./autogen.sh
 ./configure
 make
 sudo make install
 cd ..
 wget http://www.linphone.org/releases/sources/plugins/msilbc/msilbc-latest.tar.gz
 tar xvf msilbc-latest.tar.gz
 cd msilbc*
 ./configure
 make
 sudo make install
 cd ..

echo 
echo      INSTALLING MS-SILK
echo -------------------------------

wget http://www.linphone.org/releases/sources/plugins/mssilk/mssilk-latest.tar.gz
tar xvf mssilk-latest.tar.gz
cd mssilk*
./configure
make
sudo make install
cd ..


echo ===============================
echo    INSTALLING LINPHONE4RPI
echo ===============================
sudo easy_install pip
sudo pip install --upgrade pip
sudo pip install wheel

wget http://linphone.org/releases/linphone-python-raspberry/linphone4raspberry-3.9.1-cp27-none-any.whl
sudo pip install linphone4raspberry-*

cd ..
rm -rf linphone-tmp