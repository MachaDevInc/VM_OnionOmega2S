# pip install adafruit-circuitpython-pn532
# pip install RPi.GPIO pyserial

import time
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
import serial
import RPi.GPIO as GPIO
from adafruit_pn532.i2c import PN532_I2C

# Configure the PN532 connection
i2c = busio.I2C(board.SCL, board.SDA)
pn532 = PN532_I2C(i2c, debug=False)

# Configure the button
BUTTON_PIN = 26  # Change this to the GPIO pin number you connected the button to
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Constants
UART_PORT = "/dev/ttySC0"
UART_BAUDRATE = 9600

# Set up the UART serial connection
uart = serial.Serial(UART_PORT, baudrate=UART_BAUDRATE, timeout=1)

def scan_barcode_RFID():
    barcode_data = ""

    while True:
        data = uart.read(10)
        if data:
            barcode_data += data.decode("utf-8")

        if "\r\n" in barcode_data:
            barcode_data.strip()
            print("Scanned barcode: ", barcode)
            break

        uid = pn532.read_passive_target(timeout=0.5)
        if uid is not None:
            print("Found an RFID card with UID:", [hex(i) for i in uid])
            break

def main():
    ic, ver, rev, support = pn532.firmware_version
    print("Found PN532 with firmware version: {0}.{1}".format(ver, rev))

    # Configure PN532 to communicate with RFID cards
    pn532.SAM_configuration()

    print("Press the button to scan an RFID card.")
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            print("Scanning RFID and Barcode...")
            scan_barcode_RFID()
            time.sleep(1)  # Debounce delay

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        GPIO.cleanup()

# ////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////

# pip install pyserial RPi.GPIO

import time
import serial
import RPi.GPIO as GPIO

# Constants
BUTTON_PIN = 18
UART_PORT = "/dev/ttyS0"
UART_BAUDRATE = 9600

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set up the UART serial connection
uart = serial.Serial(UART_PORT, baudrate=UART_BAUDRATE, timeout=1)

def scan_barcode():
    barcode_data = ""

    while True:
        data = uart.read(10)
        if data:
            barcode_data += data.decode("utf-8")

        if "\r\n" in barcode_data:
            break

    return barcode_data.strip()

try:
    print("Waiting for button press...")
    while True:
        button_state = GPIO.input(BUTTON_PIN)
        if button_state == GPIO.LOW:
            print("Scanning barcode...")
            barcode = scan_barcode()
            print("Scanned barcode: ", barcode)
            time.sleep(1)  # Debounce delay

finally:
    GPIO.cleanup()

