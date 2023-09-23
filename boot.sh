#!/bin/sh -e

mkswap /dev/mmcblk0p1
swapon /dev/mmcblk0p1

output=$(cat /root/install_step)
if [ "$output" != 3 ]; then
    sh /root/install.sh >> /root/install_output.txt 2>&1
else
    /etc/init.d/my_gunicorn_server enable >> /root/gunicorn_output.txt 2>&1
    /etc/init.d/my_gunicorn_server start >> /root/gunicorn_output.txt 2>&1
    python3 /root/WiFiSetup.py >> /root/output.txt 2>&1
    python3 /root/VM.py >> /root/output.txt 2>&1
fi