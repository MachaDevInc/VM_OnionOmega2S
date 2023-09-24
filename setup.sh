cd ..
cd ..
cd ..
cd ..

cd tmp

opkg update

opkg install git-http

git clone https://github.com/MachaDevInc/VM_OnionOmega2S.git

cp -r /tmp/VM_OnionOmega2S/* /tmp/

rm -r /tmp/VM_OnionOmega2S/

cp -r /tmp/rclocal.txt /etc/rc.local

sh /tmp/install.sh