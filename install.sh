# Function to check internet connectivity
check_internet() {
    while true; do
        ping -c 1 google.com &> /dev/null && return
        echo "Waiting for internet connectivity..."
        sleep 10
    done
}

pip_install_retry() {
    local cmd="$1"
    local package="$2"

    while true; do
        check_internet
        if [ "$cmd" == "--upgrade" ]; then
            pip3 install --upgrade "$package" && return
        else
            pip3 install "$package" && return
        fi
        echo "Failed to install $package. Retrying in 10 seconds..."
        sleep 10
    done
}

opkg_update_retry() {
    local max_retries=5  # number of times to retry opkg update
    local delay=10  # delay (in seconds) between retries

    i=1
    while [ "$i" -le "$max_retries" ]; do
        i=$((i + 1))
        # Uncomment the following line if you want to check for internet connectivity before each retry
        # check_internet
        
        opkg update && return  # if opkg update succeeds, exit the function

        # If we're here, opkg update failed
        echo "Failed to run 'opkg update'. Attempt $i of $max_retries."
        sleep "$delay"
    done

    echo "Failed to run 'opkg update' after $max_retries attempts."
    exit 1  # Exit the script or handle this failure differently if you want
}

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

    # opkg update
    # opkg install python3-pip
    # opkg install python3-setuptools
    # opkg install python3-cryptography

    # pip3 install --upgrade pip
    # pip3 install stripe
    # pip3 install python-dotenv
    # pip3 install pyserial
    # pip3 install esptool

    # pip3 install flask
    # pip3 install Flask-Session
    # pip3 install gunicorn
    # opkg install nginx

    opkg_update_retry  # use the fail-safe opkg update function

    # Retry opkg installs 
    while ! opkg install python3-pip; do
        echo "Failed to install python3-pip via opkg. Retrying in 10 seconds..."
        sleep 10
    done

    while ! opkg install python3-setuptools; do
        echo "Failed to install python3-setuptools via opkg. Retrying in 10 seconds..."
        sleep 10
    done

    while ! opkg install python3-cryptography; do
        echo "Failed to install python3-cryptography via opkg. Retrying in 10 seconds..."
        sleep 10
    done

    while ! opkg install nginx; do
        echo "Failed to install python3-cryptography via opkg. Retrying in 10 seconds..."
        sleep 10
    done
    
    pip_install_retry "--upgrade" "pip"
    pip_install_retry "" "stripe"
    pip_install_retry "" "python-dotenv"
    pip_install_retry "" "pyserial"
    pip_install_retry "" "esptool"
    pip_install_retry "" "flask"
    pip_install_retry "" "Flask-Session"
    pip_install_retry "" "gunicorn"

    cp /VM/omega2s.conf /etc/nginx/conf.d/
    rm -r /VM/omega2s.conf

    cp /VM/my_gunicorn_server /etc/init.d/
    rm -r /VM/my_gunicorn_server
    chmod +x /etc/init.d/my_gunicorn_server

    /etc/init.d/nginx restart
    /etc/init.d/my_gunicorn_server enable

    git clone https://github.com/MachaDevInc/esp32s2.git
    python3 -m esptool --chip esp32s2 --port /dev/ttyUSB0 --baud 921600  --before default_reset --after hard_reset write_flash --flash_mode dio --flash_size detect --flash_freq 40m 0x1000 /esp32s2/VM_ESP32-S2.ino.bootloader.bin 0x8000 /esp32s2/VM_ESP32-S2.ino.partitions.bin 0x10000 /esp32s2/VM_ESP32-S2.ino.bin
    rm -r /esp32s2

    # Update the flag to indicate that step 3 is complete
    echo 4 > /VM/install_step

    reboot && exit
fi
