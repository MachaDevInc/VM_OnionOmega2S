cd

opkg update

opkg install git-http

git clone https://github.com/MachaDevInc/VM_OnionOmega2S.git

cp /root/VM_OnionOmega2S/* /root/

rm -r /root/VM_OnionOmega2S/

# cp /root/rclocal.txt /etc/rc.local

sh /root/install.sh