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
    ser.write(str.encode('9'))  # transmit data serially
    time.sleep(0.001)
    while ser.in_waiting == 0:
        pass
    Received = ser.read_until('\n').decode()  # read serial port
    time.sleep(0.001)

    if (Received != ''):
        Received = Received.replace('\n', '')
        Received.strip()
        print(Received)  # print received data

        if (Received == "okay"):
            print("Received okay from ESP32-S2")
            break
