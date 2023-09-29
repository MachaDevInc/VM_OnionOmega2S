#!/bin/sh -e

mkswap /dev/mmcblk0p1
swapon /dev/mmcblk0p1

output=$(cat /VM/install_step)
if [ "$output" != 4 ]; then
    sh /VM/install.sh >> /VM/install_output.txt 2>&1
else
    /etc/init.d/my_gunicorn_server enable >> /root/gunicorn_output.txt 2>&1
    /etc/init.d/my_gunicorn_server start >> /root/gunicorn_output.txt 2>&1
    python3 /root/WiFiSetup.py >> /root/output.txt 2>&1
    python3 /root/VM.py >> /root/output.txt 2>&1
fi
