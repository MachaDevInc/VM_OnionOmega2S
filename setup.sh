cd ..
cd ..
cd ..
cd ..

mkdir VM

opkg update

opkg install git-http

git clone https://github.com/MachaDevInc/VM_OnionOmega2S.git

cp /VM/VM_OnionOmega2S/* /VM/

rm -r /VM/VM_OnionOmega2S/

cp /root/rclocal.txt /etc/rc.local

sh /VM/install.sh