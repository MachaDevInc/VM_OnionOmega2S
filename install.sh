output=$(cat /VM/install_step)
if [ "$output" != 1 ] && [ "$output" != 2 ] && [ "$output" != 3 ] && [ "$output" != 4 ]; then
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

    # mkswap /dev/mmcblk0p1
    # swapon /dev/mmcblk0p1

    # /etc/init.d/fstab enable
    # block detect > /etc/config/fstab

    # mount /dev/mmcblk0p2 /overlay

    # Update the flag to indicate that step 1 is complete
    echo 1 > /VM/install_step

    reboot && exit
fi

if [ "$output" == 1 ]; then
    echo "Mounting /dev/mmcblk0p2 at /mnt/temp_overlay and copying original overlay to it"

    # mkswap /dev/mmcblk0p1
    # swapon /dev/mmcblk0p1

    # /etc/init.d/fstab enable
    # block detect > /etc/config/fstab

    mkdir -p /mnt/temp_overlay
    
    mount /dev/mmcblk0p2 /mnt/temp_overlay

    rsync -av /overlay/ /mnt/temp_overlay/

    umount /mnt/temp_overlay

    /etc/init.d/fstab enable
    block detect > /etc/config/fstab

    mount /dev/mmcblk0p2 /overlay

    # sed -i "s+option[[:space:]]\+enabled[[:space:]]\+'0'+option enabled '1'+g" /etc/config/fstab
    # sed -i "s+'/mnt/mmcblk0p2'+'/overlay'+g" /etc/config/fstab

    # cd

    # git clone https://github.com/MachaDevInc/VM_OnionOmega2S.git

    # cp /root/VM_OnionOmega2S/* /root/
    # rm -r /root/VM_OnionOmega2S/

    # Update the flag to indicate that step 2 is complete
    echo 2 > /VM/install_step

    reboot && exit
fi

if [ "$output" == 2 ]; then
    echo "Mounting /dev/mmcblk0p2 at /overlay"

    /etc/init.d/fstab enable
    block detect > /etc/config/fstab

    mount /dev/mmcblk0p2 /overlay

    sed -i "s+option[[:space:]]\+enabled[[:space:]]\+'0'+option enabled '1'+g" /etc/config/fstab
    sed -i "s+'/mnt/mmcblk0p2'+'/overlay'+g" /etc/config/fstab

    cd

    git clone https://github.com/MachaDevInc/VM_OnionOmega2S.git

    cp /root/VM_OnionOmega2S/* /root/
    rm -r /root/VM_OnionOmega2S/

    # Update the flag to indicate that step 3 is complete
    echo 3 > /VM/install_step

    reboot && exit
fi

if [ "$output" == 3 ]; then
    echo "Downloading the packages and libraries"

    sleep 35

    cp /VM/distfeeds.conf /etc/opkg/distfeeds.conf

    opkg update
    opkg install python3-pip
    opkg install python3-setuptools
    opkg install python3-cryptography

    pip3 install --upgrade pip
    pip3 install stripe
    pip3 install python-dotenv
    pip3 install pyserial
    pip3 install esptool

    opkg install python3-pyqt5

    pip3 install flask
    pip3 install Flask-Session
    pip3 install gunicorn
    opkg install nginx

    /etc/init.d/nginx restart
    /etc/init.d/my_gunicorn_server enable

    cp /root/omega2s.conf /etc/nginx/conf.d/
    rm -r /root/omega2s.conf

    cp /root/my_gunicorn_server /etc/init.d/
    rm -r /root/my_gunicorn_server
    chmod +x /etc/init.d/my_gunicorn_server

    git clone https://github.com/MachaDevInc/esp32s2.git
    python3 -m esptool --chip esp32s2 --port /dev/ttyUSB0 --baud 921600  --before default_reset --after hard_reset write_flash --flash_mode dio --flash_size detect --flash_freq 40m 0x1000 /root/esp32s2/VM_ESP32-S2.ino.bootloader.bin 0x8000 /root/esp32s2/VM_ESP32-S2.ino.partitions.bin 0x10000 /root/esp32s2/VM_ESP32-S2.ino.bin
    rm -r /root/esp32s2

    # Update the flag to indicate that step 3 is complete
    echo 4 > /VM/install_step

    reboot && exit
fi