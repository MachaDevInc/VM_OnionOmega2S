output=$(cat /root/install_step)
if [ "$output" != 1 ] && [ "$output" != 2 ]; then
    echo "Partitioning the memory and setting up swap memory"
    # opkg update
    # opkg install fdisk kmod-fs-ext4 e2fsprogs swap-utils block-mount
    # umount /dev/mmcblk0
    fdisk /dev/mmcblk0 << EOF
    I
    Disk_Partition_Table
    w
EOF

    mkfs.ext4 /dev/mmcblk0p2 << EOF
    y
EOF

    sleep 5
    
    mkswap /dev/mmcblk0p1
    swapon /dev/mmcblk0p1

    /etc/init.d/fstab enable
    block detect > /etc/config/fstab

    mount /dev/mmcblk0p2 /overlay

    sed -i "s+option enabled '0'+option enabled '1'+g" /etc/config/fstab
    sed -i "s+'/mnt/mmcblk0p2'+'/overlay'+g" /etc/config/fstab

    cd

    git clone https://github.com/MachaDevInc/VM_OnionOmega2S.git

    cp /root/VM_OnionOmega2S/* /root/
    rm -r /root/VM_OnionOmega2S/

    # cp /root/omega2s.conf /etc/nginx/conf.d/
    # rm -r /root/omega2s.conf

    # cp /root/my_gunicorn_server /etc/init.d/
    # rm -r /root/my_gunicorn_server
    # chmod +x /etc/init.d/my_gunicorn_server

    flag_update=/root/install_step
    cat /root/flag_one>$flag_update

    reboot && exit
fi

# if [ "$output" == 1 ]; then
#     echo "Downloading the packages and libraries"

#     opkg update
#     opkg install python3-pip
#     opkg install python3-setuptools
#     opkg install python3-cryptography

#     pip3 install --upgrade pip
#     pip3 install stripe
#     pip3 install python-dotenv
#     pip3 install pyserial
#     pip3 install esptool

#     opkg install python3-pyqt5

#     pip3 install flask
#     pip3 install Flask-Session
#     pip3 install gunicorn
#     opkg install nginx

#     /etc/init.d/nginx restart
#     /etc/init.d/my_gunicorn_server enable

#     git clone https://github.com/MachaDevInc/esp32s2.git
#     python3 -m esptool --chip esp32s2 --port /dev/ttyUSB0 --baud 921600  --before default_reset --after hard_reset write_flash --flash_mode dio --flash_size detect --flash_freq 40m 0x1000 /root/esp32s2/VM_ESP32-S2.ino.bootloader.bin 0x8000 /root/esp32s2/VM_ESP32-S2.ino.partitions.bin 0x10000 /root/esp32s2/VM_ESP32-S2.ino.bin
#     rm -r /root/esp32s2

#     flag_update=/root/install_step
#     cat /root/flag_two>$flag_update

#     reboot && exit
# fi