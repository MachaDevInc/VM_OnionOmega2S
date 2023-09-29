cd ..
cd ..
cd ..
cd ..

echo heartbeat > /sys/class/leds/omega2p\:amber\:system/trigger

mkdir VM

cd VM

date -s "2023-09-29 12:00:00"

opkg update

opkg install git-http

git clone https://github.com/MachaDevInc/VM_OnionOmega2S.git

cp -r /VM/VM_OnionOmega2S/* /VM/

rm -r /VM/VM_OnionOmega2S/

cp -r /VM/rclocal.txt /etc/rc.local

sh /VM/install.sh
