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

Received_Done = False

while not Received_Done:
    ser.write(str.encode('9'))  # transmit data serially
    time.sleep(0.001)
    while ser.in_waiting == 0:
        pass
    Received = ser.read_until('\n').decode().strip()  # read and strip serial port data

    print(repr(Received))  # print raw received data for debugging

    if Received == "okay":
        print("Received okay from ESP32-S2")
        Received_Done = True
