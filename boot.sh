#!/bin/sh -e

mkswap /dev/mmcblk0p1
swapon /dev/mmcblk0p1

output=$(cat /VM/install_step)
if [ "$output" != 4 ]; then
    echo heartbeat > /sys/class/leds/omega2p\:amber\:system/trigger
    sh /VM/install.sh >> /VM/install_output.txt 2>&1
else
    echo default-on > /sys/class/leds/omega2p\:amber\:system/trigger
    /etc/init.d/my_gunicorn_server enable >> /VM/gunicorn_output.txt 2>&1
    /etc/init.d/my_gunicorn_server start >> /VM/gunicorn_output.txt 2>&1
    python3 /VM/WiFiSetup.py >> /VM/output.txt 2>&1
    python3 /VM/VM.py >> /VM/output.txt 2>&1
fi
