import os
import time
import serial

ser = serial.Serial(
    port='/dev/ttyS2',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

while 1:
    ser.write(str.encode('8'))  # transmit data serially
    time.sleep(0.001)
    while ser.in_waiting == 0:
        pass
    SSID = ser.read_until('\n').decode()  # read serial port
    time.sleep(0.001)

    if (SSID != ''):
        SSID = SSID.replace('\n', '')
        SSID.strip()
        print(SSID)  # print received data

    time.sleep(0.01)
    ser.write(str.encode('9'))  # transmit data serially
    time.sleep(0.001)
    while ser.in_waiting == 0:
        pass
    Password = ser.read_until('\n').decode()  # read serial port
    time.sleep(0.001)

    if (Password != ''):
        Password = Password.replace('\n', '')
        Password.strip()
        print(Password)  # print received data
        break

SSID = "'" + SSID + "'"
Password = "'" + Password + "'"
command = "wifisetup add -ssid " + SSID + " -encr psk2 -password " + Password
os.system(command)

command = "wifisetup priority -ssid " + SSID + " -move top"
os.system(command)
