import time
import serial

ser = serial.Serial(
    port='/dev/ttyS1',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

while 1:
    received_data = ser.read_until('\n').decode()  # read serial port
    time.sleep(0.001)

    if (received_data != ''):
        received_data = received_data.replace('\n', '')
        print(received_data)  # print received data