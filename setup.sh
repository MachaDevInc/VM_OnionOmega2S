cd

opkg update

opkg install git-http

git clone https://github.com/MachaDevInc/VM_OnionOmega2S.git

cp /root/Vending-Machine/* /root/

rm -r /root/Vending-Machine/

cp /root/rclocal.txt /etc/rc.local

sh /root/install.sh